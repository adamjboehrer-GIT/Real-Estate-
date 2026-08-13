---
name: ig-content
description: Build Adam's week of Instagram posts into the approval queue, including the flagship Deal of the Week carousel. Invoke when Adam says "/ig-content", "build this week's Instagram", "run deal of the week", "refresh the IG queue". Produces finished graphics plus captions and stops at the approval gate. Never publishes without Adam approving each post.
---

# ig-content — a week of Instagram posts, drafted and gated

Generates finished, publish-ready posts into `outreach/instagram/QUEUE.md` and
`instagram_posts`. Everything stops at `status='draft'` until Adam approves.

Repo root: `~/Desktop/Claude Code/`. Read
`outreach/instagram/INSTAGRAM_PLAN.md` first for pillars, voice, and compliance.

## Invocation

- `/ig-content` — build the full week (4 posts)
- `/ig-content deal` — just the Deal of the Week
- `/ig-content approve <slug>` — mark a draft approved and publish it
- `/ig-content status` — what is in the queue and what published

## Procedure — full week

### 1. Check the data is fresh

Deal of the Week needs current CRMLS exports in `data/imports/mls_comps/`.

```bash
ls -lt data/imports/mls_comps/*.csv | head
```

If the newest actives export is more than 8 days old, **stop and ask Adam for a
fresh Agent 1-Line export** (Actives + Closed, San Clemente, Residential). Do not
publish a deal claim off stale inventory. A listing that went pending four days
ago and gets posted as this week's best value is the single most damaging
mistake this system can make.

### 2. Deal of the Week (Wednesday)

```bash
python3 scripts/ig_deal_of_week.py --city SC --top 5 \
  --json outreach/instagram/deal_of_week_latest.json
```

Read the ranked output. Then:

1. **Filter to high-confidence cohorts only.** Medium and low are Adam's
   reference, not the feed.
2. **Read the `review_flags` on the top pick.** Flags are not automatic
   disqualifiers, they are the questions Adam has to answer. A 28% discount on a
   1964 build usually means condition, not opportunity.
3. **Verify the listing is still active** and pull the **listing brokerage**. The
   1-Line export does not carry List Office, so check the listing in CRMLS or on
   the listing detail. Attribution is mandatory and the renderer refuses without it.
4. Render:
   ```bash
   python3 scripts/ig_render_deal_card.py \
     --deal outreach/instagram/deal_of_week_latest.json \
     --pick 0 --listing-office "<brokerage>" \
     --out-dir outreach/instagram/assets/<YYYY-MM-DD>-deal-of-the-week
   ```
5. Write the caption. The claim is always "priced N% under what comparable homes
   have been closing at, per square foot." Never "underpriced," "steal," or
   "below market value."

Caption shape (short beats, one line each):

> The best value in San Clemente this week is not the cheapest house on the market.
>
> [Address-free description: what it is, beds/baths/size, the neighborhood.]
>
> Asking $X. Comparable homes in the neighborhood have been closing at $Y a foot.
> This one is asking $Z.
>
> That gap is not free money. Price per foot does not price a view or a
> renovation. But it tells you where to look.
>
> Want to see it? I can represent you on this one.
>
> Listed by [brokerage].
>
> [3–5 geographic hashtags]

If no pick clears the bar this week, **say so in the caption and post the read
anyway**: "Nothing in San Clemente is trading below its neighborhood this week,
and that is itself the story." An honest empty week builds more trust than a
manufactured deal.

### 3. Market read (Saturday)

One number. Pull from `website/data/stats.json` and the newest file in
`Newsletter/market_data/briefs/`. Never invent a figure. Use Expected Market Time,
not days on market, as the pace metric.

Render with `Marketing/social_posts/build_stat_card.py` (1080x1350).

### 4. Coast moment (Sunday)

Needs a real photo from Adam's roll. No stock, no filters, no B&W, no text over
the photo. If Adam has not supplied one, **ask** rather than substituting. Caption
is 3–5 short lines: an observation about the place, optionally one line
connecting it to the market.

### 5. The question (Monday)

One real question a buyer or seller actually asked, answered plainly. Sources:
`instagram_dms`, the newsletter Submissions sheet, recent client emails. The
reader IS the buyer or seller. Never "your clients."

### 6. Compliance walk

For each post, verify against the six non-negotiables in `INSTAGRAM_PLAN.md`:
name, DRE #02419464 at conspicuous size, "Real Estate Agent," Pacific Sotheby's
equally prominent, AB 723 disclosure on any AI-generated image, fair-housing-safe
copy. Deal of the Week also needs listing brokerage attribution.

Only then set `compliance_ok = 1`.

### 7. Write the queue

Insert each post into `instagram_posts` with `status='draft'`, and add a dated
section at the **top** of `outreach/instagram/QUEUE.md` containing, per post: the
slug, planned date, pillar, the caption verbatim in a blockquote, the asset
paths, the source note, and (for the deal) the review flags Adam needs to weigh.

### 8. Report

Show Adam every caption inline in the response, with the rendered frames. Name
the review flags on the deal pick explicitly. Ask which to approve.

Do not bury a flag. If the top pick is a 1964 fixer with no view, say that in
the first sentence of the report, not in a footnote.

## Approving and publishing

When Adam approves a post:

```bash
python3 scripts/ig_publish.py --slug <slug>
```

The publisher refuses any post where `compliance_ok = 0` or `status != 'approved'`.

If Graph API credentials are not configured, it prints the caption and asset
paths for manual posting and marks the post `approved` but not `posted`. Adam
posts from his phone, then `/ig-content` marks it posted on the next run. See
`outreach/instagram/GRAPH_API_SETUP.md`.

## Notes

- Never publish without an explicit approval from Adam for that specific post.
- A skipped week beats a filled one. Three good posts beat four with one dud.
- After Adam reports how a post performed, record it in `instagram_post_metrics`
  so the rotation can lean toward what works.
- When Adam dictates his own caption, treat it as a draft to polish for grammar,
  flow, and repetition, then confirm the refined version back before saving it.
