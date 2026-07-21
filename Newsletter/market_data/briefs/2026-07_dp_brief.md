# Issue 05 Brief — "How often does a home here actually change hands?" (late July 2026)

**Send window:** Late July 2026. Issue file: `Newsletter/issues/2026-07-21_issue-05.html`.

**FORMAT CHANGE, starts with this issue.** Adam flagged that the market-report format was going redundant. Diagnosis: the *thesis* was repeating (Issues 03, 04, and the first 05 draft all concluded "price it right"), and the recurring stat furniture (6 tiles + 5-city peer table = ~21 numbers) was identical every issue. New format is **one question per issue**, answered concretely, with the recurring stat tables moved to adamboehrer.com and linked. Result: 3,791 characters of prose vs ~8,100 in Issue 04, roughly half.

**Explicit constraint from Adam:** this issue must NOT be about price. Three in a row already were.

---

## The question
**How often does a home around here actually change hands?**

## The answer
About **one in thirty a year**. The rest of the neighborhood is staying put.

## Source: Adam's own title database (this is the differentiator)
`database/leads.db`, `properties` table. **2,179** First American IgniteRE title records across San Clemente (1,551) and Capistrano Beach (628). **1,604** carried a parseable `last_sale_date`.

This is the proprietary asset no other agent newsletter on this coast has. It answers questions the MLS structurally cannot, because the MLS only knows about homes that listed.

| Finding | Value |
|---|---:|
| Median tenure | **13.0 years** |
| Sold in last 12 months | **53 of 1,604 = 3.3%, about 1 in 30** |
| Sold in last 24 months | 7.3% |
| Owned 10+ years | 59.9% |
| Owned 20+ years | 33.2% |
| Owned 30+ years | 11.2% |
| Last bought before 2000 | 20.1% |

Median price **paid**, by decade of purchase (actual recorded transaction prices):

| Decade last sold | n | Median paid |
|---|---:|---:|
| 1980s | 45 | $279,000 |
| 1990s | 278 | $277,000 |
| 2000s | 306 | $674,750 |
| 2010s | 533 | $890,000 |
| 2020s | 429 | **$1,694,000** |

1990s to 2020s = **6.1x**.

Per-city split (the two towns are strikingly similar, which is why the issue treats them as one stretch of coast):

| | San Clemente | Capistrano Beach |
|---|---:|---:|
| Records / usable | 1,551 / 1,165 | 628 / 439 |
| Median tenure | 12.9 yr | 13.2 yr |
| Sold last 12 mo | 3.3% (1 in 31) | 3.4% (1 in 29) |
| Owned 20+ yr | 31.7% | 37.1% |
| Owned 30+ yr | 9.4% | **16.2%** |

Capistrano Beach has notably deeper roots than San Clemente (16.2% vs 9.4% at 30+ years). Held in reserve as a future Capo-specific issue rather than spent here.

## The "why it matters" — the payload (added after Adam's v2 note)

**Adam's critique of the first build of this issue was correct and is the key lesson for the format:** a surprising statistic is not an insight. The v1 draft found low turnover, said it was "quietly remarkable," and explicitly closed with "that isn't a reason to do anything." It never made the reader a smarter buyer or seller. **Every question-led issue must end with the reader knowing something they can use.**

The fix: prove that low turnover makes homes here genuinely hard to value, which is a thing readers already feel and can act on.

**Street-level comp analysis** (same table, `property_address` parsed to street; streets with >=10 sampled homes, 1,974 homes across 67 streets):

| Window | Median same-street sales per home | Homes with ZERO | Homes with <=2 |
|---|---:|---:|---:|
| Last 1 yr | 1 | **43%** | 86% |
| Last 3 yr | 3 | 12% | 43% |
| Last 5 yr | 5 | 6% | 26% |

**Within-street size dispersion:** median largest/smallest home = 3.0x; outlier-resistant 90th/10th percentile = **1.9x**. Copy uses "about twice the size," from the 1.9x figure, not the 3.0x.

**The argument the issue makes:** every automated valuation (Zillow, Redfin, bank tools) needs sales that are *recent*, *nearby*, and *similar*. This coast breaks all three at once. 43% of homes had no same-street sale last year; the median home had exactly one; and on a typical street the larger homes are double the smaller ones, so even that one comp may be a different house. The algorithm still returns a confident number to the dollar and never signals its own uncertainty.

**The four takeaways the issue gives the reader** (this is the "makes you more knowledgeable" payload):
1. Treat an online estimate here as a wide range, not a number; be suspicious when it swings month to month on no news.
2. One recent sale on your street is a data point, not a value, especially at a different size.
3. Price per square foot adjusted for condition, view, and lot travels across a thin comp set far better than raw sale price.
4. Buyers: a list price in a low-turnover pocket may be anchored to very little and has not necessarily been tested. Fair to ask what it was based on.

This also **earns the CTA honestly**: a hand-built comp analysis is the logical conclusion of the data, not a pitch bolted on.

