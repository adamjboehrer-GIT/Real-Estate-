# Outreach Round 2 — "You Shouldn't Sell. Let's Get Coffee."

Generated 2026-08-13. The don't-sell pattern break, cut down and pointed at a coffee instead of at a
listing. Nothing sends automatically.

The hook buys the read. The ask is a cup of coffee, which is small enough that saying yes costs
nothing. Low pressure comes from the size of the ask, so there are no "no pressure" disclaimers in
the copy.

---

## The list

`scripts/build_send_list.py --write --date 2026-08-13`. Deduped by address, exclusions by address.

| | Count |
|---|---|
| Distinct addresses | 1,233 |
| Blocked (52 bounced round 1, 4 opted out) | 56 |
| **Version A · never emailed** | **517** |
| **Version B · emailed Jun/Jul, no reply** | **659** |
| **Sendable before verification** | **1,176** |

Verify `outreach/verify_list_2026-08-13.csv` before sending. See `VERIFICATION.md`.

**Greetings:** only 396 rows have a usable first name (A: 170, B: 226). The rest are trusts and
vesting strings, so they rotate between `Hi neighbor,` and `Hello, neighbor!` like round 1.

**Disclosure + opt-out:** both go in as **live text in the body**, not left to the Outlook signature
image. Outlook and Gmail block remote images by default, and a disclosure nobody can see is a
disclosure that does not count. Every email ends:

```
Best,

Adam Boehrer
REALTOR® · DRE #02419464
Pacific Sotheby's International Realty
949.541.8247 · adam.boehrer@pacificsir.com

If you'd rather not hear from me again, just reply "stop" and I'm gone for good.
```

DRE # renders at body size, so it is never smaller than anything else in the piece. The Outlook
signature block still lands below this. No images in the body, so no AB 723 disclosure applies.

---

## Version A · never emailed (517)

**Subject:** you probably shouldn't sell your house

> Hi {{name}},
>
> Odd thing to get from a Realtor. Stay with me.
>
> The market almost never decides when someone sells. Life does. If nothing in yours is changing,
> you probably shouldn't sell.
>
> So take this as an introduction instead. If there's a real estate question rattling around in the
> back of your head, bring it to me. Coffee is on me, or a phone call if that's easier.
>
> That's the whole email. I'm right here when you want me.
>
> Best,
>
> Adam
>
> Don't want to hear from me again? Reply "stop" and I'm gone for good.

**Subject alternates:** `don't sell your house` · `coffee, and I'll talk you out of selling` · `an odd email from a Realtor`

---

## Version B · emailed in June, no reply (659)

Round 1 told them buyers were waiting for a home in their neighborhood. This one owns that, keeps
the part that's true, and turns on the double meaning of "move."

**Subject:** what actually moves people

> Hi {{name}},
>
> I emailed you back in June about buyers looking in your neighborhood. Very Realtor of me. You
> didn't reply, which is fair.
>
> The interest is real. Homes here get attention. But interest has never once made someone move.
>
> Life does that. A job changes, a family grows or empties out, a place stops fitting. If none of
> that is happening at your house, you probably shouldn't sell.
>
> So take this as an introduction instead. If there's a real estate question sitting in the back of
> your head, bring it to me. Coffee is on me, or a phone call if that's easier.
>
> That's the whole email. I'm right here when you want me.
>
> Best,
>
> Adam
>
> Don't want to hear from me again? Reply "stop" and I'm gone for good.

**Subject alternates:** `let me try that again` · `about that email in June` · `interest doesn't move anyone`

---

## Optional P.S. (Version A only)

> P.S. I write a short local market note every couple of weeks called Coastal Currents.
> https://adamboehrer.com if you want it.

Turns a non-reply into a subscriber. Leave it off B, where it steps on the close.

---

## Send mechanics

1. Verify the list first.
2. Pacific Sotheby's Outlook, individually, **3 minutes apart**, small batches across the day. Tight
   spacing throttled around 150/day in June.
3. Watch NDR bounces. A closed compose window is not proof of delivery.
4. Any reply with "stop" gets set to `do_not_contact` same day.
5. Log sends with `scripts/log_resident_sends.py` under campaign `camp-coffee-2026-08`.

Roughly 8 working days at that pace. Send B first: they have seen the name once, so they are the
faster read on whether the angle works.

Supersedes `cold_emails_2026-08-12_dont-sell.md`, which was never sent.
