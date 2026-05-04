# Home Value Reports — Workflow

When a lead submits the home-value form on adamboehrer.com, the CMA notifier
emails Adam. This folder is where every CMA gets built, one folder per lead.

## End-to-end flow

```
Form submit on adamboehrer.com
  ↓ (Mailchimp tag SOURCE=cma)
notify_cma_submissions.py emails Adam
  ↓
python3 scripts/cma_kickoff.py "Smith" "187 Avenue La Cuesta, San Clemente, CA"
  ↓ (creates folder, pre-fills subject.md from title DB + market_metric)
Marketing/Home Value Reports/2026-05-04_smith_187-avenue-la-cuesta/
  ├── lead.json       intake fields + Mailchimp member id
  ├── subject.md      property facts pre-filled from leads.db
  ├── comps.yaml      skeleton — Adam fills from CRMLS
  ├── notes.md        Adam's narrative read on the property
  └── (report.pdf)    generated below
  ↓
Adam pulls 3-5 sold + 2-3 active comps from CRMLS, edits comps.yaml
Adam writes a 2-3 sentence read in notes.md
  ↓
python3 scripts/generate_cma.py 2026-05-04_smith_187-avenue-la-cuesta
  ↓
report.pdf — 2 pages, Sotheby's branded
  ↓
Adam emails personally, replies in the same Gmail thread the notifier started
```

## Per-lead folder layout

| File | Who fills it | Purpose |
|---|---|---|
| `lead.json` | kickoff script | intake fields, Mailchimp member id, kickoff timestamp |
| `subject.md` | kickoff script | property facts (sqft, beds, baths, last sale, market snapshot for the city) |
| `comps.yaml` | Adam (from CRMLS) | sold + active comps, adjustments |
| `notes.md` | Adam | the "read" — paragraph that ends up in the report narrative |
| `report.pdf` | generate script | final deliverable |

## comps.yaml schema

```yaml
sold_comps:
  - address: "172 Avenida La Cuesta, San Clemente, CA 92672"
    sold_date: "2026-04-15"
    sold_price: 1450000
    list_price: 1495000
    beds: 3
    baths: 2
    sqft: 1500
    lot_sqft: 7500
    year_built: 1958
    dom: 12
    distance_mi: 0.3
    notes: "Renovated kitchen, comparable lot"

active_comps:
  - address: "201 Calle Cuervo, San Clemente, CA 92672"
    list_price: 1599000
    list_date: "2026-04-01"
    beds: 3
    baths: 2
    sqft: 1480
    lot_sqft: 7800
    year_built: 1960
    dom: 33
    distance_mi: 0.5
    notes: "Original condition, priced ambitiously"

adjustments:
  notes: |
    Subject is smaller than the sold-comp average (1401 vs 1500 sqft),
    so we pull the midpoint down ~3%. Subject lacks the kitchen reno
    seen in comp #1, so we discount that one further.
```

## Value range math (in generate_cma.py)

1. Compute weighted $/sqft of sold comps
   - Weight = recency (newer = higher) × proximity (closer = higher)
2. Multiply subject sqft → midpoint
3. Low / High = midpoint ± 4%
4. Round all to nearest $5,000
5. Active comps shown for context but not used in the math

## Naming convention

Folder name: `YYYY-MM-DD_lastname_address-slug`
- date = kickoff date (not submit date)
- lastname = lowercase
- address-slug = first line of street address, lowercase, hyphens

Example: `2026-05-04_smith_187-avenue-la-cuesta`
