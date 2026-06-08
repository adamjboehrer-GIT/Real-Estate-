---
name: market-moves
description: Pull a full monthly market rundown from CRMLS InfoSparks (ShowingTime Plus) via Playwright for Orange County, San Clemente, Dana Point, and Laguna Beach. Adam logs in by hand; automation only drives the InfoSparks export clicks after login (CRMLS-compliant). Produces raw CSVs, a parsed JSON snapshot, and a plain-English month-over-month briefing Adam can take to clients. Invoke when Adam types `/market-moves`, or says "monthly market moves", "what's happening in the market", "run the market update".
---

# Market Moves — CRMLS InfoSparks → monthly market briefing

## What this is

A once-a-month, on-demand market pull. The underlying CRMLS data only updates
monthly, so this is NOT scheduled — Adam runs it when he wants the current
picture (e.g., start of the month, or before a client conversation).

It answers the question that started this: *"a client asked if inventory was up
or down and I didn't have an answer."* After a run, Adam has a current,
client-ready rundown of where each market sits and what moved versus last month.

## Compliance — read first

CRMLS Rules prohibit automated/bot access to MLS data under agent credentials.
This skill stays compliant the exact same way `title-pull` does: **Adam logs in
and lands on InfoSparks himself. Automation never touches the login.** Once he's
authenticated and says "ready," automation drives the in-tool export clicks only.
Never automate the CRMLS/InfoSparks login or 2FA. If asked to, decline and have
Adam do it by hand.

## Geographies (fixed)

Orange County (county-level), San Clemente, Dana Point, Laguna Beach.

## Metrics (the full picture, not just inventory)

| Snapshot key        | InfoSparks metric label            | Why it's in the rundown            |
|---------------------|------------------------------------|------------------------------------|
| active_listings     | Active Listings                    | Inventory on hand right now        |
| new_listings        | New Listings                       | Incoming supply this month         |
| pending_sales       | Pending Sales                      | Demand / deals going under contract|
| closed_sales        | Closed Sales                       | Actual transactions closing        |
| months_supply       | Inventory Months Supply            | Buyer's vs seller's market balance |
| median_sales_price  | Median Sales Price                 | Price level                        |
| median_dom          | Median Days Active in MLS          | How fast homes sell                |
| pct_list_received   | Percent of List Price Received     | Pricing power / negotiation room   |

Standard InfoSparks settings: **Time Calculation = Monthly**, default 5-year
range. Property filter = **Residential, Single Family, Detached** (matches Adam's
existing San Clemente series so months/years stay comparable). If Adam asks for
condos/townhomes, add that filter as a second pass.

## Step 0 — Open the browser, Adam logs in

Open Playwright to InfoSparks. First run: navigate to the CRMLS portal / Adam's
InfoSparks bookmark and **capture the working URL into this file** (see
"First-run capture" at the bottom) so future runs go straight there.

    mcp__playwright__browser_navigate → <INFOSPARKS_URL — capture on first run>

Then send Adam exactly:

> "Browser's open. Log into CRMLS and get to InfoSparks (ShowingTime Plus), then say **ready**."

Wait for `ready` / `go` / `ok`. If he hits a snag (2FA, wrong page), help him get
there — do not start pulling until he confirms he's on InfoSparks.

## Step 1 — Pull each metric

Preferred path (fewest clicks): InfoSparks lets you put **multiple segments on one
chart**. For each of the 8 metrics, build one chart with all four geographies as
series, set Monthly, then **Export → CSV**. That's ~8 exports total instead of 32.

If the plan/UI doesn't support multi-segment compare, fall back to one chart per
(geography × metric) and export each — 32 CSVs. Either way the parser handles it.

For each export, use `browser_snapshot` to find the controls, set:
- Metric = the InfoSparks label from the table above
- Segment(s) = OC + San Clemente + Dana Point + Laguna Beach
- Property type filter = Residential, Single Family, Detached
- Time Calculation = Monthly

then click the chart's **Export / Download → CSV**. Record the exact selector path
the first time it works so subsequent metrics reuse it.

Save every downloaded CSV into a dated import folder:

    data/imports/mls_stats/<YYYY-MM-DD>/   (today's date)

Keep InfoSparks' own filenames; the parser reads metric + segments from inside
each file, not the name.

## Step 2 — Parse into a snapshot

    python3 scripts/ingest_market_moves.py data/imports/mls_stats/<YYYY-MM-DD>

Writes `data/market_stats/<YYYY-MM>_market_moves.json` (month taken from the last
populated data row — the real reporting month, not today's export date), with
`current`, `prior_month`, `mom_pct`, `year_ago`, `yoy_pct` for every geo × metric.

Sanity-check the JSON: confirm the reporting month is what you expect (current
month usually isn't closed yet, so it typically reports the prior month), all four
geos are present, and no metric came back all-null (a null column means an export
didn't capture that segment — re-pull it).

## Step 3 — Write the briefing

Write a plain-English rundown to:

    reports/market_briefings/<YYYY-MM>_market_moves.md

Structure:
1. **Headline** — one line on the overall OC market this month (direction of
   inventory + what it means).
2. **Orange County** — inventory, supply balance, pace, price, pricing power,
   each with the month-over-month move and the year-over-year for context.
3. **San Clemente / Dana Point / Laguna Beach** — same shape, one section each,
   ending with a single "here's the story you can tell a client" sentence.
4. **What changed vs last month** — the 3-5 moves that actually matter.

Voice rules (Adam's standing preferences):
- No em-dashes or en-dashes in prose; commas/periods/short sentences.
- Lead with substance, not filler.
- Single-month medians are volatile at low transaction counts. Frame price moves
  against the last 2-3 months and flag any obvious one-month spike rather than
  reporting it as a trend (see the data-quality notes in past snapshots).
- Always cite the source as "California Regional MLS via InfoSparks (ShowingTime
  Plus)" and name the reporting month.
- Months Supply reading: < ~3 months = seller's market, 3-6 = balanced, > 6 =
  buyer's market (state the number, then the plain-English read).

## Step 4 — Hand it back

Post the headline + the four city one-liners directly in chat so Adam has the
answer immediately, and tell him where the full briefing + JSON live. Note the
reporting month explicitly (e.g., "this reports May data; June isn't closed yet").

## First-run capture (do this the first time, then delete this section's TODOs)

The InfoSparks UI hasn't been automated before. On the first successful run,
record into this file so future months are deterministic:
- [ ] The working InfoSparks URL for Step 0
- [ ] Whether multi-segment compare worked (8 exports) or we fell back to 32
- [ ] The exact selectors/click-path for: setting the metric, adding segments,
      setting the property-type filter, setting Monthly, and Export → CSV
- [ ] Any plan limits hit (export caps, metrics not available on Adam's tier)