**Is this a price issue?** No, and the distinction matters. Issues 03/04 were seller *strategy* ("price it right to sell"). This is *valuation literacy* for buyers and sellers both ("here is why any number you are handed is uncertain, and how to read it"). Adam should sanity-check that call.

## Secondary points, kept in prose not tiles
- Tight inventory is structural, not cyclical: Dana Point is down 26% in active listings YoY, but where median tenure is 13 years there simply aren't many homes in play.
- The reader lives somewhere people don't leave. Flattering and true, with nothing to sell.
- The 6.1x appreciation figure moved out of the stat tiles into the closing paragraph, since the tiles now all serve the valuation argument.

## Honesty guardrails (all reflected in the issue's method note)
- The sample is **the farm polygons Adam has pulled, not a census** of either town. Never write "every home in San Clemente." The issue says "a large sample rather than the final word."
- 1,604 of 2,179 had usable sale dates (74%). Stated in the issue.
- **Trust and intra-family transfers can reset a recorded sale date**, so true tenure is likely *longer* than measured, not shorter. Disclosed, and it cuts in the story's favor.
- `01/01/1900` sentinel dates and any future dates are filtered out by the analysis.
- **Never use assessed value (`total_value`) as current market value.** Prop 13 pins assessed value near purchase price for long-tenure owners, which would badly understate. The issue uses only *actual recorded transaction prices*.
- The 6x is decade-median-paid vs decade-median-paid across different homes, not the same house tracked over time. Copy says "on streets where homes have been changing hands closer to $1.7 million this decade," not "your home is now worth."

## Market data carried in this issue
Only one market figure survives into the email: Dana Point active inventory **down about 26% year over year** (92 active, 33 fewer homes), from the Pacific Sotheby's July 1 2026 deck. Everything else moved to the website.

Full Dana Point / peer-set numbers are current in `data/market_stats/2026-07_oc_market_report.json` and `data/market_stats/2026-07_dana_point_sfr.json` and are linked from the issue to `https://adamboehrer.com/dana-point-housing-market/`.

**Unused but ready** (parked from the abandoned price-led draft, still accurate, good for a future issue):
- The June 2026 Dana Point median/mix finding: median sale price -10.7% YoY while median $/sqft +2.3% and Zillow HVI +4.4%. A clean "the median is lying to you" issue.
- Reports on Housing OC June 2026 reduction breakdown: 75% of sales never cut price and got 100% of original ask in 9 days; the 12% that cut 5%+ took 90% of original ask after 70 days.
- Dana Point $5M+ vs under-$5M bifurcation: 97 days vs 8 days DOM in May.

## Local item
**Wind & Sea closing Sept 15** after 54 years, last of the original harbor restaurants, for the Dana Wharf rebuild. Verified 2026-07-21 via Dana Point Times, Patch, OC Business Journal. Alternates verified and unused: new Wednesday harbor farmers market from Sept 24; Ohana Festival Sept 25-27; Maritime Festival Sept 11-13.

**Do NOT use** (research could not verify): a "Mack's Tavern" in the Lantern District; a June 2026 Dana Point special election.

## Question bank for future issues
Each of these is answerable from data already in hand, and none of them is a pricing lecture.

1. **What share of homes here are owned free and clear?** Needs a loan-data cleanup first: `first_loan_amount` is NULL on 297 of 628 Capo records and NULL is ambiguous between "no loan" and "not captured." Do not publish until that's resolved.
2. **What does the ocean view actually cost?** View vs non-view comps on the same street.
3. **What did 40 people at an open house actually ask?** Firsthand from Calle Dolores. Fresh by construction.
4. **Can you actually short-term rent it?** Adam already has verified rules research for Oceanside, Carlsbad, and Newport through Santa Barbara. Dana Point's bed tax was its top revenue source at $16M+ in 2024. Strong second-home/investor issue.
5. **What does $2M actually get you in each of the five towns?** Concrete and comparative.
6. **Capistrano Beach has deeper roots than anywhere else nearby.** 16.2% owned 30+ years. A Capo-specific follow-up to this issue.
7. **What do sellers actually spend getting a house ready, and does it come back?**

## Build notes
- CTA deliberately soft, because the issue just finished saying most readers aren't moving. Leaning hard on a sales CTA after that would undercut the piece. Drives to adamboehrer.com, `utm_campaign=2026-07_issue-05`.
- Locked header/footer JPGs unchanged. `*|UNSUB|*` intact. Brand palette and weights validated (max 600).
- No em-dashes, no "client" language, no overpromising.
- The **city rotation may no longer be needed.** In a question-led format the question sets the scope, not a rotating city. This issue already spans San Clemente and Capistrano Beach because that's where the data is. `NEWSLETTER_GUIDE.md` still documents the old rotation and section lineup and needs updating once Adam confirms the format sticks.
- Still open from Adam: a firsthand observation, and any coming-soon deal for a First Look block.
- After publish: regenerate `website/data/stats.json` and offer to commit + push (standing rule). Website SC row is still on May closings from the 2026-06-16 pull; June closings should be available now.
