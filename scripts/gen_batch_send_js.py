#!/usr/bin/env python3
"""Generate a self-contained Playwright run_code_unsafe JS file for a range of
resident emails, with the email data embedded inline (the MCP sandbox has no
fs/require/import). The generated script composes + sends each email paced, and
RETURNS a JSON results array (no file writes). Log sent numbers afterward with
scripts/log_resident_sends.py.

Usage: python3 scripts/gen_batch_send_js.py START END [DELAY_MS] [LEAD_MS] [--queue NAME]
       --queue defaults to resident_send_queue.json; round 2 uses coffee_send_queue.json
       --campaign ID   override the campaign the ledger is seeded from
       --force         generate even for numbers already logged as sent (never do
                       this to fix a suspected failure; reconcile Sent Items first)
Writes: scripts/_batch_send_generated.js

DOUBLE-SEND PROTECTION (added 2026-08-18 after 6 addresses got the same email twice)
------------------------------------------------------------------------------------
On 8/18 batch #228-252 hit the MCP idle timeout and the tool call aborted. The JS
kept running inside the Playwright server process, so when the next batch was
launched two loops drove the same Outlook tab at once and every address in the
overlap went out twice. Four independent guards now make that impossible:

  1. RUN BUDGET  - the loop stops itself well before the MCP idle timeout, so a
                   run ends by returning rather than by being aborted. No orphans.
  2. RUN LOCK    - a heartbeat lock in the page's localStorage. A second run
                   refuses to start while a live loop still holds it. It lives in
                   localStorage, not window, so it survives the navigation that
                   defeated the first stop attempt.
  3. SEND LEDGER - every number is written to localStorage immediately BEFORE the
                   Send click, and checked before each compose. A crash after Send
                   therefore skips, rather than resends. Missed sends are caught by
                   reconciling Sent Items; duplicates cannot be taken back.
  4. DB SEED     - numbers already logged in leads.db for this campaign are dropped
                   at generation time and pre-seeded into the ledger.

If a run ever does abort anyway: CLOSE THE TAB FIRST. Do not navigate the tab back
to Outlook to check Sent Items, which is what let the orphaned loops resume. Open a
new tab to reconcile, and wait for the lock to go stale before relaunching.
"""
import json, sys, os, re, uuid, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv[1:]
queue_name = "resident_send_queue.json"
if "--queue" in argv:
    i = argv.index("--queue"); queue_name = argv[i + 1]; del argv[i:i + 2]
campaign = None
if "--campaign" in argv:
    i = argv.index("--campaign"); campaign = argv[i + 1]; del argv[i:i + 2]
force = False
if "--force" in argv:
    argv.remove("--force"); force = True
nums = None
if "--nums" in argv:
    i = argv.index("--nums"); spec = argv[i + 1]; del argv[i:i + 2]
    nums = set()
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-"); nums |= set(range(int(lo), int(hi) + 1))
        else:
            nums.add(int(part))
    argv = ["0", "0"] + argv
start, end = int(argv[0]), int(argv[1])
delay = int(argv[2]) if len(argv) > 2 else 25000
lead_delay = int(argv[3]) if len(argv) > 3 else 0  # seam wait before first send

if campaign is None:
    campaign = ("camp-coffee-2026-08" if "coffee" in queue_name
                else "camp-resident-2026-06")

queue = json.load(open(os.path.join(ROOT, "outreach", queue_name)))
todo = [e for e in queue if (e["n"] in nums if nums else start <= e["n"] <= end)]

# --- guard 4: drop anything leads.db already records as sent for this campaign
db = sqlite3.connect(os.path.join(ROOT, "database", "leads.db"))
already = set()
for (notes,) in db.execute(
        "SELECT notes FROM interactions WHERE campaign_id=? AND direction='outbound'",
        (campaign,)):
    m = re.search(r"cold email #(\d+)", notes or "")
    if m:
        already.add(int(m.group(1)))
db.close()

overlap = sorted({e["n"] for e in todo} & already)
if overlap and not force:
    todo = [e for e in todo if e["n"] not in already]
    print(f"!! Dropped {len(overlap)} already-sent number(s): "
          f"{','.join(str(n) for n in overlap)}")
    print("   (they are logged in leads.db for " + campaign + "; pass --force to override)")
