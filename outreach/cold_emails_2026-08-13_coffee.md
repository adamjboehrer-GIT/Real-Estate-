# Outreach Round 2 — "Coffee On Me"

Generated 2026-08-13. Relational, low pressure, no listing ask. Nothing sends automatically.

**The position:** every other Realtor email in the inbox is asking for a transaction. This one asks
for a question. The only thing being offered is access to someone who knows the coast, and a cup of
coffee. That is a small enough ask that answering it costs nothing, which is the point.

Low pressure comes from the size of the ask, not from saying "no pressure." No disclaimers in the
copy.

---

## The list

Built by `scripts/build_send_list.py --write --date 2026-08-13`, deduped by address, exclusions
applied by address rather than by row.

| | Count |
|---|---|
| Contact rows with an email | 1,252 |
| Distinct addresses | 1,233 |
| Blocked (52 bounced in round 1, 4 opted out) | 56 |
| Already responded, handled by hand | 1 |
| **Version A · never emailed** | **517** |
| **Version B · emailed Jun/Jul, no reply** | **659** |
| **Total sendable, before verification** | **1,176** |

Cities: San Clemente 838, Capistrano Beach 327, Dana Point 10, Riverside 1.

Send `outreach/verify_list_2026-08-13.csv` to the bounce checker first. See
`VERIFICATION.md` in this folder for where and what to do with the file that comes back.

---

## Greetings

Only 396 of the 1,176 rows have a usable first name. The rest are trusts, LLCs, and vesting strings
that do not parse into anything you would say out loud, so they get a neighborly opener instead.

| Version | By name | Neighborly opener |
|---|---|---|
| A | 170 | 347 |
| B | 226 | 433 |

Named rows open `Hi {{name}},`. The rest rotate between `Hi neighbor,` and `Hello, neighbor!` so the
no-name batch does not read as one identical blast. Same rotation round 1 used.

`{{city}}` is the property city: San Clemente, Capistrano Beach, or Dana Point.

---

## Signature + opt-out (every send)

Name, DRE #02419464, REALTOR® designation, brokerage, and office address are carried by the Outlook
footer image. That satisfies the disclosure requirement.

The opt-out goes in as **live text, last line before the footer image.** Not inside the image.
Outlook and Gmail block remote images by default, and an opt-out nobody can read is an opt-out that
does not count.

```
Don't want to hear from me again? Reply "stop" and I'm gone for good.
```

No images in the body, so no AB 723 disclosure applies. Copy describes the neighborhood and the
work, never the people, so fair housing is clean.

---

## Version A · never emailed (517)

**Subject:** coffee?

> Hi {{name}},
>
> I'm a Realtor in {{city}}, so the last email you got from someone like me was probably about
> selling your house.
>
> This is not that.
>
> I've worked this coast long enough to be genuinely useful on it, and most of that has nothing to
> do with a transaction. What your place is actually worth today. Whether a remodel pays you back or
> just costs you a summer. What your street has done over the last year while nobody was watching.
>
> All of it is useless to you right up until the day it isn't.
>
> So if there's a real estate question rattling around in the back of your head, buying, selling,
> renting, refinancing, or just curiosity, I'd like to be the person you bring it to.
>
> Coffee is on me. A phone call if that's easier.
>
> And if nothing's on your mind, that's the best answer there is. I'll be around either way.
>
> Best,
>
> Adam
>
> Don't want to hear from me again? Reply "stop" and I'm gone for good.

**Subject alternates:** `coffee is on me` · `a question you've been sitting on` · `the Realtor email that isn't about selling`

---

## Version B · emailed in June, no reply (659)

Round 1 told them I had buyers waiting for a home in their neighborhood. Owning that opener is
better than pretending it never happened, and it earns the second read.

**Subject:** I owe you a better email

> Hi {{name}},
>
> I sent you a note back in June about buyers looking in your neighborhood. Very Realtor of me. You
> didn't reply, which is fair.
>
> Here's the email I should have sent instead.
>
> I've worked this coast long enough to be genuinely useful on it, and most of that has nothing to
> do with a transaction. What your place is actually worth today. Whether a project pencils before
> you start it. What your street has done over the last year while nobody was watching.
>
> If a question like that has been rattling around, I'd like to be the person you bring it to.
>
> Coffee is on me. A phone call if that's easier.
>
> And if nothing's on your mind, that's the best answer there is. I'll be around either way.
>
> Best,
>
> Adam
>
> Don't want to hear from me again? Reply "stop" and I'm gone for good.

**Subject alternates:** `round two, better email` · `let me try that again` · `coffee, and I'll skip the pitch this time`

---

## Optional P.S. (Version A only)

> P.S. I write a short local market note every couple of weeks called Coastal Currents. Nothing
> salesy, just what's actually happening on the coast. https://adamboehrer.com if you want it.

On Version A it turns a non-reply into a subscriber, which is the second-best outcome available.
Leave it off Version B, where it competes with the apology and muddies a clean close.

---

## Send mechanics

Same rails as the June round, which is where the 52 bounces and the throttling lesson came from.

1. Verify the list first. That alone should remove most of what would bounce.
2. Send from the Pacific Sotheby's Outlook address, individually, **3 minutes apart**, in small
   batches spread across the day. Tight spacing throttled hard around 150/day in June.
3. Watch the NDR bounces. A closed compose window is not proof of delivery.
4. Any reply containing "stop" gets set to `do_not_contact` same day.
5. Log every send with `scripts/log_resident_sends.py` under campaign `camp-coffee-2026-08` so
   round 3 can segment off this one.

At 3-minute spacing and roughly 150/day, 1,176 sends is about 8 working days. Version B first: they
have seen your name once, so they are the warmer half and the faster read on whether this angle works.

---

## Note on the "You Shouldn't Sell Your House" draft

`cold_emails_2026-08-12_dont-sell.md` was written but never sent, so nothing has gone out since
July 16. Both pieces are pattern breaks against the same "now is the time to sell" wallpaper, and
sending both in a row would repeat the trick. Pick one for this round. The coffee version asks for a
conversation, the don't-sell version asks for nothing at all.
