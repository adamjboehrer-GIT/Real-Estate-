"""
Regenerate website/data/stats.json from the latest market-stats JSONs.

Pulls the six numbers Adam uses in Coastal Currents' "By The Numbers" block:
  Row 1 (San Clemente SFR, InfoSparks):
    - Median Days on Market
    - Months of Supply
    - Median Sales Price
  Row 2 (San Clemente city-wide, Pacific Sotheby's deck):
    - Listings with a Price Cut
    - Sale-to-List Ratio (all residential, most recent sold month)
    - 10-Year Home Value Growth (Zillow HVI ten-year)

Run after Adam drops new InfoSparks CSVs + new deck JSON into data/market_stats/.
Re-run safely — idempotent overwrite.

Usage:
    python3 scripts/generate_website_stats.py
"""
import datetime as dt
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MARKET_DIR = os.path.join(ROOT, "data", "market_stats")
OUT_PATH = os.path.join(ROOT, "website", "data", "stats.json")

MONTHS = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]


def latest_matching(pattern):
    """Return the newest file matching `data/market_stats/<pattern>` by filename."""
    paths = sorted(glob.glob(os.path.join(MARKET_DIR, pattern)))
    if not paths:
        sys.exit(f"No file matched: {pattern}")
    return paths[-1]


def load_json(path):
    with open(path) as f:
        return json.load(f)


def fmt_price_short(usd):
    """1810000 -> '$1.81M'. 7200000 -> '$7.2M'."""
    if usd is None:
        return "-"
    m = usd / 1_000_000
    if m >= 10:
        return f"${m:.1f}M"
    return f"${m:.2f}M".rstrip("0").rstrip(".") + "M" if "M" not in f"${m:.2f}M" else f"${m:.2f}M"


def fmt_price_clean(usd):
    """Clean shortform: $1.81M, $7.2M, $11.4M."""
    if usd is None:
        return "-"
    m = usd / 1_000_000
    if m >= 10:
        return f"${m:.1f}M"
    # 2 decimals trimmed
    s = f"{m:.2f}"
    s = s.rstrip("0").rstrip(".")
    return f"${s}M"


def fmt_pct_signed(pct):
    """10-year HVI: +123%, -2%. Round to nearest int."""
    if pct is None:
        return "-"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{round(pct)}%"


def month_year_label(ym):
    """'2026-03' -> 'March 2026'."""
    year, month = ym.split("-")
    return f"{MONTHS[int(month) - 1]} {year}"


def find_sold_key(city, suffix):
    """The OC deck hard-codes keys like 'sold_march_2026_all'. Find the
    newest one and return the dict. `suffix` is 'all' or 'under_5m'."""
    best = None
    best_sort = None
    for key, val in city.items():
        m = re.match(r"^sold_([a-z]+)_(\d{4})_" + suffix + "$", key)
        if not m:
            continue
        month_name, year = m.group(1), m.group(2)
        if month_name.capitalize() not in MONTHS:
            continue
        sort_key = (int(year), MONTHS.index(month_name.capitalize()))
        if best_sort is None or sort_key > best_sort:
            best_sort = sort_key
            best = (key, val, month_name.capitalize(), year)
    return best


def main():
    sc_sfr = load_json(latest_matching("*_san_clemente_sfr.json"))
    oc = load_json(latest_matching("*_oc_market_report.json"))

    # Row 1 — InfoSparks SFR
    cm = sc_sfr["current_month"]
    yoy = sc_sfr.get("year_over_year_march", {})
    reporting_month = sc_sfr["reporting_month"]
    month_label = month_year_label(reporting_month)
    month_name_only = month_label.split()[0]  # "March"

    dom = cm["median_days_active_in_mls"]
    dom_last_year = yoy.get("median_days_active_in_mls", {}).get("2025")
    months_supply = cm["inventory_months_supply"]
    months_supply_last_year = yoy.get("inventory_months_supply", {}).get("2025")
    price = cm["median_sales_price_usd"]
    actives = cm["active_listings"]
    pendings = cm["pending_sales"]

    # Row 2 — Pacific Sotheby's deck, San Clemente
    sc_city = next((c for c in oc["cities"] if c["name"] == "San Clemente"), None)
    if not sc_city:
        sys.exit("San Clemente not found in OC deck JSON")

    pct_reduced = sc_city["pct_listings_reduced"]

    sold_all = find_sold_key(sc_city, "all")
    sold_under_5m = find_sold_key(sc_city, "under_5m")
    if not sold_all:
        sys.exit("No sold_MONTH_YEAR_all key found for San Clemente")
    _, sold_all_val, sold_month, sold_year = sold_all
    sl_ratio = sold_all_val["sl_ratio_pct"]
    sl_ratio_under_5m = sold_under_5m[1]["sl_ratio_pct"] if sold_under_5m else None

    hvi = sc_city["zillow_hvi_feb_2026"]["ten_year_pct"]

    stats = [
        {
            "value": str(dom),
            "label": "Median Days on Market",
            "note": f"Down from {dom_last_year} days last {month_name_only}."
                    if dom_last_year else "",
        },
        {
            "value": str(months_supply),
            "label": "Months of Supply",
            "note": f"Tighter than {months_supply_last_year} months a year ago."
                    if months_supply_last_year else "",
        },
        {
            "value": fmt_price_clean(price),
            "label": "Median Sales Price",
            "note": f"{actives} active listings. {pendings} new pendings in {month_name_only}.",
        },
        {
            "value": f"{pct_reduced}%",
            "label": "Listings with a Price Cut",
            "note": "Among the lowest in Orange County.",
        },
        {
            "value": f"{sl_ratio}%",
            "label": "Sale-to-List Ratio",
            "note": (f"Homes under $5M closed at {sl_ratio_under_5m}% in {sold_month}."
                     if sl_ratio_under_5m is not None else
                     f"Most recent closings, {sold_month} {sold_year}."),
        },
        {
            "value": fmt_pct_signed(hvi),
            "label": "10-Year Home Value Growth",
            "note": "Top tier of Orange County.",
        },
    ]

    deck_label = month_year_label(oc["reporting_month"])
    out = {
        "last_updated": dt.date.today().isoformat(),
        "reporting_label": f"San Clemente · {month_label}",
        "row_1_label": f"San Clemente Single-Family · {month_label}",
        "row_2_label": f"San Clemente City-Wide · {deck_label} Snapshot",
        "sources": "California Regional MLS (via InfoSparks / ShowingTime Plus) "
                   f"and Pacific Sotheby's {deck_label} Market Report.",
        "stats": stats,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {OUT_PATH}")
    print(f"  Row 1: {out['row_1_label']}")
    print(f"  Row 2: {out['row_2_label']}")
    for s in stats:
        print(f"    {s['value']:>8}  {s['label']}")


if __name__ == "__main__":
    main()
