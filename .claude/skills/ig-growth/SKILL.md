---
name: ig-growth
description: Daily unattended Instagram growth routine for @adamonthecoastoc. Follows vetted local accounts, runs unfollow hygiene, leaves substantive comments inside the local graph, replies to stories, and triages inbound DMs into leads.db. Invoked as /ig-growth or by the launchd job scripts/ig_growth_run.sh. Never posts to the feed and never sends a DM reply without approval.
---

# ig-growth — the daily Instagram growth loop

Runs unattended. Grows the follower base and captures inbound leads. It does
**not** publish feed content (that is `/ig-content`, which requires Adam's
approval) and it does **not** send DM replies (it drafts them).

Repo root: `~/Desktop/Claude Code/`. All paths relative to it.

Read `outreach/instagram/INSTAGRAM_PLAN.md` first. Caps, targeting categories,
fair-housing rules, and voice all live there and this skill does not override them.

## Caps (hard)

| Action | Cap/day |
|--------|---------|
| follow | 15 |
| unfollow | 15 |
| comment | 10 |
| story reply | 5 |

Space actions 60–180 seconds apart, randomized. Never burst. These are ceilings.
Finishing a run under cap is a fine outcome; getting the account restricted is not.

## Step 0 — Browser and session

Playwright MCP. The profile lock issue in memory `project_playwright_profile_lock`
bites at the start of these runs: if you see "Browser already in use", kill the
orphaned Chrome and remove the `SingletonLock` before retrying.

Navigate to `https://www.instagram.com/`. Confirm logged in as
**@adamonthecoastoc**. If Instagram shows a login screen or checkpoint, stop
immediately, write the status file noting "session expired, Adam must log in by
hand," and exit 0. Never attempt to log in, and never touch 2FA.

## Step 1 — Read today's budget

```sql
SELECT action, count FROM instagram_daily_actions WHERE run_date = date('now');
```

Subtract from the caps. A re-run on the same day continues where the last one
stopped rather than starting the counters over. Increment the counter after each
successful action, not in a batch at the end, so a crash mid-run cannot lose
count and double-spend the budget.

## Step 2 — Follow pass

Work one city at a time, in order: San Clemente → Dana Point → Laguna Beach →
Oceanside → Carlsbad. Finish a city's vetted list before opening the next.

1. Pull the queue:
   ```sql
   SELECT id, handle, display_name, category, followers, relevance_note
   FROM instagram_targets
   WHERE follow_status = 'approved' AND do_not_engage = 0
   ORDER BY city, followers DESC;
   ```
2. If fewer than 10 approved targets remain, run **discovery** (step 2b) and
   stop for the day. Newly discovered accounts are written as `identified`, and
   Adam approves them. Never follow an unvetted account.
3. For each target, navigate to the profile and find the first header button
   matching `/^(Follow|Following|Requested)$/`. Click only if it reads `Follow`.
   Wait ~2.5s and verify it flipped to `Following` or `Requested`. Ignore the
   "Suggested for you" carousel that appears after a follow.
4. Scan for block phrases: "Try again later", "We restrict certain activity",
   "Action Blocked". On any hit, **stop the entire run**, write the status file,
   and exit. Do not retry.
5. On success: `follow_status='followed'`, `followed_at=datetime('now')`, and
   bump the daily counter.

### Step 2b — Discovery (when the approved queue runs dry)

Find accounts whose *followers* are local homeowners. Sources, in order of yield:
- Followers and following lists of already-followed local business accounts
- Location tags for the city (pier, downtown, known landmarks)
- Geographic hashtags from the approved set
- Accounts that engaged with a local business's recent posts

For each candidate, capture handle, display name, follower count, bio snippet,
and a one-line `relevance_note` explaining why their audience matters to Adam.
Follower counts can be read via same-origin `fetch('https://instagram.com/<handle>/')`
and parsing `og:description`, but that returns blank for some large verified
accounts, so visit those profiles directly rather than recording a wrong number.

Skip: national brands, accounts with no local tie, other agents' personal brands
competing in the same market (log as `do_not_engage=1`), private accounts with
under ~200 followers, and anything with no posts in 6 months.

