# Instagram Agent — @adamonthecoastoc

The operating doc for the two Instagram skills. `/ig-growth` runs unattended every
day. `/ig-content` drafts posts that wait for Adam's approval before anything
publishes.

**The split, and why:** follower growth is mechanical, reversible, and low-stakes
if a single action is wrong, so it runs on its own. A published post carries
Adam's license number and a public claim about somebody else's listing, and it
cannot be un-seen. So every post stops at an approval gate. Nothing reaches the
feed that Adam has not read.

---

## The strategy in one paragraph

Reach on Instagram is bought with saves and shares, not likes. A post that a
local homeowner sends to their spouse is worth more than fifty passive likes, so
every recurring format is built to be forwarded: a number someone wants to check
against their own house, a deal someone wants a second opinion on. Follower
growth comes from showing up inside the local graph (commenting where the target
audience already is) rather than from broadcasting. Deal of the Week is the
flagship because it is the rare real estate post with a reason to exist: it
answers "is anything actually a good buy right now," which is the question every
lurking buyer in San Clemente has and no agent's feed answers.

---

## Content pillars and cadence

Four posts a week. That is the ceiling and the floor. A week with nothing real to
say gets three posts, not four filled with noise.

| Day | Pillar | Format | Engine |
|-----|--------|--------|--------|
| Wed | **Deal of the Week** | 3-frame carousel | `ig_deal_of_week.py` → `ig_render_deal_card.py` |
| Sat | **Market read** | Single stat card | `website/data/stats.json`, newest `Newsletter/market_data/briefs/` |
| Sun | **Coast moment** | Photo or 2–3 photo carousel | Adam's camera roll, no stock |
| Mon | **The question** | Text-forward carousel | One real buyer/seller question, answered plainly |

Stories run alongside on weekdays via the existing `/story-pull` skill. Stories
are where listings go; the feed is where authority goes.

### Deal of the Week — the rules that keep it honest

The claim is always **"priced N% under what comparable homes have been closing
at, per square foot."** Never "underpriced," never "a steal," never "below
market value." The first is a measurement. The others are opinions Adam would
have to defend to a listing agent.

- Only publish a pick with a **high-confidence cohort** (same area, same property
  class, within 30% on size, 5+ closed comps). Medium and low confidence picks
  are for Adam's eyes, not the feed.
- Every pick carries `review_flags`. Adam reads them before approving. A 30%
  discount on a 1964 build with no view is not a deal, it is a fixer, and posting
  it as the best value in town costs credibility that took months to build.
- **Listing brokerage attribution is mandatory** on the final frame. Advertising
  another broker's listing without attribution is an MLS rules problem, not a
  style preference. The renderer refuses to run without `--listing-office`.
- No MLS photography. Data-only frames sidestep the photo-permission question
  entirely and read more like Sotheby's than a Canva flyer does.
- Frame 3 always carries the caveat: price per square foot does not price a
  view, a lot, or condition. Saying the limitation out loud is what separates
  this from every "HOT DEAL 🔥" post in the market.

---

## Growth loop (automated, runs daily)

Three mechanics, each with a hard cap. Caps are ceilings, not targets, and any
Instagram action-block stops the whole run immediately.

| Action | Daily cap | Notes |
|--------|-----------|-------|
| Follow | 15 | Vetted local accounts, spaced 60–180s |
| Unfollow | 15 | Only accounts that did not follow back after 10+ days |
| Comment | 10 | Substantive, on-topic, never emoji-only |
| Story reply | 5 | Highest-signal, lands directly in DM |

**Targeting categories** (unchanged from the 2026-06 loop): `business_venue`
(their followers are local residents and homeowners), `creator_influencer`,
`agent_allied` (referral network). Community/civic accounts stay excluded.

**Fair housing.** Targeting is geographic and interest-based only. Never filter,
rank, or skew the target list by race, religion, familial status, color,
disability, national origin, or sex, and never let a proxy for one of those in
through the side door. This applies to who we follow, who we comment on, and who
sees a post.

**Account safety beats hitting a number.** If Instagram shows "Try again later,"
"We restrict certain activity," or any checkpoint, the run stops, writes the
status file, and waits for a human. A restricted account is worth less than a
week of missed follows.

