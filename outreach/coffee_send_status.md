# Round 2 "Coffee" Send Status

Campaign `camp-coffee-2026-08`. Copy: `cold_emails_2026-08-13_coffee.md`.
Queue: `coffee_send_queue.json` (#1-479 version B, #480-843 version A).

## Progress

| Date | Sent | Numbers | Failures | Bounces | Opt-outs |
|---|---|---|---|---|---|
| 2026-08-14 | 77 | #1-77 (version B) | 0 | 1 | 0 |

**Next batch starts at #78.**

- Version B remaining: 402
- Version A waiting: 364 (#480-843)
- Risky/catch-all held back, never queued: 309

## Resume command

```
python3 scripts/gen_batch_send_js.py --nums 78-87 180000 --queue coffee_send_queue.json
```

Then run `scripts/_batch_send_generated.js` through Playwright against a logged-in
outlook.office.com tab, and log with:

```
python3 scripts/log_resident_sends.py 78-87 --campaign camp-coffee-2026-08
```

Batches of 10 at 180s spacing take about 30 minutes and land inside the MCP idle
timeout. Do not go much past 12 per batch.

## Bounces / retries

| # | Address | Notice | Action |
|---|---|---|---|
| 17 | Pheckler@hotmail.com | "A communication failure occurred during delivery" (transient, not a dead mailbox) | Retry once on a later day. Not marked `bounced`. |

Two other hotmail addresses in the same batch delivered fine, so this is not a
Microsoft-level block.

## Notes from day one

- The signature banner image is what triggered Outlook's "please wait to send" dialog
  and stalled the first batch for 30+ minutes on a single email. `gen_batch_send_js.py`
  now strips every image from the compose right before Send. Sends went 70-for-70 after
  that change, with exact 3-minute spacing.
- The saved Outlook signature is untouched. The strip is per-compose, in memory.
- Disclosure (name, DRE #02419464, REALTOR®, brokerage, phone, email) and the opt-out
  line are live text in the body of every email, so nothing compliance-bearing depends
  on the banner rendering.
- Reconcile against Sent Items, not the script's return value, if a run ever times out.
  The browser keeps sending after the MCP call is aborted.
