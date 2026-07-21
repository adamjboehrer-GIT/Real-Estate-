# Dana Point Market Brief — Issue 05 (late July 2026)

**Send window:** Late July 2026. Issue file: `Newsletter/issues/2026-07-21_issue-05.html`. Featured area rotates from San Clemente (Issue 04) to **Dana Point**. CTA rotation → Issue 2 slot: "what's your home worth right now."

**Sources:**
- CRMLS via InfoSparks, pulled 2026-07-15: `data/market_stats/2026-07_dana_point_sfr.json` (Dana Point SFR detached, **June 2026** closings). Fresh. Note this pull swapped the usual Active Listings + Pending Sales reports for **Median Price Per Square Foot**, which turns out to be the key metric for this issue.
- Pacific Sotheby's **July 1 2026** Market Report: `data/market_stats/2026-07_oc_market_report.json`, PDF at `Newsletter/market_data/sources/2026-07-01_pacific_sothebys_deck.pdf`. Loaded to SQLite 2026-07-13. Snapshot is as of 7/1/2026; **sold figures cover MAY 2026** (this deck lags two months, not the usual one); Zillow HVI is May 2026.
- Reports on Housing (Orange County, June 2026) price-reduction breakdown, captured in the deck JSON under `orange_county.reduction_breakdown`.

---

## The data story in one sentence
Dana Point's median sale price fell 10.7% year over year while the price per square foot rose 2.3% and Zillow's index for the town rose 4.4%, which means the median moved because a different **mix** of homes closed in June, not because Dana Point homes lost value. The whole issue hangs on that gap, and it lands directly on the CTA: a citywide median tells you nothing about what your specific home is worth.

## Dana Point — the recurring stats

**Single-family detached (InfoSparks, June 2026 closings):**
| Metric | June 2026 | June 2025 | YoY |
|---|---:|---:|---:|
| Median price per sq ft | **$972** | $950 | **+2.3%** |
| Median days active in MLS | **13** | 19 | -31.6% |
| Months of supply | **3.2** | 4.3 | -25.6% |
| Median sales price | $2,097,500 | $2,350,000 | **-10.7%** |

Trailing three months (Apr / May / Jun 2026):
- Median price: $2.99M → $3.15M → $2.10M
- Median $/sqft: $1,442 → $1,538 → $972
- Months supply: 3.2 → 3.2 → 3.2 (flat all quarter)
- DOM: 12 → 9 → 13

**Read carefully:** median price and median $/sqft fell together and by similar proportions. Both moving in lockstep is the signature of a **mix shift** (a batch of smaller, lower-priced homes closed in June), not a broad markdown. The InfoSparks JSON `data_quality_notes` says exactly this. Corroborating evidence that values did not fall: Zillow HVI for Dana Point is **+0.3% month over month and +4.4% year over year** (May 2026), and months of supply never budged off 3.2 all quarter.

**All residential (July 1 deck snapshot / May 2026 closings):**
- Active inventory **92**, down 26% year over year (33 fewer homes, was 125).
- New pendings 34, down 6% (2 fewer).
- Estimated Market Time **81 days**, down from **104** a year ago.
- **32%** of active listings carrying a price cut. Lowest in the coastal peer set.
- May 2026 closings, all: 31 homes, **$2.1M** median, **95.6%** sale-to-list, **8 days** DOM.
  - Under $5M: 29 homes, $2.1M, 95.5%, 8 days.
  - $5M+: 2 homes, $12.3M, 103.8%, 97 days. (n=2, do not lean on this.)
- Zillow HVI (May 2026): +0.3% MoM, +4.4% YoY, **+113.3%** over ten years.

**The interesting tension:** homes go pending in about 8 days yet close at 95.6% of last list. Fast AND negotiated. Sellers are setting the ask a few points high, buyers are trimming it, and the deal is done inside a week and a half. That is the price story with a Dana Point accent, and it is different from San Clemente (10 days, 101.1%).

*Deck transcription gotcha already handled:* the per-city Dana Point sold slide reads 314 homes / $2.2M (count-bleed corruption). The aggregate slide's 31 homes / $2.1M is correct and reconciles ($0-5M 29 + $5M+ 2 = 31). Use 31 / $2.1M / 95.6% / 8 days.

