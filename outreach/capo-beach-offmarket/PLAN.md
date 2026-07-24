# Capo Beach Off-Market Teardown / Renovation Sourcing Plan

**Client goal:** One buyer, off-market only, seeking a rundown / teardown-worthy home in Capistrano Beach (Dana Point) to renovate.
**Operator:** Adam Boehrer, DRE #02419464, Real Estate Agent, Pacific Sotheby's International Realty.
**Created:** 2026-07-24

This is a precision sourcing project, not a mass campaign. The target is a small, hand-built list of unlisted homes whose owners we approach one at a time, in a compliant, human way.

---

## 0. Compliance guardrails (read first — these govern everything below)

Every step of research and outreach is bound by these. They are not optional.

### NAR Code of Ethics
- **Article 16 — do not solicit property already listed with another broker.** Before any home goes on the outreach list, confirm it is **not currently an active or pending MLS listing**. Off-market/unlisted owners are fair game; a home listed with another agent is not. A truly general mailing to a neighborhood is permitted, but our list is targeted, so we filter out active listings first.
- **Article 12 — true picture / honest advertising.** No misleading claims, no fake urgency, no "we have multiple buyers" when we have one.
- **Article 1 — client's interest first**, balanced with honest treatment of all parties, including the owner we're approaching.

### The buyer representation is real — so we may say so, truthfully
Because Adam genuinely represents an actual buyer actively looking in Capo Beach, he may honestly say *"I'm working with a buyer looking for a home to renovate in Capistrano Beach."* Keep it truthful and singular:
- Only make this claim once a **signed Buyer Representation Agreement (CAR form BRBC)** is in place.
- Say **"a buyer,"** never "buyers" or "several buyers." (See the standing rule against overpromising demand.)
- Never promise the owner a price, a fast close, or an all-cash deal we haven't confirmed the buyer can deliver.

### Telephone / text — TCPA + National Do Not Call (current as of 2026)
- **Scrub every phone number against the National DNC Registry before dialing.** Texts are treated the same as calls under DNC now.
- **No autodialer (ATDS), no prerecorded/robo voice, no mass texting tools.** The FCC one-to-one prior-express-written-consent rule (effective Jan 27, 2025) applies to those; we avoid the issue entirely by **manual, one-at-a-time dialing only.**
- A number **not** on the DNC list may be manually cold-called. A number **on** the DNC list may only be called if we have prior express written consent, or it's a past client within 18 months of the last transaction.
- **First-contact text messages must include Adam's license number** (CA requirement). Given the added TCPA text exposure, default to **no cold texting** — use mail and door first; text only a warm/consented contact.
- Honor any "stop / do not contact" immediately (must be within 10 business days; we do it same day) and log it as `do_not_contact` in leads.db.

### California DRE — license number on first-contact materials
Every first-point-of-contact piece (mailer, notecard, flyer, email, door-hanger) must show Adam's **8-digit DRE #02419464**, in a font **no smaller than the smallest font used elsewhere in the piece**, plus the responsible broker name (Pacific Sotheby's International Realty). This is the same 6-point disclosure standard in CLAUDE.md — name, DRE #, designation, brokerage equally prominent.

### CAN-SPAM (any email)
Honest subject line, real physical mailing address in the footer, working one-click opt-out honored promptly, no purchased/scraped lists blasted.

### Fair Housing (CA FEHA + federal)
We target the **property and its condition**, never the people. "Older home, deferred maintenance, high land value" is a property description and is fine. We never select, rank, or word outreach based on a protected class (race, religion, familial status, disability, national origin, sex, age, source of income). Estate/probate or long-tenure situations may be noted as *property situations*, but copy always speaks to the home, not the household.

### AB 723 — AI-altered images
If any mailer or flyer uses an AI-generated or AI-retouched image, it needs the AB 723 disclosure with a link to the unaltered original. Simple text notecards avoid this entirely — preferred here.

---

## 1. Define the target (what "teardown-worthy" means, in data)

We score candidates on property signals only. **We do not use ARM/loan-rate pressure as a ranking signal** (rejected approach). Signals, strongest first:

1. **High land-to-improvement value ratio** — from the OC Assessor, improvement value is a small fraction of land value. This is the single best teardown signal: the dirt is worth more than the house.
2. **Original / very old construction** — year built roughly pre-1965, especially original Capo Beach beach cottages never substantially rebuilt.
3. **Underbuilt lot** — small living area on a normal-or-large lot (room to expand, or a rebuild pencils out).
4. **Long ownership tenure** — 20+ years, often original owners; correlates with deferred maintenance.
5. **No recent permit activity** — no major remodel/addition permits on file for many years (Dana Point / county permit records).
6. **Visible condition** — confirmed by drive-by / street view: worn roof, dated exterior, overgrown, boarded, obvious deferred maintenance.
7. **Not currently listed** — no active/pending MLS status (Article 16 filter — mandatory).

A property should hit **several** of these, and #6 (visible condition) and #7 (not listed) are effectively required before it earns a contact.

---

## 2. Where the data comes from (PropStream is retired)

