#!/usr/bin/env python3
"""Generate a self-contained Playwright run_code_unsafe JS file for a range of
resident emails, with the email data embedded inline (the MCP sandbox has no
fs/require/import). The generated script composes + sends each email paced, and
RETURNS a JSON results array (no file writes). Log sent numbers afterward with
scripts/log_resident_sends.py.

Usage: python3 scripts/gen_batch_send_js.py START END [DELAY_MS]
Writes: scripts/_batch_send_generated.js
"""
import json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
start, end = int(sys.argv[1]), int(sys.argv[2])
delay = int(sys.argv[3]) if len(sys.argv) > 3 else 25000
queue = json.load(open(os.path.join(ROOT, "outreach", "resident_send_queue.json")))
todo = [e for e in queue if start <= e["n"] <= end]
data = json.dumps(todo, ensure_ascii=False)

JS = """async (page) => {
  const todo = %s;
  const delayMs = %d;
  const wait = (ms) => page.waitForTimeout(ms);
  async function pollFor(fn, timeout = 12000, step = 250) {
    const t0 = Date.now();
    while (Date.now() - t0 < timeout) { if (await fn()) return true; await wait(step); }
    return false;
  }
  const results = [];
  for (const e of todo) {
    let status = 'ok', detail = '';
    try {
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
      await page.locator('button[aria-label="Send"]').first().click();
      const closed = await pollFor(async () =>
        (await page.locator('input[aria-label*="subject" i]').count()) === 0, 10000);
      if (!closed) throw new Error('compose did not close after Send');
    } catch (err) {
      status = 'fail'; detail = String(err).slice(0, 120);
    }
    results.push({ n: e.n, to: e.to, status, detail });
    await wait(delayMs); // pace after every send (uniform spacing, incl. batch seams)
  }
  const ok = results.filter(r => r.status === 'ok').map(r => r.n);
  const bad = results.filter(r => r.status === 'fail');
  return JSON.stringify({ sent: ok.length, sentNums: ok, failed: bad.length, failures: bad });
}
""" % (data, delay)

out = os.path.join(ROOT, "scripts", "_batch_send_generated.js")
open(out, "w").write(JS)
print(f"Generated {out} for #{start}-{end} ({len(todo)} emails), delay {delay}ms")
