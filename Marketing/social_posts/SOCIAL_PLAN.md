# Coastal Currents Social Plan — LinkedIn & Instagram

Purpose: drive newsletter subscriptions and quietly build authority in the South OC coastal market. Not a vanity feed. Every post either (a) shows real read on the market or (b) points to the newsletter / website.

Voice rules in force: no em-dashes, no client-speak (the reader IS the buyer/seller, not someone with their own clients), substance over generic, meet people where they are. Brand rules in `CLAUDE.md` apply to every visual (SIR Blue, Gold accents only, Freight/Mercury/Benton Sans or web fallbacks, no bold-or-heavier weights, 1pt borders max, no text overlaid on property photos).

Handles: IG `@adamonthecoastoc` · LinkedIn `/in/adam-boehrer-0b2118133`

---

## Cadence (weekly rhythm)

| Day | Channel | Format |
|-----|---------|--------|
| Tue 7–9am PT | LinkedIn | Market read (biweekly) **or** What I'm watching (alternating week) |
| Sat 9–11am PT | Instagram | Coast moment (weekly) |
| 1st of month | Both | Newsletter subscribe reminder (existing graphic) |

Three repeatable formats per week max. Anything more becomes a content engine that needs feeding, and that is not what we're trying to build right now.

---

## LinkedIn — three formats

### LI-1. Market Read (biweekly, after each InfoSparks pull)
**Image:** 1200x1200 stat card. Top: Coastal Currents header. Middle: ONE number that matters this cycle, set in Mercury/serif at large size in SIR Blue, with one supporting line in Benton Sans / sans-serif. Thin gold divider. Bottom: realtor lockup (reuse from `build_subscribe_post.py`).

**Post copy template (150–200 words):**
> [One sentence stating the headline number in plain English. Example: "Median sold price in San Clemente moved up 1.4% this cycle, while days on market stretched to 38."]
>
> [Two to three sentences of read on what that means for someone living in the market. Not a forecast. What buyers and sellers are actually doing right now.]
>
> [One sentence on the implication: who this favors this cycle, with no hype.]
>
> Full breakdown for Newport, Laguna, Dana Point, San Clemente, Oceanside, and Carlsbad in this week's Coastal Currents. Link in profile.

No hashtags on LinkedIn for this format. Keep it clean.

---

### LI-2. What I'm Watching (text-only, off weeks)
**No image.** Text post, 100–150 words.

**Template:**
> What I'm watching on the coast this week:
>
> [One specific thing, named precisely. A neighborhood seeing price reductions. An STR ordinance change. An ARM-vintage cohort approaching reset. A listing pattern. Always concrete, never "the market is shifting."]
>
> [Two sentences of read on why it matters.]
>
> [One sentence inviting reply or pointing to the newsletter for the deeper version.]
>
> Coastal Currents goes out every other week. Link in profile.

---

### LI-3. Subscribe Reminder (1st of month)
Existing graphic: `coastal_currents_subscribe_linkedin.jpg`.

**Caption:**
> A quiet read on the South OC coast market. No noise, no lead-magnet gimmicks. Goes out every other week.
>
> Subscribe at the link in my profile.

---

## Instagram — three formats

### IG-1. Coast Moment (weekly)
**Image:** Single photo or 2–3 image carousel. Coastal photography, no overlays, no B&W, no filters (per brand rules). Pier, bluff, neighborhood at golden hour, a property exterior (no on-photo text), a quiet detail.

**Caption template (3–5 short lines):**
> [One observational line about the moment or the place. Specific street, time of day, what was happening.]
>
> [One line connecting it to the market or to living here. Optional.]
>
> Coastal Currents in profile.
>
> [3–5 hashtags, geographic only: #SanClemente #DanaPoint #SouthOC #CoastalLiving #PacificSothebysRealty]

### IG-2. Market Stat Card (biweekly, mirrors LI-1)
**Image:** 1080x1350 portrait. Same single-number layout as LI-1 reformatted vertical.

**Caption (shorter than LinkedIn):**
> [Headline number in plain English.]
>
> [One line of read.]
>
> Full cycle breakdown in this week's Coastal Currents. Link in profile.
>
> #SanClemente #DanaPoint #LagunaBeach #NewportBeach #Oceanside #Carlsbad

### IG-3. Subscribe Reminder (1st of month)
Existing graphic: `coastal_currents_subscribe_instagram.jpg`.

Caption: same as LI-3.

---

## Hashtag conventions

- LinkedIn: usually none. Adds noise to a professional feed.
- Instagram: 5 max per post. Geographic + brand only. No lifestyle clutter (`#blessed`, `#realestategoals`, etc.).
- Approved set: `#SanClemente #DanaPoint #LagunaBeach #NewportBeach #Oceanside #Carlsbad #SouthOC #CoastalLiving #PacificSothebysRealty`

---

## Asset pipeline

All graphics generated programmatically from the existing template engine, not designed by hand each week. That is the whole point of the brand-compliant Python script.

**Existing:**
- `build_subscribe_post.py` — produces the monthly subscribe reminder (IG + LinkedIn). Already brand-correct.

**To build (next steps, in order):**
1. `build_stat_card.py` — single-number market-stat card. Inputs: headline number (string), supporting line (string), output filename. Outputs both 1080x1350 (IG) and 1200x1200 (LinkedIn). Reuses header, gold divider, realtor lockup from the existing script. Pulls cycle dates from the latest `Newsletter/market_data/briefs/` JSON if available.
2. Posting checklist file — short markdown that walks through "what to publish this week" given which week of the cycle it is.

Photos for IG-1 come from Adam's own roll. No stock. No filters.

---

## What we are NOT doing

- Reels or video. Voice/face on camera is a future bet, not week-1 scope.
- TikTok, Threads, Facebook, YouTube. Not active per memory `reference_adam_social.md`.
- Daily posting. Cadence above is the ceiling, not the floor. Skipping a week is fine.
- Lead-magnet gating ("download my free guide to..."). Newsletter itself is the magnet.
- Any post without a reason to exist. If a week has no real read on the market and no good photo, skip it.

---

## Open items

- Confirm: does Adam want Christian co-posting from the same handles, or does Christian have his own?
- Confirm: monthly subscribe reminder cadence — once/month feels right; revisit after 60 days based on subscribe-link clicks.
- Decide: do we cross-post the LI-1 market-read text to IG as a static text card, or only the stat card with shorter caption? Current plan is the latter.
