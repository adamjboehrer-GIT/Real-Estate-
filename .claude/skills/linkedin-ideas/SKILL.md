---
name: linkedin-ideas
description: Generate 3 finished, copy-paste-ready LinkedIn posts for the day into the daily ideas backlog. Invoke when Adam says "/linkedin-ideas," "give me today's LinkedIn posts," "3 LinkedIn ideas," "fill the LinkedIn backlog," or similar. Produces three complete drafts across distinct pillars, following the voice rules, and logs them. Never auto-posts.
---

# linkedin-ideas

Generate **3 finished, copy-paste-ready LinkedIn posts for today**, each from a different
pillar, into the daily backlog (`IDEAS.md`). Review-and-post model: Claude writes finished
drafts, Adam reads, picks the ones he likes, edits, and posts himself. Nothing auto-posts.

This is the daily idea engine. It is separate from the `linkedin-posts` skill (the curated
2x/week `QUEUE.md`). Think of `IDEAS.md` as the deep bench: Adam pulls the strongest drafts
from here whenever he wants to post, and the weekly queue stays the polished short list.

Repo root: `~/Desktop/Claude Code/`. All paths below are relative to it.

## Procedure

1. **Read the system docs** so voice and pillars are fresh:
   - `Marketing/social_posts/linkedin/PILLARS.md` (the four pillars, voice rules, lengths)
   - `Marketing/social_posts/SOCIAL_PLAN.md` (broader cadence + brand context)

2. **Read today's existing backlog.** Open the top of
   `Marketing/social_posts/linkedin/IDEAS.md` and the last day or two of entries. Do not
   repeat an angle, hook, neighborhood, or story already used recently. Variety is the point.

3. **Pick today's 3 pillars (all distinct).** Default daily trio is **P2 Neighborhood +
   P3 Personal + P4 Education** — these can run any day on real material. Use **P1 Market
   data** in place of one of them ONLY when there is genuinely fresh data to lead with
   (a new InfoSparks pull or deck since the last P1 post). Never force a market number on a
   day with no new read. Rotate which neighborhood (P2) and which angle (P3/P4) so the bench
   stays varied across the week.

4. **Pull fresh material per pillar:**
   - **Market data (P1):** read `website/data/stats.json` and the newest file in
     `Newsletter/market_data/briefs/`. Lead with ONE real number. Never invent figures.
   - **Neighborhood (P2):** pick a South OC pocket not used in the recent backlog.
     WebSearch to verify any named opening, build, permit, or sale before writing it.
   - **Personal (P3):** draw on memory `user_adam_background` (father/neighbor first,
     out-of-state investor + brand strategist before real estate). Specific, grounded.
   - **Education (P4):** one concrete, practical seller/buyer tip. Reader IS the
     seller/buyer. Pairs with the South OC Sellers Playbook lead magnet.

5. **Write all 3 posts** to the length targets and voice rules in PILLARS.md. Hard checks
   before writing anything:
   - No em-dashes or en-dashes. Commas, periods, or short splits.
   - No client-speak. The reader IS the buyer/seller, never "your clients/your buyers."
   - No overpromising. Never "I have buyers lined up."
   - No "no pressure / no obligation" disclaimers.
   - No street naming. "San Clemente" or a neighborhood name is the right specificity.
   - No fabricated local claims. Web-verify any specific before writing it.
   - First line earns the click-to-expand on its own (LinkedIn truncates ~210 chars).
   - No hashtags.
   Each post must be a complete, copy-paste-ready body. Hit the per-pillar word target.

6. **Write the backlog.** Add a new dated section to the TOP of
   `Marketing/social_posts/linkedin/IDEAS.md`. Format per day:
   ```
   ## Friday, June 5, 2026

   ### Idea 1 — Pillar: Neighborhood · STATUS: DRAFT
   > full post body as a blockquote

   ### Idea 2 — Pillar: Personal · STATUS: DRAFT
   > full post body as a blockquote

   ### Idea 3 — Pillar: Education · STATUS: DRAFT
   > full post body as a blockquote
   ```
   Keep prior days below for reference. When Adam posts one, he marks it `POSTED` (or moves
   it to `posted/`).

7. **Log.** Append 3 rows to `Marketing/social_posts/linkedin/linkedin_log.csv`:
   `date,day,iso_week,pillar,headline,status(draft),engagement_notes(blank)`.
   (Get iso_week from `python3 -c "import datetime;print(datetime.date.today().isocalendar()[1])"`.)

8. **Report back** to Adam: show all 3 posts inline, name the pillar of each, and ask which
   he wants to run. Remind him to mark rows `posted` after publishing (or offer to do it).

## Notes
- Quality over filling the slot. If one pillar has no genuine material today, write 2 strong
  posts rather than 3 with one padded. Say so.
- When Adam dictates his own copy, treat it as a draft to polish, then confirm back.
- After Adam reports engagement on a posted idea, record it in `engagement_notes` so the
  rotation can lean into what works.
- The strongest drafts here can be promoted into the weekly `QUEUE.md` instead of reinventing
  them.
