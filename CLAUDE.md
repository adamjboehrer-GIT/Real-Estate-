# Real Estate AI Lead Generation System

## Project Overview

An AI-powered lead generation and CRM system built for Adam Boehrer (Sotheby's International Realty, San Clemente, CA) and his business partner Christian. The goal is to systematically identify, track, and convert quality buyers and sellers in coastal Southern California real estate markets using AI-assisted data analysis and outreach optimization.

This is not a mass-blast marketing tool — it is a precision targeting system designed to identify the most ready, most qualified buyers and sellers and reach them through the right channels with the right message.

---

## Team

- **Adam Boehrer** — Licensed real estate agent at Sotheby's International Realty, San Clemente, CA. Primary operator. Non-technical but proficient with Claude Code.
- **Christian** — Business partner. Also non-technical but understands Claude Code. Collaborates on strategy and data.

Both are non-engineers. Claude Code is the primary technical operator for this system.

---

## Target Markets

**Primary focus — Coastal Southern California:**
- Newport Beach
- Laguna Beach
- Dana Point
- San Clemente
- Oceanside
- Carlsbad
- San Diego

**Price range:** $1M–$5M (bulk of deals). Always looking to scale upward.

---

## Data Sources

### PropStream
- **Access:** Portal login only. No API access available on current plan.
- **Usage:** Primary bulk data source. Filter and export CSV files manually, then ingest into SQLite database via ingestion script.
- **Key fields available:** Owner name, mailing address, property address, estimated equity, loan origination date, loan type (ARM vs fixed), years owned, estimated property value, cash buyer flag, phone number, email (when available).
- **Export limits:** Check current plan limit in Account Settings → Export Credits. Limits vary by plan (2,000–10,000+/month).
- **Workflow:** Adam/Christian set filters in PropStream → export CSV → drop in `/data/imports/` folder → ingestion script loads into SQLite with deduplication.

### First American Title
- **Access:** Portal login (specific portal TBD — need to confirm with Sotheby's office or title rep which portal they use: FastWeb, TitleWave, or AgentNet).
- **Usage:** Cross-reference owner contact info, lien history, transfer history. Supplements PropStream data.
- **Status:** Portal identification still pending.

### MLS (CRMLS)
- **Access:** Adam's licensed agent credentials.
- **Usage:** Property research, looking up specific listings, deal analysis.

### First American IgniteRE
- **Access:** Adam's licensed agent credentials. OAuth via login.firstam.com.
- **Usage:** Draw-polygon farming tool → per-property title reports (owner, vesting, APN, sale/loan history, tax info). Playwright automation validated 2026-04-21 — DOM-based extraction from the PDF.js textLayer (no PDF download needed).
- **Workflow:** Navigate to properties.ignitere.firstam.com/Polygon/MapSearch → draw polygon → click each property in the list → click Property Detail → wait for green ready arrow → click arrow → extract textLayer → upsert to SQLite + write markdown → back → back → reopen list → next.

---

## Tech Stack

### Database
- **SQLite** — Single `.db` file stored directly in the repo. No external software or server required. Claude Code reads and writes directly. This is the master data store for all contacts, properties, interactions, and campaign performance.

### Working CRM
- **Google Sheets** — Collaborative working layer for Adam and Christian. Synced from SQLite. Active leads, outreach status, deal notes. Keep to 500–2,000 rows max at any time (working pipeline only, not full database).
- **Setup needed:** Google Cloud project, Sheets API + Drive API enabled, service account credentials (JSON key file), Sheet shared with service account email.

### Outreach
- **Cold outreach (new leads):** Instantly.ai or Smartlead.ai — built for cold email at scale with domain warming. NOT Mailchimp/Beehiiv for cold contacts.
- **Newsletter (opted-in):** Beehiiv — for brand-building content once contacts have opted in. Free up to 2,500 subscribers.
- **Other channels:** Direct mail flyers (already active in San Clemente), cold calling, geo-fenced ads, in-person visits, word of mouth.

### MCP Servers
- **Playwright MCP** — Available. Use for assisted browsing, research, and automation of portal workflows (e.g., PropStream exports, FirstAm IgniteRE property detail extraction).
- **Google Sheets MCP** — To be configured once Google Cloud service account credentials are ready.

### Skills
- **`/title-pull`** — Canonical workflow for pulling FirstAm IgniteRE Property Detail reports for a range of properties in a drawn polygon. Adam invokes by typing `/title-pull` (or saying "title-pull", "pull titles", etc). On invocation, the skill opens a Playwright browser to the FirstAm IgniteRE MapSearch URL; Adam then logs in, draws the polygon, and replies "ready". The skill then asks Adam for the property-number range (e.g., "1 to 10"); Adam responds with the range; the skill loops continuously through that range. The skill handles: clicking each row, triggering Property Detail generation, retrying on Temporary Error, extracting the PDF.js textLayer, piping through `scripts/ingest_firstam_property.py`, writing SQLite rows + per-property markdown to `Title Database/`, and clicking back through to the next property. Full procedure at `.claude/skills/title-pull/SKILL.md` — always follow that exactly; do not invent a new procedure from scratch for this workflow.

---

## Current Active Deals (as of project start)

1. **Price-reduced coastal properties** — San Clemente and Dana Point homes where market shift has brought price/sqft to below-market levels. Good value play. Target buyers: move-up buyers already in South OC with high equity, or cash buyers relocating to coastal CA.

2. **ARM/balloon payment motivated seller** — Property purchased in 2021 at low interest rates. Likely adjustable-rate mortgage with balloon payment due ~year 5. Seller has set high price but is likely highly motivated — strong negotiating leverage. Target buyers: cash buyers and investors who specifically look for motivated seller situations and can move fast.

3. **Two off-market deals** — Details TBD. Off-market deals require relationship-driven outreach, not mass email. Target through personal network, Sotheby's colleague network, and title rep relationships.

---

## Buyer & Seller Targeting Logic

### Quality Buyer Signals (to be refined over time)
- Cash buyer flag in title/PropStream data
- Prior purchases in coastal CA markets ($1M+ range)
- Active searchers with high equity in current home (move-up potential)
- Out-of-state owners with CA coastal interest
- Repeat investors with 3+ closed transactions

### Quality Seller Signals
- 5+ years ownership with high equity position
- ARM loans originated 2020–2022 (balloon payment pressure)
- Life events (divorce, estate, job relocation) — surfaced through title data
- Absentee owners in target geographies
- Long tenure + high equity + no recent refinance activity

### Outreach Performance Tracking
Every outreach action should be logged with: channel, contact ID, date, message type, outcome. Over time this data trains the targeting model — doubling down on what works, stopping what doesn't.

---

## Data Schema (Planned)

**Core tables:**
- `contacts` — All leads (buyers + sellers) with source, contact info, property info, score
- `properties` — Active and watch-list properties with deal type and status
- `interactions` — Every outreach touchpoint logged (channel, date, outcome)
- `campaigns` — Newsletter, cold email, and direct mail campaigns with performance metrics
- `signals` — Flags and scoring data that inform targeting (equity, loan type, tenure, etc.)

---

## Key Decisions & Constraints

1. **PropStream CSV → SQLite** is the primary data pipeline. Simple, compliant, scalable within plan limits.
2. **FirstAm IgniteRE textLayer → SQLite + per-property markdown** — automated property-detail extraction from the PDF.js preview DOM. No PDF download needed. Lands in `database/leads.db` and `Title Database/*.md`.
3. **Google Sheets is the working CRM** — Not a replacement for SQLite. It's the collaborative interface layer.
4. **Precision over volume** — Sotheby's brand is luxury. System should identify 12 perfect buyers, not blast 10,000 people.
5. **Feedback loop is the core asset** — Every closed deal, every response, every unsubscribe gets logged and fed back to improve targeting. This is what compounds over time.
6. **Seller side is high leverage** — Listings give control. The seller identification system (ARM holders, high equity, long tenure) may produce revenue faster than the buyer side.

---

## Setup Checklist (Pending)

- [ ] Confirm PropStream monthly export credit limit
- [ ] Identify First American portal (FastWeb / TitleWave / AgentNet)
- [ ] Set up Google Cloud project and enable Sheets + Drive APIs
- [ ] Create service account and download JSON credentials
- [ ] Configure Google Sheets MCP server
- [ ] Create master Google Sheet and share with service account
- [ ] Select and configure cold email platform (Instantly.ai recommended)
- [ ] Set up Beehiiv account for newsletter
- [ ] Initialize SQLite database with schema
- [ ] Write PropStream CSV ingestion script
- [ ] Define "quality buyer" and "quality seller" scoring criteria in writing
- [ ] Get details on the two off-market deals

---

## Working Directory Structure

```
/
├── CLAUDE.md                  # This file
├── database/
│   └── leads.db               # SQLite master database
├── data/
│   └── imports/               # Drop PropStream CSV exports here
├── scripts/
│   ├── ingest_propstream.py            # CSV → SQLite ingestion + dedup
│   ├── ingest_firstam_property.py      # FirstAm textLayer dict → SQLite + markdown
│   ├── migrate_add_firstam_columns.py  # Idempotent schema migration
│   ├── sync_sheets.py                  # SQLite → Google Sheets sync
│   └── score_leads.py                  # Lead scoring logic
├── outreach/
│   └── templates/             # Email and messaging templates
├── reports/                   # Campaign performance reports
├── Title Database/            # Per-property markdown docs from FirstAm IgniteRE
└── Newsletter/
    ├── NEWSLETTER_GUIDE.md    # Process guide and brand standards
    └── issues/                # One HTML file per issue, named YYYY-MM-DD_issue-##.html
```
