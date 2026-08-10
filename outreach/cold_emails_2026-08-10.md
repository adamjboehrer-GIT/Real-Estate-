# Cold Email Round 2 — Draft Copy
Generated 2026-08-10. Nothing is sent automatically. Pick the angles you like, then I'll generate the merge file.

**The premise:** no market stats, no listing pitch. These sell Adam. The only thing each email is trying to accomplish is that the reader finishes it thinking "huh, that guy is not like the other seven agents in my mailbox."

**Segments in leads.db:**

| Segment | Count |
|---|---|
| San Clemente, never contacted, has email | 273 |
| Capistrano Beach, never contacted, has email | 248 |
| Emailed Jun/Jul, never replied | 657 |

Swap "San Clemente" for "Capo Beach" on segment 2. Everything else holds.

**Round 1 (665 sends, Jun–Jul):** 53 bounced, 4 opt-outs, 1 reply. The copy claimed "I have buyers waiting in the wings." That's gone. The differentiator below is true and checkable, which is the only kind worth building on.

---

## Signature block (every send, DRE compliance)

```
Adam Boehrer
Real Estate Agent · DRE #02419464
Pacific Sotheby's International Realty
949.541.8247 · adam.boehrer@pacificsir.com
```

---

## A · "what I did before this"

**Subject:** what I did before this

> Hi {{name}},
>
> Before real estate I spent my career in brand strategy. Which is a long way of saying I spent years figuring out why a person picks one thing over another when both things look identical on paper.
>
> Turns out that's the entire job here.
>
> Two houses, same street, same year, same square footage. One sells in a week with people climbing over each other. One sits until the price comes down twice. Everybody blames the market.
>
> It's almost never the market.
>
> I'm a Realtor with Pacific Sotheby's and I live here in San Clemente. When you eventually sell, next spring or nine years from now, I want to be the call you make first. Not because I'll show up with a stack of names, but because I know how to position a home so that people fight over it.
>
> That's the whole email. I'm right here when you want me.
>
> Best,

**Why it works:** the brand-strategy background is the single most differentiating thing about you and almost no agent can say it. "It's almost never the market" is a real position that costs you something to say, which is exactly why it lands.

---

## B · "I buy them too"

**Subject:** I buy them too

> Hi {{name}},
>
> Most agents have never bought a piece of real estate with their own money. I have, and I still do.
>
> It changes what you see when you walk into a house. You stop looking at a listing and start looking at risk, upside, and the gap between what a place is worth and what somebody is hoping it's worth. You also learn to say "don't buy that" out loud, which is not a sentence that helps an agent get paid.
>
> I'm a Realtor with Pacific Sotheby's, I live in San Clemente, and I think about this neighborhood constantly whether or not anyone is paying me to.
>
> If you ever want a genuinely straight read on what your place is worth, or on something you're thinking about buying, that's a conversation I'd actually enjoy.
>
> Best,

**Why it works:** "don't buy that is not a sentence that helps an agent get paid" is the whole email. You're proving the trait by demonstrating it costs you money.

---

## C · "the new guy"

**Subject:** the new guy

> Hi {{name}},
>
> I'll tell you the thing the other agents in your mailbox are hoping you don't ask.
>
> I'm newer at this than they are.
>
> Here's what that actually buys you. I'm not juggling nineteen listings. I answer my own phone. I still show up to things I don't have to show up to. And I chose Pacific Sotheby's deliberately, because if I was going to be new, I wanted my neighbors on the best platform available from day one instead of whenever I'd finally earned it.
>
> What I'm not new at is real estate. I invest in it with my own money, and my career before this was brand strategy, which is the part of selling a home almost nobody is genuinely good at.
>
> I live in San Clemente and I'd like to know my neighbors. Reply if you ever want to talk about your house. Or don't, and I'll still wave.
>
> Best,

**Why it works:** this is the most Serhant thing in the file. He built a brand on being the broke actor who'd never sold anything. Naming your own weakness first takes it off the table and makes everything after it credible. "Or don't, and I'll still wave" is the line people will actually remember.

---

## D · "30 seconds"

**Subject:** 30 seconds

> Hi {{name}},
>
> Short version.
>
> I live in San Clemente. I'm a Realtor with Pacific Sotheby's. Before this I was in brand strategy, and I invest in real estate myself, so I come at a house from how it gets positioned and what it's honestly worth, not from how fast I can get a sign in the yard.
>
> All I want out of this email is that you remember my name.
>
> Because for most people the day does eventually come, and when it does I want to be the first call. Between now and then, ask me anything. I like this stuff.
>
> Best,

**Why it works:** the shortest one will probably outperform the clever ones. "All I want out of this email is that you remember my name" is honest about what a cold email actually is, which is disarming without ever announcing that it's disarming.

---

# How to run it

Send **A** and **C** against each other, roughly 130 each into San Clemente. They're the two strongest and they're strong for opposite reasons: A is competence, C is character. Whichever pulls better tells you which lever your farm responds to, and that answer is worth more than this round of replies.

Hold **B** for Capo Beach, where the investor angle fits the ownership mix better. **D** is your follow-up to the 657 who ignored June.

- 3-minute spacing, small batches across the day, from the Pacific Sotheby's Outlook. Tighter than that and sends throttle around 150/day.
- Verify delivery via NDR bounces. A closed compose window is not a delivered email.
- Any "stop" reply goes to `do_not_contact` in leads.db.
- Round 1 bounced at 8%. Higher than that this round means the title data needs cleaning before the next batch.
