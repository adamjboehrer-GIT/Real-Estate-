# The Coastal Insider — Newsletter Guide

## Cadence
Bi-weekly. New issue every two weeks. File naming: `YYYY-MM-DD_issue-##.html`

## How to Get the Next Issue
Come back every two weeks and say: **"Build the next newsletter issue."**
Claude will research current content, pull updated stats, and generate a new HTML file ready to upload to Mailchimp.

When a fresh Pacific Sotheby's deck lands (also biweekly), say: **"Ingest the new Sotheby's deck."** Claude will transcribe the data into `data/market_stats/YYYY-MM_oc_market_report.json`, load it into SQLite (`market_metric` table), and refresh the stats blocks in the current issue.

---

## What Adam Fills In Each Issue
These are the only items that require your personal input. Everything else is researched automatically.

1. **Personal note headline + body** — 3 to 4 sentences in your voice. What are you seeing? What are people asking? What's your read on the market right now?
2. **Hyper-local neighborhood intel** — One thing you personally noticed in this issue's featured area: a renovation, a permit pulled, a neighbor prepping to list, a specific home that just sold. Never name Adam's home street.
3. **Coming soon teaser** (if applicable) — Neighborhood, price range, one compelling detail. No address needed.

---

## Uploading to Mailchimp

1. In Mailchimp, go to **Campaigns → Create Campaign → Email**
2. Choose **"Code your own"** template option
3. Paste the full HTML file contents
4. The header and footer images are already linked to Mailchimp-hosted URLs; they render automatically.
5. Preview and send

**Note:** The `*|UNSUB|*` in the footer is a Mailchimp merge tag. Leave it exactly as written. Mailchimp replaces it automatically with the unsubscribe link.

---

## Sections (in order)

| Section | Label | Updated By | Source |
|---------|-------|------------|--------|
| Personal note | "A Note From Adam" | Adam — every issue | Adam's voice |
| Neighborhood intel | "What's Happening in the Neighborhood" | Claude researches + Adam adds one personal item | Field observation |
| Lifestyle | "What's New in San Clemente" | Claude researches | Local news, openings, events |
| Deal highlights | "Deals Worth Knowing About" | Adam provides deal context, Claude writes copy | Adam's pipeline |
| Market stats | "By The Numbers" | Claude researches | InfoSparks SFR + Pacific Sotheby's deck |
| Peer comparison | "San Clemente in Context" | Claude researches | Pacific Sotheby's deck |
| OC comparison | "San Clemente vs. Orange County" | Claude researches | InfoSparks + CRMLS Local Market Update |
| Coming soon | "First Look" | Adam — only when applicable | Adam's pipeline |
| CTA | — | Rotates each issue | — |

---

## CTA Rotation (alternate these)
- Issue 1: "Do you know someone thinking about selling?"
- Issue 2: "Want to know what your home is worth right now?"
- Issue 3: "Know a buyer who's been sitting on the sidelines?"
- Issue 4: Back to issue 1

---

## Market Stats: Sources and Structure

### Sources used
| Source | Covers | Frequency | Used For |
|---|---|---|---|
| CRMLS via InfoSparks (ShowingTime Plus) | San Clemente, Single-Family Residential | Monthly | "By The Numbers" top row |
| Pacific Sotheby's Market Report (internal deck) | 12 OC cities, all property types, city-wide | Biweekly | "By The Numbers" bottom row + "San Clemente in Context" |
| Mortgage News Daily | 30-year fixed rate | Continuous | National framing (optional) |
| Fannie Mae HPSI / NAR RCI | National demand, offers, first-time buyer share | Monthly | National framing (optional) |

### "By The Numbers" — 6 stats, 2 rows of 3

**Row 1 — San Clemente Single-Family (InfoSparks, last closed month):**
- Median days on market
- Months of supply
- Median sales price

**Row 2 — San Clemente city-wide (Pacific Sotheby's deck, current snapshot):**
- Active listings with price reduction (%)
- Sale-to-list ratio (most recent closed month)
- Price band split: under $5M vs $5M+ S/L ratio

Source footnote cites both InfoSparks and the Pacific Sotheby's report with their respective reporting months.

### "San Clemente in Context" — 5-city peer table

**Peer cities (fixed set):** San Clemente, Dana Point, Laguna Beach, Newport Coast, San Juan Capistrano.

*Why this set:* Coastal-equal peers for an SC reader. Laguna Beach is the cultural comp; Newport Coast is the $5M+ comp; SJC is the natural equity-up or retirement/estate move; Dana Point is the next-door neighbor. Laguna Niguel was considered but dropped (inland-feeling, not aspirational for a coastal reader).

**Metrics in the 5-city table (rotate by issue, pick 3):**
- Expected Market Time (days)
- % listings with price reductions
- Sale-to-list ratio (most recent closed month)
- Median sold price (most recent closed month)
- Median DOM (sold homes)

**Footnote always includes:** 10-year Zillow HVI growth for all 5 cities. This anchors SC's long-term performance.

### Brief national framing (optional)

When it strengthens the issue's narrative, add a two-line "national pulse" paragraph inside "A Note From Adam" or at the top of "By The Numbers." Never jargon-heavy. Example tone: "30-year fixed rates are sitting near 6.3% heading into May. Nationally, spring is still the deepest buyer pool of the year. Locally, that's showing up as fast closings in San Clemente under $5M."

---

## Data Pipeline: How Stats Get Into an Issue

1. **Deck arrives** → save PDF to `Newsletter/market_data/sources/YYYY-MM-DD_pacific_sothebys_deck.pdf`
2. **Transcribe** key city and national figures into `data/market_stats/YYYY-MM_oc_market_report.json` (one file per deck)
3. **Load** into SQLite: `python3 scripts/load_market_stats_json.py data/market_stats/<file>.json`
4. **Write editorial brief** at `Newsletter/market_data/briefs/YYYY-MM_sc_brief.md`: the "what's the story this issue" distillation
5. **Refresh issue HTML** with the new numbers and one-line interpretations

To query the latest value for any metric across cities:
```sql
SELECT geo_name, metric_value
FROM market_metric_latest
WHERE metric_key = 'expected_market_time_days'
ORDER BY metric_value ASC;
```

---

## Brand Standards (do not modify)
- Colors: SIR Blue `#002349`, Gold `#C29B40`, Text Grey `#666666`, White `#FFFFFF`
- Fonts: Amiri (serif/headlines), Source Sans Pro (body)
- No bold heavier than semibold. No underlined text. No black backgrounds.
- Gold used as accent dividers only, never as background.
- No em-dashes in prose. Use commas, periods, or "to" for ranges.
- No "client" language when addressing the reader. The reader is the client.
