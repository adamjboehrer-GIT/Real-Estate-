#!/usr/bin/env python3
"""Derive a safe email greeting name for each contact and store it on the row.

Why this exists
---------------
`contacts.first_name` for title-sourced rows holds the raw vesting string from
the county record, not a usable first name:

    first_name = "Jennison Stephen M Tr / The S & M A Jennison Family"
    last_name  = "Tr"

Merging that field into a salutation produces "Hi Jennison Stephen M Tr,".

The subtler trap is that the vesting owner and the person who actually opens
the inbox are often different people:

    Morton Gregory Scott      -> Audrey.morton1@att.net    (spouse)
    Jennison Stephen M Tr     -> Mjennison@gmail.com       (the "M" in S & M A)
    Sears William P           -> Rodriguezeduard@gmail.com (unrelated party)

So we greet the INBOX OWNER, derived from the email local-part and corroborated
against the vesting string. When the two do not corroborate, we emit NULL and
the templates fall back to "Hi there,". A missing name is invisible; a wrong
name is a blown first impression.

Writes to a new `greeting_name` column. `first_name` is never modified, so this
is reversible and the raw vesting string stays available for title work.

Usage:
    python3 scripts/clean_owner_names.py --dry-run    # propose + write review CSV
    python3 scripts/clean_owner_names.py --apply      # persist greeting_name
"""
from __future__ import annotations

import argparse
import csv
import re
import sqlite3
from collections import Counter
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "database" / "leads.db"
REVIEW_CSV = Path(__file__).resolve().parent.parent / "reports" / "greeting_name_review.csv"

# Tokens that mark the row as an entity rather than a person. Entities get no
# greeting and are flagged so campaigns can skip them outright.
ENTITY_TOKENS = {
    "llc", "llp", "lp", "inc", "corp", "corporation", "ltd", "co", "company",
    "partners", "partnership", "properties", "property", "holdings", "group",
    "series", "fund", "capital", "ventures", "enterprises", "investments",
    "realty", "estate", "church", "association", "foundation",
}

# Vesting noise: trust/role/suffix tokens that are never a given name.
NOISE_TOKENS = {
    "tr", "trs", "tre", "trust", "trustee", "trustees", "qprt", "etal", "et", "al",
    "jr", "sr", "ii", "iii", "iv", "v", "md", "dds", "esq", "the", "and", "family",
    "living", "revoc", "revocable", "inter", "vivos", "survivors", "decd",
    "successor", "joint", "tenants", "community", "separate", "sole", "dtd",
}

# Diminutives. If the inbox local-part opens with a known nickname of the
# vesting given name, prefer the nickname: it is what the person calls himself.
NICKNAMES = {
    "thomas": "tom", "michael": "mike", "robert": "bob", "william": "bill",
    "david": "dave", "jeffrey": "jeff", "ronald": "ron", "charles": "chuck",
    "stephen": "steve", "steven": "steve", "richard": "rick", "daniel": "dan",
    "james": "jim", "joseph": "joe", "kenneth": "ken", "gregory": "greg",
    "andrew": "andy", "christopher": "chris", "matthew": "matt",
    "anthony": "tony", "nicholas": "nick", "patrick": "pat", "samuel": "sam",
    "benjamin": "ben", "edward": "ed", "lawrence": "larry", "douglas": "doug",
    "philip": "phil", "peter": "pete", "frederick": "fred", "albert": "al",
    "arthur": "art", "eugene": "gene", "henry": "hank", "walter": "walt",
    "victor": "vic", "vincent": "vince", "katherine": "kate", "elizabeth": "liz",
    "deborah": "debbie", "barbara": "barb", "patricia": "pat", "susan": "sue",
    "jennifer": "jen", "rebecca": "becky", "christine": "chris",
}


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def vesting_segments(first_name: str, last_name: str) -> list[list[str]]:
    """Split a vesting string into per-person token lists.

    "Pham Duc Quy / Wynn Elizabeth" describes two people; both are candidates
    for the inbox owner, so return both rather than assuming the first.
    """
    raw = norm(f"{norm(first_name)} {norm(last_name)}")
    raw = raw.replace("&", "/")
    out = []
    for seg in raw.split("/"):
        toks = [t for t in re.split(r"[^A-Za-z]+", seg) if t]
        toks = [t for t in toks if t.lower() not in NOISE_TOKENS]
        if toks:
            out.append(toks)
    return out


def is_entity(first_name: str, last_name: str) -> bool:
    raw = f"{first_name} {last_name}".lower()
    toks = set(re.split(r"[^a-z]+", raw))
    return bool(toks & ENTITY_TOKENS)


def email_tokens(email: str) -> tuple[str, list[str]]:
    """Return (flattened local-part, separator-split tokens), digits stripped."""
    local = email.split("@")[0].lower()
    parts = [re.sub(r"\d+", "", p) for p in re.split(r"[._\-+]+", local)]
    parts = [p for p in parts if p]
    return re.sub(r"[^a-z]", "", local), parts


