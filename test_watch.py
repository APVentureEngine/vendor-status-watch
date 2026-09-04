#!/usr/bin/env python3
"""Offline tests for watch.py: the diff engine and the four webhook renderers.
Then an END-TO-END run against a local HTTP webhook receiver with a fake map,
so the whole path (config -> map -> poll -> diff -> POST -> state.json) is
exercised without touching the network or a real chat channel."""
import json, os, sys, threading, tempfile, subprocess, http.server, re
import watch as W

# 0. SHIPPED-COPY GUARD (c143). The file a forker runs is template/watch.py, but this
# test imports product/watch.py — two copies, edited independently, and they HAD
# drifted: product/ still pointed SITE at apventureengine.github.io (404 — org Pages
# builds are frozen) and printed a "/vendors/" URL that HF 302s off-site to a
# huggingface.co 404. Tests that exercise a file nobody ships are worthless, so keep
# them byte-identical and fail loudly the moment they diverge again.
for _f in ("watch.py", "platforms.py"):
    _a, _b = open(_f).read(), open(os.path.join("template", _f)).read()
    assert _a == _b, f"{_f} has drifted from template/{_f} — the shipped copy is template/; sync them"
# HF static Spaces do NOT resolve /dir/ to /dir/index.html; they 302 to huggingface.co/dir
# (a 404). Any directory-style URL in shipped code is therefore a dead link for a user.
for _f in ("watch.py", "platforms.py", os.path.join("template", "watch.py")):
    _bad = re.findall(r"https?://[^\s\"'`]*static\.hf\.space/[A-Za-z0-9_\-/]*/(?=[\s\"'`)|])", open(_f).read())
    assert not _bad, f"{_f}: directory-style URL(s) {_bad} — HF 302s these off-site; use an explicit .html"
print("shipped-copy guard: PASS (watch.py/platforms.py match template/, no directory-style HF URLs)")

def snap(slug, state="ok", incidents=(), error=None):
    return {"vendor": slug.title(), "slug": slug, "platform": "statuspage",
            "status_url": f"https://status.{slug}.com", "state": state, "description": state,
            "incidents": list(incidents), "checked_at": "2026-09-04T05:00:00Z", "error": error}

def inc(i, title, state="investigating", upd="2026-09-04T05:00:00Z"):
    return {"id": i, "title": title, "state": state, "impact": "minor", "url": "https://status.x.com/i/" + i,
            "started_at": "2026-09-04T04:50:00Z", "updated_at": upd, "body": "body " + title}

# 1. first poll, no incidents -> no events
ev, st = W.diff_vendor(None, snap("github"), 3)
assert [e["event"] for e in ev] == ["watching"] and st["incidents"] == {} and st["fails"] == 0
# 1b. first sight WITH standing incidents -> one 'watching' line, incidents baselined, no 'opened'
ev, stb = W.diff_vendor(None, snap("twilio", "degraded", [inc("m1", "carrier maint", "maintenance"), inc("m2", "delays")]), 3)
assert [e["event"] for e in ev] == ["watching"] and "2 open incident" in ev[0]["detail"] and set(stb["incidents"]) == {"m1", "m2"}
ev, _ = W.diff_vendor(stb, snap("twilio", "degraded", [inc("m1", "carrier maint", "maintenance"), inc("m2", "delays")]), 3)
assert ev == []
# 1c. mute_maintenance: maintenance items never open, never resolve
ev, stc = W.diff_vendor(None, snap("twilio", "ok"), 3, mute_maintenance=True)
ev, stc = W.diff_vendor(stc, snap("twilio", "maintenance", [inc("m1", "carrier maint", "maintenance")]), 3, mute_maintenance=True)
assert ev == [] and stc["incidents"] == {}, (ev, stc)
ev, stc = W.diff_vendor(stc, snap("twilio", "degraded", [inc("m1", "carrier maint", "maintenance"), inc("r1", "real")]), 3, mute_maintenance=True)
assert [e["event"] for e in ev] == ["opened"] and ev[0]["title"] == "real"
# 2. incident appears -> opened
ev, st = W.diff_vendor(st, snap("github", "degraded", [inc("a1", "API slow")]), 3)
assert [e["event"] for e in ev] == ["opened"] and ev[0]["title"] == "API slow"
# 3. same incident, nothing changed -> silence
ev, st2 = W.diff_vendor(st, snap("github", "degraded", [inc("a1", "API slow")]), 3)
assert ev == []
# 4. incident state changes -> updated
ev, st3 = W.diff_vendor(st2, snap("github", "degraded", [inc("a1", "API slow", "monitoring", "2026-09-04T05:10:00Z")]), 3)
assert [e["event"] for e in ev] == ["updated"] and ev[0]["incident_state"] == "monitoring"
# 5. incident disappears -> resolved
ev, st4 = W.diff_vendor(st3, snap("github", "ok"), 3)
assert [e["event"] for e in ev] == ["resolved"] and st4["incidents"] == {}
# 6. errors: no alert on 1st/2nd, ONE alert on 3rd, silence on 4th; known incidents kept, not resolved
s = st3
for n in (1, 2):
    ev, s = W.diff_vendor(s, snap("github", "unknown", error="http 503"), 3)
    assert ev == [] and s["fails"] == n and "a1" in s["incidents"], (n, ev, s)