Write them as `follow_status='identified'` and surface the list for approval in
the status file.

## Step 3 — Unfollow hygiene

Keeps the following/follower ratio defensible.

```sql
SELECT id, handle, followed_at FROM instagram_targets
WHERE follow_status = 'followed'
  AND unfollowed_at IS NULL
  AND julianday('now') - julianday(followed_at) >= 10
ORDER BY followed_at;
```

For each, check whether they follow back (the profile shows "Follows you"). Record
`follows_back` and `followback_checked_at` either way.

- Follows back → keep. They are now audience.
- Does not follow back after 10 days → unfollow, set `unfollowed_at`.
- **Never unfollow** anyone with `category='agent_allied'` or a non-zero
  `engagement_count`. Referral relationships and accounts we have actually talked
  to are worth more than a ratio.

Same block-phrase check as the follow pass.

## Step 4 — Engagement pass

The highest-leverage part of this whole routine. A thoughtful comment on a local
business's post puts @adamonthecoastoc in front of an audience of exactly the
right people, in a context where he looks like a neighbor rather than an ad.

1. Pick up to 10 accounts from `instagram_targets` where `follow_status='followed'`
   and `do_not_engage=0`, preferring `business_venue` and `creator_influencer`,
   and ordering by `last_engaged_at IS NULL DESC, last_engaged_at ASC` so the
   rotation spreads rather than hammering the same five accounts.
2. Open their most recent post. Read it. Comment only if there is something real
   to say.
3. **What a comment must be:** specific to the actual post, in Adam's voice,
   one or two sentences, and useful or warm on its own. A comment that would
   read as generic under any post is worse than no comment.
   - Never: "Great post!", emoji-only, "🔥🔥", "DM me", anything selling.
   - Never mention real estate unless the post is about real estate.
   - Never pitch. The comment is the introduction, not the offer.
4. Check `instagram_engagement` for the `post_url` first. Never comment twice on
   the same post, and never comment on the same account two days running.
5. Log every comment to `instagram_engagement` with the body, and bump
   `engagement_count` and `last_engaged_at` on the target row.

Story replies (cap 5) follow the same standard and land in DMs, so treat them as
the start of a conversation, not a broadcast.

## Step 5 — DM and story-reply triage

1. Open the inbox. Read unread threads and story replies.
2. For each, classify `intent`: `buyer` / `seller` / `valuation` / `agent` /
   `vendor` / `spam` / `social`. Score `lead_quality`: `hot` (a specific property,
   a timeline, or a direct ask) / `warm` (real interest, no specifics) / `cold` /
   `none`.
3. Draft a reply in Adam's voice. Short. No "no pressure" disclaimers, no
   "Adam Boehrer here" opener, no client-speak, no em-dashes. If they asked a
   question, answer it. Newsletter CTAs use the full `https://adamboehrer.com`.
4. Write to `instagram_dms` with `reply_status='pending'`. **Do not send.**
5. For `hot` and `warm`, also upsert a `contacts` row (source `instagram`) and an
   `interactions` row so the lead lands in the CRM alongside every other channel.
6. Spam and vendor pitches: log and ignore. No reply.

If a thread contains anything time-sensitive (a showing request, a listing
question with a deadline), flag it at the very top of the status file.

## Step 6 — Status file

Write `outreach/instagram/status/YYYY-MM-DD.md`:

- Actions taken against each cap (`follows 12/15`, `comments 8/10`, ...)
- Any block or checkpoint hit, verbatim
- New accounts discovered awaiting approval, as a table Adam can skim
- **DMs needing a reply**, with the drafted text inline, hottest first
- Follow-back rate on the accounts checked today
- Anything that needs a human

Lead with what needs Adam's attention. He should be able to read the first five
lines and know whether to open the file.

## Notes

- Never post to the feed or stories from this skill.
- Never send a DM.
- Never follow an account that is not `approved` in the table.
- If anything is ambiguous, log it and skip it. An unattended run should be
  boring. The interesting decisions belong to Adam.