- **CRMLS** — pull all Capo Beach / Capistrano Beach parcels; identify what's currently active/pending (to *exclude*), and recent teardown/land sales as comps for the buyer.
- **FirstAm IgniteRE (title-pull skill)** — per-property owner, mailing address, tenure, and assessor value split. Draw the Capo Beach polygon, snapshot the row labels, then pull. This is our owner-of-record + equity/value source now.
- **OC Assessor / public records** — land vs improvement value, year built, lot size.
- **Dana Point / county permit records** — recency of major permits.
- **Drive-by / walking route** — Adam confirms condition in person; this is what turns a data candidate into a real target. (There's already a "Farming Walking Route" folder to extend.)
- **leads.db** — the master tracker; add a `capo_offmarket` tag/table so every candidate and touch is logged (owner, APN, signals, channel, date, outcome).

Workflow: build the raw parcel list from CRMLS + IgniteRE → score on the signals above → strip out anything currently listed → Adam drives the shortlist → the confirmed-condition homes become the outreach list.

---

## 3. Outreach sequence (lowest legal risk first)

Off-market sourcing lives on **mail and doors**, not cold calling. That's both the most compliant and, for luxury coastal owners, the most effective.

### Channel A — Direct mail notecard (primary)
Handwritten-style personal notecard, on-brand (SIR Blue / white, gold hairline divider, no black/gold backgrounds, max semibold, no underlines). One per owner, sent to the mailing address of record.
- Must carry: Adam Boehrer · DRE #02419464 · Real Estate Agent · Pacific Sotheby's International Realty · phone · email. DRE # no smaller than smallest font on the card.
- Voice: lead as a person, acknowledge the business reality once, no "no pressure / not selling" disclaimers, no em-dashes.

### Channel B — Door knock / in-person (primary, pairs with A)
Adam is already farming Capo Beach on foot. For homes he's confirmed by drive-by, a brief, respectful in-person intro is the highest-trust first contact. Leave the same compliant notecard if no answer.

### Channel C — Phone (secondary, tightly gated)
Only after: (1) number scrubbed against National DNC, (2) manual dial, no autodialer, (3) not on DNC or a qualifying exception. First-contact **text** avoided by default; if ever used, it must include the license number.

### Channel D — Email (tertiary)
Only where we have a legitimate email and a real reason; full CAN-SPAM footer (physical address + opt-out). Not a blast.

**Cadence:** Notecard → (7-10 days) door knock / follow-up card → optional compliant call. 2-3 touches max, then rest. Log every touch and every opt-out in leads.db.

---

## 4. Draft first-contact notecard (compliance-checked)

> Hi [Owner first name, or "neighbor" if no clean name],
>
> I'm a local agent here on the South OC coast and I'm working with a buyer who's looking for a home to renovate in Capistrano Beach. Your place came to mind as I've been getting to know the neighborhood.
>
> If you've ever wondered what your home might be worth today, or would consider a quiet, off-market sale to a buyer who wants to invest in the property, I'd genuinely welcome the conversation. No obligation on your end.
>
> Either way, it's a pleasure to be in the neighborhood.
>
> Adam Boehrer
> Real Estate Agent · Pacific Sotheby's International Realty
> DRE #02419464
> 949.541.8247 · adam.boehrer@pacificsir.com

Checklist for this piece: ✅ Name ✅ DRE # (size it ≥ smallest font) ✅ Designation ✅ Brokerage ✅ truthful single-buyer claim ✅ property-focused, not people-focused ✅ no em-dashes ✅ no overpromise. Add PSIR physical mailing address if used as an email.

---

## 5. Suggested next steps

1. Confirm the **signed Buyer Representation Agreement** is (or will be) in place before we make the "I'm working with a buyer" claim.
2. Confirm the buyer's real parameters: budget, cash vs financed, target lot size / rebuild vs remodel, timeline. This sharpens the target list and keeps the outreach honest.
3. I build the scored Capo Beach candidate list (CRMLS + IgniteRE title-pull), strip active listings, and hand you a drive-by shortlist.
4. You confirm condition on the ground; we finalize the outreach list and print compliant notecards.
5. Every candidate and touch logged in leads.db under a `capo_offmarket` tag.

---

## Sources (compliance verification, 2026-07-24)
- NAR — Telemarketing & Cold-Calling: https://www.nar.realtor/telemarketing-cold-calling
- REDX — Real Estate Agent's Guide to the DNC List / TCPA: https://www.redx.com/blog/agents-dnc-list-tcpa-guide/
- NAR — 2026 Code of Ethics & Standards of Practice: https://www.nar.realtor/about-nar/governing-documents/code-of-ethics/2026-code-of-ethics-standards-of-practice
- NAR — Case Interpretations Related to Article 16: https://www.nar.realtor/about-nar/governing-documents/code-of-ethics/case-interpretations-related-to-article-16
- Kimball Tirey & St. John — CA license number disclosure requirements: https://www.kts-law.com/license-number-disclosure-requirements-for-real-estate-agents-and-brokers/
- CA DRE — advertising / first-point-of-contact regulation (CCR §2773): https://regulations.justia.com/states/california/title-10/chapter-6/article-9/section-2773
