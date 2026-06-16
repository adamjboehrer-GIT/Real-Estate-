#!/usr/bin/env python3
"""Log resident cold-email sends to interactions in leads.db.

Usage:  python3 scripts/log_resident_sends.py 1 5 12 20-35 [--manifest PATH]
Accepts individual email numbers and ranges (as shown in the markdown file).
Idempotent: an already-logged email for this campaign is skipped, not doubled.
"""
import sqlite3, sys, json, os, uuid, glob
from datetime import datetime

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB=os.path.join(ROOT,"database","leads.db")
CAMP_ID="camp-resident-2026-06"

def latest_manifest():
    m=sorted(glob.glob(os.path.join(ROOT,"outreach","resident_emails_*_manifest.json")))
    if not m: sys.exit("No resident_emails_*_manifest.json found in outreach/")
    return m[-1]

def expand(args):
    nums=[]
    for a in args:
        if '-' in a:
            lo,hi=a.split('-'); nums+=list(range(int(lo),int(hi)+1))
        else: nums.append(int(a))
    return sorted(set(nums))

def main():
    argv=sys.argv[1:]
    manifest=latest_manifest()
    if "--manifest" in argv:
        i=argv.index("--manifest"); manifest=argv[i+1]; del argv[i:i+2]
    if not argv:
        print("usage: log_resident_sends.py 1 5 12 20-35 [--manifest PATH]"); return
    nums=expand(argv)
    man=json.load(open(manifest))
    db=sqlite3.connect(DB)
    today=datetime.now().strftime("%Y-%m-%d")
    logged=skipped=missing=0
    for n in nums:
        e=man.get(str(n))
        if not e: print(f"  #{n}: not in manifest, skipped"); missing+=1; continue
        name=e.get('name') or 'neighbor'
        for cid in e['cids']:
            dup=db.execute("SELECT 1 FROM interactions WHERE contact_id=? AND campaign_id=?",
                           (cid,CAMP_ID)).fetchone()
            if dup: skipped+=1; continue
            db.execute("""INSERT INTO interactions(id,contact_id,channel,direction,date,outcome,notes,campaign_id)
                          VALUES(?,?,?,?,?,?,?,?)""",
                (str(uuid.uuid4()),cid,'email','outbound',today,'sent',
                 f"Resident canvassing cold email #{n} ({name}, {e.get('city','')})",CAMP_ID))
            db.execute("UPDATE contacts SET status='contacted',last_updated=? WHERE id=?",(today,cid))
            logged+=1
    db.commit()
    print(f"Logged {logged} send(s) on {today}. Skipped {skipped} already-logged. {missing} not found.")

if __name__=="__main__": main()