## The supporting stat: what a price cut actually costs
Reports on Housing, Orange County, June 2026 (as of 7/1/2026). This is the strongest, most concrete seller stat in the whole dataset and it belongs in this issue:

| Listing history | Share of sales | % of **original** list received | Median days on market |
|---|---:|---:|---:|
| Never reduced | **75%** | **100.0%** | **9** |
| Reduced 1 to 4% | 13% | 95.5% | 47 |
| Reduced 5% or more | 12% | 90.0% | 70 |

Three quarters of Orange County sales never cut price at all, and those sold at the full original asking price in nine days. The ones that had to cut 5% or more ended up taking 90 cents on the original dollar and waited ten weeks to do it. Getting the number right the first time is worth roughly ten percent and two months. Frame this as information, not pressure. No urgency language, no "I have buyers."

## "Dana Point in Context" peer table (fixed 5 coastal peers, **Dana Point** highlighted)
Full residential, May 2026 closings, July 1 2026 deck snapshot.

| City | Est. Market Time (days) | % price cuts | Sale-to-list (May, all) | 10-yr growth |
|------|------------------------:|-------------:|------------------------:|-------------:|
| **Dana Point** | **81** | **32%** | **95.6%** | **+113%** |
| San Clemente | 68 | 34% | 101.1% | +115% |
| Laguna Beach | 176 | 40% | 97.6% | +86% |
| Newport Coast | 173 | 33% | 92.2% | +132% |
| San Juan Capistrano | 74 | 34% | 99.0% | +96% |

10-yr exact (Zillow HVI, May 2026): DP +113.3%, SC +114.7%, Laguna +85.6%, Newport Coast +131.5%, SJC +96.4%.

Interpretation: Dana Point is the **second-fastest-clearing market in the set** at 81 days, behind San Clemente (68) and essentially tied with San Juan Capistrano (74), and it clears in less than half the time of Laguna Beach (176) or Newport Coast (173). It also has the **lowest price-cut rate** in the group at 32%, meaning fewer Dana Point sellers are having to reset. Over ten years it has nearly matched San Clemente and run well ahead of Laguna Beach.

*Watch the Zillow revisions:* Laguna Beach's 10-year figure moved from +97% (June deck) to +85.6% (July deck) and Dana Point from +114.7% to +113.3%. These are Zillow index revisions, not errors. Cite the July deck.

## National framing
The July 1 deck has **no national/macro section at all** (no mortgage-rate, NAR confidence, ARM, or Fannie forecast slides). Skip national framing this issue or keep it to a single general line. Standing rule: NO rate-pressure or ARM angle to frame sellers.

## Build notes
- **Row 1 hero stat is median price per square foot ($972), not median sales price.** Leading a tile with "$2.10M, down 10.7%" would be actively misleading given the mix shift. The median is addressed head-on in the neighborhood section narrative instead, which is both more honest and the more interesting read.
- CTA = Issue 2 slot, home value report, driving to https://adamboehrer.com. utm_campaign=2026-07_issue-05. **Rewrite the copy from scratch** — Issue 02 (May, also Dana Point) used this same CTA slot and the language should not repeat.
- **Do not repeat Issue 02's lifestyle items.** That issue already covered the harbor revitalization (marina progress, Mariner's Village, The Brig / Beach Harbor Pizza closing) and the Lantern District / White Rooster / summer concert series. Issue 05 needs fresh, web-verified Dana Point items.
- Carry the locked Coastal Currents header/footer JPGs unchanged.
- Deal Highlights / First Look: pending Adam. Ask.
- Personal note and one firsthand Dana Point observation: pending Adam. Ask.
- Never name Adam's home street. No em-dashes in prose. No "client" language addressing the reader.
- After publish: regenerate `website/data/stats.json` and offer to commit + push (standing rule).

## Open data item (not blocking this issue)
The website's San Clemente SFR row is still **May 2026** closings from the 2026-06-16 InfoSparks pull. June closings should be posted by now. A fresh San Clemente SFR pull (the five standard reports) would refresh `website/data/stats.json` Row 1 and re-align the page header month. Worth doing in the same session as this send.

## Next issue (Issue 06, early-to-mid August)
Featured area rotates to **Capistrano Beach**. CTA rotation → Issue 3 slot: "know a buyer who's been sitting on the sidelines." Brief at `Newsletter/market_data/briefs/2026-08_capo_brief.md`.
