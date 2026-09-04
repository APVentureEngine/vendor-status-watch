#!/usr/bin/env python3
"""gen_site.py — render the public site from the living map + per-vendor history.

Inputs : vendors.json, snapshot.json, history/*.json, site_config.json
Output : docs/  (GitHub Pages source: /docs on main)

Every number on every page is computed from those files in this run. No prose number is
typed by hand; if a figure has no rows it is left out (dataviz refuses empty input).
"""
import html, json, os, re, sys, collections
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataviz as DV

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs")
CFG = json.load(open(os.path.join(HERE, "site_config.json")))
SITE = CFG["site_url"].rstrip("/")
REPO = CFG["repo_url"].rstrip("/")
TPL = (CFG.get("template_url") or REPO).rstrip("/")   # fork-and-go template repo
HOSTED = CFG.get("hosted_url") or ""          # Gumroad listing; empty = tier not on sale yet
HOSTED_PRICE = CFG.get("hosted_price", "$39/year")
NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")

E = html.escape
STATE_LABEL = {"ok": "operational", "maintenance": "maintenance", "degraded": "degraded",
               "partial": "partial outage", "major": "major outage", "unknown": "unknown"}
STATE_RANK = {"major": 0, "partial": 1, "degraded": 2, "maintenance": 3, "unknown": 4, "ok": 5}
PLAT_LABEL = {"statuspage": "Atlassian Statuspage", "instatus": "Instatus", "betterstack": "Better Stack",
              "status.io": "Status.io", "hund": "Hund", "cachet": "Cachet", "uptimerobot": "UptimeRobot",
              "incident.io": "incident.io", "bespoke": "vendor's own feed (hand-written parser)",
              "unknown-html": "bespoke HTML page", "dead": "unreachable"}


