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
| median_dom          | Days Active in MLS                 | How fast homes sell                |
| pct_list_received   | % of Last List Price               | Pricing power / negotiation room   |

The bottom metric chips read: New Listings · Active Listings · Pending Sales ·
Closed Sales · Total Closed Sides · Closed Volume · Days Active in MLS · Months
Supply · Price Per Sq Ft · % of Last List Price · % of Original Price · Sales
Price · Shows to Contract · Shows Per Listing. Click the 8 in the table. Two have
a Median/Average sub-toggle (Days Active, Sales Price) — leave on **Median**
(the default; the parser keys off the "Median ..." label).

Standard InfoSparks settings: **Time Calculation = Monthly** (default), default
5-year range. Property filter = **Residential** (Property Type) + **Single
Family** (Property Sub-Type). Adam's saved view already has this; do NOT add the
Attached/Detached restriction (the on-screen series is Single Family, not
Detached-only). If Adam asks for condos/townhomes, add that sub-type as a second
pass.

## Step 0 — Open the browser, Adam logs in

Open Playwright to the CRMLS login. Adam logs in there, then InfoSparks opens as
its own tab.

    mcp__playwright__browser_navigate → https://go.crmls.org/

Then send Adam exactly:

> "Browser's open. Log into CRMLS and get to InfoSparks (ShowingTime Plus), then say **ready**."

Wait for `ready` / `go` / `ok`. If he hits a snag (2FA, wrong page), help him get
there — do not start pulling until he confirms he's on InfoSparks.

**The InfoSparks tab.** InfoSparks runs at `https://crmls.stats.10kresearch.com/stats/market`
and usually opens as a separate browser tab. After Adam says ready, list tabs and
select the InfoSparks one before doing anything:

    mcp__playwright__browser_tabs (action: list)   → find the "InfoSparks" tab
    mcp__playwright__browser_tabs (action: select, index: <that tab>)

If the Playwright profile is locked ("Browser is already in use") from a stale
session, find the orphaned Chrome on profile `mcp-chrome-bb6278f`
(`ps aux | grep mcp-chrome-bb6278f`), `kill` the main PID, then reopen.

## Step 1 — Pull each metric

Multi-segment compare WORKS on Adam's plan: all four areas go on one chart, so it
is **8 exports total** (one per metric), each CSV carrying all four area columns.

### 1a — Set up the four areas (once, before any export)

The chart loads with **Orange County** already set. Add the other three:

1. Click **"+ ADD AN AREA"**. A new row appears defaulting to "Entire MLS".
2. Click that row's search box, then click the **"City"** category tab (the
   dropdown defaults to "All" / Associations and will NOT filter to a city until
   you pick City).
3. Type the city name (`San Clemente`, then `Dana Point`, then `Laguna Beach`).
   Type slowly so the autocomplete fires. Click the matching "<City> City" result.
4. Repeat "+ ADD AN AREA" for each of the three cities.

**Quirk:** adding an area resets the Property Sub-Type filter to none ("Residential"
only). After all four areas are in, open **Property Sub-Types** and click **Single
Family** so the chart title reads "...: Residential, Single Family". Verify the
chart title lists all four areas before exporting.

Refs in the snapshot churn between steps; re-snapshot the area block (the `+ ADD AN
AREA` list) before each add rather than reusing a stale ref.

### 1b — Export each metric to CSV

For each of the 8 metrics, repeat this exact path:

1. Click the **metric chip** at the bottom (e.g. "Active Listings").
2. Click **Share** (top-left of the chart, next to Print).
3. In the Share Options dialog: Step 1 stays **Static** (default). Under Step 2,
   click **"CSV - grab the raw data"** (the dialog often defaults to "Social Media
   and Email", so always click CSV explicitly).
4. Click the **Share** button — this generates the file and reveals a "Your URL"
   box with a **"Download CSV file"** button.
5. Click **Download CSV file**. It downloads to `~/.playwright-mcp/` as
   `<Metric>-Orange County San Clemente Dana Point Laguna Beach-<YYYYMMDD>.csv`.
6. Click **Close**, then go to the next metric.

The dialog gets fresh refs every time it opens; snapshot it (depth 4 finds it near
the end of the page) to grab the CSV radio, the generate-Share button, and the
Download button each pass.

### 1c — Move the files into the repo

The downloads land in `~/.playwright-mcp/`, not the repo. Copy the 8 area CSVs into
a dated import folder:

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
