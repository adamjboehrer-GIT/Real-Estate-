# San Clemente Market Brief — Issue 04 (July 2026)

**Send window:** First week of July 2026. Issue file: `Newsletter/issues/2026-07-01_issue-04.html`. Featured area rotates from Capistrano Beach (Issue 03) back to **San Clemente** per the rotation. CTA rotation returns to Issue 1 slot: seller "thinking about selling" angle (Adam's approved seller voice).

**Sources:**
- CRMLS via InfoSparks, pulled 2026-06-16: `data/market_stats/2026-06_san_clemente_sfr.json` + `data/market_stats/2026-05_market_moves.json` (San Clemente SFR, May 2026 closings). Latest available; June closings not posted until mid-to-late July.
- Pacific Sotheby's **June 2026** Market Report ("Laguna Beach Office Meeting June 16 2026 FINAL"), PDF at `Newsletter/market_data/sources/2026-06-16_pacific_sothebys_deck.pdf`. Image-based deck (no extractable text); San Clemente city-wide + peer figures transcribed by hand for the June (Capo) issue and reused here. Covers May 2026 closings, April 2026 Zillow HVI. NOTE: this deck was NOT loaded into SQLite; the DB `market_metric_latest` still holds the older May-1 deck for San Clemente (EMT 54, etc.) — do not use the DB row for this issue.

---

## The data story in one sentence
San Clemente is holding: the median home sold at 100% of its asking price and values are up ~10% YoY, it leads the coastal peer set on 10-year appreciation (+116%), and inventory finally loosened this summer (active listings 79 → 97 in a month) — so the story is "more to choose from, without the discount," not a slowdown. (Two-markets angle from the prior draft was retired at Adam's request; DOM pulled from By The Numbers to avoid confusion next to Estimated Market Time.)

## San Clemente — the recurring stats
**Single-family (InfoSparks, May 2026 closings):**
- Median days on market **8** (down from 14 a year ago).
- Months of supply **2.7** (down from 3.5 a year ago; a seller's market under six months).
- Median sales price **$2.24M** (up 10.5% YoY from $2.025M; 39 closed sales, up from $2.05M in April — read as a range at low volume, lean on the ~10% YoY).
- Active listings 97 (down 37% from 155 a year ago). New pendings 36 vs 51 (soft, late-posting artifact — do not feature; see June SFR json note).

**All residential (June deck, May closings / June snapshot):**
- Estimated Market Time **65 days**.
- **36%** of listings with a price cut (highest in the fast tier — the overpricing signal).
- Sale-to-list **97.6%** (all residential, May closings).
- Zillow HVI 10-year **+115.8%** (April 2026), top of the coastal-peer pack with Newport Coast.

## "San Clemente in Context" peer table (fixed 5 coastal peers, San Clemente highlighted)
Full residential, May 2026 closings, June deck snapshot.

| City | Est. Market Time (days) | % price cuts | Sale-to-list (May, all) | 10-yr growth |
|------|------------------------:|-------------:|------------------------:|-------------:|
| San Clemente | 65 | 36% | 97.6% | +116% |
| Dana Point | 112 | 31% | 93.1% | +115% |
| Laguna Beach | 180 | 43% | 99.8% | +97% |
| Newport Coast | 123 | 31% | 93.8% | +133% |
| San Juan Capistrano | 68 | 27% | 92.7% | +98% |

10-yr exact (Zillow HVI, April 2026): SC +115.8%, DP +114.7%, Laguna +97.2%, Newport Coast +133.3%, SJC +97.8%.

Interpretation: San Clemente is the fastest-clearing market in the set at 65 days, essentially tied with San Juan Capistrano, and roughly half the time of Newport Coast and a third of Laguna Beach. Its 36% price-cut rate is the highest of the fast movers, which is exactly the two-markets story: a lot of listings are testing high prices and cutting, yet well-priced homes still close near 98% of asking. Long term, SC leads the coastal peers alongside Newport Coast.

## Verified local items (web-checked 2026-07-01)
- **Miramar Food Hall (North Beach) — USED as neighborhood item 2:** the historic 1938 Miramar theater / old bowling alley reopened **June 18, 2026** as the Miramar Food Hall at 1720 N. El Camino Real: ~12,600 sq ft, 15 independent food vendors + 2 full bars. Wedgewood led the historic restoration; Tiger Hospitality Group operates. Key piece of North Beach revitalization. (San Clemente Journal, Picket Fence Media, OCBJ, Hoodline)
- **OCTA coastal-rail sand nourishment — DROPPED at Adam's request** (felt low-relevance vs. the Miramar). Kept here for reference: initial North Beach placement complete, ~540,000 cu yd planned across SC beaches, ~$310M emergency rail package, Beach Trail + ~1,400-ft catchment wall near Mariposa due summer 2026.
- **Summer Concert Series:** free Thursday concerts, 6pm, at the San Clemente Pier and Linda Lane Park, running roughly **July 9 through August 13, 2026**. Highlights: Knyght Ryder (Jul 16, Pier), V-Time Firefighter Band (Jul 23, Pier), Pistol Blonde (Jul 30, Pier), Common Sense (Aug 13). 20+ year tradition, 1,000+ per show. (sanclemente.gov, SC Chamber)
- **Fiesta Music Festival:** Aug 8, 2026, free, two stages of continuous entertainment. (SC Chamber)

## National framing (June deck outlook, unchanged from Issue 03)
Market normalizing into summer: supply climbing toward its July–August peak, demand past peak, buyers with a bit more negotiating room. Rates mid-6%. Per standing guidance: NO rate-pressure or ARM angle to frame sellers.

## Build notes
- CTA rotation = Issue 1 slot: "thinking about selling." Adam's approved seller voice (meet people where they are, understand what matters most, position the home for the most offers and best terms). NO overpromising ("I have buyers"), NO "no pressure/no obligation" disclaimer padding. Points to https://adamboehrer.com. utm_campaign=2026-07_issue-04.
- Deal Highlights / First Look: omitted (no Adam-provided coming-soon). Offer to add a block if he supplies one.
- Carry the locked Coastal Currents header/footer JPGs unchanged.
- Personal note drafted in Adam's voice for him to edit. Ask him for one firsthand San Clemente observation for the neighborhood section.
- After publish: regenerate website/data/stats.json and offer to commit + push (standing rule).

## Next issue (Issue 05, mid-to-late July)
Featured area rotates to **Dana Point**. CTA rotation → Issue 2 slot: "what's your home worth right now." Brief at `Newsletter/market_data/briefs/2026-07_dp_brief.md`.
</content>
</invoke>
