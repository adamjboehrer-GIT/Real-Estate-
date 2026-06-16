#!/usr/bin/env python3
"""Generate cold emails for OWNER-OCCUPIED residents (not absentee) with a valid
email in leads.db, in San Clemente and Capo Beach (Capistrano Beach).

Resident = mailing address contains the property address (owner lives in the home).
Body is Adam's approved V1 "canvassing the neighborhood, buyers waiting" copy.
Only fill-ins are {First} and {City}. Capistrano Beach renders as "Capo Beach".

Writes a dated markdown file to outreach/ for Adam to copy from and send
individually from his Pacific Sotheby's address. Nothing is sent automatically.

Usage:  python3 scripts/gen_resident_emails.py [YYYY-MM-DD]
"""
import json, re, sqlite3, sys, os
from collections import defaultdict

DATE = sys.argv[1] if len(sys.argv) > 1 else "today"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB   = os.path.join(ROOT, "database", "leads.db")
OUT  = os.path.join(ROOT, "outreach", f"resident_emails_{DATE}.md")

# Owner-occupied: mailing address contains the property address. Local cities only.
SQL = """
SELECT c.id, c.first_name, c.last_name, c.email, c.mailing_address,
       p.property_address, p.city
FROM contacts c JOIN properties p ON p.contact_id=c.id
WHERE c.email IS NOT NULL AND c.email!='' AND p.property_address IS NOT NULL
  AND instr(lower(c.mailing_address), lower(p.property_address))>0
  AND lower(p.city) IN ('san clemente','capistrano beach')
ORDER BY p.city, p.property_address;
"""

CITY_LABEL = {"san clemente": "San Clemente", "capistrano beach": "Capo Beach"}

# ---- name parsing (shared logic with gen_absentee_emails.py) ----
PARTICLES={'von','van','de','del','della','di','la','le','los','mac','mc','st','san','da','dela'}
SUFFIX={'tr','trust','family','revoc','revocable','living','jr','sr','ii','iii','iv','md','dba','etal',
        'et','al','the','of','declaration','irrevoc','intervivos','separate','ppty','sep','co','llc',
        'inc','lp','llp','partners','properties','holdings','investments','group','series','decedents','security'}
ENTITY_KW={'llc','inc','lp','llp','holdings','investments','properties','property','group','company',
           'ltd','media','restoration','holding','realestate','estate'}

def is_word(t): return bool(re.match(r'^[A-Za-z][a-zA-Z\-]+$', t)) and t.lower() not in SUFFIX and len(t)>1

def first_name(first,last):
    first=(first or '').strip(); last=(last or '').strip()
    full=(first+' '+last).strip()
    toks=[t for t in re.split(r'[\s/]+',full) if t]
    if any(t.lower() in ENTITY_KW for t in toks): return (None,'ENTITY')
    segs=[s.strip() for s in re.split(r'/',full) if s.strip()]
    def given(seg):
        t=[x for x in seg.split() if x]
        if t and t[0].lower()=='the': t=t[1:]
        if not t: return None
        i=2 if (t[0].lower() in PARTICLES and len(t)>1) else 1
        for w in t[i:]:
            if w.lower() in SUFFIX: continue
            if len(w)<3: continue
            if is_word(w): return w.capitalize()
        return None
    for seg in segs:
        if 'family' in seg.lower() or 'trust' in seg.lower(): continue
        g=given(seg)
        if g: return (g,'HIGH')
    if len(first.split())==1 and is_word(last): return (last.capitalize(),'HIGH')
    for seg in segs:
        g=given(seg)
        if g and g.lower() not in PARTICLES: return (g,'REVIEW')
    return (None,'NONAME')

# ---- approved V1 body ----
# Upbeat, day-agnostic neighborly openers used when the owner's name is unclear
# (sends happen over several days, so no day-of-week greeting). Rotated so the
# no-name batch doesn't read as identical.
GENERIC_GREET = ["Hi neighbor,", "Hello, neighbor!"]

def subject(city):
    return f"Looking for the right home in {city}"

def body(greeting, city):
    b = (f"{greeting}\n\n"
         f"I'm Adam Boehrer, a Realtor with Pacific Sotheby's right here in {city}, and "
         f"I'll keep this short. This is a highly sought-after neighborhood right now, and I "
         f"have buyers waiting in the wings for the right home in it. So I'm working through "
         f"the area to find the owner who might be thinking about selling.\n\n"
         f"If that could be you, now or down the road, I'd love to connect.\n\n"
         f"Best,")
    assert '—' not in b and '–' not in b, "em dash in body"
    return b

def main():
    rows=[dict(zip(['cid','first_name','last_name','email','mailing_address','property_address','city'],r))
          for r in sqlite3.connect(DB).execute(SQL).fetchall()]
    byemail=defaultdict(list)
    for r in rows: byemail[(r['email'] or '').lower()].append(r)

    named=[]; generic=[]
    for email,group in byemail.items():
        r=group[0]
        fn,cat=first_name(r['first_name'],r['last_name'])
        city=CITY_LABEL.get((r['city'] or '').strip().lower(), (r['city'] or '').strip().title())
        if cat=='HIGH':
            named.append({'email':r['email'],'first':fn,'city':city,'cat':cat,
                          'greeting':f"Hi {fn},",'subject':subject(city),
                          'cids':[g['cid'] for g in group]})
        else:  # REVIEW / ENTITY / NONAME -> unclear name, use neighborly opener
            generic.append({'email':r['email'],'first':None,'city':city,'cat':cat,
                            'subject':subject(city),'cids':[g['cid'] for g in group]})
    # assign rotated generic greetings
    for i,r in enumerate(generic): r['greeting']=GENERIC_GREET[i%len(GENERIC_GREET)]
    for r in named+generic: r['body']=body(r['greeting'],r['city'])

    L=[f"# Resident Owner Cold Emails - San Clemente & Capo Beach\n",
       f"Generated {DATE}. Source: leads.db, owner-occupied residents (mailing matches property) with a valid email.\n",
       "Send individually from your Pacific Sotheby's address. Your signature goes below \"Best,\". Nothing is sent automatically.\n",
       f"\n**{len(named)} addressed by name · {len(generic)} neighborly greeting (name unclear) · {len(named)+len(generic)} total ready to send**\n",
       "\nNamed greetings use the owner name from public record. Glance at the To: line before sending.\n",
       "\n---\n\n## READY TO SEND - addressed by name\n"]
    manifest={}
    n=1
    def block(r,n):
        manifest[str(n)]={'email':r['email'],'name':r['first'],'city':r['city'],
                          'cat':r['cat'],'greeting':r['greeting'],'cids':r['cids']}
        label=r['first'] if r['first'] else r['greeting'].rstrip(',!')
        return (f"### {n}. {label}  ·  {r['city']}\n"
                f"**To:** {r['email']}\n\n**Subject:** {r['subject']}\n\n{r['body']}\n\n---\n")
    for r in named: L.append(block(r,n)); n+=1
    L.append("\n## READY TO SEND - neighborly greeting (owner name unclear: trust/LLC/parsed)\n")
    for r in generic: L.append(block(r,n)); n+=1

    open(OUT,'w').write("".join(L))
    open(OUT.replace('.md','_manifest.json'),'w').write(json.dumps(manifest,indent=1))
    print(f"Wrote {OUT}\n  {len(named)} by-name, {len(generic)} neighborly-greeting, {len(named)+len(generic)} total")

if __name__=='__main__': main()