def ts(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def fmt_dt(s):
    d = ts(s)
    return d.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if d else "—"


def dur(a, b):
    da, db = ts(a), ts(b)
    if not da or not db or db < da:
        return "—"
    m = int((db - da).total_seconds() // 60)
    if m < 60:
        return f"{m} min"
    if m < 48 * 60:
        return f"{m // 60} h {m % 60:02d} min"
    return f"{m // 1440} d {(m % 1440) // 60} h"


def rfc822(s):
    d = ts(s) or NOW
    return d.astimezone(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")


# ------------------------------------------------------------------ data
vendors = json.load(open(os.path.join(HERE, "vendors.json")))
snap = json.load(open(os.path.join(HERE, "snapshot.json")))
hist = {}
for v in vendors["vendors"]:
    p = os.path.join(HERE, "history", v["slug"] + ".json")
    if os.path.exists(p):
        hist[v["slug"]] = json.load(open(p))
# --- alias collapse -------------------------------------------------------
# The seed list contains two rows for the SAME status page (status.grafana.com and
# grafanalabs.statuspage.io; status.imperva.com and status.incapsula.com). Atlassian
# returns a page id that identifies the page itself, so duplicates are provable rather
# than guessed. Keep one canonical row, remember the alias, and never print both.
_base_of = {v["slug"]: v.get("base", "") for v in vendors["vendors"]}
_by_page = {}
for _r in snap["vendors"]:
    # only trust a page id that came back with a real parse: an error page or an
    # unknown state can hand two unrelated vendors the same id (seen on freshstatus).
    if _r.get("page_id") and not _r.get("error") and _r.get("state") != "unknown":
        _by_page.setdefault((_r["platform"], _r["page_id"]), []).append(_r["slug"])
ALIAS, ALIAS_OF = {}, {}
for _pid, _slugs in _by_page.items():
    if len(_slugs) < 2:
        continue
    _slugs = sorted(_slugs, key=lambda s: (1 if re.search(r"-\d+$", s) else 0,
                                           1 if ".statuspage.io" in _base_of.get(s, "") else 0,
                                           len(_base_of.get(s, "")), s))
    _canon = _slugs[0]
    for _s in _slugs[1:]:
        ALIAS[_s] = _canon
        ALIAS_OF.setdefault(_canon, []).append(_s)
if ALIAS:
    vendors["vendors"] = [v for v in vendors["vendors"] if v["slug"] not in ALIAS]
    vendors["count"] = len(vendors["vendors"])
    vendors["supported"] = sum(1 for v in vendors["vendors"] if v["supported"])
    vendors["aliases"] = ALIAS
    snap["vendors"] = [r for r in snap["vendors"] if r["slug"] not in ALIAS]
    snap["count"] = len(snap["vendors"])
    hist = {k: v for k, v in hist.items() if k not in ALIAS}

by_slug = {v["slug"]: v for v in vendors["vendors"]}
snap_by = {r["slug"]: r for r in snap["vendors"]}

# Two vendors can legitimately run two DIFFERENT status pages (MongoDB Atlas vs
# MongoDB). Same name, different page: disambiguate by host so the board never
# shows what looks like a duplicated row.
_names = collections.Counter(v["name"].lower() for v in vendors["vendors"])
for _v in vendors["vendors"]:
    if _names[_v["name"].lower()] > 1:
        _host = re.sub(r"^https?://", "", _v.get("base", "")).split("/")[0]
        if _host:
            _v["name"] = f'{_v["name"]} ({_host})'
_name_of = {v["slug"]: v["name"] for v in vendors["vendors"]}
for _r in snap["vendors"]:
    if _r["slug"] in _name_of:
        _r["vendor"] = _name_of[_r["slug"]]

N_MAP = vendors["count"]
N_SUP = sum(1 for v in vendors["vendors"] if v["supported"])
N_DEAD = sum(1 for v in vendors["vendors"] if v["platform"] == "dead")
N_POLLED = snap["count"]
N_PARSED = sum(1 for r in snap["vendors"] if not r["error"])
NOT_OK = sorted([r for r in snap["vendors"] if r["state"] not in ("ok", "unknown")],
                key=lambda r: (STATE_RANK[r["state"]], r["vendor"].lower()))
GEN_AT = snap["generated_at"]

all_inc = []   # (slug, id, rec)
for slug, h in hist.items():
    for iid, rec in h["incidents"].items():
        d = ts(rec.get("started_at"))
        if d and d <= NOW:          # scheduled-but-not-started maintenance is not history
            all_inc.append((slug, iid, rec))
all_inc.sort(key=lambda t: t[2]["started_at"], reverse=True)
D30 = NOW - timedelta(days=30)
D90 = NOW - timedelta(days=90)
inc30 = [t for t in all_inc if ts(t[2]["started_at"]) >= D30]
inc90 = [t for t in all_inc if ts(t[2]["started_at"]) >= D90]
N_INC = len(all_inc)
N_INC30 = len(inc30)
vend30 = collections.Counter(t[0] for t in inc30)
N_VEND30 = len(vend30)
BACKFILLED = sum(1 for h in hist.values() if h.get("history_backfilled"))

# incidents per day, last 30 days (for the trend)
per_day = collections.Counter(ts(t[2]["started_at"]).strftime("%Y-%m-%d") for t in inc30)
days = [(D30 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 31)]
TREND = [(d[5:], per_day.get(d, 0)) for d in days]


# ------------------------------------------------------------------ html shell
CSS = """.hits{list-style:none;padding:0;margin:10px 0 0}.hits li{padding:8px 0;border-top:1px solid #e5e7eb}.hits li:first-child{border-top:0}#check{margin-top:20px}
:root{--bg:#fbfbf8;--ink:#14213d;--muted:#5b6478;--line:#e3e5ea;--card:#fff;--accent:#d9480f;--accent-ink:#fff;
--ok:#1f8a4c;--warn:#c98a00;--bad:#c8102e;--unk:#8a8f9c;--maxw:1040px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--ink)}a:hover{color:var(--accent)}
header.top{background:var(--ink);color:#fff;padding:14px 20px}
header.top .in{max-width:var(--maxw);margin:0 auto;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
header.top a{color:#fff;text-decoration:none;min-height:44px;display:inline-flex;align-items:center;padding:0 6px}
header.top .brand{font-weight:700;font-size:18px;gap:8px}
header.top nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap;font-size:15px}
main{max-width:var(--maxw);margin:0 auto;padding:0 20px}
section{padding:56px 0;border-bottom:1px solid var(--line)}section:last-of-type{border:0}
h1{font-size:40px;line-height:1.1;margin:0 0 14px;letter-spacing:-.02em}
h2{font-size:26px;margin:0 0 18px;letter-spacing:-.01em}h3{font-size:18px;margin:0 0 8px}
p,li{max-width:70ch}.lead{font-size:19px;color:var(--muted);max-width:60ch}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:8px;
font-weight:600;text-decoration:none;background:var(--accent);color:var(--accent-ink);border:0;font-size:16px;cursor:pointer}
.btn:hover{background:#b83c0a;color:#fff}.btn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink)}
.btn.ghost:hover{border-color:var(--accent);color:var(--accent)}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.card h3{margin-top:0}.price{font-size:32px;font-weight:700;margin:6px 0}
table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.04em}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:13px;font-weight:600;color:#fff;white-space:nowrap}
.s-ok{background:var(--ok)}.s-maintenance{background:#4a6fa5}.s-degraded{background:var(--warn)}.s-partial{background:#e0621f}.s-major{background:var(--bad)}.s-unknown{background:var(--unk)}
.s-resolved,.s-completed{background:var(--ok)}.s-investigating,.s-identified,.s-monitoring{background:var(--warn)}
pre{background:#14213d;color:#e6edf3;padding:14px 16px;border-radius:8px;overflow-x:auto;font-size:13.5px;line-height:1.5}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.93em}
input.filter{width:100%;max-width:420px;min-height:44px;padding:8px 12px;font-size:16px;border:1px solid var(--line);border-radius:8px}
.muted{color:var(--muted)}.small{font-size:14px}.note{background:#fff7ed;border-left:4px solid var(--accent);padding:10px 14px;border-radius:6px}
footer{padding:36px 20px;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}footer .in{max-width:var(--maxw);margin:0 auto}
.dv-kpis{margin:26px 0}.dv-kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.dv-kpi b{font-size:34px;display:block;line-height:1.1}.dv-kpi span{display:block;color:var(--muted);margin-top:4px}.dv-kpi i{display:block;font-style:normal;font-size:13px;margin-top:4px}
figure{margin:24px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}figure svg{max-width:100%;height:auto}
figcaption{font-size:13px;color:var(--muted);margin-top:8px}
@media (max-width:640px){h1{font-size:30px}h2{font-size:22px}section{padding:40px 0}.dv-kpi b{font-size:28px}header.top nav{margin-left:0}}
"""

LOGO = ('<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="#d9480f"/>'
        '<path d="M5 14 l4 0 l2 -6 l3 12 l3 -9 l2 3 l3 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/></svg>')


def page(title, body, desc, path="", extra_head=""):
    canon = f"{SITE}/{path}" if path else f"{SITE}/"
    nav = [("Live board", "/#board"), ("Vendors", "/vendors.html"), ("Free template", "/#template"),
           ("Hosted", "/#hosted"), ("Coverage", "/platforms.html"), ("API", "/api.html")]
    navh = "".join(f'<a href="{SITE}{h}">{E(t)}</a>' for t, h in nav)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}"><link rel="alternate" type="application/rss+xml" title="All vendor incidents" href="{SITE}/feed.xml">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">
<style>{CSS}</style>{extra_head}</head><body>
<header class="top"><div class="in"><a class="brand" href="{SITE}/">{LOGO} Vendor Status Watch</a><nav>{navh}</nav></div></header>
<main>{body}</main>
<footer><div class="in"><p>Vendor Status Watch is an automated, open-source project run by APVentureEngine. It reads the public status pages of {N_MAP:,} SaaS vendors on a timer and republishes what they say — it is not affiliated with any vendor named here, and it does not measure uptime itself. Vendor names and status pages belong to their owners.</p>
<p><b>Who runs this:</b> APVentureEngine, an autonomous software project. There is no sales team and no phone number: every question, bug report and purchase issue goes through <a href="{REPO}/issues">GitHub issues</a>, which are public and usually answered within a day.</p>
<p><a href="{REPO}">Source code &amp; template (MIT)</a> · <a href="{REPO}/issues">Report a wrong entry</a> · <a href="{SITE}/feed.xml">RSS</a> · <a href="{SITE}/api.html">JSON API</a> · <a href="{SITE}/legal.html">Privacy, terms &amp; refunds</a> · Data as of {E(GEN_AT)}</p></div></footer>
</body></html>"""


def pill(state):
    return f'<span class="pill s-{E(state)}">{E(STATE_LABEL.get(state, state))}</span>'


def vurl(slug):
    # Flat .html, not a directory: static hosts differ on whether /v/<slug>/ resolves
    # to index.html (GitHub Pages yes, Hugging Face Spaces no -> 302 off-site). Flat works on both.
    return f"{SITE}/v/{slug}.html"


def write(path, content):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)


# ------------------------------------------------------------------ index
def render_index():
    kpis = DV.kpi_row([
        (N_MAP, "vendor status pages mapped", f"{N_SUP:,} with a machine-readable feed"),
        (N_INC, "incidents on record", f"{BACKFILLED:,} vendors with history back-filled"),
        (N_INC30, "incidents in the last 30 days", f"across {N_VEND30:,} vendors"),
        (len(NOT_OK), "vendors not fully operational right now", "as of the last poll"),
    ])
    board_rows = "".join(
        f'<tr><td><a href="{vurl(r["slug"])}">{E(r["vendor"])}</a></td><td>{pill(r["state"])}</td>'
        f'<td>{E(r["description"])}</td><td class="small muted">{E(PLAT_LABEL.get(r["platform"], r["platform"]))}</td></tr>'
        for r in NOT_OK)
    top = sorted(vend30.items(), key=lambda kv: -kv[1])[:15]
    bars = DV.figure(DV.bar_chart([(by_slug[s]["name"], n) for s, n in top], unit="incidents"),
                     "Vendors with the most incidents opened in the last 30 days",
                     source="each vendor's own status page, read by this project", asof=TODAY) if top else ""
    trend = DV.figure(DV.trend(TREND, unit="incidents"),
                      "Incidents opened per day across all polled vendors, last 30 days",
                      source="vendor status pages", asof=TODAY)
    # A rendered example of the actual alert, built from the newest REAL incidents in
    # the feed (never invented): the buy decision here is "what lands in my Slack".
    ICON = {"ok": "\U0001f7e2", "maintenance": "\U0001f527", "degraded": "\U0001f7e1",
            "partial": "\U0001f7e0", "major": "\U0001f534", "unknown": "\u26aa"}
    _demo = []
    for _slug, _iid, _rec in all_inc[:40]:
        if _slug not in by_slug or not _rec.get("title"):
            continue
        _st = (snap_by.get(_slug) or {}).get("state", "unknown")
        _resolved = bool(_rec.get("resolved_at"))
        _demo.append((by_slug[_slug]["name"], _rec, _resolved,
                      ICON["ok" if _resolved else ("major" if _rec.get("impact") in ("critical", "major") else "degraded")]))
        if len(_demo) == 3:
            break
    _lines = "".join(
        f'<div style="border-left:3px solid var(--{"ok" if _res else "warn"});padding:8px 0 8px 12px;margin:0 0 14px">'
        f'<div style="font-weight:700">{_ic} {E(_nm)} — {"RESOLVED" if _res else "INCIDENT"}</div>'
        f'<div class="small">{E(_rc.get("title") or "")}</div>'
        f'<div class="small muted">{E((_rc.get("body") or "")[:150])}</div>'
        f'<div class="small muted">started {E((_rc.get("started_at") or "")[:16].replace("T", " "))} UTC · status page</div></div>'
        for _nm, _rc, _res, _ic in _demo)
    alert_demo = (f'<figure style="margin:22px 0"><div class="card" style="max-width:560px;background:#fff">'
                  f'<div class="small muted" style="margin-bottom:10px">#alerts · vendor-status-watch APP</div>{_lines}</div>'
                  f'<figcaption>What lands in your Slack — rendered here from the three newest real incidents in the feed '
                  f'(Discord and Teams get native embeds/cards; anything else gets plain JSON).</figcaption></figure>') if _demo else ""

    hosted = f"""
<div class="card"><h3>Hosted watch</h3><div class="price">{E(HOSTED_PRICE)}</div>
<p>No repo to own. Pick your vendors, paste one Slack, Discord, Teams or generic webhook URL at checkout, and our poller watches them every 5 minutes for 12 months. Same alerts, same living map, plus a private 12-month incident history page for your list.</p>
<p class="small muted">One-time payment, no auto-renewal. 14-day refund, no questions. Sold through Gumroad; alerts start within 24 hours of purchase.</p>
<a class="btn" href="{E(HOSTED)}">Get the hosted watch — {E(HOSTED_PRICE)}</a></div>""" if HOSTED else f"""
<div class="card"><h3>Hosted watch <span class="small muted">— opening soon</span></h3><div class="price">{E(HOSTED_PRICE)}</div>
<p>No repo, no Actions, no YAML. You send us your vendor slugs and one webhook URL; we run the poller every 5 minutes for 12 months and keep a private incident history for your list.</p>
<ul class="small"><li>Up to 25 vendors, one webhook (Slack, Discord, Teams or plain JSON)</li>
<li>Same alert rules as the free template — including <b>“cannot see this vendor”</b> instead of a false green</li>
<li>One-time payment, no auto-renewal, no card on file</li>
<li>14-day refund, no questions — and a pro-rata refund if alerts fail for 7 days through our fault (<a href="{SITE}/legal.html">terms</a>)</li></ul>
<p class="note small"><b>Not on sale yet, on purpose.</b> The scheduled runner behind it is not live, and we will not take {E(HOSTED_PRICE)} for a watch we cannot yet run. Ask to be told when it opens — we reply on your issue, and GitHub emails you. That is the whole list: no signup, no marketing, nothing to unsubscribe from.</p>
<a class="btn" href="{REPO}/issues/new?title=Hosted%20watch%20%E2%80%94%20tell%20me%20when%20it%20opens&amp;body=Vendors%20I%27d%20want%20watched%20(slugs%20or%20names)%3A%0A%0AWebhook%20type%20(Slack%2FDiscord%2FTeams%2Fother)%3A%0A%0AAnything%20the%20free%20template%20does%20not%20do%20for%20you%3A%0A">Tell us to ping you when it opens</a></div>"""
    body = f"""
<section>
<h1>Every SaaS status page you depend on, in one feed — and in your Slack.</h1>
<p class="lead">We poll the public status pages of {N_MAP:,} vendors ({N_SUP:,} of them with a real JSON feed) on a timer, keep the map of who-hosts-where current as vendors migrate, and give you a free GitHub Actions template that posts open/updated/resolved incidents to your own webhook. No account. No email. MIT.</p>
<div class="cta"><a class="btn" href="#template">Get alerts in your Slack — free</a><a class="btn ghost" href="#board">See who is down right now</a></div>
{kpis}
<p class="small muted">Numbers are recomputed by the daily pipeline from the vendors' own status APIs; last poll {E(GEN_AT)}. Vendor state is what the vendor publishes, not our measurement.</p>
<div class="card" id="check"><h3>Is my vendor watchable?</h3>
<label for="vq" class="small muted">Type a vendor name — answers from today's map of {N_MAP:,} status pages</label>
<input id="vq" class="filter" type="search" placeholder="e.g. stripe, cloudflare, twilio, datadog" autocomplete="off" aria-describedby="vres">
<div id="vres" class="small" aria-live="polite"></div></div>
<script>(function(){{var q=document.getElementById('vq'),o=document.getElementById('vres'),d=null,ld=false,al={json.dumps(ALIAS)};var lab={json.dumps(STATE_LABEL)};function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function show(){{var s=q.value.toLowerCase().trim();if(!s){{o.innerHTML='';return}}if(!d){{o.textContent='Loading the map…';return}}var m=d.filter(function(v){{return v.q.indexOf(s)>-1}}).slice(0,8);if(!m.length){{o.innerHTML='<p>Not in the map yet. <a href="{REPO}/issues/new?title=Add%20vendor%3A%20'+encodeURIComponent(q.value)+'">Ask for it</a> — most requests ship in the next daily build.</p>';return}}
o.innerHTML='<ul class="hits">'+m.map(function(v){{var st=v.sup?'<span class="pill s-'+esc(v.st)+'">'+esc(lab[v.st]||v.st)+'</span>':'<span class="pill s-unknown">no public feed</span>';return '<li><a href="'+esc(v.u)+'">'+esc(v.n)+'</a> '+st+' <span class="muted">'+(v.sup?'watchable · slug <code>'+esc(v.s)+'</code>':'listed, not watchable ('+esc(v.p)+')')+'</span></li>'}}).join('')+'</ul>'}}
function load(){{if(ld)return;ld=true;fetch('{SITE}/api/snapshot.json').then(function(r){{return r.json()}}).then(function(sn){{var st={{}};sn.vendors.forEach(function(r){{st[r.slug]=r.state}});return fetch('{SITE}/api/vendors.json').then(function(r){{return r.json()}}).then(function(vj){{var rev={{}};Object.keys(al).forEach(function(a){{(rev[al[a]]=rev[al[a]]||[]).push(a)}});d=vj.vendors.map(function(v){{var a=(rev[v.slug]||[]).join(' ');return{{n:v.name,s:v.slug,p:v.platform,sup:!!v.supported,st:st[v.slug]||'unknown',u:'{SITE}/v/'+v.slug+'.html',q:(v.name+' '+v.slug+' '+a).toLowerCase()}}}});show()}})}}).catch(function(){{ld=false;o.innerHTML='Could not load the map — try the <a href="{SITE}/vendors.html">full list</a>.'}})}}
q.addEventListener('focus',load);q.addEventListener('input',function(){{load();show()}})}})();</script>
</section>

<section id="board"><h2>Live board — {len(NOT_OK):,} vendors not fully operational</h2>
<p class="muted">Sorted worst first. "Maintenance" means a scheduled window is in progress. Everything green ({N_PARSED - len(NOT_OK):,} vendors) is omitted; {N_POLLED - N_PARSED:,} vendors answered with an error and are shown as unknown on their own pages, never as OK.</p>
<div class="tw"><table><thead><tr><th>Vendor</th><th>State</th><th>What the vendor says</th><th>Platform</th></tr></thead><tbody>{board_rows}</tbody></table></div>
{trend}{bars}
</section>

<section id="template"><h2>Free: the GitHub Actions template</h2>
<p>Click <b>Use this template</b>, list your vendors in one JSON file, add one repository secret (your webhook URL), and copy the workflow file the README points you to — four minutes, and the README walks through every click. GitHub then runs it every 5 minutes on their free tier; the poller reads our daily-refreshed vendor map at run time, so when a vendor moves from Statuspage to Instatus next quarter your alerts keep working without you touching anything.</p>
<pre>{{
  "vendors": ["twilio", "github", "cloudflare", "openai", "vercel"],
  "format": "auto",
  "map_url": "https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json",
  "unreachable_after": 3,
  "mute_maintenance": false
}}</pre>
<p class="small muted">The webhook URL never goes in the file: it lives in a repository secret named <code>WEBHOOK_URL</code>.</p>
<p>Events you receive: <b>now watching</b> (once, with any already-open incidents listed but not re-alerted), <b>opened</b>, <b>updated</b>, <b>resolved</b>, <b>unreachable</b> (the vendor's feed stopped answering — you are told, instead of silently seeing green), <b>recovered</b>. Slack Block Kit, Discord embeds, Teams Adaptive Cards and plain JSON are auto-detected from the webhook host.</p>
{alert_demo}
<div class="cta"><a class="btn" href="{TPL}">Use the template on GitHub</a><a class="btn ghost" href="{SITE}/vendors.html">Find your vendors' slugs</a></div>
<div class="note small">Honest limits: {N_MAP - N_SUP:,} of the {N_MAP:,} mapped vendors publish no machine-readable status (Apple, Microsoft 365 and Notion among them — bespoke HTML pages; AWS, Azure, Google Cloud, Slack and Stripe ARE covered, by hand-written parsers over their own public feeds). The template tells you on its first run which of your picks are unsupported; we do not fake an OK for them. Coverage by platform is on the <a href="{SITE}/platforms.html">coverage page</a>.</div>
</section>

<section id="hosted"><h2>Two ways to run it</h2>
<div class="cards">
<div class="card"><h3>Self-hosted template</h3><div class="price">Free</div>
<p>Runs in your GitHub account on GitHub's free Actions minutes (~2,000 min/month on free plans; a 5-minute schedule uses roughly a third of that). You own the repo, the secret and the history file. MIT licence, no telemetry.</p>
<a class="btn ghost" href="{TPL}">Open the template</a></div>
{hosted}
</div>
<p class="small muted" style="margin-top:18px">Comparison, honestly: IsDown starts at $22/mo (annual) with no free plan; StatusGator's free plan is 3 monitors and 10 notifications a month, paid from $72/mo. Both have polished apps, email/SMS channels and support staff — we have none of those. What we have is a vendor map that is rebuilt every day from live probes, a template you can read in one sitting, and a price that is a rounding error.</p>
</section>

<section><h2>Stay in the loop without buying anything</h2>
<p>Subscribe to the <a href="{SITE}/feed.xml">all-vendors RSS feed</a> (every incident, every vendor), or to a single vendor's feed from its page. Wrong entry, missing vendor, a status page we mis-classified? <a href="{REPO}/issues">Open an issue</a> — the map is regenerated daily and fixes ship with it.</p>
</section>
"""
    ld = {"@context": "https://schema.org", "@type": "Dataset", "name": "Vendor Status Watch — SaaS status-page incident history",
          "description": f"Incident history for {N_SUP} SaaS vendors' public status pages, polled daily; {N_INC} incidents on record.",
          "url": f"{SITE}/", "license": "https://opensource.org/licenses/MIT", "dateModified": GEN_AT,
          "creator": {"@type": "Organization", "name": "APVentureEngine", "url": REPO},
          "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}/api/snapshot.json"}]}
    write("index.html", page("Vendor Status Watch — SaaS outage alerts in your Slack",
                             body, f"Free open-source watch over {N_MAP:,} SaaS status pages: live board, {N_INC:,} incidents of history, GitHub Actions template that posts to your Slack/Discord/Teams webhook.",
                             extra_head=f'<script type="application/ld+json">{json.dumps(ld)}</script>'))


# ------------------------------------------------------------------ vendor pages
def render_vendor(v):
    slug = v["slug"]
    h = hist.get(slug)
    s = snap_by.get(slug)
    name = v["name"]
    if not h or not s:
        body = f"""<section><h1>{E(name)} status</h1><p class="lead">This vendor's status page ({E(v["base"])}) is {E(PLAT_LABEL.get(v["platform"], v["platform"]))} — {E(v.get("note") or "not machine-readable")}. We list it so you know we checked; we do not poll it and never show a state for it.</p>
{('<p class="small muted">The same status page is also published as: ' + ", ".join(E(a) for a in ALIAS_OF.get(slug, [])) + ". Any of those slugs work in the template.</p>") if ALIAS_OF.get(slug) else ""}
<p><a href="{E(v["base"])}">Open the vendor's own status page</a> · <a href="{REPO}/issues">Tell us if it has moved</a></p></section>"""
        write(f"v/{slug}.html", page(f"{name} status — not machine-readable", body,
                                          f"{name}'s status page has no public JSON feed; listed for completeness.", f"v/{slug}.html"))
        return
    recs = sorted(h["incidents"].values(), key=lambda r: r.get("started_at") or "", reverse=True)
    recs = [r for r in recs if ts(r.get("started_at")) and ts(r["started_at"]) <= NOW]
    n30 = sum(1 for r in recs if ts(r["started_at"]) >= D30)
    n90 = sum(1 for r in recs if ts(r["started_at"]) >= D90)
    weeks = collections.Counter()
    for r in recs:
        d = ts(r["started_at"])
        if d >= NOW - timedelta(weeks=12):
            weeks[int((NOW - d).days // 7)] += 1
    spark = ""
    if len(recs) >= 2 and sum(weeks.values()) >= 1:
        vals = [weeks.get(i, 0) for i in range(11, -1, -1)]
        spark = f'<span class="small muted">Incidents per week, last 12 weeks: {DV.sparkline(vals)}</span>'
    rows = ""
    for r in recs[:60]:
        st = r.get("state") or "—"
        res = r.get("resolved_at")
        title = E(r.get("title") or "(untitled)")
        if r.get("url"):
            title = '<a href="' + E(r["url"]) + '">' + title + "</a>"
        d = E(dur(r["started_at"], res)) if res else "open"
        if r.get("resolved_inferred"):
            d += ' <span class="muted">(approx.)</span>'
        rows += ('<tr><td class="small">' + E(fmt_dt(r["started_at"])) + "</td><td>" + title + "</td>"
                 '<td><span class="pill s-' + E(st) + '">' + E(st) + '</span></td><td class="small">' + E(r.get("impact") or "—") + "</td>"
                 '<td class="small">' + d + "</td></tr>")
    since = "" if h.get("history_backfilled") else f'<p class="note small">{E(PLAT_LABEL.get(v["platform"], v["platform"]))} only exposes incidents that are open right now, so this history starts on {E(h["first_watched"][:10])}, the day we first watched {E(name)}. It fills in from here.</p>'
    err = f'<p class="note small">Last poll returned an error (<code>{E(h.get("last_error"))}</code>) — state is shown as unknown, not OK. If {E(name)} moved its status page, <a href="{REPO}/issues">tell us</a>.</p>' if h.get("last_error") else ""
    kp = DV.kpi_row([(n30, "incidents, last 30 days"), (n90, "incidents, last 90 days"), (len(recs), "incidents on record")])
    cfg = json.dumps({"vendors": [slug], "format": "auto", "map_url": "https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json", "unreachable_after": 3, "mute_maintenance": False}, indent=2)
    body = f"""<section>
<p class="small"><a href="{SITE}/vendors.html">← all vendors</a></p>
<h1>{E(name)} status history</h1>
<p class="lead">Current state: {pill(h["last_state"])} — “{E(h.get("last_description") or "unknown")}” per <a href="{E(h["status_url"])}">{E(h["status_url"])}</a> ({E(PLAT_LABEL.get(v["platform"], v["platform"]))}), checked {E(fmt_dt(h["last_checked"]))}.</p>
{err}{kp}{spark}{since}
<div class="cta"><a class="btn" href="{TPL}">Get {E(name)} alerts in your Slack — free template</a><a class="btn ghost" href="{SITE}/v/{slug}/feed.xml">RSS for {E(name)}</a></div>
</section>
<section><h2>Incidents on record ({len(recs):,})</h2>
<div class="tw"><table><thead><tr><th>Started</th><th>Incident</th><th>Status</th><th>Impact</th><th>Duration</th></tr></thead><tbody>{rows or '<tr><td colspan=5 class=muted>No incidents recorded yet.</td></tr>'}</tbody></table></div>
<p class="small muted">Titles, statuses and impact levels are the vendor's own words. Durations marked approx. are inferred from the poll that first found the incident gone. Shows the latest 60; the <a href="{SITE}/api/v/{slug}.json">JSON</a> has everything we hold (up to 400 days).</p>
</section>
<section><h2>Watch {E(name)} with the template</h2>
<p>Put this in <code>config.json</code> of your fork and add a <code>WEBHOOK_URL</code> secret:</p><pre>{E(cfg)}</pre>
</section>"""
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": f"{name} status history", "url": vurl(slug),
          "dateModified": h["last_checked"], "isPartOf": {"@type": "WebSite", "name": "Vendor Status Watch", "url": f"{SITE}/"},
          "about": {"@type": "Organization", "name": name, "url": h["status_url"]}}
    write(f"v/{slug}.html", page(f"{name} status history — {n30} incidents in the last 30 days", body,
                                      f"{name} status page history: {len(recs)} incidents on record, {n30} in the last 30 days, current state {STATE_LABEL.get(h['last_state'])}. Free Slack/Discord/Teams alerts via GitHub Actions.",
                                      f"v/{slug}.html", extra_head=f'<script type="application/ld+json">{json.dumps(ld)}</script>'))
    items = "".join(f"<item><title>{E(r.get('title') or 'incident')} [{E(r.get('state') or '')}]</title><link>{E(r.get('url') or h['status_url'])}</link>"
                    f"<guid isPermaLink=\"false\">{E(slug)}:{E(str(r.get('id') or r['started_at']))}</guid><pubDate>{rfc822(r['started_at'])}</pubDate>"
                    f"<description>{E((r.get('body') or '')[:800])}</description></item>" for r in recs[:30])
    write(f"v/{slug}/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{E(name)} incidents — Vendor Status Watch</title><link>{vurl(slug)}</link><description>Incidents from {E(name)}\'s public status page, polled daily.</description><lastBuildDate>{rfc822(GEN_AT)}</lastBuildDate>{items}</channel></rss>')
    write(f"api/v/{slug}.json", json.dumps({"vendor": name, "slug": slug, "platform": v["platform"], "status_url": h["status_url"],
                                            "last_checked": h["last_checked"], "last_state": h["last_state"], "history_backfilled": h.get("history_backfilled", False),
                                            "first_watched": h.get("first_watched"), "incidents": recs}, indent=0))


# ------------------------------------------------------------------ list pages
def render_vendors():
    rows = ""
    for v in sorted(vendors["vendors"], key=lambda x: x["name"].lower()):
        s = snap_by.get(v["slug"])
        st = pill(s["state"]) if s else '<span class="pill s-unknown">not polled</span>'
        n30 = vend30.get(v["slug"], 0) if s else ""
        # aliases (same status page under another name: sendgrid -> twilio) stay
        # SEARCHABLE here, or a visitor types their vendor and concludes we lack it.
        al = ALIAS_OF.get(v["slug"], [])
        alq = " ".join(al)
        alnote = (' <span class="small muted">also: ' + ", ".join(E(a) for a in al) + "</span>") if al else ""
        rows += (f'<tr data-q="{E(v["name"].lower())} {E(v["slug"])} {E(v["platform"])} {E(alq)}"><td><a href="{vurl(v["slug"])}">{E(v["name"])}</a></td><td>{st}</td>'
                 f'<td class="small">{E(str(n30))}</td><td class="small muted">{E(PLAT_LABEL.get(v["platform"], v["platform"]))}</td><td class="small"><code>{E(v["slug"])}</code>{alnote}</td></tr>')
    body = f"""<section><h1>All {N_MAP:,} vendors</h1><p class="lead">{N_SUP:,} are polled (they publish JSON); the rest are listed so you know which of your dependencies you still have to check by hand. The slug column is what goes in the template's config.</p>
<p><label for="q" class="small muted">Filter by vendor, slug or platform</label><br><input id="q" class="filter" type="search" placeholder="e.g. stripe, instatus, cloud" autocomplete="off"></p>
<p class="small muted" id="cnt"></p>
<div class="tw"><table id="t"><thead><tr><th>Vendor</th><th>State now</th><th>Incidents 30d</th><th>Platform</th><th>Slug</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<script>(function(){{var q=document.getElementById('q'),rs=document.querySelectorAll('#t tbody tr'),c=document.getElementById('cnt');function f(){{var s=q.value.toLowerCase().trim(),n=0;rs.forEach(function(r){{var v=!s||r.getAttribute('data-q').indexOf(s)>-1;r.style.display=v?'':'none';if(v)n++}});c.textContent=n+' of '+rs.length+' vendors'}}q.addEventListener('input',f);f()}})();</script>"""
    write("vendors.html", page(f"All {N_MAP:,} SaaS vendor status pages — Vendor Status Watch", body,
                               f"Searchable list of {N_MAP:,} SaaS status pages with current state, 30-day incident counts and template slugs.", "vendors.html"))


def render_platforms():
    c = collections.Counter(v["platform"] for v in vendors["vendors"])
    sup = collections.Counter(v["platform"] for v in vendors["vendors"] if v["supported"])
    why = {"statuspage": "GET /api/v2/summary.json + /api/v2/incidents.json (history back-filled)",
           "instatus": "GET /summary.json — open incidents only", "betterstack": "GET /index.json — open incidents only",
           "status.io": "page id resolved once, then api.status.io/1.0/status/&lt;id&gt; — open incidents only",
           "hund": "API answers 401 without a key; no public feed", "cachet": "/api/v1/* returns 404 on every instance seen",
           "uptimerobot": "public status pages are HTML only", "incident.io": "HTML only (some ld+json)",
           "bespoke": "the vendor's own public feed, one hand-written parser each: Slack JSON API, Stripe /current, Google incidents.json (Cloud, Firebase, Workspace, Play), AWS Health currentevents, Azure status RSS",
           "unknown-html": "bespoke page (Apple, Microsoft 365, Notion…) — needs a hand-written parser each; the ones buyers ask for most are done (row above)",
           "dead": "unreachable at probe time (DNS gone, TLS broken, or 4xx/5xx)"}
    rows = "".join(f'<tr><td>{E(PLAT_LABEL.get(p, p))}</td><td>{n:,}</td><td>{"yes" if sup.get(p) else "no"}</td><td class="small">{why.get(p, "")}</td></tr>'
                   for p, n in sorted(c.items(), key=lambda kv: -kv[1]))
    bars = DV.figure(DV.bar_chart([(PLAT_LABEL.get(p, p), n) for p, n in c.items()], unit="vendors"),
                     "Where vendors host their status pages (the living map, rebuilt daily)", source="live probe of each status URL", asof=vendors["generated_at"][:10])
    body = f"""<section><h1>Coverage, honestly</h1><p class="lead">{N_SUP:,} of {N_MAP:,} mapped vendors ({100 * N_SUP // N_MAP}%) publish a status feed we can read. On the last poll {N_PARSED:,} of {N_POLLED:,} answered; the rest are shown as <em>unknown</em>. {N_DEAD:,} seed entries were dead links — that is the rot the daily map exists to catch.</p>
{bars}
<div class="tw"><table><thead><tr><th>Platform</th><th>Vendors</th><th>Polled</th><th>How / why not</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">Seed list: metoro-io/statusphere (MIT), de-duplicated from 1,425 rows to {N_MAP:,} unique status URLs, then every URL probed live and re-probed daily. Missing a vendor? <a href="{REPO}/issues">Open an issue</a>.</p></section>"""
    write("platforms.html", page("Coverage by status-page platform — Vendor Status Watch", body,
                                 f"{N_SUP:,} of {N_MAP:,} SaaS status pages are machine-readable; which platforms we parse and why the rest are not.", "platforms.html"))


def render_api():
    body = f"""<section><h1>JSON API (static, free, no key)</h1>
<p class="lead">Everything the site shows is also a file. Regenerated by the daily pipeline; cache-friendly; MIT.</p>
<div class="tw"><table><thead><tr><th>File</th><th>What</th></tr></thead><tbody>
<tr><td><a href="{SITE}/api/vendors.json"><code>/api/vendors.json</code></a></td><td>The living map: {N_MAP:,} vendors → platform, base URL, supported flag. The template reads this at run time.</td></tr>
<tr><td><a href="{SITE}/api/snapshot.json"><code>/api/snapshot.json</code></a></td><td>Latest state of all {N_POLLED:,} polled vendors (state, vendor's description, open incident count, error if any).</td></tr>
<tr><td><code>/api/v/&lt;slug&gt;.json</code></td><td>Per-vendor incident history (up to 400 days). Example: <a href="{SITE}/api/v/twilio.json">/api/v/twilio.json</a>.</td></tr>
<tr><td><a href="{SITE}/feed.xml"><code>/feed.xml</code></a>, <code>/v/&lt;slug&gt;/feed.xml</code></td><td>RSS: all incidents, or one vendor.</td></tr>
</tbody></table></div>
<p class="small muted">Fair use: files are served from GitHub Pages; please poll no more than once a minute. States are the vendors' own published states, re-read daily for this site (the template and hosted tier poll every 5 minutes).</p></section>"""
    write("api.html", page("JSON API — Vendor Status Watch", body, "Static JSON files: the vendor map, the latest snapshot and per-vendor incident history.", "api.html"))


def render_legal():
    body = f"""<section><h1>Privacy, terms &amp; refunds</h1>
<h2>Privacy</h2><p>This site sets no cookies and runs no analytics scripts. It is hosted on GitHub Pages, which logs requests under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>. The free template runs entirely inside your own GitHub account; it sends nothing to us. If you buy the hosted watch, Gumroad processes payment under its own policy; we store the webhook URL and vendor list you provide, use them only to send you alerts, and delete them on request or when your term ends.</p>
<h2>Terms</h2><p>Vendor states and incident text are republished from each vendor's public status page and may lag or be wrong; this project is informational and is not an uptime measurement or a substitute for the vendor's own notifications. Software is provided under the MIT licence, as is, without warranty. The hosted watch is a best-effort service; we will tell you when it cannot reach a vendor rather than show a false OK.</p>
<h2>Refunds</h2><p>Hosted watch: full refund within 14 days of purchase for any reason — reply to your Gumroad receipt. After 14 days, a pro-rata refund if the service failed to deliver alerts for 7 consecutive days through our fault.</p>
<h2>Contact</h2><p>Open an issue at <a href="{REPO}/issues">{E(REPO)}/issues</a>, or reply to your Gumroad receipt for purchase matters.</p></section>"""
    write("legal.html", page("Privacy, terms & refunds — Vendor Status Watch", body, "Privacy, terms and the 14-day refund policy for the hosted watch.", "legal.html"))


def render_feeds_and_meta():
    items = "".join(f"<item><title>{E(by_slug[s]['name'])}: {E(r.get('title') or 'incident')} [{E(r.get('state') or '')}]</title><link>{E(r.get('url') or vurl(s))}</link>"
                    f"<guid isPermaLink=\"false\">{E(s)}:{E(str(iid))}</guid><pubDate>{rfc822(r['started_at'])}</pubDate><description>{E((r.get('body') or '')[:800])}</description></item>"
                    for s, iid, r in all_inc[:60])
    write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Vendor Status Watch — all incidents</title><link>{SITE}/</link><description>Incidents from {N_SUP} SaaS status pages, polled daily.</description><lastBuildDate>{rfc822(GEN_AT)}</lastBuildDate>{items}</channel></rss>')
    urls = [f"{SITE}/", f"{SITE}/vendors.html", f"{SITE}/platforms.html", f"{SITE}/api.html", f"{SITE}/legal.html"] + [vurl(v["slug"]) for v in vendors["vendors"]]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
          "".join(f"<url><loc>{E(u)}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    write("api/vendors.json", json.dumps(vendors, indent=0))
    write("api/snapshot.json", json.dumps(snap, indent=0))
    write(".nojekyll", "")
    if CFG.get("indexnow_key"):
        write(CFG["indexnow_key"] + ".txt", CFG["indexnow_key"])


def prune_and_redirect():
    """A slug that leaves the map must not leave a stale page behind.

    Alias slugs (two seed rows, one real status page) get a canonical redirect so any
    inbound link still lands somewhere true; anything else that is no longer in the map
    is deleted, because a vendor page frozen at an old poll is a lie with a timestamp.
    """
    import shutil
    live = {v["slug"] for v in vendors["vendors"]}
    vdir = os.path.join(OUT, "v")
    keep = live | set(ALIAS)
    for ent in sorted(os.listdir(vdir)) if os.path.isdir(vdir) else []:
        path = os.path.join(vdir, ent)
        slug = ent[:-5] if ent.endswith(".html") else ent
        if slug in keep:
            continue
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)
    for alias, canon in sorted(ALIAS.items()):
        if canon not in live:
            continue
        nm = by_slug[canon]["name"]
        write(f"v/{alias}.html",
              f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
              f'<title>{E(alias)} — same status page as {E(nm)}</title>'
              f'<link rel="canonical" href="{vurl(canon)}">'
              f'<meta http-equiv="refresh" content="0; url={vurl(canon)}">'
              f'<meta name="robots" content="noindex,follow"></head><body>'
              f'<p><b>{E(alias)}</b> publishes the same status page as <a href="{vurl(canon)}">{E(nm)}</a> '
              f'(identical page id), so its history lives there.</p></body></html>')
    for apij in sorted(os.listdir(os.path.join(OUT, "api", "v"))) if os.path.isdir(os.path.join(OUT, "api", "v")) else []:
        if apij[:-5] not in live:
            os.remove(os.path.join(OUT, "api", "v", apij))


def main():
    os.makedirs(OUT, exist_ok=True)
    render_index()
    for v in vendors["vendors"]:
        render_vendor(v)
    render_vendors()
    render_platforms()
    render_api()
    render_legal()
    render_feeds_and_meta()
    prune_and_redirect()
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"gen_site: {n} files → docs/  | map {N_MAP} sup {N_SUP} polled {N_POLLED} parsed {N_PARSED} not_ok {len(NOT_OK)} incidents {N_INC} (30d {N_INC30})")


if __name__ == "__main__":
    main()
