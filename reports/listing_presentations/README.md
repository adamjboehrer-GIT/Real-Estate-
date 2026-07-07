# Private Market Analysis — per-homeowner report pages

This is the system behind pages like `adamboehrer.com/report/249-calle-esmarca-919475/`.
A hyper-personalized "listing presentation" web page for one homeowner: their home facts,
an estimated value today, recent nearby sales, the local market snapshot, Adam's positioning,
and a newsletter + contact CTA. Delivered by direct-mail notecard (QR + short link, **no value
shown on the card** — the value is the reveal on the page). `noindex`, unguessable hashed slug.

## Anatomy of a page (what "content like this" means)

Rendered by `scripts/build_listing_presentations.py`, one section per band:

1. **Hero** — "Private Market Analysis · <month>", the address, "Prepared privately".
2. **Approach** — "Most agents will market themselves to you. I would rather show you the work…"
3. **Your Home** — beds / baths / sqft / year built (from `database/leads.db`).
4. **What You Have Built** — estimated value **range** + $ and % gain since purchase + a
   "not an appraisal" disclaimer.
5. **What Is Selling Near You** — 3 closest recent real sales by size (from CRMLS comps).
6. **Your Market Right Now** — 6 live market stats (median price, market time, sale-to-list,
   active listings, price cuts, 10yr growth).
7. **Why Me** — Adam's father/neighbor → brand-strategy → investor positioning.
8. **Coastal Currents** — newsletter signup (Mailchimp).
9. **Let's Talk** — phone/email contact + Sotheby's brand footer.

Voice + brand: Pacific Sotheby's palette, no em-dashes, seller-voice positioning, no overpromising.

## How to generate one for a specific home

The home must exist in `database/leads.db` (from a title pull). Then:

```bash
# 0. (once per city, or when comps are stale) load recent MLS closed sales
python3 scripts/ingest_mls_comps.py "data/imports/<city>_agent_1line.csv"

# 1. draft: select homes, compute values, flag risky ones, write pilot.json
python3 scripts/build_listing_presentations.py review --limit 20 --cities "San Clemente"

# 2. Adam reviews reports/listing_presentations/pilot.json:
#    set  "status": "approved"  and (optional) "final_value": <override>  per home
#    -> re-running `review` PRESERVES status / final_value / short_code

# 3. publish approved pages to website/report/<slug>/index.html
python3 scripts/build_listing_presentations.py generate

# 4. (optional) direct-mail kit: short links, QR codes, 5x7 notecards
python3 scripts/build_report_mailers.py
```

**Preview locally** (the `localhost:8791` you saw is just this — an ad-hoc static server):

```bash
cd website && python3 -m http.server 8791
# then open http://localhost:8791/report/<slug>/
```

**Publish live:** commit + push. `website/` deploys to `adamboehrer.com` via Cloudflare Pages
(push-to-deploy). Live URL is `adamboehrer.com/report/<slug>/`.

## Value methodology (Adam reviews/overrides EVERY number before publish)

- **Method A** = last sale price compounded by the city's annualized Zillow 10yr appreciation.
  Reliable only for recent purchases; explodes on old/refi sale records.
- **Method B** = home sqft × median $/sqft of real recent MLS sales matched by property type
  (sfr/condo) and size band (±25%, widening). **This is the trusted anchor.**
- **Blend** weights A by years held (≤3yr→0.75, ≤8yr→0.45, >8yr→pure comp). The published
  range is the midpoint ±~5%.
- Methods disagreeing >20% get **flagged** for a hard look. Never ship a number unchecked.

## Files

- `scripts/build_listing_presentations.py` — `review` (draft) / `generate` (publish).
- `scripts/build_report_mailers.py` — short links, QR, notecards, mailing sheet.
- `scripts/ingest_mls_comps.py` — CRMLS "Agent 1 Line" closed-sales CSV → `comps` table.
- `scripts/sync_report_views.py` — open-tracking beacon → interactions/signals in leads.db.
- `pilot.json` — the working list + per-home status/value/short_code (source of truth for generate).
- `mailers/` — generated notecards, QR PNGs, mailing sheet.
- `track_config.example.json` — copy to `track_config.json` with the Apps Script /exec URL + token.

Data note: PropStream is gone and title data carries no current value — that's why the CRMLS
comp pull in step 0 is essential.
