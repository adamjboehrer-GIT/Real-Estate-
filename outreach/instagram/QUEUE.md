# Instagram Queue — @adamonthecoastoc

The approval gate. Every post lands here as a draft. Nothing publishes until Adam
approves it by name.

**How to use this file:** read the caption, look at the frames, check the review
flags. Then either say "approve `<slug>`" or tell me what to change. Approving
runs `scripts/ig_publish.py --slug <slug>`, which refuses anything still marked
draft or with the compliance check unwalked.

Newest week on top. Posted items move to `posted/`.

Statuses: `DRAFT` → `APPROVED` → `POSTED`, or `REJECTED` / `SKIPPED`.

---

## Nothing queued yet

Run `/ig-content` to build the week. It needs a current CRMLS Agent 1-Line export
in `data/imports/mls_comps/` first (Actives + Closed, San Clemente, Residential).
The newest actives export on file is from July, so the first run will ask for a
fresh one before it will publish a deal claim.

---

<!--
Template for each entry:

## YYYY-MM-DD · Deal of the Week
**slug:** `2026-08-15-deal-of-the-week`
**status:** DRAFT
**frames:** outreach/instagram/assets/2026-08-15-deal-of-the-week/{01_hook,02_numbers,03_method}.jpg
**source:** ig_deal_of_week.py, SC actives 2026-08-13 vs 8 closed comps in SN area
**review flags:**
- discount over 25% usually means view, condition, or lot
- built 1965, condition likely explains part of the gap

> caption goes here verbatim, exactly as it will post

-->
