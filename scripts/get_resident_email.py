#!/usr/bin/env python3
"""Extract a single resident-owner email by entry number.

Usage:
    python3 scripts/get_absentee_email.py 40
    python3 scripts/get_absentee_email.py 40 --file outreach/resident_emails_2026-06-01.md

Prints JSON: {"number", "to", "subject", "body"}
Body runs from the greeting ("Hi ...,") through the closing "Best," (inclusive),
matching what gets pasted into the Outlook compose window.
"""
import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_default_file():
    matches = sorted(glob.glob(os.path.join(REPO, "outreach", "resident_emails_*.md")))
    matches = [m for m in matches if not m.endswith(".bak")]
    if not matches:
        sys.exit("No resident_emails_*.md file found in outreach/")
    return matches[-1]  # most recent by name


def parse_entry(text, number):
    # Split into entries on the --- separators; each entry starts with "### N."
    blocks = re.split(r"\n---\n", text)
    target = None
    for block in blocks:
        m = re.search(r"^###\s+(\d+)\.\s*(.*)$", block.strip(), re.MULTILINE)
        if m and int(m.group(1)) == number:
            target = block.strip()
            break
    if target is None:
        sys.exit(f"Entry #{number} not found.")

    to_m = re.search(r"\*\*To:\*\*\s*(.+)", target)
    subj_m = re.search(r"\*\*Subject:\*\*\s*(.+)", target)
    if not to_m or not subj_m:
        sys.exit(f"Entry #{number} is missing a To: or Subject: line.")

    to = to_m.group(1).strip()
    subject = subj_m.group(1).strip()

    # Body = everything from the line after the Subject line through "Best,"
    after_subject = target[subj_m.end():]
    lines = after_subject.splitlines()
    # drop leading blank lines
    while lines and not lines[0].strip():
        lines.pop(0)
    body_lines = []
    for ln in lines:
        body_lines.append(ln)
        if ln.strip() == "Best,":
            break
    body = "\n".join(body_lines).rstrip()

    return {"number": number, "to": to, "subject": subject, "body": body}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("number", type=int)
    ap.add_argument("--file", default=None)
    args = ap.parse_args()

    path = args.file or find_default_file()
    if not os.path.isabs(path):
        path = os.path.join(REPO, path)
    with open(path, encoding="utf-8") as f:
        text = f.read()

    print(json.dumps(parse_entry(text, args.number), ensure_ascii=False))


if __name__ == "__main__":
    main()
