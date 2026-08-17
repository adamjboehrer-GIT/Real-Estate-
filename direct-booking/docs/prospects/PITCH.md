# Pitching the three San Clemente owners

Three demo sites, three owners, one conversation each. Research and sourcing:
`RESEARCH.md`. Owner economics regenerate with `node scripts/pitch-math.mjs`
against a running dev server.

---

## Before you open your mouth

**These people have not been contacted and have not agreed to anything.** Their
photos and their listing copy are on these pages because that is the only way to
show someone what their own site would look like. Same posture as the Bella
Vista demo:

- Every property is `draft`, every page is `noindex`, every URL is unlisted.
- Do not send a link to anyone but the owner it belongs to.
- If an owner says no, delete their seed, their photos and their copy file.
- No site takes a real booking. There is no payment path wired.

**Do not pitch this as a way to get more bookings.** It is not one, and Pete and
Cathy in particular will know it is not one inside of a sentence. The pitch is
narrow and it is true: the guests who already know you should not cost you 14%.

---

## The one number that matters

Not the percentage. The **break-even count** — how many direct bookings a year it
takes to clear the $1,000 subscription. Everything else is decoration.

| Owner | Owner gains per 4-night booking | Break-even |
|---|---|---|
| Shannon — Starfish | **+$103.48** | **10 bookings a year** |
| Pete & Cathy — The Balcony on Del Mar | **+$87.10** | **12 bookings a year** |
| Aneta — Garden Cottage at the Green | **+$45.36** | **23 bookings a year** |

It gets better with length, because the fee split hands more to the guest as the
stay grows and the owner's absolute gain still rises:

| | 3 nights | 4 nights | 7 nights | 14 nights |
|---|---|---|---|---|
| Starfish | +$109.59 → 10/yr | +$103.48 → 10/yr | +$125.36 → 8/yr | +$176.35 → 6/yr |
| Del Mar | +$92.24 → 11/yr | +$87.10 → 12/yr | +$105.53 → 10/yr | +$148.54 → 7/yr |
| Garden Cottage | +$48.05 → 21/yr | +$45.36 → 23/yr | +$55.01 → 19/yr | +$77.43 → 13/yr |

Both sides win at every length. The guest saves $57 to $582 depending on the
property and the stay; the owner nets more than Airbnb pays him in every single
row above. That is the whole argument and it does not require anybody to lose.

Airbnb's cut is deducted from his payout and Stripe's cut is deducted from ours,
and those two roughly cancel. The gain is entirely the 14% guest fee that
currently goes to Airbnb and, under the split, partly comes back to him.

---

## Pete & Cathy — the one to get

**Lead with:** six listings, about 2,300 reviews, nothing below 4.98. One yes is
six subscriptions, not one. They are the highest-value conversation on the list
by a distance.

**Open with the observation, not the product.** Something like: their 400-review
listing is the highest-rated place in San Clemente, and a decade of guests means
most of their bookings are people who already knew about them before they opened
the app. Ask what fraction of their bookings are repeats. Whatever number they
say is the size of the problem.

**Expect the software objection.** Their photos come through Airbnb's
professional-host API, so they are already paying for a channel manager. Ask
which one in the first five minutes. If it bundles a direct-booking page, that is
the real competitor, and the honest answer is that this is cheaper ($1,000/yr
against $100+/month) and the page is theirs rather than a template. If they are
not using its booking page, ask why not.

**Their break-even is 12 bookings a year across a portfolio doing hundreds.**
Say that out loud.

---

## Shannon — the best economics

**Lead with:** her calendar. Airbnb flags the listing "rare find, this place is
usually booked," and it was solid through late October when this was pulled. She
is not short of demand, which is exactly why the 14% is worth recovering rather
than spent on being found.

Highest rate of the three and the best per-booking gain. Break-even is 10
bookings a year.

She has at least one other unit and her own copy says "ask about our other
units," so treat this as a two-property conversation from the start.

---

## Aneta — the honest one

**Lead with the photos, not the pitch.** Hers are noticeably older and lower
resolution than the other two prospects', and that is free, useful, unsolicited
advice that costs her nothing to hear. It opens a conversation better than a
product does.

**Then be straight about the economics.** Her nightly rate is about a third of
the others', so 14% of it is a smaller number and the break-even is 23 direct
bookings a year. At roughly 38 reviews a year she is plausibly doing 55 to 75
bookings, so 23 is reachable, but it is not the easy yes the other two are. If
she is mostly booking two- and three-night stays it gets harder, not easier.

Do not oversell it. If the math does not work for her, say so. The 230 reviews
say she runs a good place, and a good place that says no this year is worth more
as a warm relationship than as a bad fit.

---

## What to fix before any of these go live

These are demos. Everything below is a placeholder that has to become real
before a property leaves `draft`:

- **The cleaning fee is an estimate** on all three. Airbnb stopped showing it
  separately, so it was solved out of the all-in total. It is the free variable
  in the pricing arithmetic and the cheapest thing to make exact.
- **Summer and holiday rates are extrapolated.** Only fall and early winter are
  anchored to real Airbnb quotes, because the calendars only open about four
  months out. Aneta's has one anchor, not two.
- **Verify San Clemente's 10% TOT** with City Finance before taking any money.
  Municode blocks automated fetching so nobody has read the ordinance directly.
  Under-collecting means the owner pays the shortfall.
- **Get each owner's STR permit number.** San Clemente requires it in
  advertising; the footer currently reads "permit pending".
- **Get the Airbnb iCal export URL.** Host dashboard → Calendar → the listing →
  Availability → Connect calendars → Export. It cannot be derived from the public
  listing. Until it exists the calendars are hand-seeded and going stale, and the
  seeded `manual` blocks must be deleted the day a feed connects or the two will
  fight.
- **Pet fees are modelled per stay, not per night.** Pete and Cathy charge
  $20/night per pet and Aneta charges $30/day. The seeded figure is right for a
  four-night stay and wrong for every other length.
- **Photos and copy are theirs.** Swap in their originals, and let them rewrite
  the prose. It is a draft written in their voice from their own listing, which
  is a useful thing to hand someone and a terrible thing to publish unread.
