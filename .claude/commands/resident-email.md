---
description: Send resident (owner-occupied) canvassing cold emails from Adam's Pacific Sotheby's Outlook, paced for deliverability. Pass a range like "251-300".
argument-hint: [START-END]  e.g. 251-300
---

Run the resident canvassing cold-email send for range **$ARGUMENTS**.

Follow `.claude/skills/resident-email/SKILL.md` exactly — that file is the single
source of truth for the procedure, copy, scripts, and deliverability rules.

Key reminders (do not deviate):
- Approved V1 copy, Pacific Sotheby's, San Clemente / Capo Beach auto-filled.
- 3-minute spacing between every send, batches of 3, ~50/day cap.
- Verify the Outlook session first (pause for Adam to log in if at the sign-in page;
  recover the mcp-chrome profile lock if needed).
- Log each batch to leads.db; check Inbox NDRs (mark bounces) and replies (mark
  "stop"/"remove me" as do_not_contact); stop immediately on "Couldn't send" throttle.
- If $ARGUMENTS is a count rather than a range, start after the highest already-sent number.

Report sent count, bounces, opt-outs, any inbound seller leads, and residents remaining.
