@AGENTS.md

# Direct Booking Platform

A direct booking website for short-term rental owners who currently take bookings
through Airbnb. The site captures repeat and referral guests so the owner keeps
the ~15% OTA cut on bookings they earned themselves.

It is **not** a guest acquisition channel and must never be built or pitched as
one. The pitch is: the guests who already know you should not cost you 15%.

Build spec: `docs/build-spec-v1.md`. Adam is the operator; owners are onboarded
manually through the admin panel. There is no self-serve signup.

**This is a separate business from the Sotheby's lead-gen work in the parent
repo.** No shared data, no shared contacts, no Sotheby's branding. The parent
`CLAUDE.md` brand and DRE-compliance rules govern Adam's real estate collateral —
they do not apply to a client's property site, which carries the client's identity,
not Adam's.

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

## Verified facts — do not re-guess these

**San Clemente TOT is 10%**, confirmed 2026-08-10 against the city:
https://www.sanclemente.gov/412/Transient-Occupancy-Taxes-TOT
It applies to all charges including cleaning fees, not to rent alone. STLU
operators file **quarterly**. Stored per-property (`properties.tot_rate`) because
this is multi-tenant and Dana Point, Oceanside and Carlsbad differ — verify each
new city against its own code before activating a property.

**Max stay is 29 nights, not 30.** San Clemente defines short-term lodging as
"29 or fewer consecutive days" (SCMC 17.28.292). The build spec says 30; the spec
is wrong. 30+ days also starts to create tenancy rights.

**Minimum stay is determined by the arrival night's rate period**, matching
Airbnb, VRBO and every channel manager. The owner already reasons about minimum
stays this way from their Airbnb calendar.

---

## Deliberate deviations from the build spec

| Spec | Built | Why |
|---|---|---|
| Next.js 15 | Next.js 16 | 16 was current at build start; same App Router and server components. Note Next 16 needs `next typegen` before `tsc --noEmit` passes — it generates the `LayoutProps`/`PageProps` globals. |
| `properties.ical_import_urls` jsonb | `ical_feeds` table | §7 requires alerting after three consecutive failures, which needs durable per-feed state. A jsonb blob can't carry that, and `blocked_dates.feed_id` needs something to point at. |
| `stripe_connect_account_id` on both `properties` and `owners` | `owners` only | Two places to store the same value means two answers to "who gets paid". |
| Max stay 30 nights | 29 | See above. |

---

## Commands

```
npm run dev         # local dev server
npm test            # vitest, run once
npm run test:watch  # vitest, watch mode
npm run typecheck   # next typegen && tsc --noEmit
```

---

## Load-bearing decisions worth not relitigating

**Request-to-book, not instant book.** iCal sync from Airbnb lags 15 minutes to
3 hours. That window is long enough to sell the same week twice, and a double
booking on the first client ends this business. Revisit only after calendar truth
moves into a channel manager.

**Dates are blocked only after money moves**, at the payment webhook — never on
request. Holding dates on request strands inventory.

**Guest funds never touch Adam's accounts.** Stripe Connect Standard; payments
settle to the owner's own account. Adam holds a California DRE license, and
handling guest funds starts to look like property management and trust-fund
handling. Platform revenue comes out as `application_fee_amount` or a separate
subscription invoice.

**The outbound iCal feed is not optional.** `/api/properties/[slug]/calendar.ics`
publishes direct bookings so the owner can import it into Airbnb and block those
dates there. Set it up with the client on day one — it's how the double booking
gets prevented from the other side.

**The `guests` table is the actual product.** Every booking upserts into it. It's
the asset the owner is really buying, and it must stay clean enough to export.

---

## Open items

- [ ] Confirm the exact advertising-disclosure language in SCMC 17.28.292 before
      any property site goes public. Municode blocks automated fetching, so this
      needs a human read or a call to Planning at (949) 361-6197. We display the
      permit number regardless, which is conservative either way.
- [ ] Get the client's Airbnb listing URL — everything about the demo content
      depends on it.
- [ ] Supabase project credentials, then run `supabase/migrations/0001_init.sql`.
- [ ] Resend account and verified sending domain.
- [ ] Demo stays on a Vercel preview URL with `noindex` and no custom domain
      until the owner agrees to the pitch. Their listing photos are theirs.
