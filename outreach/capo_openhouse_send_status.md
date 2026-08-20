# Capo Beach Open House Send Status

Campaign `camp-capo-oh-2026-08`. Copy and roster: `capo_openhouse_emails_2026-08-20.md`.
Queue: `capo_openhouse_send_queue.json` (#1-225 tier 1 verified, #226-325 tier 2 catch-all).

**The event:** 26966 Calle Dolores, open house **Saturday 8/22, 1 to 4 PM**. Price improved
to **$1,995,000**. Kameron Brown's listing (DRE #02021705); Adam is hosting, so every piece
carries the non-solicitation line.

## The list

325 sendable addresses. Everyone owns a home whose property city is Capistrano Beach, and
322 of the 325 have a Capo Beach mailing address too, so this is effectively a resident
list rather than an absentee one.

| | |
|---|---|
| Distinct Capo Beach emails | 332 |
| After suppression (`email_sendlist` + `responded`) | 325 |
| Tier 1, MillionVerifier clean | 225 (#1-225) |
| Tier 2, catch-all domains | 100 (#226-325) |

Tier 2 is held for Friday 8/21 and only goes if Thursday's bounces read clean. Catch-all
domains accept everything at the SMTP layer, so verification cannot confirm or deny them.
They are not known-bad, just unconfirmable.

Of tier 1, **75 open by name and 150 open "Hi neighbor,"**. That is the vesting-string
problem, not a bug: the county data gives "Bertagna Norma D Tr" and there is no safe way to
recover a first name from it. Judge reply rate on the named rows.

## Progress

| Date | Sent | Numbers | Failures | Bounces | Opt-outs |
|---|---|---|---|---|---|
| 2026-08-20 | 18 | #1-18 | 0 | tbd | tbd |

**Next batch starts at #37** (#19-36 in flight).

## Pacing

**18 per batch at 60-second spacing**, which is 18 minutes and fits inside the 22-minute run
budget with slack. Roughly 60/hour. **Stop at 150/day** — that is where June's
`camp-resident-2026-06` run hit throttling.

225 in a day is above that ceiling. The realistic shape is ~150 Thursday and the remaining
~75 Friday morning alongside tier 2, which still lands everything a day before the open
house. Do not chase 225 in one day by tightening the spacing.

## Ledger scoping bug, found and fixed 2026-08-20

The first launch of #1-18 returned **0 sent, 18 skipped, "already in send ledger"**.

The localStorage send ledger was a single global `__sendLedger` key, but queue numbering
restarts at 1 for every campaign. Coffee had already spent #1-312, so every number in this
campaign collided with it and the run refused itself. Nothing sent, nothing wrong went out.

`--force` would have been the wrong fix: it disables the duplicate guard rather than
correcting the collision. The key is now `__sendLedger_<campaign>`.

Coffee keeps its protection through guard 4, the DB seed, which reloads all 312 logged
sends from `leads.db` into its own key at run start. Verified: a 300-320 request still
drops 300-312 and generates only 313-320.

## Manifest-mapping bug, found and fixed 2026-08-20

After batch #1-18 sent cleanly, `log_resident_sends.py --campaign camp-capo-oh-2026-08`
logged all 18 against **the wrong contacts** and reported "0 not found".

The manifest selector was a two-way conditional: the coffee manifest for `camp-coffee*`,
the resident manifest for everything else. This campaign matched neither, so it fell
through to June's resident manifest, where #1-18 also exist and point at different people.
It could not report a miss, because nothing was missing.

Fixed to an explicit dict with no fallback; an unmapped campaign exits rather than
guessing. The 18 bad rows were deleted and re-logged correctly, verified address by
address against the queue.

Same root cause as the ledger collision above: **a queue number means nothing without the
campaign that issued it.** Anything keyed on the bare number is a bug waiting for a second
campaign to exist.

## Coffee round is paused for this

`camp-coffee-2026-08` stopped at #312, resume no earlier than Monday 8/24. Both campaigns
send from the same Outlook mailbox against the same ~150/day ceiling. See
`coffee_send_status.md`.

**Before coffee resumes at #313:** anyone who replies to this invite, or opts out of it,
has to be reflected in `leads.db` first, or they get a cold pitch days after answering a
neighbor note. `build_send_list.py` drops `do_not_contact` and `responded`, so logging the
responses is the whole fix.

## Commands

```
python3 scripts/gen_batch_send_js.py 19 36 60000 \
    --queue capo_openhouse_send_queue.json --campaign camp-capo-oh-2026-08
```

Run `scripts/_batch_send_generated.js` through Playwright against a logged-in
outlook.office.com tab, then log what the run actually reports as sent:

```
python3 scripts/log_resident_sends.py 19-36 --campaign camp-capo-oh-2026-08
```

**If a run aborts or times out:**
1. **Close the tab.** First, before anything else. Not `about:blank` — close it.
2. Reconcile against Sent Items in a **new** tab.
3. Log what actually went out, then generate the next batch. The DB seed and the ledger
   refuse anything already sent, so the resume point does not have to be perfect.

## Replies

| # | Address | Name | Date | What they said | Action |
|---|---|---|---|---|---|

## Bounces

| # | Address | Notice | Action |
|---|---|---|---|
