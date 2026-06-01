# LinkedIn Content System — Pillars & Rotation

Expands `Marketing/social_posts/SOCIAL_PLAN.md` from biweekly to **2x/week LinkedIn**
(Tue + Thu, 7–9am PT) across four content pillars. Goal unchanged: quietly build
authority as the South OC coastal agent and feed Coastal Currents. Not a vanity feed.

Publishing model: **review-and-post queue.** Claude writes finished posts into
`QUEUE.md`. Adam reads, tweaks, and posts (or schedules) himself. Nothing auto-posts.
This keeps the voice authentic and stays inside LinkedIn's terms of service.

Handles: LinkedIn `/in/adam-boehrer-0b2118133` · IG `@adamonthecoastoc`

---

## Voice rules (non-negotiable — pulled from saved feedback)

- **No em-dashes or en-dashes.** Commas, periods, or short splits. Reads as AI otherwise.
- **No client-speak.** The reader IS the buyer/seller, not an agent with their own clients.
  Never "your clients," "your buyers."
- **No overpromising.** Never "I have buyers lined up." Default to honest valuation,
  network top-of-mind, positioning expertise.
- **Seller voice:** meet people where they are, understand what matters most, position the
  home to bring the most offers and the best deal. Not "I find buyers."
- **No street naming.** "San Clemente" or a neighborhood name is the right specificity.
  Never Adam's home street.
- **No fabricated local claims.** Verify any neighborhood, event, or sales specific with a
  web search before writing it. When unsure, stay general.
- **Substance over generic.** Every post leads with a real number, a real observation, or a
  real piece of Adam's story. No "the market is shifting" filler.
- **Refine, don't paste.** Anything Adam dictates is a draft to polish, then confirm back.

LinkedIn: **no hashtags.** Clean professional feed. (Hashtags are an Instagram convention.)

---

## The four pillars

### P1 — Market data / stats
The authority anchor. Repurpose the latest InfoSparks pull, stats.json, and the Pacific
Sotheby's deck into one plain-English read. Lead with ONE number. Two to three sentences
of what it means for someone living in the market (not a forecast). One line on who it
favors this cycle, no hype. Close pointing to Coastal Currents.
Source of numbers: `website/data/stats.json` and `Newsletter/market_data/briefs/`.

### P2 — Neighborhood spotlight
Lifestyle + market angle on one South OC pocket (San Clemente, Dana Point, Capistrano
Beach, Carlsbad, Oceanside, Laguna, Newport Coast). One specific, verified detail that
places the neighborhood, then why it matters to a buyer or owner there. Web-verify any
named opening, build, or sale. No on-photo text if an image is used.

### P3 — Personal / story-driven
The human connection that converts. Adam's differentiating background: a father and
neighbor first, an out-of-state investor and brand strategist before real estate. Why he
reads markets the way he does, what he learned buying from a distance, why he picked this
coast. Specific and grounded, never a humblebrag.

### P4 — Seller / buyer education
Positioning the expert. One concrete tip, myth-busted, or checklist item. Pairs with the
South OC Sellers Playbook lead magnet. Reader IS the seller/buyer. Practical, no jargon,
no gating gimmicks.

---

## Rotation (4-week cycle, Tue + Thu)

Market data lands every other week to match the biweekly InfoSparks / deck cadence. Pillars
interleave so two consecutive posts never repeat a pillar.

| Week | Tue | Thu |
|------|-----|-----|
| 1 | P1 Market data | P3 Personal |
| 2 | P2 Neighborhood | P4 Education |
| 3 | P1 Market data | P4 Education |
| 4 | P2 Neighborhood | P3 Personal |
| (repeat) | | |

Week number = ISO-week mod 4 (1–4). Skipping a week is allowed; resume the cycle where it
left off. A week with no real market read and no genuine observation is better skipped than
filled with filler.

---

## Post length targets

- P1 Market data: 150–200 words.
- P2 Neighborhood: 120–180 words.
- P3 Personal: 120–200 words. Most leeway here; story sets the length.
- P4 Education: 100–160 words.

Open with the hook on its own line (LinkedIn truncates after ~210 chars before "see more").
First line has to earn the click-to-expand on its own.

---

## How a batch gets generated

Say: **"generate this week's LinkedIn posts."**
The `linkedin-posts` skill: reads the current ISO week, picks the two pillars for that week,
pulls the freshest stats, drafts both posts into `QUEUE.md`, and appends rows to
`linkedin_log.csv` with status `draft`. Adam reviews, edits in place, posts, then marks the
log row `posted` (or just says "mark this week posted").

Optional automation: a Monday-morning routine can pre-fill `QUEUE.md` each week so the drafts
are waiting. Not enabled by default; Adam opts in.
