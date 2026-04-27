# South OC Seller's Playbook — Package

## What's in this folder

| File | What it is |
| --- | --- |
| `South-OC-Sellers-Playbook.pdf` | The branded, print-ready PDF. This is the file you give to subscribers. |
| `playbook.html` | The HTML source the PDF is rendered from. Edit this if you want to revise content; ask Claude to regenerate the PDF afterward. |
| `README.md` | This file. |

## Should this go on the website as a download?

**No.** The whole point of a lead magnet is the email exchange. If anyone can download it without subscribing, you lose the lead. Keep it gated behind the Mailchimp signup.

The homepage already does the right thing — it describes the playbook in the signup section so prospects can see the value, but it does not link the PDF directly.

## How to deliver it (Mailchimp setup, ~10 minutes)

1. **Upload the PDF to Mailchimp's content library.**
   - Mailchimp → Content → Content Studio → Upload.
   - Upload `South-OC-Sellers-Playbook.pdf`.
   - Right-click the uploaded file → Copy link. That URL is what subscribers get.

2. **Edit your "Welcome — Coastal Currents" automation.**
   - Audience → Automations → "Welcome — Coastal Currents" (audience f44752d032).
   - Open the first welcome email.
   - Add a button or link near the top that says **"Download The South OC Seller's Playbook"** and points to the URL from step 1.
   - One short paragraph above the button explaining what they're getting works well. Something like:
     > "Welcome to Coastal Currents. As promised, here is The South OC Seller's Playbook. A short read on what your home is worth in 2026 and the decisions that move the number. The next issue will hit your inbox on the regular bi-weekly schedule."

3. **Test it.**
   - Send a test of the welcome email to yourself.
   - Click the download link. Confirm the PDF loads and the styling is right.

## When you want to update the playbook

1. Tell Claude what to change. Claude edits `playbook.html`, regenerates `South-OC-Sellers-Playbook.pdf`.
2. Re-upload the new PDF to Mailchimp's content library (replacing the old one keeps the same URL, so the welcome email keeps working without further edits).

## Other places this PDF can be used

Once it lives in Mailchimp, the same gated link can power:

- **Cold email signoffs** — soft offer at the end: "If you ever want a copy of my Seller's Playbook, just reply with your email."
- **Direct mail flyers** — a QR code on the back pointing to a signup landing page that gates it.
- **Social bios and posts** — Instagram and LinkedIn link → adamboehrer.com → signup → PDF.
- **In-person handoffs** — print a few hard copies for door-knocks or open houses where a digital handoff is awkward.

The same playbook works across every first-touch channel. That is the leverage.
