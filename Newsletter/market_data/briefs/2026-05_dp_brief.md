# Dana Point Market Brief — Issue 02 (mid-to-late May 2026)

**Source:** Pacific Sotheby's **May 1, 2026** Market Report (April 2026 closings, March 2026 Zillow HVI). PDF archived at `Newsletter/market_data/sources/2026-05-01_pacific_sothebys_deck.pdf`. JSON at `data/market_stats/2026-05_oc_market_report.json`. Loaded to SQLite and `website/data/stats.json` on 2026-05-19.

**Send window:** Mid-to-late May 2026. Issue file (to be built): `Newsletter/issues/2026-05-DD_issue-02.html`. Featured area rotates from San Clemente to **Dana Point** per the Issue 01 brief plan.

**Open dependency:** Row 1 of "By The Numbers" (San Clemente single-family, InfoSparks) is still **March 2026** data. It does not refresh from this deck. A fresh InfoSparks pull is needed before this issue sends (see the refresh checklist).

---

## The data story in one sentence
San Clemente is still one of the fastest markets in Orange County, but the price discipline loosened: typical homes still go pending in about ten days, yet the under-$5M list-to-sale gap widened and the share of listings with a price cut climbed from 28% to 36%.

## San Clemente, this deck (the recurring "By The Numbers" row 2)
- **Snapshot (May 1):** 99 active, 55 new pendings, Expected Market Time 54 days, 36% of active listings carrying a price cut.
- **Year over year:** inventory down 33% (48 fewer homes), demand up 25% (11 more pendings), market time down 46 days (was 100 a year ago). Still the second-fastest of the twelve OC cities tracked, behind only Aliso Viejo (51 days).
- **April 2026 closings:** 69 homes. All price points: $1.9M median, 98.5% sale-to-list, 10 days on market. Under $5M: 64 homes, $1.8M, 94.9%, 10 days. $5M+: 5 homes, $6.6M, 101.6%, 19 days.
- **Zillow HVI (March 2026):** +0.5% month over month, -0.2% year over year, +118.7% over ten years.

What changed from the April brief: that issue's story was "well-priced homes closing above list in about fifteen days" (S/L 100.8%, 101.1% under $5M). This deck shows homes moving even faster (10-day median) but closing about five points under last list in the under-$5M band, with more sellers reducing price. The honest read for a seller: speed is still there if the home is priced and presented right, but buyers have regained negotiating room on the typical home. Frame around meeting the market where it is and positioning for the strongest offers, not around urgency or "I have buyers."

## Featured area this issue: Dana Point
Anchor line draft: "the harbor town between San Clemente and Laguna Beach, anchored by the harbor, Doheny, Salt Creek, and the Headlands."

Dana Point in the May 1 deck:
- **Snapshot:** 84 active, 36 pending, Expected Market Time 70 days, 31% of listings with a price cut.
- **Year over year:** inventory down 30% (36 fewer homes), demand up 71% (15 more pendings), market time down 101 days (was 171 a year ago). One of the sharpest one-year tightenings in the county.
- **April 2026 closings:** 38 homes. All: $1.8M median, 100.7% sale-to-list, 13 days. Under $5M: 31 homes, $1.6M, 99.7%, 12 days. $5M+: 7 homes, $9.8M, 93.6%, 80 days.
- **Zillow HVI (March 2026):** +0.7% month over month, +3.3% year over year, +117.8% over ten years.

The Dana Point story: the everyday market (under $5M) is closing essentially at list in under two weeks and is far tighter than a year ago, while the $5M+ tier is the slower, more negotiable segment (80-day median, 93.6% of list). Two clean, data-grounded angles for either a buyer or a seller, no overpromising required.

## "San Clemente in Context" peer table (refresh these numbers)
Peer set is fixed: San Clemente, Dana Point, Laguna Beach, Newport Coast, San Juan Capistrano.

| City | Days to clear (EMT) | % listings with a price cut | Sale-to-list (April closings, all) | 10-yr home value growth |
|------|--------------------:|----------------------------:|-----------------------------------:|------------------------:|
| San Clemente | 54 | 36% | 98.5% | +119% |
| Dana Point | 70 | 31% | 100.7% | +118% |
| Laguna Beach | 198 | 38% | 96.4% | +92% |
| Newport Coast | 117 | 26% | 93.0% | +136% |
| San Juan Capistrano | 93 | 37% | 102.9% | +101% |

Footnote to carry: figures are the Pacific Sotheby's May 2026 report (April 2026 closings, March 2026 Zillow ten-year growth). San Clemente's market time is the second-shortest in the peer set and the wider county.

## Transcription gotchas in this deck (already handled in the JSON, noted here for trust)
- Dana Point's Zillow row on the main price slide was a duplicate of Huntington Beach's. The South Coastal regional slide gives the correct DP figures (+0.7% / +3.3% / +117.8%); those are what the table above uses.
- Huntington Beach's per-city demand box was a duplicate of Dana Point's. Not in the peer table, so no newsletter impact.
- Corona del Mar's $5M+ median on its per-city slide was corrupt ("$1.5"); the aggregate slide ($7.8M) was used. Not in the peer table.
- San Clemente's under-$5M days-on-market read 64 on the aggregate slide (home count bleeding into the column); the per-city slide and the math confirm 10 days.

## National framing changed this deck
This deck dropped the 7-year ARM rate, ARM application share, and the Fannie Mae five-year price forecast that the April deck carried. It instead has a Fannie Mae / MBA / Wells Fargo mortgage rate projection (30-year heading toward roughly 6.2% through 2027, Fannie Mae more optimistic at ~5.7%), national inventory still 13.8% below 2017-2019, new listings nearly doubling since December, and the NAR Realtor Confidence read for March 2026: only 26% expect demand to rise (down from 37% a month earlier), 18% of homes sold above list, 2.2 offers per listing, first-time buyers 32%. Per the standing guidance, do not use any rate-pressure or ARM angle to frame sellers. The usable macro line is simply that rates remain the swing factor and the deck's own outlook expects market time to keep rising as spring supply builds, so listing sooner is the advantage.

## Refresh-before-send checklist
- [ ] Pull a fresh InfoSparks San Clemente single-family set so Row 1 reflects April closings (the five reports: Median Sales Price, Median Days Active in MLS, Active Listings, Inventory Months Supply, Pending Sales). Drop in `data/imports/mls_stats/YYYY-MM-DD/`, then refresh `data/market_stats/2026-05_san_clemente_sfr.json` and rerun `generate_website_stats.py`.
- [ ] Build the Issue 02 HTML with Dana Point as the featured area; carry the locked Coastal Currents header/footer JPGs unchanged.
- [ ] Verify any Dana Point local items (events, openings) with a web search before writing them. Do not invent specifics.
- [ ] Keep the CTA on the approved seller-voice positioning (meet people where they are, understand what matters most, position the home for the most offers and the best deal). No "I have buyers," no urgency, no client-speak.
- [ ] Confirm the peer-table footnote month wording (April 2026 closings, March 2026 ten-year growth).
