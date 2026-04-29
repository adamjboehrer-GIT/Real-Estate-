#!/usr/bin/env python3
"""
Polls the Mailchimp audience for new Home Value (CMA) form submissions and
emails Adam when one shows up.

Detection: members in list f44752d032 whose SOURCE merge field is "cma" and
who do NOT yet carry the "cma-notified" tag. After emailing, the script tags
the member as "cma-notified" so the next run skips them.

First run is bootstrap mode: tag every existing CMA member without emailing,
so we don't flood the inbox with historical signups. Marker file at
~/.cma-notifier-initialized records that the bootstrap finished.

Secrets are read from ~/.cma-notifier.env (chmod 600). Required keys:
    MAILCHIMP_API_KEY=...
    GMAIL_APP_PASSWORD=...
    NOTIFY_EMAIL=adamjboehrer@gmail.com
"""
from __future__ import annotations

import json
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path
from urllib import error, request

LIST_ID = "f44752d032"
HOME = Path.home()
ENV_PATH = HOME / ".cma-notifier.env"
INIT_MARKER = HOME / ".cma-notifier-initialized"
LOG_PATH = HOME / "Library" / "Logs" / "cma-notifier.log"
TAG_NAME = "cma-notified"


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a") as f:
        f.write(msg.rstrip() + "\n")


def load_env() -> dict[str, str]:
    if not ENV_PATH.exists():
        log(f"FATAL: {ENV_PATH} not found. Aborting.")
        sys.exit(1)
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def mailchimp_get(env: dict[str, str], path: str, params: dict | None = None) -> dict:
    api_key = env["MAILCHIMP_API_KEY"]
    dc = api_key.split("-")[-1]
    url = f"https://{dc}.api.mailchimp.com/3.0{path}"
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"
    req = request.Request(url)
    req.add_header("Authorization", f"apikey {api_key}")
    with request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def mailchimp_post(env: dict[str, str], path: str, body: dict) -> dict:
    api_key = env["MAILCHIMP_API_KEY"]
    dc = api_key.split("-")[-1]
    url = f"https://{dc}.api.mailchimp.com/3.0{path}"
    req = request.Request(url, data=json.dumps(body).encode(), method="POST")
    req.add_header("Authorization", f"apikey {api_key}")
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"Mailchimp POST {path} failed: {e.code} {detail}")


def fetch_cma_members(env: dict[str, str]) -> list[dict]:
    members: list[dict] = []
    offset = 0
    count = 100
    while True:
        page = mailchimp_get(
            env,
            f"/lists/{LIST_ID}/members",
            {"offset": offset, "count": count, "fields": "members.id,members.email_address,members.merge_fields,members.tags,members.timestamp_signup"},
        )
        batch = page.get("members", [])
        members.extend(batch)
        if len(batch) < count:
            break
        offset += count
    cma = []
    for m in members:
        merge = m.get("merge_fields", {}) or {}
        source = (merge.get("SOURCE") or "").strip().lower()
        if source == "cma":
            cma.append(m)
    return cma


def has_tag(member: dict, tag: str) -> bool:
    for t in member.get("tags", []) or []:
        if (t.get("name") or "").lower() == tag.lower():
            return True
    return False


def tag_member_notified(env: dict[str, str], member_id: str) -> None:
    mailchimp_post(
        env,
        f"/lists/{LIST_ID}/members/{member_id}/tags",
        {"tags": [{"name": TAG_NAME, "status": "active"}]},
    )


def format_email_body(member: dict) -> tuple[str, str]:
    merge = member.get("merge_fields", {}) or {}
    fname = (merge.get("FNAME") or "").strip()
    lname = (merge.get("LNAME") or "").strip()
    name = f"{fname} {lname}".strip() or "(no name provided)"
    email = member.get("email_address", "")
    phone = (merge.get("PHONE") or "").strip() or "(none)"
    addr = merge.get("ADDRESS") or {}
    if isinstance(addr, dict):
        street = (addr.get("addr1") or "").strip() or "(not provided)"
    else:
        street = str(addr).strip() or "(not provided)"
    signup = member.get("timestamp_signup", "") or "(unknown)"
    subject = f"New Home Value request — {name}"
    body = (
        f"A new Home Value request just came in via adamboehrer.com.\n\n"
        f"Name:    {name}\n"
        f"Email:   {email}\n"
        f"Phone:   {phone}\n"
        f"Address: {street}\n"
        f"Signed up: {signup} (UTC)\n\n"
        f"Pull the comps and send the report within a day or two.\n"
    )
    return subject, body


def send_email(env: dict[str, str], subject: str, body: str) -> None:
    sender = env.get("NOTIFY_EMAIL", "adamjboehrer@gmail.com")
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = sender
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
        s.login(sender, env["GMAIL_APP_PASSWORD"])
        s.send_message(msg)


def main() -> int:
    env = load_env()
    bootstrap = not INIT_MARKER.exists()

    try:
        cma_members = fetch_cma_members(env)
    except Exception as e:
        log(f"ERROR fetching members: {e}")
        return 1

    pending = [m for m in cma_members if not has_tag(m, TAG_NAME)]
    if not pending:
        log(f"OK: 0 pending CMA submissions (bootstrap={bootstrap}).")
        if bootstrap:
            INIT_MARKER.touch()
        return 0

    if bootstrap:
        # First run: tag everyone silently so we don't email about historical signups.
        tagged = 0
        for m in pending:
            try:
                tag_member_notified(env, m["id"])
                tagged += 1
            except Exception as e:
                log(f"ERROR tagging {m.get('email_address')}: {e}")
        INIT_MARKER.touch()
        log(f"BOOTSTRAP: tagged {tagged} existing CMA member(s) as {TAG_NAME}; no emails sent.")
        return 0

    sent = 0
    for m in pending:
        subject, body = format_email_body(m)
        try:
            send_email(env, subject, body)
        except Exception as e:
            log(f"ERROR emailing about {m.get('email_address')}: {e}")
            continue
        try:
            tag_member_notified(env, m["id"])
        except Exception as e:
            log(f"WARN: emailed {m.get('email_address')} but failed to tag: {e}")
            continue
        sent += 1
    log(f"OK: emailed {sent}/{len(pending)} new CMA submission(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
