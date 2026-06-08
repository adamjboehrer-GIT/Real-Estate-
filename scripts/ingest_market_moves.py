"""
Parse InfoSparks / ShowingTime Plus CSV exports for the /market-moves command
into a single combined monthly snapshot JSON with month-over-month and
year-over-year deltas for every (geography, metric) pair.

Input: a directory of InfoSparks CSV exports. Each CSV is one metric and may
carry ONE segment (geography) or MULTIPLE segments as separate value columns
(InfoSparks lets you compare several areas on one chart). Both are handled.

CSV structure (see data/imports/mls_stats/.../*.csv):
  Metric:,<Metric Name>
  Time Calculation:,Monthly
  Data from:,<export M/D/YYYY>
  Segments:,<seg1>[,<seg2>...]
  <blank>
  Filters
  <seg>:,"<filter string>"
  <blank x2>
  Date,"<seg1>","<seg2>",...   <- column header row
  Month YYYY,<v1>,<v2>,...     <- monthly rows
  ... trailing blank + CRMLS/InfoSparks attribution

Metric name -> snapshot key mapping is normalized so the briefing template can
rely on stable keys regardless of InfoSparks' exact label wording.

Usage:
    python3 scripts/ingest_market_moves.py data/imports/mls_stats/2026-06-08 \
        [--out data/market_stats/2026-06_market_moves.json]

If --out is omitted, the output month is taken from the LAST populated data row
(the actual reporting month, not the export date) and written to
data/market_stats/<YYYY-MM>_market_moves.json.
"""
import argparse
import csv
import glob
import json
import os
import re

# InfoSparks label (lowercased, stripped) -> stable snapshot key + display label.
METRIC_MAP = {
    "active listings": ("active_listings", "Active Listings"),
    "new listings": ("new_listings", "New Listings"),
    "pending sales": ("pending_sales", "Pending Sales"),
    "closed sales": ("closed_sales", "Closed Sales"),
    "sold listings": ("closed_sales", "Closed Sales"),
    "inventory months supply": ("months_supply", "Months Supply of Inventory"),
    "months supply of inventory": ("months_supply", "Months Supply of Inventory"),
    "median sales price": ("median_sales_price", "Median Sales Price"),
    "median days active in mls": ("median_dom", "Median Days on Market"),
    "days on market until sale": ("median_dom", "Median Days on Market"),
    "median days on market": ("median_dom", "Median Days on Market"),
    "percent of list price received": ("pct_list_received", "% of List Price Received"),
    "pct. of last list price received": ("pct_list_received", "% of List Price Received"),
    "median percent of last list price received": ("pct_list_received", "% of Last List Price Received"),
    "percent of original list price received": ("pct_orig_list_received", "% of Original List Received"),
}

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


def _num(s):
    """Parse an InfoSparks cell to float, stripping $, %, commas. None if blank."""
    if s is None:
        return None
    s = s.strip().strip('"').replace("$", "").replace("%", "").replace(",", "")
    if s == "" or s == "-":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _month_key(label):
    """'April 2026' -> '2026-04'. None if not a month row."""
    m = re.match(r"\s*([A-Za-z]+)\s+(\d{4})", label.strip().strip('"'))
    if not m:
        return None
    mon = MONTHS.get(m.group(1).lower())
    if not mon:
        return None
    return f"{m.group(2)}-{mon:02d}"


def parse_csv(path):
    """Return (metric_key, metric_label, {segment: {month_key: value}})."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    metric_label = None
    header_idx = None
    for i, row in enumerate(rows):
        if not row:
            continue
        c0 = (row[0] or "").strip().lower().rstrip(":")
        if c0 == "metric":
            metric_label = (row[1] if len(row) > 1 else "").strip()
        if c0 == "date":
            header_idx = i
            break
    if header_idx is None or metric_label is None:
        raise ValueError(f"Could not locate metric/date header in {path}")

    key, label = METRIC_MAP.get(
        metric_label.strip().lower(), (re.sub(r"[^a-z0-9]+", "_", metric_label.lower()).strip("_"), metric_label)
    )

    header = rows[header_idx]
    segments = [h.strip().strip('"') for h in header[1:] if h.strip().strip('"')]
    data = {seg: {} for seg in segments}
    for row in rows[header_idx + 1:]:
        if not row or not row[0].strip():
            continue
        mk = _month_key(row[0])
        if not mk:
            continue
        for j, seg in enumerate(segments):
            val = _num(row[j + 1]) if j + 1 < len(row) else None
            if val is not None:
                data[seg][mk] = val
    return key, label, data


def pct(cur, prev):
    if cur is None or prev is None or prev == 0:
        return None
    return round((cur - prev) / prev * 100, 1)


def prev_month(mk):
    y, m = map(int, mk.split("-"))
    return f"{y - 1}-12" if m == 1 else f"{y}-{m - 1:02d}"


def year_ago(mk):
    y, m = map(int, mk.split("-"))
    return f"{y - 1}-{m:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("import_dir")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.import_dir, "*.csv")))
    if not files:
        raise SystemExit(f"No CSVs found in {args.import_dir}")

    # geo -> metric_key -> {label, series: {month: val}}
    geos = {}
    metric_labels = {}
    for path in files:
        key, label, data = parse_csv(path)
        metric_labels[key] = label
        for seg, series in data.items():
            geos.setdefault(seg, {})[key] = series

    # Reporting month = latest month present across all series.
    all_months = sorted({m for g in geos.values() for s in g.values() for m in s})
    if not all_months:
        raise SystemExit("No monthly data rows parsed.")
    report_month = all_months[-1]

    out = {
        "schema_version": "1.0",
        "command": "market-moves",
        "reporting_month": report_month,
        "source": {
            "system": "California Regional Multiple Listing Service (CRMLS)",
            "tool": "InfoSparks / ShowingTime Plus",
            "access_method": "manual login by licensed agent; export driven via Playwright (compliant)",
            "import_dir": args.import_dir,
        },
        "geographies": {},
    }

    pm, ya = prev_month(report_month), year_ago(report_month)
    for geo, metrics in sorted(geos.items()):
        block = {}
        for key, series in metrics.items():
            cur = series.get(report_month)
            block[key] = {
                "label": metric_labels.get(key, key),
                "current": cur,
                "prior_month": series.get(pm),
                "mom_pct": pct(cur, series.get(pm)),
                "year_ago": series.get(ya),
                "yoy_pct": pct(cur, series.get(ya)),
            }
        out["geographies"][geo] = block

    out_path = args.out or os.path.join(
        os.path.dirname(__file__), "..", "data", "market_stats", f"{report_month}_market_moves.json"
    )
    out_path = os.path.normpath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Reporting month: {report_month}  (prev {pm}, year-ago {ya})")
    print(f"Geographies: {', '.join(sorted(geos))}")
    print(f"Metrics: {', '.join(sorted(metric_labels.values()))}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
