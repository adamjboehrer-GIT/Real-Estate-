---
name: resident-email
description: Send Adam's resident (owner-occupied) canvassing cold emails from his Pacific Sotheby's Outlook via Playwright, paced to protect deliverability. Invoke when Adam says "/resident-email N-M", "resident email N through M", "send N resident emails", "send another 50", "keep sending [resident emails]", or "regenerate resident emails".
---

# Resident Canvassing Cold Emails — San Clemente & Capo Beach

Owner-occupied residents (mailing address matches property) in San Clemente and
Capistrano Beach ("Capo Beach"). Approved **V1** copy, Pacific Sotheby's, only
`{First}` and `{City}` vary. This is the auto-send paced workflow Adam settled on
(NOT the absentee draft-and-stop flow). Campaign id: `camp-resident-2026-06`.

## Invocation
- `/resident-email 251-300` (or "send another 50", "keep sending") → send that range.
- "regenerate resident emails" → just rebuild the source file (no sending).
- If Adam gives a count not a range ("send 50"), use the next un-sent numbers after
  the highest already logged.

## Hard rules (deliverability — learned the hard way; see [[reference_resident_email_deliverability]])
- **3-minute spacing between every send** (`delayMs=180000`), small batches of 3.
- **~50/day cap** from this personal M365 mailbox. If asked for more, send 50 and
  recommend spreading the rest across later days. A fresh day resets the limit.
- **"Compose closed" is NOT proof of delivery.** Always verify via Inbox NDR bounces.
- **Stop immediately** if "Couldn't send this message" toasts or repeated policy
  bounces appear — that's the throttle wall; discard any stuck compose and report.

## Files (all in repo)
- `scripts/gen_resident_emails.py [YYYY-MM-DD]` — (re)build `outreach/resident_emails_<date>.md` + `_manifest.json` from leads.db.
- `scripts/get_resident_email.py N` — JSON `{number,to,subject,body}` for entry N.
- `scripts/gen_batch_send_js.py START END [DELAY_MS]` — writes self-contained
  `scripts/_batch_send_generated.js` with the batch's data embedded (the Playwright
  sandbox has NO fs/require/import, so data must be inlined) + the compose/send loop.
- `scripts/log_resident_sends.py N [M ...]` — log sends to `interactions`
  (idempotent), accepts ranges like `251-260`.

## Procedure for "/resident-email START-END"
1. **Stage queue.** Build `outreach/resident_send_queue.json` for the range:
   ```
   python3 -c "import json,subprocess; out=[json.loads(subprocess.check_output(['python3','scripts/get_resident_email.py',str(n)])) for n in range(START,END+1)]; \
   [e.update({'lines':e.pop('body').split(chr(10))}) for e in out]; \
   json.dump([{'n':e['number'],'to':e['to'],'subject':e['subject'],'lines':e['lines']} for e in out], open('outreach/resident_send_queue.json','w'), ensure_ascii=False, indent=0)"
   ```
   (Or the equivalent inline python used in past runs.)
2. **Check Outlook.** `browser_run_code_unsafe`: navigate to outlook.office.com/mail/,
   confirm `button[aria-label="New mail"]` exists.
   - If at the Microsoft sign-in page → STOP and ask Adam to log in (password+MFA);
     Playwright can't do MFA.
   - If "Browser is already in use / mcp-chrome-bb6278f" lock → kill orphaned Chrome
     PIDs (`ps aux | grep mcp-chrome-bb6278f`), relaunch, re-check. See
     [[project_playwright_profile_lock]].
3. **Send in batches of 3:** for each chunk,
   `python3 scripts/gen_batch_send_js.py A B 180000` then
   `browser_run_code_unsafe(filename=scripts/_batch_send_generated.js)`.
   On success log it: `python3 scripts/log_resident_sends.py A-B`.
4. **NDR/opt-out checks** every ~5 batches and at the end: open Inbox, scan for
   "Microsoft Outlook … couldn't be delivered / wasn't found" (bounces) and inbound
   replies. For each bounce: delete its interaction row + set `contacts.status='bounced'`.
   For each "stop"/"remove me" reply: set `contacts.status='do_not_contact'`.
   (Keyed by manifest number → cids.)
5. **Report:** sent count, bounces (with addresses), opt-outs, any inbound seller
   leads, and how many residents remain. Clean up `scripts/_batch_send_generated.js`
   and the queue file.

## Compose mechanics (baked into gen_batch_send_js.py — don't reinvent)
- New mail via button whose aria-label/text is "New mail"; dismiss any "Dismiss all"
  reminder + Viva Insights popups.
- To = `[aria-label="To"][contenteditable="true"]` (NO role=textbox); type address + Enter to chip.
- Subject = `input[aria-label*="subject" i]`.
- **Body font gotcha:** never type into the caret (it inherits the signature's Aptos
  Serif 22pt). Build `<div>`s styled `font-family: Aptos, sans-serif; font-size:16px;
  color: rgb(0,0,0);` and `insertBefore` the `#Signature` div, then dispatch `input`.
- Send = `button[aria-label="Send"]`; confirm compose closed.

See [[reference_absentee_outlook_automation]] for the sibling absentee flow.
