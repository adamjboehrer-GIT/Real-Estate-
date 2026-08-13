---
name: ig-reels
description: Write a batch of finished, film-ready Instagram Reel scripts for Adam, backed by real CRMLS closing data. Invoke when Adam says "/ig-reels", "write my reels", "reel scripts for this week", "give me a batch to film". Produces hook, spoken beats, on-screen text, shot list, and caption per reel into REEL_QUEUE.md so Adam only has to read and record.
---

# ig-reels — a batch of film-ready Reel scripts

Reels are the only mechanism that takes this account to 10K, and the bottleneck
is filming, not writing. So this skill front-loads everything that is not
standing in front of a camera: the number, the argument, the hook, the exact
words, the on-screen text, and the shot list.

Target cadence: **3–4 Reels a week.** Batch-film them. One afternoon produces
two weeks of content, which is the only way this survives a busy month.

Repo root: `~/Desktop/Claude Code/`. Read `outreach/instagram/INSTAGRAM_PLAN.md`
for the growth strategy, voice rules, and compliance.

## Invocation

- `/ig-reels` — write the next batch of 4
- `/ig-reels 8` — write 8, for a bigger shoot
- `/ig-reels price band 2.5m` — one specific reel
- `/ig-reels status` — what is scripted, filmed, and posted

## The formats, in rotation

Rotate so a batch is never four of the same thing. Yield order:

| Format | Engine | What it argues |
|--------|--------|----------------|
| `price_band` | `ig_price_band.py` | What $X actually buys here |
| `deal` | `ig_deal_of_week.py` | This week's best value, and the catch |
| `reality_check` | research + WebSearch | What people get wrong about moving here |
| `neighborhood_verdict` | `ig_price_band.py` by area | Should you live in this pocket, honestly |
| `market_data` | `website/data/stats.json` | One number, one implication |

**`price_band` is the workhorse.** It is endlessly repeatable across price points
and cities, it is inherently comparative, and it travels nationally while
converting locally, which is the whole relocation thesis in the plan. When in
doubt, write another one.

## Procedure

### 1. Pull real numbers first

Never script a Reel and backfill the data. The number is the reason the Reel
exists.

```bash
cd scripts
python3 ig_price_band.py --city SC --compare 1500000 2000000 3000000
python3 ig_price_band.py --city SC --band 2000000 --json ../outreach/instagram/price_band_latest.json
python3 ig_deal_of_week.py --city SC --top 5 --json ../outreach/instagram/deal_of_week_latest.json
```

The band tool prints a `script:` block of plain spoken beats. That is raw
material, not the final script. Sharpen it.

**Look for the counterintuitive finding.** That is what makes a Reel travel. In
the current San Clemente data, price per foot *drops* from $849 at the $1.5M band
to $787 at $2M, then jumps to $944 at $3M. The $2M band is the value pocket. That
one line is worth more than any amount of production polish.

If the data is more than ~30 days stale, ask for a fresh CRMLS Agent 1-Line
export before scripting anything that quotes a number.

### 2. Write the hook

The hook is the whole game. It gets 1.5 seconds.

- Lead with the number or the contradiction. Never with a greeting, never with
  "Hey guys," never with "Let's talk about."
- No throat-clearing. The first word is already the point.
- Good: "Two million dollars in San Clemente buys less house than one-five does
  per foot. Here is why." / "The best value in San Clemente this week is a 1965
  house nobody has offered on."
- Bad: "Today I want to break down what you can get in San Clemente."

The hook must also work as text on screen, because most of the first view is
muted.

### 3. Write the beats

- 20–40 seconds, which is roughly 60–110 spoken words. Count them.
- One idea per beat. Short sentences. Adam's voice: short beats, one-line
  paragraphs, blunt payoffs, wry specifics.
- **Include the unflattering part.** The marine layer, the Mello-Roos, the 1965
  kitchen, the fact that a discount usually means condition. Credibility is the
  entire product here, and it is the thing every other agent's feed lacks.
- End on a reason to follow, not a pitch. "I do this every week" beats "DM me."
- No em-dashes or en-dashes. No client-speak. No overpromising. No
  "no pressure" disclaimers. Never name Adam's street.

### 4. Write the on-screen text

One short line per beat, parallel to the spoken track. This carries the Reel
muted, so it has to stand alone. Numbers on screen, always.

### 5. Write the shot list

Be specific enough that Adam does not have to think while filming:

- Where to stand (a location that reads as the place, no address-identifying
  detail on Adam's own street)
- Talking head or b-roll for each beat
- Any b-roll to grab while there
- Note if a shot needs golden hour

Brand rules still apply to anything rendered: no filters, no B&W, no text over
property photos. Reels shot on a phone are footage, not collateral, so the
disclosure requirement lands in the caption.

### 6. Compliance

Instagram content about the business is advertising. Caption carries: **Adam
Boehrer · Real Estate Agent · DRE #02419464 · Pacific Sotheby's International
Realty**. If the Reel names or shows a specific listing that is not Adam's, add
the listing brokerage. If any frame is AI-generated or AI-retouched, add the
AB 723 disclosure. Fair housing: describe the property, never the people.

### 7. Write the batch

Insert each into `instagram_reels` with `status='scripted'` and a shared `batch`
label. Then write the batch to the top of `outreach/instagram/REEL_QUEUE.md`,
formatted so Adam can film straight off his phone screen: hook in bold, beats
numbered, on-screen text beside each, shot list at the bottom, caption last.

### 8. Report

Show all scripts inline. Lead with the strongest hook in the batch and say why
it is the strongest. Name the data behind each number.

## Notes

- Volume beats polish. A flop costs an hour, a hit is worth a thousand
  followers, so ship the batch rather than perfecting one.
- After Adam reports how a Reel performed, write it to `performance_note` and
  weight the rotation toward what worked. This is the whole point of tracking it.
- Never invent a number, a neighborhood detail, a local business, or an event.
  WebSearch to verify anything specific before it goes in a script.
- If Adam dictates his own reel idea, treat it as a draft to sharpen, then
  confirm the refined version back.
