# Terramar — Reference Folder

All Terramar-related materials in one place. Carlsbad, CA, ZIP 92008 — the 7 streets that qualify for Terramar Association membership and private beach access.

## What's in here

| File | What it is |
|---|---|
| `Terramar Appreciation Brief.pdf` | **Client-ready PDF** — 10-year parcel-level sales analysis for the 7 qualifying streets, benchmarked against the 92008 ZIP. This is the file to send. |
| `Terramar Appreciation Brief.md` | Markdown source of the PDF above. Edit this if you want to revise content, then re-render. |
| `Terramar Association Buyer Brief.md` | Internal buyer-side summary of HOA rules, costs, the 7 qualifying streets, and the critical STR caveat (sub-30-day guests can't independently use the private landing). |
| `ZIP 92008 Appreciation Context.md` | The earlier ZIP-92008-only analysis (no Terramar parcel detail). Useful as broader market context. |
| `source data/` | Raw inputs: parcel-level sales CSV (transcribed from CRMLS Matrix screenshots) and the 5 InfoSparks ZIP-92008 CSVs. |

## How the appreciation brief was built

1. **InfoSparks ZIP 92008 export** — 5 CSVs (Median Sales Price, Median $/sqft, Average Sales Price, Median % of Original Price Received, Total Closed Transaction Sides) covering Jan 2008 through March 2026, monthly.
2. **CRMLS Matrix parcel pull** — closed SFR/D sales 2016–2026 on the 7 qualifying streets, transcribed into `source data/terramar_sales.csv`.
3. **Analysis script** — `scripts/analyze_terramar_parcel.py` reads both, produces the markdown brief.
4. **PDF render** — `scripts/md_to_pdf.py` converts the markdown to a brand-styled PDF (SIR Blue headers, Gold dividers, page numbers).

## To re-run with fresh data

1. Pull updated InfoSparks CSVs for ZIP 92008, drop them in `source data/` (replacing the dated files).
2. Pull updated Matrix sales for the 7 streets, append new rows to `source data/terramar_sales.csv`.
3. Run from the repo root:
   ```
   python3 scripts/analyze_terramar_parcel.py
   python3 scripts/md_to_pdf.py "Terramar/Terramar Appreciation Brief.md" "Terramar/Terramar Appreciation Brief.pdf"
   ```

## Last updated

2026-04-27 — initial folder consolidation. Brief covers Jan 2008 through March 2026 InfoSparks data and 2016–2026 parcel-level Matrix data.