ev, s = W.diff_vendor(s, snap("github", "unknown", error="http 503"), 3)
assert [e["event"] for e in ev] == ["unreachable"] and s["unreachable"] and ev[0]["consecutive_failures"] == 3
ev, s = W.diff_vendor(s, snap("github", "unknown", error="http 503"), 3)
assert ev == [] and s["fails"] == 4
# 7. recovery -> recovered + (incident still there, no duplicate 'opened')
ev, s = W.diff_vendor(s, snap("github", "degraded", [inc("a1", "API slow", "monitoring", "2026-09-04T05:10:00Z")]), 3)
assert [e["event"] for e in ev] == ["recovered"], ev
# 8. recovery where the incident vanished meanwhile -> recovered + resolved
ev2, _ = W.diff_vendor(s if False else {"incidents": {"a1": {"title": "API slow"}}, "fails": 3, "unreachable": True},
                       snap("github", "ok"), 3)
assert sorted(e["event"] for e in ev2) == ["recovered", "resolved"], ev2
# 9. two incidents at once, one new -> exactly one opened
_, s9 = W.diff_vendor(None, snap("aws", "major", [inc("x", "A")]), 3)
_, s9 = W.diff_vendor(s9, snap("aws", "major", [inc("x", "A")]), 3)
ev, _ = W.diff_vendor(s9, snap("aws", "major", [inc("x", "A"), inc("y", "B")]), 3)
assert [e["event"] for e in ev] == ["opened"] and ev[0]["title"] == "B"
print("diff engine: PASS (12 scenarios)")

# renderers
sample = [{"event": "opened", "vendor": "GitHub", "slug": "github", "state": "degraded", "title": "API slow",
           "incident_state": "investigating", "impact": "minor", "detail": "We are investigating.",
           "url": "https://www.githubstatus.com", "started_at": None},
          {"event": "unreachable", "vendor": "Acme", "slug": "acme", "state": "unknown", "detail": "http 503",
           "url": "https://status.acme.com", "consecutive_failures": 3}]
for fmt, must in (("slack", "blocks"), ("discord", "embeds"), ("teams", "attachments"), ("json", "events")):
    p = W.render(sample, fmt)
    assert must in p, (fmt, p.keys())
    json.dumps(p)  # serializable
assert W.detect_format("https://hooks.slack.com/services/T/B/x", "auto") == "slack"
assert W.detect_format("https://discord.com/api/webhooks/1/2", "auto") == "discord"
assert W.detect_format("https://x.webhook.office.com/webhookb2/…", "auto") == "teams"
assert W.detect_format("https://example.com/hook", "auto") == "json"
assert W.detect_format("https://example.com/hook", "slack") == "slack"
s = W.render(sample, "slack")
assert "UNKNOWN, not OK" in s["text"] and "<https://www.githubstatus.com|status page>" in s["blocks"][0]["text"]["text"]
print("renderers: PASS (slack/discord/teams/json)")