### Why unfollow hygiene matters
An account following 2,000 with 400 followers reads as a bot to both the
algorithm and to any homeowner who checks. The hygiene pass keeps the ratio
defensible, which matters more for a luxury brand than raw follower count.

---

## Lead capture

Every inbound DM and story reply gets classified (`buyer` / `seller` /
`valuation` / `agent` / `vendor` / `spam` / `social`), scored, and written to
`instagram_dms`. Anything above `cold` also gets a `contacts` row and an
`interactions` row so Instagram leads land in the same CRM as everything else.

Replies are **drafted, never auto-sent.** A DM is a one-to-one conversation with
a real person and it goes out in Adam's voice or not at all.

Newsletter CTAs point to `https://adamboehrer.com` (full https so it auto-links).

---

## Voice

Adam's marketing voice applies without exception: short beats, one-line
paragraphs, blunt payoffs, wry specifics. Never corporate. Never disparage the
market he sells in.

Hard rules, checked before anything is written to the queue:
- **No em-dashes or en-dashes.** Commas, periods, or a line break.
- **No client-speak.** The reader IS the buyer or seller. Never "your clients."
- **No overpromising.** Never "I have buyers lined up." He cannot deliver it.
- **No "no pressure / no obligation" disclaimers.**
- **Never name Adam's street.** "San Clemente" is the right specificity.
- **No fabricated local claims.** WebSearch to verify any named opening, build,
  permit, or sale before it goes in a caption.
- **Hashtags: 5 max**, geographic and brand only, from the approved set in
  `Marketing/social_posts/SOCIAL_PLAN.md`.

---

## Compliance on every published post

Instagram posts about the business are advertising. All six non-negotiables in
`CLAUDE.md` apply. The renderer bakes the disclosure into the image, but the
check is per-post, not per-template:

1. Adam Boehrer
2. DRE #02419464, all eight digits, no smaller than any other type in the piece
3. "Real Estate Agent"
4. Pacific Sotheby's International Realty, equally prominent
5. AB 723 disclosure on any AI-generated or AI-retouched image
6. Fair housing: describe the property, never the people

Plus, for Deal of the Week: listing brokerage attribution.

`instagram_posts.compliance_ok` only flips to 1 after this list is walked. The
publisher refuses to send a post where it is 0.

---

## Files

```
outreach/instagram/
├── INSTAGRAM_PLAN.md          # this file
├── QUEUE.md                   # the approval gate, newest week on top
├── assets/<slug>/             # rendered frames per post
├── status/YYYY-MM-DD.md       # daily growth-loop log
├── dms/                       # DM triage notes
└── posted/                    # archived queue entries

scripts/
├── ig_deal_of_week.py         # rank actives by $/sqft vs closed comps
├── ig_render_deal_card.py     # 3-frame carousel renderer
├── ig_publish.py              # approved queue -> Instagram Graph API
├── ig_growth_run.sh           # launchd entry point
└── migrate_instagram_agent.py # schema
```

Database: `database/leads.db`, tables `instagram_*`.

---

## Weekly data refresh

Deal of the Week needs current CRMLS data. Export two Agent 1-Line CSVs into
`data/imports/mls_comps/` and the engine picks up whatever is freshest:

1. **Actives** — San Clemente, Residential, status Active
2. **Closed** — San Clemente, Residential, closed in the last 9 months

The 1-Line export does **not** include the listing office, which the attribution
requires. Adam supplies it per pick, or the skill pulls it from the listing
detail. Adding List Office to the saved 1-Line view would remove that step.

---

## Open items

- Meta Graph API credentials for auto-publish after approval. See
  `outreach/instagram/GRAPH_API_SETUP.md`. Until that is done, `/ig-content`
  writes the queue and Adam posts approved items from his phone.
- Collaborator posts with local businesses are the single biggest untapped reach
  lever (the post lands on both accounts' feeds). Needs a human relationship
  first, so it stays a manual play for now.
- Reels. Highest reach format on the platform by a wide margin and currently out
  of scope. Revisit once the feed cadence has held for 60 days.
