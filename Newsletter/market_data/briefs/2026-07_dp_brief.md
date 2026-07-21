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

## Why this is the story, and why it isn't a price story
1. **It reframes what "the market" means.** Every stat we publish describes ~3% of homes. The other 97% aren't participating. That's a genuinely new idea for the reader, not pricing advice.
2. **It explains tight inventory structurally.** Dana Point is down 26% in active listings year over year. The easy read is "cycle." The title data says otherwise: where median tenure is 13 years and 1 in 5 last bought before 2000, there simply aren't many homes in play. Low inventory is a property of the neighborhood, not a phase.
3. **It's flattering and true.** The reader lives somewhere people don't leave. No pressure, no urgency, nothing to sell.

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
