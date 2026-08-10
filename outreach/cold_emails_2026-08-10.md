# Cold Email Round 2 — Draft Copy
Generated 2026-08-10. Nothing is sent automatically. Pick the angles you like, then I'll generate the merge file.

**Segments available in leads.db:**

| Segment | Count | Channel |
|---|---|---|
| San Clemente, never contacted, has email | 273 | email |
| Capistrano Beach, never contacted, has email | 248 | email |
| Emailed in June/July, never replied, has phone | 657 | **phone** |
| Never contacted, has phone | 836 | **phone** |

**Round 1 results (655 resident + 10 absentee sends, Jun 9 – Jul 16):** 53 bounced (8%), 4 opt-outs, 1 warm seller reply. 0.15% reply rate.

**What Round 1 did wrong:** the copy said "I have buyers waiting in the wings." That claim can't be backed, and homeowners in a farm area compare notes. Every email below leads with a verifiable number instead.

**Stats used below are real** (Pacific Sotheby's July 2026 deck + CRMLS via InfoSparks, reporting Jun/Jul 2026). Refresh before sending if this sits more than a few weeks.

---

## Signature block (goes on every send, DRE compliance)

```
Adam Boehrer
Real Estate Agent · DRE #02419464
Pacific Sotheby's International Realty
949.541.8247 · adam.boehrer@pacificsir.com
```

---

# SEGMENT 1 — San Clemente owners, never contacted (273)

## A1 · "70 days"

**Subject:** 70 days

> Hi {{name}},
>
> That is how long it now takes to sell the average home in San Clemente. Last year it was 98.
>
> At the same time, 40% of the homes currently listed here have already cut their price at least once.
>
> Both of those are true right now, which is why almost everything you're hearing about this market is half a story. Fast market, and a lot of people getting it wrong on the way in.
>
> I work San Clemente block by block. If you want to know what your specific street is doing instead of the city average, reply with your address and I'll put the real number together for you.
>
> Best,

**Why it works:** the number is the hook, not you. The contradiction earns the read. The ask is one word (your address) and the payoff is concrete.

---

## A2 · "the 10-day house"

**Subject:** the 10-day house

> Hi {{name}},
>
> The median San Clemente home sold in 10 days last month. It closed at 101.1% of asking.
>
> That is not a hot market being hot. That is a small number of homes that were priced and prepped correctly, dragging the whole average up. The ones that missed are sitting there right now with a price cut on them, and there are a lot of those.
>
> The difference between those two outcomes is almost entirely decided before a home ever goes live.
>
> If you're anywhere near thinking about selling, this year or in three years, I'd rather have the conversation early than get called in after a listing has gone stale. Reply and I'll walk you through what your place would actually do.
>
> Best,

**Why it works:** takes a side. "Priced correctly beats hoping" is a real position, and it makes the early conversation the logical next step instead of a favor.

---

# SEGMENT 2 — Capistrano Beach owners, never contacted (248)

## B1 · "five points"

**Subject:** five points

> Hi {{name}},
>
> Last month, homes in Dana Point sold for 95.6% of asking. In San Clemente, 101.1%.
>
> Same coastline, twenty minutes apart, five and a half points of difference. On a $2M house that's roughly $110,000 that showed up in one seller's account and not the other's.
>
> That gap is not the market. It's preparation, pricing, and how a home gets put in front of people.
>
> Capo Beach is the pocket I know best. If you ever want to know what your house would really do, ask me. I'll give you the honest number, including when the honest answer is "not yet."
>
> Best,

**Why it works:** the dollar figure does the arguing. "Including when the answer is not yet" is the line that separates you from the other seventeen agents mailing this block.

---

## B2 · "89 homes"

**Subject:** 89 homes

> Hi {{name}},
>
> There are 89 homes for sale in Dana Point right now and 28 in escrow. At that pace, it takes about 95 days to clear the shelf. A year ago it was 131, so things have genuinely tightened.
>
> The part nobody puts in the postcard: about a third of those 89 have already dropped their price.
>
> I'd rather you have the real picture than the version that fits on a mailer. If your address is on my list and you want to know where you actually sit in that 89, reply and I'll send it over.
>
> Best,

**Why it works:** most agents send "the market is hot!" You're sending the asterisk. That's the credibility play.

---

# SEGMENT 3 — Follow-up to the 657 who got the June email and never replied

Serhant's actual rule is that the follow-up is where the money is, and almost nobody sends it. This one goes to people who have already heard from you once.

## C1 · "me again"

**Subject:** me again

> Hi {{name}},
>
> I wrote you back in June about the San Clemente market. You didn't reply, which is fair. Most people don't, and most agents quit after one email.
>
> So here's the update instead of a nudge.
>
> Since that note: expected market time dropped to 70 days from 98 a year ago. Median sale price is $1.9M. Homes are closing at 101.1% of asking, and 40% of active listings have still taken a price cut.
>
> That's the whole market in four lines. If you want the version that's about your house instead of the city, that's a ten-minute conversation and I'm glad to have it.
>
> If you'd rather I stop, reply "stop" and you're off my list for good.
>
> Best,

**Why it works:** naming the silence disarms it. Leading with the update instead of the ask makes the second email feel like a service, not a chase. The opt-out line protects the domain and keeps the list clean.

---

# Send mechanics

- 3-minute spacing, small batches across the day, from the Pacific Sotheby's Outlook. Cold sends throttle around 150/day at tighter spacing.
- Verify delivery via NDR bounces. A closed compose window is not a delivered email.
- Any "stop" reply goes straight to `do_not_contact` in leads.db.
- Round 1 bounced at 8%. Anything above that on Round 2 means the title data needs cleaning before the next batch.
