@AGENTS.md

# Direct Booking Platform

A direct booking website for short-term rental owners who currently take bookings
through Airbnb. The site captures repeat and referral guests so the owner keeps
the ~15% OTA cut on bookings they earned themselves.

It is **not** a guest acquisition channel and must never be built or pitched as
one. The pitch is: the guests who already know you should not cost you 15%.

Build spec: `docs/build-spec-v1.md`. Adam is the operator; owners are onboarded
manually through the admin panel. There is no self-serve signup.

**Multi-tenant and nationwide from day one.** Each property gets its own branded
site, and properties are not assumed to be in any one city or state. Nothing
about a jurisdiction may be hardcoded — see the tax section below, which is where
this constraint bites hardest.

**This is a separate business from the Sotheby's lead-gen work in the parent
repo.** No shared data, no shared contacts, no Sotheby's branding. The parent
`CLAUDE.md` brand and DRE-compliance rules govern Adam's California real estate
collateral; they do not apply to a property site, which carries the property
owner's identity, not Adam's.

---

## Demo property

Adam's own lakefront home in **Bella Vista, Arkansas**. Because he owns it, there
is no client-permission question about photos or copy, and the demo doubles as a
live site he actually benefits from.

Note that Bella Vista is also the subject of Adam's personal investing project at
`~/Desktop/Bella Vista Investing/`, which is deliberately kept separate from the
Sotheby's work. This repo sits inside the Sotheby's repo for convenience; do not
let that leak Sotheby's branding, contacts, or the CA real estate identity onto
an Arkansas property site.

Bella Vista specifics confirmed 2026-08-10:
- The city requires an STR permit, renewed annually, **posted visibly at the
  property**. Cap of 600 non-owner-occupied STR units citywide.
- Lodging tax is a five-line stack — see below.

---

## Conventions that will bite you if you ignore them

**Money is integer cents.** Every column and field named `*_cents` is an integer
number of US cents. Never a float, never dollars. Rounding happens once per line
item, in `calculateQuote`. See `src/lib/money.ts`.

**Date ranges describe NIGHTS, inclusive on both ends.** A stay arriving Aug 3
and departing Aug 10 occupies nights Aug 3 through Aug 9 and is stored as
`start_date = 2026-08-03, end_date = 2026-08-09`. The departure date is not
blocked — the next guest checks in that morning.

iCal does the opposite: `VEVENT DTEND` is **exclusive**. The conversion
(`end_date = DTEND - 1 day`) happens in exactly one place, the iCal parser, and
nowhere else. Getting this wrong either strands a sellable night on every
turnover or double-books one.

The exception is `bookings.check_in` / `check_out`, which hold the literal
arrival and departure dates a guest would recognize, because those appear on
confirmations.

**Dates are `YYYY-MM-DD` strings, not `Date` objects.** `new Date('2026-08-03')`
parses as UTC midnight, which is Aug 2 in California. All date arithmetic goes
through `src/lib/dates.ts`, which works in UTC and has no DST to trip over.

**`calculateQuote` is pure.** No database, no network, no clock. The current date
is passed in via `today`, sourced from `todayInTimeZone()` at the call site. This
is what makes the tax and deposit arithmetic testable.

---

## Lodging tax is a stack, never a single rate

This is the single most jurisdiction-dependent part of the system, and the
easiest thing to get quietly, expensively wrong — a wrong rate means the owner
under-remits and eats the difference.

Taxes live in the `tax_rates` table, one row per levy, each with its own rate,
its own base, and its own remitting authority. Compare:

| Property | Lines | Combined |
|---|---|---|
| San Clemente, CA | 10% city TOT | 10% |
| Bella Vista, AR | 6.5% state sales + 2% state tourism + 1% Benton County + 2% city sales + 2% city A&P | ~13.5% |

Rules that fall out of this:

- **Each line rounds independently.** The owner files A&P with the city and
  everything else with Arkansas DFA; each return must carry a whole-cent figure
  that reconciles to what the guest paid. Summing rates and rounding once breaks
  that by a cent or two.
- **The taxable base differs by jurisdiction.** Arkansas and San Clemente both
  tax cleaning fees; many places tax room rent only. Hence `tax_base`.
- **Rates are entered per property during onboarding, verified against the
  taxing authority — never inferred from the address.**
