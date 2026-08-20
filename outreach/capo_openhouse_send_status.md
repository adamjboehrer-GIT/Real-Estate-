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
| 2026-08-20 | 131 | #1-130, #132 | 1 (#131, retryable) | 7 | 1 |

**STOPPED FOR THE DAY at 131.** Resume Friday 8/21 with **#131 first**, then #133-225.
94 remain. Do not send #226-325: tier 2 is dropped.

#131 `gilbertabrigo1@gmail.com` hit the 120s per-email watchdog and **never sent**.
Confirmed twice: absent from Sent Items, and absent from the ledger, so it is not marked
spent and is safe to retry. It is deliberately unlogged for that reason.

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

## Why the day stopped at 131 rather than 150

The last batch returned **4 sent, 1 watchdog failure, 13 skipped on run budget, in 23
minutes.** Five composes consumed a 22-minute budget that normally carries 18. The Outlook
tab had degraded to the point where each compose was taking minutes instead of seconds.

That is the third failure in a row on the same browser: crash at #89, crash at #127, then
this stall. Continuing would have meant more crashes, more reconciliation, and more chances
to lose track of what actually sent, in exchange for a handful of emails. **Stopped at 131
on purpose**, comfortably under the 150 ceiling.

Friday starts on a fresh browser with 94 to send, which fits a normal day easily. Restart
Chrome before the first batch rather than reusing this session's profile state.

## Tier 2 dropped, 2026-08-20 (Adam's call)

