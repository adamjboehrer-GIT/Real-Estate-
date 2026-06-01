---
name: linkedin-posts
description: Generate Adam's twice-weekly South OC LinkedIn posts into the review queue. Invoke when Adam says "generate this week's LinkedIn posts," "write my LinkedIn posts," "refresh the LinkedIn queue," or similar. Produces two finished, copy-paste-ready posts following the pillar rotation and voice rules, and logs them.
---

# linkedin-posts

Generate Adam's 2x/week LinkedIn posts (Tue + Thu) into the review queue. Review-and-post
model: Claude writes finished drafts, Adam reads, edits, and posts himself. Never auto-post.

Repo root: `~/Desktop/Claude Code/`. All paths below are relative to it.

## Procedure

1. **Read the system docs** so voice and rotation are fresh:
   - `Marketing/social_posts/linkedin/PILLARS.md` (pillars, rotation, voice rules, lengths)
   - `Marketing/social_posts/SOCIAL_PLAN.md` (broader cadence + brand context)

2. **Determine the week.** Run:
   ```
   python3 -c "import datetime; d=datetime.date.today(); iso=d.isocalendar(); print(iso[1], ((iso[1]-1)%4)+1)"
   ```
   First number is the ISO week, second is the rotation slot (1–4). Look up the slot in the
   PILLARS rotation table to get the two pillars (Tue + Thu). Confirm the actual Tue/Thu dates
   of the current week. If today is already past Thursday, generate for next week.

3. **Pull fresh material per pillar:**
   - **Market data (P1):** read `website/data/stats.json` and the newest file in
     `Newsletter/market_data/briefs/`. Lead with ONE real number. Never invent figures.
   - **Neighborhood (P2):** pick the next pocket in the SOCIAL_PLAN featured-area rotation.
     WebSearch to verify any named opening, build, permit, or sale before writing it.
   - **Personal (P3):** draw on memory `user_adam_background` (father/neighbor first,
     out-of-state investor + brand strategist before real estate). Specific, grounded.
   - **Seller/buyer education (P4):** one concrete, practical tip. Pairs with the South OC
     Sellers Playbook lead magnet. Reader IS the seller/buyer.

4. **Write both posts** to the voice rules in PILLARS.md. Hard checks before writing anything:
   no em/en-dashes; no client-speak; no overpromising ("buyers lined up"); no
   "no pressure/no obligation" disclaimers; no street naming; no fabricated local claims;
   first line earns the click-to-expand on its own; no hashtags. Hit the per-pillar word target.

5. **Write the queue.** Add a new dated section to the TOP of
   `Marketing/social_posts/linkedin/QUEUE.md` (keep prior weeks below for reference, or move
   posted ones to `posted/`). Each post: heading with date, day, pillar, `STATUS: DRAFT`, then
   the post body as a blockquote.

6. **Log.** Append two rows to `Marketing/social_posts/linkedin/linkedin_log.csv`:
   `date,day,iso_week,pillar,headline,status(draft),engagement_notes(blank)`.

7. **Report back** to Adam: show both posts inline, name the two pillars and dates, and ask
   for edits. Remind him to mark rows `posted` after publishing (or offer to do it).

## Notes
- Skipping a week is fine; resume the cycle where it left off.
- A week with no genuine market read and no real observation is better skipped than filled.
- When Adam dictates his own copy, treat it as a draft to polish, then confirm back.
- After Adam reports engagement on past posts, record it in the `engagement_notes` column so
  the rotation can lean into what works.
