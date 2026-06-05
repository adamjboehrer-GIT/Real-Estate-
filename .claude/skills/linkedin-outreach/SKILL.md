---
name: linkedin-outreach
description: Run Adam's LinkedIn prospecting workflow — find community-invested high earners in coastal South OC / North SD, draft personalized connection notes and post-accept messages, send at human pace with Adam's approval, triage inbound DMs, and log every touch to leads.db. Invoke when Adam says "/linkedin-outreach," "find LinkedIn prospects," "draft LinkedIn connects," "send my LinkedIn requests," "triage LinkedIn DMs," or similar. Never auto-blasts.
---

# linkedin-outreach

Adam's LinkedIn prospecting command. Wraps the PROSPECT_SPEC workflow: find the right people,
draft genuine personalized outreach, send at a safe human pace (Adam approves, often clicks
send himself), triage replies, and log everything. Precision over volume. Never auto-blast.

Repo root: `~/Desktop/Claude Code/`. All paths below are relative to it.
Browser automation uses the Playwright MCP. DB is `database/leads.db` → `linkedin_prospects`.

## Always read first (voice + rules stay fresh)

- `outreach/linkedin/PROSPECT_SPEC.md` — targeting, geography, who we're after, account-safety rules
- `outreach/linkedin/templates/connection_outreach.md` — approved post-accept + short-note copy

Hard voice rules (from memory, never violate):
- **Lead with the person.** Order: husband, father, then realtor. Real estate is secondary, never the lead.
- Personalize the company/city hook from each profile so nothing reads as a blast.
- No em/en-dashes. No "no pressure / not selling / no obligation" disclaimers.
- No overpromising — never "I have buyers looking" or any demand Adam can't deliver.
- Skip thin profiles: empty profile AND very few connections (~<30).

## Modes

Pick the mode from what Adam asks. Default (bare `/linkedin-outreach`) = **find → draft → review**,
stopping before send for approval. Modes can chain.

### Mode: FIND (identify new prospects)

1. Confirm target city + role focus with Adam if not given (default: walk the geography priority
   order in PROSPECT_SPEC — San Clemente, Dana Point/Capo, Laguna, Newport, Oceanside, Carlsbad).
2. Use Playwright to search LinkedIn **sparingly and human-paced** (FREE account = commercial-use
   search limit). One narrow search at a time. Stop instantly on any "you've reached the limit" /
   commercial-use / checkpoint warning — log what was collected and report.
3. For each candidate, judge the **community-investment** filter (heart of the spec): owns/runs a
   local business, long local tenure, board/chamber/volunteer involvement, local references
   (kids' schools, "proudly serving [city]"). Infer income from title + seniority + industry +
   geography (income is never a LinkedIn field).
4. **Skip thin profiles** (empty + ~<30 connections). Log skips with `connect_status='skipped'`
   and a one-line reason in `outcome` so they don't resurface.
5. **Dedup** against the table by `profile_url` before inserting.
6. Insert keepers as `identified` with: name, headline, title, company, city, profile_url,
   category (business_owner/doctor/financial_advisor/attorney/tech/other), community_signal.

### Mode: DRAFT (write personalized outreach)

1. Pull rows needing copy (`connect_status IN ('identified','queued')`).
2. For each, write a **post-accept message** (primary — unlimited on free) personalized from the
   profile's company/city/community signal, off the approved template + voice rules.
3. For top-tier / warmest only, also draft a **short connection note** (reserve the ~5/month
   note allotment — most requests go noteless).
4. Save drafts to `drafted_note`, set `connect_status='note_drafted'`.
5. Show every draft inline to Adam for approval before anything is sent.

### Mode: SEND (fire approved requests)

1. Only after Adam approves the drafts. Send via Playwright, **human-spaced** (~10–15 requests/day
   max, no bursts).
2. **Scope the Connect click to the profile's own name** to avoid sending stray invites to people
   in the sidebar. Most requests go **noteless**; attach a note only for the warm few Adam flagged.
3. After each send: set `connect_status='request_sent'`, stamp `note_sent_at`.
4. Stop immediately on any rate/limit/checkpoint warning. Log progress and report.
5. To withdraw an errant invite, do it from **the profile page**, not the invite manager.

### Mode: TRIAGE (inbound)

1. Check for newly accepted connections and inbound DMs (connection requests + DM replies only —
   not proactive commenting, not reply-to-post monitoring).
2. Newly accepted → set `connected_at`, `connect_status='connected'`, and send the drafted
   post-accept message (show Adam first unless he's said to auto-send).
3. Replies → set `replied_at`, `connect_status='replied'`, summarize the thread, and draft Adam's
   next reply in his voice for approval. Record disposition in `outcome`.

## Logging cheatsheet

`connect_status` flow: identified → queued → note_drafted → request_sent → connected → replied
(plus `skipped` for filtered-out profiles). Always set the matching timestamp column when you
advance a stage. Update by `profile_url` (it's UNIQUE).

## Report back

End every run with: how many found / drafted / sent / triaged, the current funnel counts
(`SELECT connect_status, COUNT(*) FROM linkedin_prospects GROUP BY connect_status;`), any
limit/checkpoint warnings hit, and what's queued for the next session.

## Notes

- On-demand only — no auto-schedule (per Adam, 2026-06-03).
- A small, genuine batch beats volume. When in doubt, send fewer.
- When Adam dictates his own message copy, treat it as a draft to polish, then confirm back.
