# Round 2 "Coffee" Send Status

Campaign `camp-coffee-2026-08`. Copy: `cold_emails_2026-08-13_coffee.md`.
Queue: `coffee_send_queue.json` (#1-479 version B, #480-843 version A).

## Progress

| Date | Sent | Numbers | Failures | Bounces | Opt-outs |
|---|---|---|---|---|---|
| 2026-08-14 | 77 | #1-77 | 0 | 1 | 0 |
| 2026-08-17 | 150 | #78-227 | 0 | 2 | 1 |
| **Total** | **227** | | **0** | **3** | **1** |

**Next batch starts at #228.**

- Version B remaining: 252
- Version A waiting: 364 (#480-843)
- Risky/catch-all held back, never queued: 309

## Pacing

Settled at **60-second spacing, batches of 25**, roughly 60/hour. Got there in steps
(180s/10, then 90s/20, then 60s/25) with a bounce and throttle check between each. No
throttle toast at any point.

**Stop at 150/day.** That is where June's `camp-resident-2026-06` run hit throttling.
8/17 stopped exactly there by sizing the last batch to 15 instead of 25.

## Resume command

```
python3 scripts/gen_batch_send_js.py --nums 228-252 60000 --queue coffee_send_queue.json
```

Run `scripts/_batch_send_generated.js` through Playwright against a logged-in
outlook.office.com tab, then log:

```
python3 scripts/log_resident_sends.py 228-252 --campaign camp-coffee-2026-08
```

If the Playwright MCP server is disconnected, `scripts/send_batch_local.js` does the same
job through the repo's own Playwright install (`--nums 228-252`). It needs a Bash
permission the classifier currently blocks, so reconnecting MCP via `/mcp` is the faster path.

## Opt-outs (permanent)

| # | Address | Date | Action taken |
|---|---|---|---|
| 198 | amkindness@gmail.com ("Andre") | 2026-08-17 | `do_not_contact`, opt-out logged. Never contact again on any channel. |

## Bounces / retries

| # | Address | Notice | Action |
|---|---|---|---|
| 17 | Pheckler@hotmail.com | communication failure during delivery (transient) | retry once later |
| 139 | Steph_ulm@hotmail.com | mailbox full | retry once later |
| 226 | Bsimanton@hotmail.com | mailbox full | retry once later |

None marked `bounced`. All three are retryable conditions, not dead mailboxes.

## Response so far

**Zero positive replies through 227 sends.** One opt-out. If this is still the picture
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
