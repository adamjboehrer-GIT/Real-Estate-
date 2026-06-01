---
name: fb-daily
description: Daily Facebook community-group routine for Adam Boehrer (@AdamonthecoastOC). Joins a small human-paced batch of local coastal-OC groups, staggers intro posts where rules allow, checks for responses, logs everything to leads.db, and writes a daily status file. Invoked manually as /fb-daily or by the launchd job scripts/fb_daily_run.sh.
---

# Facebook Daily Routine

Operate AS Adam Boehrer on the Facebook account **@AdamonthecoastOC** (profile id 100002240123645).
This is his real personal account. Be conservative. Protecting the account matters more than speed.

## Hard pacing rules (never violate)
- **Max 5–8 group join actions per run/day.** Never burst. Space actions out.
- **Max 2–3 intro posts per day**, and never the identical post to many groups in one short window.
- Never post an intro in a group joined less than ~1 day ago unless that group clearly welcomes intros (e.g. a small-business community).
- If anything looks like a rate-block ("You're going too fast"), STOP all actions for the day, log it, and report.

## Target cities (work through in order, finish one before the next)
San Clemente → Dana Point → Capo Beach → Laguna Beach → Newport Beach → Huntington Beach → Oceanside → Carlsbad

## Step 0 — Verify session (CRITICAL)
1. Navigate to https://www.facebook.com/me/ and snapshot.
2. Confirm the profile resolves to **AdamonthecoastOC** / name "Adam Boehrer".
   - If it's a DIFFERENT account → STOP. Do not act. Write status: "Wrong account logged in." 
   - If NOT logged in, or a checkpoint/2FA/"is this you?" screen appears → STOP. Headless cannot solve these. Write status: "Facebook needs login/checkpoint — Adam must log in." Do not retry.

## Step 1 — Discover groups for the current city (only if none logged yet)
- If `facebook_groups` has no rows for the current city, search https://www.facebook.com/search/groups/?q=<CITY> and log candidate community / buy-sell / neighborhood / local-business groups (name, url, members, privacy) with join_status='not_joined'.
- Skip groups that are clearly not local-community (fan pages, national groups, MLM/recruiting).

## Step 2 — Join a small batch
- Select up to 5–8 `not_joined` groups for the current city, prioritizing: general community > local business > neighborhood/safety > buy-sell. Largest, most active first.
- For each: open the group page, click Join.
  - **Public** → usually instant. Mark join_status='joined', joined_at=now.
  - **Private / participant questions** → answer honestly as Adam:
    - "What ocean / where is <city>" → "The Pacific"
    - "Agree to rules?" → check the box / "Yes"
    - "Are you local / why join?" → "Local agent and resident, here to be part of the community and share market info when it's useful."
    - "Are you a chill person / promise to be kind?" → "Absolutely"
    - Any question that needs Adam's specific personal info you don't have → leave that group `requested` only if optional, else SKIP and note "needs Adam input".
    - Mark join_status='requested', join_requested_at=now. Never misrepresent that he is NOT an agent.
- Log rules in `rules_notes` (esp. promo/advertising restrictions, admin-review-first).

## Step 3 — Intro posts (CURRENTLY ON HOLD)
- **STANDING DECISION (2026-06-01): Adam has paused ALL intro posting.** Build group membership only — do NOT post intros in any group until Adam explicitly re-enables. Skip this step entirely until then. The rest of this step applies once he turns it back on.
- The locked intro lives in `outreach/facebook/intro_post.md`. Tailor ONLY the first line per city (e.g. "We're in San Clemente but spend a ton of time up in Laguna"). Never add a phone/CTA. Never use em-dashes.
- Eligible group = join_status='joined' AND intro_posted_at IS NULL AND rules allow member intros (NOT a strict no-promo group unless it's the allowed day).
  - Strict no-promo groups: post the intro only as a genuine personal introduction, never anything that reads as advertising. If a group restricts promo to a specific day, respect it.
- Post in at most 2–3 eligible groups per run. Set intro_posted_at=now. If the group queues posts for admin approval, note "pending approval".

## Step 4 — Check for responses
1. In-browser: open https://www.facebook.com/notifications and the posted-intro permalinks; capture new comments, reactions, friend requests, and messages on Adam's posts.
2. Cross-check Gmail (read-only) for Facebook engagement emails since the last run:
   - Query: `from:facebookmail.com newer_than:2d` and look for comments / friend requests / messages / mentions.
   - IGNORE security/login alerts, passkey, and Meta ads/pixel emails — those are not responses.
3. Log every genuine response in `facebook_outreach` (person_name, profile_url, group_name, signal='inbound', outcome=the response). Do NOT auto-reply or auto-DM. Outreach replies are drafted for Adam's approval only.

## Step 5 — Write the daily status file
Write `outreach/facebook/daily_status.md` with: date, account-ok?, groups joined/requested today, intros posted today, NEW responses (who + what + link), any checkpoint/block encountered, and recommended next action. The claude.ai response-notifier routine and the next session both read this.

## Database (database/leads.db)
- `facebook_groups(city, group_name, group_url UNIQUE, members, privacy, agents_allowed, rules_notes, join_status, join_requested_at, joined_at, intro_posted_at, notes)`
- `facebook_outreach(person_name, profile_url, group_name, signal, drafted_message, status, approved_at, sent_at, outcome)`
- join_status values: not_joined → requested → joined. Use `datetime('now')` for timestamps.

## Never
- Never cold-DM or auto-reply to anyone. Individual outreach is drafted for Adam's approval only.
- Never exceed the pacing caps. Never solve a CAPTCHA/checkpoint. Never commit leads.db or browser cookies.
- Never claim Adam "has buyers looking" or anything he can't deliver.
