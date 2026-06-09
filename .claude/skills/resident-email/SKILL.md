---
name: resident-email
description: Compose Adam's resident (owner-occupied) canvassing cold emails into Outlook web one at a time, paused at the draft for review. Also regenerates the source file. Invoke when Adam says "resident email N", "resident email N through M", "regenerate resident emails", or similar.
---

# Resident Canvassing Cold Emails — San Clemente & Capo Beach

Owner-occupied residents (mailing address matches the property) in San Clemente and
Capistrano Beach / "Capo Beach". Approved **V1** copy: short intro, neighborhood in
high demand, buyers waiting in the wings, canvassing to find a potential seller,
"I'd love to connect." Pacific Sotheby's. Only `{First}` and `{City}` vary.

This is the resident counterpart to the absentee flow. See
[[reference_absentee_outlook_automation]] for the shared Outlook gotchas.

## Files
- **Generator:** `scripts/gen_resident_emails.py [YYYY-MM-DD]` → writes
  `outreach/resident_emails_<date>.md` + `_manifest.json`.
- **Source file:** latest `outreach/resident_emails_*.md`. Two sections:
  "addressed by name" (`Hi {First},`) and "neighborly greeting" (name unclear:
  trust/LLC/parsed → `Hi neighbor,` / `Hello, neighbor!`).
- **Parser:** `python3 scripts/get_resident_email.py N` → JSON `{number,to,subject,body}`.
  Body runs greeting → "Best," inclusive.
- **Logger:** `python3 scripts/log_resident_sends.py N [M ...]` → logs sends to
  `interactions` (campaign `camp-resident-2026-06`), idempotent.

## "regenerate resident emails"
Run `python3 scripts/gen_resident_emails.py <today>`; report the by-name /
neighborly / total counts.

## "resident email N" (or "N through M")
For each N, compose into Outlook web and STOP at the draft. Never auto-send;
Adam reviews and clicks Send himself.

1. `python3 scripts/get_resident_email.py N` to get `{to, subject, body}`.
2. Outlook on the web (outlook.office.com), account adam.boehrer@pacificsir.com.
   Adam must already be logged in (password + MFA); Playwright can't drive the
   desktop app.
3. New mail → fill **To** (contenteditable `#…_TO .EditorClass`, then Enter to
   chip the address) → fill **Subject** (`Add a subject`).
4. **Body — critical font gotcha (same as absentee):** do NOT type into the
   cursor. A fresh compose places the caret inside the signature wrapper
   (`#Signature`, Aptos Serif / 22pt / SIR blue), so typed text inherits that
   oversized serif. Build the body as paragraph `<div>`s with inline style
   `font-family: Aptos, sans-serif; font-size: 16px; color: rgb(0,0,0);`
   (blank lines = `<div><br></div>`) and `insertBefore` the `#Signature` div,
   then dispatch an `input` event. Signature auto-appends as an image; leave it.
5. Screenshot the draft and STOP. Tell Adam it's ready to review + Send.
6. After Adam confirms a batch is sent, run `log_resident_sends.py` for those
   numbers.

## Pacing / deliverability
These go from a real Microsoft 365 account. Sending many in rapid succession
risks throttling or spam-flagging. Default to small human-paced batches and let
Adam click Send; do not auto-fire large volumes.
