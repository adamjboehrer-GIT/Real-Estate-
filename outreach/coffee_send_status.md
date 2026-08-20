# Round 2 "Coffee" Send Status

Campaign `camp-coffee-2026-08`. Copy: `cold_emails_2026-08-13_coffee.md`.
Queue: `coffee_send_queue.json` (#1-479 version B, #480-843 version A).

## PAUSED — 2026-08-20

**Stopped at #312. Do not resume before Monday 2026-08-24.**

Adam pulled the Capo Beach slice of the list out for a one-off open house invite
for 26966 Calle Dolores on Saturday 8/22 (`camp-capo-oh-2026-08`). Both campaigns
send from the same Outlook mailbox against the same ~150/day ceiling, so they
cannot run on the same day without one starving the other or tripping throttling.

The coffee queue is untouched: #313 is still the resume point, the send ledger and
the DB seed still hold, and nothing about the pause changes the guards below.

**One overlap to know about before resuming.** Some Capo Beach addresses in the
open house send have already had a coffee email, and the rest are still sitting in
the pending coffee queue. Anyone who replies to the open house invite, or who opts
out of it, must be reflected in `leads.db` before #313 goes out, or they will get a
cold pitch days after answering a neighbor note. `build_send_list.py` already drops
`do_not_contact` and `responded`, so logging the responses is the whole fix.

---

## Progress

| Date | Sent | Numbers | Failures | Bounces | Opt-outs |
|---|---|---|---|---|---|
| 2026-08-14 | 77 | #1-77 | 0 | 1 | 0 |
| 2026-08-17 | 150 | #78-227 | 0 | 2 | 1 |
| 2026-08-18 | 85 | #228-312 | 0 | 0 | 2 |
| **Total** | **312** | | **0** | **3** | **3** |

**Next batch starts at #313.**

- Version B remaining: 167
- Version A waiting: 364 (#480-843)
- Risky/catch-all held back, never queued: 309

8/18 came in at 85 rather than the 150/day target, entirely from lost time, not
throttling: the double-send incident cost the early afternoon, a `setTimeout` bug
burned one 18-minute run with zero sends, and the machine slept mid-run on the last
batch. No throttle toast at any point. Nothing about deliverability argues against a
full 150 next session.

## Pacing

Settled at **60-second spacing, batches of 25**, roughly 60/hour. Got there in steps
(180s/10, then 90s/20, then 60s/25) with a bounce and throttle check between each. No
throttle toast at any point.

**Stop at 150/day.** That is where June's `camp-resident-2026-06` run hit throttling.
8/17 stopped exactly there by sizing the last batch to 15 instead of 25.

## 2026-08-18 — double-send incident (fixed)

**Six people got the same email twice, about a minute apart:** Carolynmcowen@me.com,
Cchafner11@gmail.com, Cdpete2000@yahoo.com, Cestarke@gmail.com, Cgarcia6769@gmail.com,
Charlotte@charlottefryer.com (#237-241, #243). Not recallable — Outlook message recall
only reaches mailboxes inside the same Exchange org, and every one of these is an
external consumer mailbox. Outlook offers no Recall control on them at all.

**Cause.** Batch #228-252 hit the MCP idle timeout at 31 minutes and the tool call
aborted. The JS kept running inside the Playwright server process. Sent Items showed it
had stopped at #236, which looked like a dead loop but was really a 23-minute stall on
one compose. The next batch was launched on top of the still-live one, and from #237 two
loops drove the same tab in lockstep.

**Made worse by the stop attempt.** Navigating the tab to `about:blank` did not kill the
loops; navigating back to Outlook to check Sent Items handed them a working page and they
resumed. **Closing the tab is what actually kills a runaway loop** — the `page` handle
dies with it.

**Four guards now in `gen_batch_send_js.py`**, all verified live against the real Outlook
tab on 8/18 with the recipient swapped to Adam's own address:

1. **Run budget** — the loop stops itself at 22 minutes and returns. A run that ends by
   returning cannot orphan itself. This is the guard that matters most; the other three
   are there for when it fails.
2. **Run lock** — a heartbeat lock in the page's `localStorage`. A second run refuses to
   start while a live loop holds it, and a running loop exits if it loses it. In
   `localStorage`, not `window`, so it survives exactly the navigation that defeated the
   first stop attempt. *Verified: returned `ANOTHER_RUN_IS_LIVE`, 0 sent, no compose.*
3. **Send ledger** — every number is written to `localStorage` immediately **before** the
   Send click and checked before each compose. A crash after Send therefore skips rather
   than resends. Missed sends surface in Sent-Items reconciliation; duplicates cannot be
   taken back, so the asymmetry is deliberate. *Verified: returned `already in send
   ledger`, 0 sent.*
4. **DB seed** — numbers already logged in `leads.db` for this campaign are dropped at
   generation time and pre-seeded into the ledger. *Verified: dropped #240-243 from a
   requested #240-250 range.*

A per-email watchdog (120s) also stops one stalled compose from eating the run, and
discards the compose it abandons.

**Two follow-on failures on 8/18, both caught by the guards, both worth knowing:**

- **`setTimeout` does not exist in the MCP sandbox.** The first watchdog used it and
  threw `ReferenceError` synchronously on all 18 emails — a whole run, zero sent. The
  watchdog now uses `page.waitForTimeout`, the only timer available there. Verified both
  branches (work-wins and watchdog-fires) before resuming.
- **Machine sleep freezes every timer.** The last run of the day reported 128 minutes of
  wall clock: the Mac slept mid-batch, and because both the run budget and the watchdog
  are measured with page-side timers, neither could fire while it slept. The MCP call
  aborted; the loop woke, finished #312, and released its lock cleanly. **The ledger held
  — it matched Sent Items number for number, and #313-315 correctly never sent.** This is
  the case the guards exist for. Reconcile after any long gap; do not assume the run
  budget bounded it.

## Resume command

```
python3 scripts/gen_batch_send_js.py --nums 313-330 60000 --queue coffee_send_queue.json
```

Run `scripts/_batch_send_generated.js` through Playwright against a logged-in
outlook.office.com tab, then log the numbers the run actually reports as sent:

```
python3 scripts/log_resident_sends.py 313-330 --campaign camp-coffee-2026-08
```

**Batch size: 25 at 60s is 25 minutes, which is over the 22-minute run budget — the tail
of the batch will come back as `run budget reached` and simply needs a second run. Use 18
per batch at 60s to fit inside the budget with slack.**

**If a run ever aborts or times out:**
1. **Close the tab.** First, before anything else. Not `about:blank` — close it.
2. Reconcile against Sent Items in a **new** tab.
3. Log what actually went out, then generate the next batch. The DB seed and the ledger
   will refuse anything already sent, so the resume point does not have to be perfect.

If the Playwright MCP server is disconnected, `scripts/send_batch_local.js` does the same
job through the repo's own Playwright install. It needs a Bash permission the classifier
currently blocks, so reconnecting MCP via `/mcp` is the faster path. **Note that it has
not been given the four guards above — do not use it until it has.**

## Opt-outs (permanent)

These addresses are permanently suppressed. `scripts/build_send_list.py` blocks every
`do_not_contact` row, so round 3 will not rebuild them into a list. Verified against the
pending queue (#228-843): zero suppressed addresses remain in it.

| # | Address | Name | Date | Their words | Action taken |
|---|---|---|---|---|---|
| 97 | kkhadivi@me.com | Kamran Khadivi | 2026-08-17 | "I'm not interested in selling my house. Please stop sending me unsolicited emails." | `do_not_contact`, opt-out logged. Never contact again on any channel. |
| 169 | fitzblossom@gmail.com | Amy Fitzpatrick | 2026-08-17 | "STOP!" | `do_not_contact`, opt-out logged. Never contact again on any channel. |
| 198 | amkindness@gmail.com | Andre | 2026-08-17 | "STOP" | `do_not_contact`, opt-out logged. Never contact again on any channel. |

## Soft declines (suppress from future cold rounds)

Not opt-out requests, so no `do_not_contact` flag, but they answered the question. Marked
`responded`, which `build_send_list.py` also excludes from any rebuilt list.

| # | Address | Name | Date | Their words |
|---|---|---|---|---|
| 148 | wadeguthrie@gmail.com | Wade Guthrie | 2026-08-17 | "We're happy here and not interested in selling. Thank you." |

## Bounces / retries

| # | Address | Notice | Action |
|---|---|---|---|
| 17 | Pheckler@hotmail.com | communication failure during delivery (transient) | retry once later |
| 139 | Steph_ulm@hotmail.com | mailbox full | retry once later |
| 226 | Bsimanton@hotmail.com | mailbox full | retry once later |

None marked `bounced`. All three are retryable conditions, not dead mailboxes.

## Response so far

**Zero positive replies through 312 sends.** Three opt-outs, one soft decline. If this is still the picture
around 300, the angle is not landing and the right move is to test a different subject
line on a slice of Version A rather than spend the rest of the list on it.

Note that from #155 onward the list is the no-name portion (trusts, LLCs, unparseable
vesting strings) opening "Hi neighbor," which historically pulls lower than a first name.
Judge the copy on the named rows, not the whole run.

## Notes

- Signature banner images are stripped from every compose before Send. Without that,
  Outlook's "please wait to send" dialog stalls batches for 30+ minutes.
- Disclosure (name, DRE #02419464, REALTOR®, brokerage, phone, email) and the opt-out line
  are live text in the body, so nothing compliance-bearing depends on the banner.
- If a run ever times out, reconcile against Sent Items. The browser keeps sending after
  the MCP call is aborted.