- **Show every line to the guest, named.** "Arkansas State Sales Tax 6.5%" is
  comprehensible in a way a bundled "Taxes and fees" row is not. That
  transparency is the pitch against Airbnb.

**Max stay is 29 nights, not the spec's 30.** The 30-day boundary recurs across
US jurisdictions: San Clemente defines short-term lodging as "29 or fewer
consecutive days" (SCMC 17.28.292); Arkansas assesses lodging tax on stays "of
less than 30 days", and Bella Vista's A&P ordinance uses the same wording. Past
that line the tax treatment changes and the guest may begin acquiring tenancy
rights. 29 is the safe national default, overridable per property.

**Minimum stay is determined by the arrival night's rate period**, matching
Airbnb, VRBO and every channel manager. Owners already reason about minimum stays
this way from their Airbnb calendar.

---

## Deliberate deviations from the build spec

| Spec | Built | Why |
|---|---|---|
| Next.js 15 | Next.js 16 | 16 was current at build start; same App Router and server components. Next 16 needs `next typegen` before `tsc --noEmit` passes — it generates the `LayoutProps`/`PageProps` globals. |
| `properties.tot_rate` single rate | `tax_rates` table | A single percentage models California TOT and nothing else. See above. |
| `properties.ical_import_urls` jsonb | `ical_feeds` table | §7 requires alerting after three consecutive failures, which needs durable per-feed state. A jsonb blob can't carry that, and `blocked_dates.feed_id` needs something to point at. |
| `stripe_connect_account_id` on both `properties` and `owners` | `owners` only | Two places to store the same value means two answers to "who gets paid". |
| Max stay 30 nights | 29 | See above. |
| Design skill at `/mnt/skills/public/...` | Local design skills | That path is from a different environment and does not exist here. The §11 constraints still apply. |

---

## Commands

```
npm run dev              # local dev server
npm test                 # vitest, run once
npm run test:watch       # vitest, watch mode
npm run typecheck        # next typegen && tsc --noEmit
./scripts/validate-schema.sh   # apply migrations to a throwaway local Postgres
```

`validate-schema.sh` needs `postgresql@17` (installed via Homebrew and running as
a service). Stop it with `brew services stop postgresql@17` if it is not wanted
in the background.

---

## Load-bearing decisions worth not relitigating

**Request-to-book, not instant book.** iCal sync from Airbnb lags 15 minutes to
3 hours. That window is long enough to sell the same week twice, and a double
booking on the first property ends this business. Revisit only after calendar
truth moves into a channel manager.

**Dates are blocked only after money moves**, at the payment webhook — never on
request. Holding dates on request strands inventory.

**Guest funds never touch Adam's accounts.** Stripe Connect Standard; payments
settle to the owner's own account. Adam holds a California DRE license, and
handling guest funds starts to look like property management and trust-fund
handling. Platform revenue comes out as `application_fee_amount` or a separate
subscription invoice. This holds even when the owner is Adam himself — the demo
property should still be onboarded as a normal connected account, because the
demo is meant to prove the real flow.

**The outbound iCal feed is not optional.** `/api/properties/[slug]/calendar.ics`
publishes direct bookings so the owner can import it into Airbnb and block those
dates there. Set it up on day one — it's how the double booking gets prevented
from the other side.

**The `guests` table is the actual product.** Every booking upserts into it. It's
the asset the owner is really buying, and it must stay clean enough to export.

---

## Open items

- [ ] **Confirm the Bella Vista tax stack against Arkansas DFA's lodging tax
      lookup and the Bella Vista A&P Commission before taking a real booking.**
      Sources disagree on the city sales tax component (1% vs 2%), and the 1%
      state short-term-rental tax needs verifying. The seeded values are a
      starting point, not authoritative.
- [ ] Get Adam's Bella Vista STR permit number — must be displayed on the site
      and posted at the property.
- [ ] Airbnb iCal export URL for the lakefront home (Calendar → Availability →
      Connect calendars → Export). Single most important thing to obtain.
- [ ] Photos, nightly rates by season, min-stay rules, cleaning and pet fees.
- [ ] Supabase project credentials, then run `supabase/migrations/0001_init.sql`.
- [ ] Resend account and verified sending domain.
- [ ] Confirm the advertising-disclosure language in SCMC 17.28.292 before any
      *California* property site goes public. Municode blocks automated fetching,
      so this needs a human read or a call to Planning at (949) 361-6197. Not
      blocking for Arkansas.