def derive(first_name: str, last_name: str, email: str) -> tuple[str | None, str, str]:
    """Return (greeting_name, confidence, reason)."""
    if not email:
        return None, "none", "no email"
    if is_entity(first_name, last_name):
        return None, "entity", "vesting row is an entity, not a person"

    segs = vesting_segments(first_name, last_name)
    if not segs:
        return None, "none", "no parseable vesting tokens"

    flat, parts = email_tokens(email)
    surnames = {s[0].lower() for s in segs}
    givens = [s[1] for s in segs if len(s) > 1 and len(s[1]) > 1]

    surname_hit = next((s for s in surnames if s in flat and len(s) >= 4), None)

    # R1: separator-split local-part carrying a name token alongside the
    # surname. Catches audrey.morton1 -> Audrey and kim.tarantino -> Kim, i.e.
    # the spouse who actually reads the mail.
    if surname_hit and len(parts) >= 2:
        for p in parts:
            if len(p) >= 3 and p != surname_hit and p not in surnames:
                # A near-miss against the vesting given name means one of the two
                # sources has a typo and we cannot tell which. "aroon.allen" vs
                # title "Aaron Allen" is the same household either way, but the
                # spelling is a coin flip, so route it to a human instead of
                # guessing on a first-contact email.
                near = next((g for g in givens if 0 < edit_distance(p, g.lower()) <= 2), None)
                if near:
                    return p.title(), "review", f"'{p}' vs title spelling '{near}' - confirm before sending"
                return p.title(), "high", f"inbox owner '{p}' beside surname '{surname_hit}'"

    # R2: local-part opens with a vesting given name (or its diminutive).
    for g in givens:
        gl = g.lower()
        if flat.startswith(gl):
            return g.title(), "high", f"local-part opens with given name '{gl}'"
        nick = NICKNAMES.get(gl)
        if nick and flat.startswith(nick) and (surname_hit or len(flat) > len(nick)):
            return nick.title(), "high", f"local-part opens with diminutive '{nick}' of '{gl}'"

    # R1b: the local-part is plainly "firstname.lastname" but the surname does
    # NOT match the vesting owner. The property record still lists this address,
    # so this person is the contact, they are simply not the person on title
    # (relative, spouse under another name, or the buyer of record). Greet the
    # human who opens the inbox.
    if not surname_hit and len(parts) >= 2:
        first, last = parts[0], parts[1]
        if first.isalpha() and last.isalpha() and len(first) >= 3 and len(last) >= 3:
            return first.title(), "medium", f"inbox belongs to '{first.title()} {last.title()}', not the title owner"

    # R3: initial + surname. Only trust it when the initial matches a vesting
    # given name. mjennison against "Stephen M" is the spouse, not Stephen, so
    # a mismatched initial must fall through to no-name.
    if surname_hit:
        m = re.match(rf"^([a-z]){re.escape(surname_hit)}", flat)
        if m:
            initial = m.group(1)
            for g in givens:
                if g.lower().startswith(initial):
                    return g.title(), "medium", f"initial '{initial}' + surname matches '{g}'"
            return None, "none", f"initial '{initial}' does not match any vesting given name"

    return None, "none", "email local-part does not corroborate the vesting name"


def ensure_column(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(contacts)")}
    if "greeting_name" not in cols:
        conn.execute("ALTER TABLE contacts ADD COLUMN greeting_name TEXT")
        conn.commit()
        print("added column contacts.greeting_name")


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    ap.add_argument("--city", help="limit to one city, e.g. 'Capistrano Beach'")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    sql = "SELECT id, first_name, last_name, email, city FROM contacts WHERE email IS NOT NULL AND email != ''"
    params: tuple = ()
    if args.city:
        sql += " AND city = ?"
        params = (args.city,)
    rows = conn.execute(sql, params).fetchall()

    tally: Counter[str] = Counter()
    results = []
    for r in rows:
        name, conf, reason = derive(r["first_name"] or "", r["last_name"] or "", r["email"] or "")
        tally[conf] += 1
        results.append((r["id"], r["city"], r["first_name"], r["email"], name, conf, reason))

    REVIEW_CSV.parent.mkdir(parents=True, exist_ok=True)
    with REVIEW_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "city", "vesting_first_name", "email", "greeting_name", "confidence", "reason"])
        w.writerows(results)

    if args.apply:
        ensure_column(conn)
        conn.executemany(
            "UPDATE contacts SET greeting_name = ?, last_updated = datetime('now') WHERE id = ?",
            [(name, cid) for cid, _, _, _, name, conf, _ in results if conf in ("high", "medium")],
        )
        conn.commit()

    named = tally["high"] + tally["medium"]
    total = len(results)
    print(f"{'APPLIED' if args.apply else 'DRY RUN'}: {total} contacts with email")
    print(f"  high   : {tally['high']}")
    print(f"  medium : {tally['medium']}")
    print(f"  review : {tally['review']}  (spelling conflict, confirm by hand)")
    print(f"  entity : {tally['entity']}  (skip these entirely)")
    print(f"  no-name: {tally['none']}  (greet 'Hi there,')")
    print(f"  -> {named} greetable ({named * 100 // total if total else 0}%)")
    print(f"review CSV: {REVIEW_CSV}")
    conn.close()


if __name__ == "__main__":
    main()
