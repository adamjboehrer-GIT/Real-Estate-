#!/usr/bin/env python3
"""Generate the Capo Beach open house invite for 26966 Calle Dolores (8/22).

A one-off neighbor invite, not a cold pitch. Everyone on it owns a home whose
property city is Capistrano Beach, which for this list is effectively the same
set as people who live there: 322 of the 325 sendable addresses have a Capo
Beach mailing address too.

Two tiers, numbered continuously, verified first:

    tier 1  MillionVerifier-clean addresses     -> send Thursday 8/20
    tier 2  catch-all domains, unconfirmable    -> send Friday 8/21 if 8/20 is clean

Suppression comes from the email_sendlist view, which drops do_not_contact and
bounced, plus the 'responded' soft declines. Dedupe is on the lowercased address:
the title data has up to four rows per person.

Writes:
    outreach/capo_openhouse_emails_<date>.md            human review copy
    outreach/capo_openhouse_emails_<date>_manifest.json manifest for logging
    outreach/capo_openhouse_send_queue.json             queue for gen_batch_send_js.py

Usage:
    python3 scripts/gen_capo_openhouse_emails.py [--date 2026-08-20]
"""

import argparse
import csv
import json
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "outreach"
DB = REPO / "database" / "leads.db"
VERIFIED_DATE = "2026-08-13"

SUBJECT = "Open house on Calle Dolores this Saturday"

# Rotated so the no-name portion does not read as one identical blast.
GENERIC_GREET = ["Hi neighbor,", "Hello, neighbor!"]

BODY = [
    "Quick note to the neighborhood. I'm hosting the open house at 26966 Calle Dolores "
    "this Saturday, 1 to 4.",
    "The price just came down to $1,995,000. Fully remodeled and turn-key in the Golden "
    "Triangle, repiped and rewired, owned solar with a whole-home battery, no HOA. Worth "
    "seeing in person at that number.",
    "Walking through a house on your own street is also the most honest way to find out what "
    "your place would do in this market. Come look, tell me what you think of it, and I'll "
    "tell you what I'm seeing around Capo Beach.",
    "Photos and details: https://adamboehrer.com/26966-calle-dolores/",
    "Hope to meet you Saturday.",
]

# Live text in every email. The Outlook signature carries the same disclosure but rides
# on a banner image that Outlook and Gmail block by default, and a disclosure nobody can
# see is a disclosure that does not count. DRE # renders at body size, never smaller.
DISCLOSURE = [
    "Adam Boehrer",
    "REALTOR® · DRE #02419464",
    "Pacific Sotheby's International Realty",
    "949.541.8247 · adam.boehrer@pacificsir.com",
]

# Kameron Brown's listing, not Adam's. Required on every piece that promotes it.
NON_SOLICIT = ("Listed by Kameron Brown, DRE #02021705, Pacific Sotheby's International Realty. "
               "This is not a solicitation of property already listed with another broker.")

OPT_OUT = 'If you\'d rather not hear from me again, just reply "stop" and I\'m gone for good.'


def lines_for(greeting):
    out = [greeting, ""]
    for para in BODY:
        out += [para, ""]
    out += ["Best,", ""] + DISCLOSURE + ["", NON_SOLICIT, "", OPT_OUT, ""]
    joined = "\n".join(out)
    assert "—" not in joined and "–" not in joined, "em/en dash in body"
    return out


def load_csv_emails(name):
    p = OUT / name
    if not p.exists():
        return set()
    return {r["email"].strip().lower() for r in csv.DictReader(open(p)) if r.get("email")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="2026-08-20")
    args = ap.parse_args()

    verified = (load_csv_emails(f"send_list_{VERIFIED_DATE}_version_A_verified.csv")
                | load_csv_emails(f"send_list_{VERIFIED_DATE}_version_B_verified.csv"))
    if not verified:
        raise SystemExit("No verified lists found. Run apply_verification.py first.")

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    # email_sendlist already dedupes on the address and drops do_not_contact/bounced.
    # 'responded' is excluded here as well: they answered a cold email already.
    rows = con.execute("""
        SELECT s.email, s.greeting_name, s.city, s.contact_ids
        FROM email_sendlist s
        WHERE s.email IN (
            SELECT DISTINCT lower(trim(c.email))
            FROM contacts c
            JOIN properties p ON p.contact_id = c.id
            WHERE p.city = 'Capistrano Beach'
              AND c.email IS NOT NULL AND trim(c.email) != ''
        )
        AND NOT EXISTS (
            SELECT 1 FROM contacts c2
            WHERE lower(trim(c2.email)) = s.email AND c2.status = 'responded'
        )
    """).fetchall()

    tiers = {1: [], 2: []}
    for r in rows:
        tiers[1 if r["email"] in verified else 2].append(r)

    # Named first, then no-name, so a partial day still favours the stronger greeting.
    for t in tiers:
        tiers[t].sort(key=lambda r: ((r["greeting_name"] or "").strip() == "", r["email"]))

    queue, manifest, md = [], {}, []
    n = 0
    generic_i = 0
    tier_label = {1: "Tier 1 (verified) - send Thursday 8/20",
                  2: "Tier 2 (catch-all) - send Friday 8/21 only if 8/20 bounces clean"}

    for t in (1, 2):
        rs = tiers[t]
        named = sum(1 for r in rs if (r["greeting_name"] or "").strip())
        md.append(f"\n## {tier_label[t]} - {len(rs)} emails\n")
        md.append(f"{named} by name, {len(rs) - named} neighborly greeting.\n")
        for r in rs:
            n += 1
            name = (r["greeting_name"] or "").strip()
            if name:
                greeting = f"Hi {name},"
            else:
                greeting = GENERIC_GREET[generic_i % len(GENERIC_GREET)]
                generic_i += 1
            queue.append({"n": n, "to": r["email"], "subject": SUBJECT,
                          "lines": lines_for(greeting)})
            manifest[str(n)] = {"email": r["email"], "name": name or None,
                                "city": r["city"], "tier": t, "greeting": greeting,
                                "cids": r["contact_ids"].split(",")}
            md.append(f"**#{n}** · {r['email']} · {name or 'no name'} · {r['city']} · _{greeting}_")

    t1 = len(tiers[1])
    header = (f"# Capo Beach Open House Invite - {args.date}\n\n"
              f"{n} emails for 26966 Calle Dolores, open house Saturday 8/22, 1 to 4 PM.\n"
              f"Campaign `camp-capo-oh-2026-08`. Subject: **{SUBJECT}**\n\n"
              f"Tier 1 is #1-{t1} (verified). Tier 2 is #{t1 + 1}-{n} (catch-all, hold for Friday).\n"
              f"Nothing sends automatically.\n\n"
              "## Copy\n\n```\n" + "\n".join(lines_for("Hi {name},")) + "```\n")

    (OUT / f"capo_openhouse_emails_{args.date}.md").write_text(header + "\n".join(md) + "\n")
    (OUT / f"capo_openhouse_emails_{args.date}_manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False))
    (OUT / "capo_openhouse_send_queue.json").write_text(
        json.dumps(queue, ensure_ascii=False, indent=1))

    print(f"Queued {n} emails: #1-{t1} tier 1 verified, #{t1 + 1}-{n} tier 2 catch-all")
    for f in (f"capo_openhouse_emails_{args.date}.md",
              f"capo_openhouse_emails_{args.date}_manifest.json",
              "capo_openhouse_send_queue.json"):
        print(f"  outreach/{f}")


if __name__ == "__main__":
    main()