# ---- end-to-end with a local webhook receiver and a stubbed platform check
received = []
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); received.append(json.loads(self.rfile.read(n)))
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

tmp = tempfile.mkdtemp()
for f in ("watch.py", "platforms.py"):
    open(os.path.join(tmp, f), "w").write(open(f).read())
json.dump({"generated_at": "2026-09-04T00:00:00Z", "vendors": [
    {"slug": "github", "name": "GitHub", "platform": "statuspage", "base": "https://www.githubstatus.com", "supported": True},
    {"slug": "stripe", "name": "Stripe", "platform": "unknown-html", "base": "https://status.stripe.com", "supported": False, "note": "bespoke page"}]},
    open(os.path.join(tmp, "vendors.json"), "w"))
json.dump({"vendors": ["github", "stripe", "nope"], "webhook": f"http://127.0.0.1:{port}/hook",
           "format": "slack", "map_url": "", "unreachable_after": 1}, open(os.path.join(tmp, "config.json"), "w"))
# stub the network: platforms.check is monkeypatched through a sitecustomize-free trick — a stub module
open(os.path.join(tmp, "platforms.py"), "a").write('''
_SCRIPT = {"github": [dict(state="ok", incidents=[]), dict(state="degraded", incidents=[{"id":"i1","title":"Git ops slow","state":"investigating","impact":"minor","url":"https://www.githubstatus.com/i/i1","started_at":"t0","updated_at":"t0","body":"looking"}])]}
import itertools, os as _os
def check(vendor):
    n = int(open(_os.environ["STEP"]).read())
    s = vendor["slug"]
    if s == "stripe":
        return _blank(vendor["name"], s, vendor["platform"], vendor["base"], error="bespoke page")
    d = _SCRIPT[s][min(n, 1)]
    out = _blank(vendor["name"], s, vendor["platform"], vendor["base"], state=d["state"], desc=d["state"])
    out["incidents"] = d["incidents"]; return out
''')
step = os.path.join(tmp, "step"); env = dict(os.environ, STEP=step)
def run(n, *args):
    open(step, "w").write(str(n))
    r = subprocess.run([sys.executable, "watch.py", *args], cwd=tmp, env=env, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
rc, out = run(0)
assert rc == 0 and "unknown vendor slug(s) not in map: ['nope']" in out and "stripe: bespoke page" in out, out
assert len(received) == 1 and "CANNOT SEE" in received[0]["text"] and "WATCHING" in received[0]["text"], received
st = json.load(open(os.path.join(tmp, "state.json")))
assert st["vendors"]["github"]["state"] == "ok" and st["vendors"]["stripe"]["unreachable"] is True
rc, out = run(0); assert rc == 0 and "no changes" in out and len(received) == 1, out   # idempotent
rc, out = run(1); assert rc == 0 and "opened" in out and len(received) == 2, out
assert "Git ops slow" in received[1]["text"] and received[1]["blocks"][0]["type"] == "section"
rc, out = run(1, "--dry-run"); assert rc == 0 and "no changes" in out and len(received) == 2
# failing webhook must NOT save state (events re-fire next run)
json.dump(json.load(open(os.path.join(tmp, "config.json"))) | {"webhook": f"http://127.0.0.1:{port}/", "unreachable_after": 1},
          open(os.path.join(tmp, "config.json"), "w"))
class Bad(H):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); self.rfile.read(n); self.send_response(500); self.end_headers()
srv.RequestHandlerClass = Bad
before = open(os.path.join(tmp, "state.json")).read()
rc, out = run(0)   # github goes back to ok -> 'resolved' event -> webhook 500
assert rc == 2 and "state NOT saved" in out and open(os.path.join(tmp, "state.json")).read() == before, out
print(f"end-to-end: PASS (local webhook received {len(received)} payloads; state.json round-trips; failed POST keeps state)")
print("ALL PASS")