if not todo:
    sys.exit("Nothing left to send in that range.")

data = json.dumps(todo, ensure_ascii=False)
seed = json.dumps(sorted(already))
run_id = uuid.uuid4().hex

# Stop the loop this far in, so it always ends by RETURNING rather than by being
# aborted at the MCP idle timeout. An aborted call leaves the JS running.
run_budget_ms = 1_320_000   # 22 min
per_email_ms = 120_000      # watchdog: no single compose may eat the whole run

JS = """async (page) => {
  // Auto-dismiss any native browser dialog (beforeunload / "please wait to send" /
  // unsaved-changes) so it never freezes the page and hangs the run_code call until
  // the MCP idle-timeout. Learned the hard way — intermittent 33-min hangs.
  page.on('dialog', d => { d.accept().catch(() => {}); });
  const todo = %s;
  const delayMs = %d;
  const leadDelayMs = %d;
  const RUN_ID = '%s';
  // Ledger is scoped per campaign. Numbering restarts at 1 for every campaign, so a
  // single global ledger made campaign B's #1-N collide with campaign A's spent numbers
  // and skip the entire run. Caught 2026-08-20 when the Capo open house batch refused
  // all 18 against the coffee round's ledger.
  const LEDGER_KEY = '__sendLedger_' + '%s';
  const RUN_BUDGET_MS = %d;
  const PER_EMAIL_MS = %d;
  const LOCK_STALE_MS = 150000;   // a heartbeat older than this means the run died
  const SEED = %s;                // numbers leads.db already records as sent
  const wait = (ms) => page.waitForTimeout(ms);
  const tStart = Date.now();

  // The MCP sandbox has no setTimeout — a setTimeout-based watchdog throws
  // ReferenceError synchronously and fails every email. page.waitForTimeout is the
  // only timer available here. `fn` is passed unstarted so the work never begins
  // unless the race is actually set up.
  const withTimeout = async (fn, ms, label) => {
    let done = false;
    const timer = page.waitForTimeout(ms).then(() => {
      if (!done) throw new Error('WATCHDOG ' + label);
    });
    timer.catch(() => {});   // the losing side must never surface as an unhandled rejection
    try { return await Promise.race([fn(), timer]); }
    finally { done = true; }
  };

  // --- guard 2: claim the run lock. Two loops once drove this same tab at once and
  //     sent every address in the overlap twice. localStorage, not window, so the
  //     lock survives navigating the tab away and back.
  const lock = await page.evaluate(({ id, staleMs, seed, LEDGER_KEY }) => {
    let cur = null;
    try { cur = JSON.parse(localStorage.getItem('__sendLock') || 'null'); } catch (e) {}
    if (cur && cur.id !== id && (Date.now() - cur.beat) < staleMs) {
      return { ok: false, holder: cur.id, ageMs: Date.now() - cur.beat };
    }
    localStorage.setItem('__sendLock', JSON.stringify({ id, beat: Date.now() }));
    let led = [];
    try { led = JSON.parse(localStorage.getItem(LEDGER_KEY) || '[]'); } catch (e) {}
    localStorage.setItem(LEDGER_KEY, JSON.stringify([...new Set([...led, ...seed])]));
    return { ok: true };
  }, { id: RUN_ID, staleMs: LOCK_STALE_MS, seed: SEED, LEDGER_KEY });
  if (!lock.ok) {
    return JSON.stringify({ aborted: 'ANOTHER_RUN_IS_LIVE', holder: lock.holder,
      heartbeatAgeMs: lock.ageMs, sent: 0, sentNums: [],
      note: 'A send loop is still running against this tab. Close the tab to kill it, ' +
            'reconcile Sent Items in a NEW tab, then relaunch.' });
  }

  const cleanupCompose = async () => {
    // Never leave a compose open — it collides with the next iteration's field lookups.
    try {
      for (let i = 0; i < 3; i++) {
        if ((await page.locator('input[aria-label*="subject" i]').count()) === 0) break;
        await page.keyboard.press('Escape');
        await wait(700);
        await page.evaluate(() => {
          const b = [...document.querySelectorAll('button')]
            .find(x => /^discard$/i.test((x.textContent || '').trim()));
          if (b) b.click();
        });
        await wait(700);
      }
    } catch (err) { /* best effort */ }
  };

  async function pollFor(fn, timeout = 12000, step = 250) {
    const t0 = Date.now();
    while (Date.now() - t0 < timeout) { if (await fn()) return true; await wait(step); }
    return false;
  }

  const sendOne = async (e) => {
      await page.evaluate(() => {
        const b = [...document.querySelectorAll('button,[role=button]')]
          .find(x => /^(new mail|new message)$/i.test((x.getAttribute('aria-label')||x.textContent||'').trim()));
        if (b) b.click();
      });
      await page.evaluate(() => {
        const d = [...document.querySelectorAll('button')].find(b=>/dismiss all/i.test(b.textContent||''));
        if (d) d.click();
      });
      const ready = await pollFor(async () =>
        (await page.locator('[aria-label="To"][contenteditable="true"]').count()) > 0 &&
        (await page.locator('input[aria-label*="subject" i]').count()) > 0 &&
        (await page.locator('#Signature').count()) > 0);
      if (!ready) throw new Error('compose fields not ready');
      const toField = page.locator('[aria-label="To"][contenteditable="true"]').first();
      await toField.click();
      await page.keyboard.type(e.to, { delay: 15 });
      await wait(400);
      await page.keyboard.press('Enter');
      await wait(500);
      const subj = page.locator('input[aria-label*="subject" i]').first();
      await subj.click();
      await page.keyboard.type(e.subject, { delay: 8 });
      await wait(250);
      const ins = await page.evaluate((lines) => {
        const sig = document.querySelector('#Signature');
        if (!sig) return 'NO_SIG';
        const frag = document.createDocumentFragment();
        for (const ln of lines) {
          const d = document.createElement('div');
          d.setAttribute('style', 'font-family: Aptos, sans-serif; font-size: 16px; color: rgb(0,0,0);');
          if (ln === '') d.innerHTML = '<br>'; else d.textContent = ln;
          frag.appendChild(d);
        }
        sig.parentNode.insertBefore(frag, sig);
        const body = document.querySelector('[aria-label="Message body"]');
        if (body) body.dispatchEvent(new Event('input', { bubbles: true }));
        return 'ok';
      }, e.lines);
      if (ins !== 'ok') throw new Error('body insert: ' + ins);
      await wait(400);
      const toText = (await toField.innerText().catch(()=> '')).toLowerCase();
      if (!toText.includes(e.to.toLowerCase())) throw new Error('To not chipped: ' + toText.slice(0,40));
      // Strip every image out of the compose before Send. The signature's banner is what
      // triggers Outlook's "please wait to send, inline images still loading" dialog, which
      // stalled the 8/14 batch for 30+ min on a single email. Disclosure is live text in the
      // body, so nothing compliance-bearing rides on the banner. Per-compose only; the saved
      // Outlook signature is never modified.
      const stripped = await page.evaluate(() => {
        const scope = document.querySelector('[aria-label="Message body"]') || document;
        const imgs = [...scope.querySelectorAll('img')];
        imgs.forEach(i => i.remove());
        return imgs.length;
      });
      await wait(600);
      // --- guard 3: record BEFORE the click. If this run dies between Send and the
      //     confirmation check, the number is already spent and no later run will
      //     re-send it. A missed send shows up in Sent-Items reconciliation; a
      //     duplicate cannot be taken back.
      await page.evaluate(({ n, LEDGER_KEY }) => {
        let led = [];
        try { led = JSON.parse(localStorage.getItem(LEDGER_KEY) || '[]'); } catch (e) {}
        if (!led.includes(n)) led.push(n);
        localStorage.setItem(LEDGER_KEY, JSON.stringify(led));
      }, { n: e.n, LEDGER_KEY });
      await page.locator('button[aria-label="Send"]').first().click();
      let closed = false;
      for (let i = 0; i < 40; i++) {
        if ((await page.locator('input[aria-label*="subject" i]').count()) === 0) { closed = true; break; }
        const throttled = await page.evaluate(() =>
          /couldn'?t send|wasn'?t sent|try again later|too many/i.test(document.body.innerText || ''));
        if (throttled) throw new Error('THROTTLE: send blocked toast');
        // "Please wait to send – inline images still loading" dialog: OK, wait, re-Send
        const dlg = await page.evaluate(() => {
          const b = [...document.querySelectorAll('button')].find(x => /^ok$/i.test((x.textContent||'').trim()));
          if (b) { b.click(); return true; } return false;
        });
        if (dlg) { await wait(3500); await page.locator('button[aria-label="Send"]').first().click(); }
        await wait(300);
      }
      if (!closed) throw new Error('compose did not close after Send');
      return stripped;
  };

  const results = [];
  for (const e of todo) {
    // --- guard 1: end by returning, never by being aborted at the idle timeout.
    if (Date.now() - tStart > RUN_BUDGET_MS) {
      results.push({ n: e.n, to: e.to, status: 'skip', detail: 'run budget reached' });
      continue;
    }
    // --- guard 2 (cont): heartbeat, and bail out if another run took the lock.
    const own = await page.evaluate((id) => {
      let cur = null;
      try { cur = JSON.parse(localStorage.getItem('__sendLock') || 'null'); } catch (e) {}
      if (!cur || cur.id !== id) return false;
      cur.beat = Date.now();
      localStorage.setItem('__sendLock', JSON.stringify(cur));
      return true;
    }, RUN_ID);
    if (!own) {
      results.push({ n: e.n, to: e.to, status: 'abort', detail: 'lost the run lock' });
      break;
    }
    // --- guard 3 (cont): never compose a number the ledger already spent.
    const dup = await page.evaluate(({ n, LEDGER_KEY }) => {
      let led = [];
      try { led = JSON.parse(localStorage.getItem(LEDGER_KEY) || '[]'); } catch (e) {}
      return led.includes(n);
    }, { n: e.n, LEDGER_KEY });
    if (dup) {
      results.push({ n: e.n, to: e.to, status: 'skip', detail: 'already in send ledger' });
      continue;
    }

    let status = 'ok', detail = '', stripped = null;
    try {
      stripped = await withTimeout(() => sendOne(e), PER_EMAIL_MS, 'email #' + e.n);
    } catch (err) {
      status = 'fail'; detail = String(err).slice(0, 140);
      await cleanupCompose();
    }
    results.push({ n: e.n, to: e.to, status, detail, imgsStripped: typeof stripped === 'number' ? stripped : null });
    if (e !== todo[todo.length - 1]) await wait(delayMs); // pace BETWEEN sends only; caller spaces batch seams
  }

  await page.evaluate((id) => {   // release the lock so the next batch can start at once
    let cur = null;
    try { cur = JSON.parse(localStorage.getItem('__sendLock') || 'null'); } catch (e) {}
    if (cur && cur.id === id) localStorage.removeItem('__sendLock');
  }, RUN_ID);

  const ok = results.filter(r => r.status === 'ok').map(r => r.n);
  const bad = results.filter(r => r.status === 'fail');
  const skipped = results.filter(r => r.status === 'skip' || r.status === 'abort');
  return JSON.stringify({ sent: ok.length, sentNums: ok, failed: bad.length, failures: bad,
    skipped: skipped.length, skips: skipped, elapsedMin: Math.round((Date.now() - tStart) / 60000) });
}
""" % (data, delay, lead_delay, run_id, campaign, run_budget_ms, per_email_ms, seed)

out = os.path.join(ROOT, "scripts", "_batch_send_generated.js")
open(out, "w").write(JS)
label = ",".join(str(e["n"]) for e in todo)
print(f"Generated {out} for #{label} ({len(todo)} emails), delay {delay}ms")
print(f"  run id {run_id} · budget {run_budget_ms // 60000} min · "
      f"watchdog {per_email_ms // 1000}s/email · ledger seeded with {len(already)} sent")