**The 100 catch-all addresses (#226-325) will not be sent.** Adam chose verified-only
after seeing the Friday arithmetic: 182 remained against a ~150/day ceiling, and Yahoo was
already rejecting. Tier 1 alone (#1-225) fits comfortably before Saturday.

The queue file still holds #226-325. Nothing needs deleting; simply stop at #225. If a
later round wants them, they should be re-verified first rather than sent on 8/13 data.

## The ledger does NOT survive a browser crash

Batch #126-143 died with `Page crashed`, and after recovery
`localStorage.__sendLedger_camp-capo-oh-2026-08` came back **empty** — not stale, gone.
The earlier #89 crash had preserved it, so this is not reliable either way.

**Consequence: the localStorage ledger is a within-session guard only. The DB seed
(guard 4) is the durable one.** It re-seeded all 127 logged numbers into the fresh ledger
on the next generate, which is the only reason the campaign could resume safely.

**So: always log a batch to `leads.db` before generating the next one.** An unlogged batch
plus a wiped ledger equals no duplicate protection at all.

Reconciliation here had to come from Sent Items alone: newest was `fjbill24@yahoo.com`
(#127), so #126-127 sent and #128 onward never ran. The crash landed about three minutes
into the batch, consistent with the 234s the call was alive.

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

## Opt-outs (permanent)

`build_send_list.py` blocks every `do_not_contact` row, so no rebuilt list will
resurface them.

| # | Address | Name | Date | Their words | Action taken |
|---|---|---|---|---|---|
| 26 | gwynne99@gmail.com | Gwynne Simmons | 2026-08-20 | "Stop" | `do_not_contact`, opt-out logged. Never contact again on any channel. Verified she has nothing pending in either the capo queue (#26, already sent) or the coffee queue (#10, sent 8/14). |

## Replies

| # | Address | Name | Date | What they said | Action |
|---|---|---|---|---|---|

## Bounces

**Both rejections so far are Yahoo, both `5.0.350`** — a generic policy/security
rejection, explicitly *not* "no such user". Neither is marked `bounced`: the mailboxes
are not dead, Yahoo declined the message. Marking them bounced would permanently
suppress two real neighbors.

**Yahoo exposure worth watching.** 62 of the 325 addresses are Yahoo. 6 have gone out
and 2 were rejected. 56 remain (31 in tier 1, 25 in tier 2). Overall delivery is still
34 of 36. Not a reason to stop, but if the Yahoo rejection rate holds through tier 1,
those addresses want a different channel rather than a retry from the same mailbox.

| # | Address | Notice | Action |
|---|---|---|---|
| 20 | eburkow@yahoo.com | 5.0.350 policy rejection (Yahoo) | not marked bounced; mailbox is live |
| 28 | hilaryjean_kalb@yahoo.com | 5.0.350 policy rejection (Yahoo) | not marked bounced; mailbox is live |
| 46 | lwinters@hotmail.com | delivery failed (postmaster) | not marked bounced pending a reason code |
| 53 | pheckler@hotmail.com | delivery failed (postmaster) | **second failure** — also failed in the coffee round 8/14 as "transient". Two strikes; stop retrying this one. |
| 57 | rmarkley2k@yahoo.com | couldn't be delivered (Yahoo) | not marked bounced; mailbox is live |
| 80 | aleighess@yahoo.com | couldn't be delivered (Yahoo) | not marked bounced; mailbox is live |
| 103 | clwboo@aol.com | couldn't be delivered (AOL) | not marked bounced; mailbox is live |

**Rate check: 7 of 107, about 6.5%.** Round 1 ran 8% unverified and that is the level
`VERIFICATION.md` calls reputation-damaging, so this is close enough to watch rather than
ignore, *but* the composition matters: 4 of 7 are Yahoo and 1 is AOL, both Yahoo-operated.
This reads as one mailbox provider throttling a single sender, not a bad list. The
addresses were MillionVerifier-clean less than a week ago.

**None are marked `bounced`.** They are policy rejections against live mailboxes, and
marking them would permanently suppress real neighbors over a provider dispute.

## Auto-responders

| # | Address | What came back | Action |
|---|---|---|---|
| 44 | lneitzel@winston.com | "Lisa Neitzel is no longer with the firm" | Marked `bounced` to suppress. The mailbox accepts mail but it no longer reaches the owner, and mail about her home was landing in an inbox now staffed by strangers. Suppression here is a privacy call as much as a deliverability one. If Adam wants to reach her, it needs a different address. |

## Browser died mid-batch at #89, 2026-08-20

Batch #73-90 returned `page.waitForTimeout: Target page, context or browser has been
closed`. The browser went away underneath a live run.

**Nothing was orphaned.** The loop drives the page through the `page` handle, so it dies
with the tab. That is the same property the double-send postmortem relies on: closing the
tab is what actually kills a runaway loop.

**Reconciled two independent ways, and they agreed exactly:**

| Source | Says |
|---|---|
| `localStorage.__sendLedger_camp-capo-oh-2026-08` | 89 numbers spent, max 89, batch range #73-89 |
| Outlook Sent Items, newest first | #89, 88, 87, 86, 85, 84, 83 |

So **#73-89 sent and #90 never started**. Logged 73-89 and resumed at #90. The ledger
survived because it lives in the profile directory, not the process.

The dead run still held `__sendLock`. Cleared it explicitly rather than waiting out the
150s staleness window, since both sources had already confirmed the run was dead.

### Row count exceeds send count, and that is correct

`leads.db` shows 90 outbound rows for 89 sends. `benji_2003@hotmail.com` (#88) maps to
two contact records; the title data carries duplicate rows per person, up to five for
`richardkay@sbcglobal.net`. The logger records the touch against every contact record for
that person, while the send list dedupes on the address, so the person received exactly
one email. Six manifest entries have more than one contact id. **Count sends by distinct
queue number, never by interaction rows.**

## Playwright profile lock, 2026-08-20

Mid-session the MCP server threw `Browser is already in use for .../mcp-chrome-bb6278f`.
The lock pointed at a Chrome that was **34 seconds old**, not the hour-old one holding the
Outlook session: the original had exited and a fresh instance grabbed the profile.

Fix was `pkill -f mcp-chrome-bb6278f`, then remove `SingletonLock`/`SingletonCookie`/
`SingletonSocket`, then reconnect. **The Outlook session survived**, because cookies live
in the profile directory rather than in the process.

Safe only because no send loop was live at the time. Never do this mid-run: killing the
browser during a batch loses the loop with no way to know where it stopped. Check that
nothing is in flight first, then reconcile Sent Items after.
