# Email Verification — where to run the list before a send

Applies to any cold round. The file for this round is `outreach/verify_list_2026-08-13.csv`
(1,176 rows, one per distinct address, with `version`, `contact_id`, `greeting_name`, `city`
carried alongside so the vendor's return file maps straight back into the database).

Round 1 went out unverified and produced 52 hard bounces out of 655 sends, about 8%. Anywhere near
that on a single-mailbox Outlook send is what gets a domain reputation dinged, so this step is
cheap insurance rather than a nicety.

---

## Where to run it

**Recommended: MillionVerifier** (millionverifier.com). Upload the CSV, download the results.
10,000 credits runs about $39 and credits do not expire, so one purchase covers this list roughly
eight times over as the database grows. Roughly six to seven times cheaper per email than the
premium options, with accuracy in the same band for standard consumer domains, which is what this
list is almost entirely made of.

**Alternative: ZeroBounce** (zerobounce.net) or **NeverBounce** (neverbounce.com). Both run about
$0.008 per email at this volume, so about $10 for the whole list. NeverBounce gives 1,000 free
credits at signup, which would cover most of this round on its own. ZeroBounce returns more
metadata (catch-all detection, activity data, suggested spelling corrections) and has the nicer
interface. Either is a fine choice if you would rather pay a bit more for a name you have heard of.

All three take a CSV in and hand a CSV back with a status column appended. Nothing to configure.

---

## What to do with the results

1. Drop the vendor's return file anywhere in the repo.
2. Run:

   ```
   python3 scripts/apply_verification.py path/to/results.csv
   ```

   Report only. Add `--apply` when the numbers look right.

The script auto-detects the email and status columns, understands the vocabulary all three vendors
use, and does two things: marks bad addresses `bounced` in `contacts` so they are excluded from
every future round automatically, and rewrites the send lists with only the verified-good rows.

---

## How to treat each status

| Vendor status | Meaning | Do |
|---|---|---|
| `ok` / `valid` / `deliverable` | Mailbox confirmed | Send |
| `invalid` / `bad` / `undeliverable` | Will bounce | Drop, mark `bounced` |
| `disposable` | Throwaway inbox | Drop, mark `bounced` |
| `catch_all` / `accept_all` / `unknown` / `risky` | Domain accepts everything, so the mailbox cannot be confirmed either way | Judgment call, see below |

Catch-all is usually 5 to 15% of a consumer list. Some of those are real people and some are dead
addresses on a domain that never says no. On a normal send you would include them. On a
single-mailbox Outlook send that already throttled in June, hold them out of the main batch and run
them last, in small groups, once the good rows are through and the bounce rate is confirmed clean.
`apply_verification.py` sorts them into their own file so that stays easy.

Nothing in the risky bucket gets marked `bounced`. An unconfirmed address is not a bad address, and
burning it permanently in the database over an inconclusive check would be a mistake you cannot
undo from a CSV.
