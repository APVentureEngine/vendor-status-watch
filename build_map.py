#!/usr/bin/env python3
"""Build vendors.json — the LIVING VENDOR MAP — from the probe results.

Input : ../../research/vendor-status-probe-2026-09-04.json (1,425 seed vendors,
        platform classified by probe_status_pages.py; seed list = metoro-io/statusphere, MIT)
Output: vendors.json  [{slug, name, platform, base, supported, page_id?, note?}]

Rules
- slug is unique (name-derived; collisions get -2, -3 ...).
- 'dead' vendors are kept with supported=false so the map documents rot instead
  of hiding it (the moat number on the homepage comes from this).
- status.io vendors get their 24-hex page_id resolved ONCE here so the poller's
  steady state is a single request per vendor.
"""
import collections, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import platforms as P

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
import time as _time
_T0 = _time.time()
def _lap(label):
    print(f"[{_time.time() - _T0:5.1f}s] {label}", flush=True)
_CACHE_P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reprobe_cache.json")
try:
    _HTML_CACHE = json.load(open(_CACHE_P))
except Exception:
    _HTML_CACHE = {}

SRC = sys.argv[1] if len(sys.argv) > 1 else "../../research/vendor-status-probe-2026-09-04.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "vendors.json"
PLAT = {"statuspage-html": "statuspage", "instatus-html": "instatus"}

# --- display-name hygiene (c127) -------------------------------------------
# The upstream seed carries slug-shaped names ("genesys-cloud", "akamai-edge-dns")
# and a few obvious test pages. Both showed up on the public board. Title-casing
# does NOT change the derived slug (slug is lowercase+hyphenated either way), so
# history files keyed by slug stay valid.
JUNK_NAMES = {"sg test", "own company", "test", "test page", "example", "demo",
              "your company", "untitled", "status page", "new company"}
KEEP_CASE = {"npm": "npm", "pypi": "PyPI", "github": "GitHub", "gitlab": "GitLab",
             "iot": "IoT", "openai": "OpenAI", "youtube": "YouTube"}
UPPER = {"api", "dns", "cdn", "aws", "gcp", "sms", "crm", "erp", "ai", "hr", "it",
         "ftp", "vpn", "sql", "ui", "ux", "ip", "sip", "voip", "uk", "us", "eu"}


def clean_name(n):
    n = (n or "").strip()
    if not n or " " in n or n != n.lower():
        return n                      # already human-written; leave it alone
    if n in KEEP_CASE:
        return KEEP_CASE[n]
    words = [w for w in re.split(r"[-_.]+", n) if w]
    return " ".join(KEEP_CASE.get(w, w.upper() if w in UPPER else w.capitalize())
                    for w in words) or n


rows = json.load(open(SRC))["rows"]
seen_slug, seen_base, out = {}, set(), []
for r in rows:
    base = (r.get("base") or r["url"]).rstrip("/")
    if base in seen_base:
        continue
    seen_base.add(base)
    r = dict(r, name=clean_name(r.get("name")))
    if not r["name"] or r["name"].lower() in JUNK_NAMES:
        continue
    plat = PLAT.get(r["platform"], r["platform"])
    slug = re.sub(r"[^a-z0-9]+", "-", r["name"].lower()).strip("-") or "vendor"
    if slug in seen_slug:
        seen_slug[slug] += 1
        slug = f"{slug}-{seen_slug[slug]}"
    else:
        seen_slug[slug] = 1
    v = {"slug": slug, "name": r["name"], "platform": plat, "base": base,
         "supported": plat in P.PARSERS and plat != "incident.io"}  # incident.io needs a feed (reprobe below)
    if plat == "dead":
        v["note"] = f"unreachable at probe time ({r.get('error') or r.get('http')})"
    elif not v["supported"]:
        v["note"] = P.UNSUPPORTED.get(plat, "unsupported")
    out.append(v)

# Curated extras the seed list lacks (Slack, Anthropic, SendGrid, Linear, Sentry, npm ...).
# They enter as unknown-html and the live re-probe below classifies them like everything else.
EXTRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_extra.json")
if os.path.exists(EXTRA):
    added = 0
    for e in json.load(open(EXTRA)):
        base = e["url"].rstrip("/")
        if base in seen_base:
            continue
        seen_base.add(base)
        slug = re.sub(r"[^a-z0-9]+", "-", e["name"].lower()).strip("-") or "vendor"
        if slug in seen_slug:
            seen_slug[slug] += 1
            slug = f"{slug}-{seen_slug[slug]}"
        else:
            seen_slug[slug] = 1
        out.append({"slug": slug, "name": e["name"], "platform": "unknown-html", "base": base,
                    "supported": False, "note": "bespoke page"})
        added += 1
    print("seed_extra added:", added)

# c130: bespoke parsers (platforms.BESPOKE) for the vendors buyers search first — Slack,
# Stripe, AWS, Azure, Google Cloud/Firebase/Workspace/Play. Keyed by host, so the seed row
# is promoted here whatever the HTML classifier called it.
n_besp = 0
for v in out:
    hit = P.bespoke_for(v["base"])
    if hit and v["platform"] in ("unknown-html", "dead", "bespoke"):
        v["platform"], v["supported"], v["note"] = "bespoke", True, hit[1]
        n_besp += 1
print("bespoke parsers attached:", n_besp)

# Re-probe every 'unknown-html' base for a JSON endpoint the HTML classifier missed.
# (2026-09-03: rescued cloudflare, elastic, bandwidth, qualys -> statuspage; railway -> instatus.)
# This is the daily self-healing step: vendors migrate platforms; the map follows.
def _reprobe(v):
    """Return (platform, extra_fields) for an unknown-html/incident.io row, or (None, {})."""
    b = v["base"]
    # 6 s per probe: a host that has not answered a JSON path in 6 s is not going to,
    # and 200 rows x 4 paths x 15 s was blowing the pipeline's 120 s cap (c152).
    for plat, path, key in (("statuspage", "/api/v2/summary.json", "status"),
                            ("instatus", "/summary.json", "page"),
                            ("betterstack", "/index.json", "data"),
                            ("sorry", "/api/v1/status", "page")):
        code, body = P._get(b + path, timeout=6)
        if code == 200 and body[:1] in (b"{", b"["):
            try:
                j = json.loads(body)
            except Exception:
                continue
            if isinstance(j, dict) and key in j:
                return plat, {}
    # c152: the HTML itself can name a machine-readable source the JSON probes miss.
    # Fetching ~180 HTML pages costs 2-3 min, so each base is re-read at most weekly
    # (reprobe_cache.json); a hit is re-validated live every day by the poller anyway.
    cached = _HTML_CACHE.get(b)
    if cached and cached.get("until", "") >= TODAY:
        return (cached.get("plat"), cached.get("extra") or {}) if cached.get("plat") else (None, {})
    plat, extra = _reprobe_html(b)
    _HTML_CACHE[b] = {"until": (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d"),
                      "plat": plat, "extra": extra}
    return plat, extra


def _reprobe_html(b):
    code, body = P._get(b, limit=800_000, timeout=10)
    if code != 200:
        return None, {}
    html = body.decode("utf-8", "replace")
    # (a) incident.io pages: a Next.js SPA on the custom host, real RSS on the canonical host
    if "incident.io" in html or "incident-io-status-page" in html:
        feed = P._incidentio_feed(b)
        if feed:
            fcode, fbody = P._get(feed)
            if fcode == 200 and P._xml_items(fbody) is not None:
                return "incident.io", {"feed": feed}
    # (b) a vendor-owned host that is only a shell around an Atlassian Statuspage
    #     (status.loom.com -> loom.status.atlassian.com): adopt the real page as base.
    for host in dict.fromkeys(re.findall(r"https?://([a-z0-9.-]+\.(?:statuspage\.io|status\.atlassian\.com))", html)):
        if host.startswith("subscriptions.") or host.startswith("manage."):
            continue
        scode, sbody = P._get(f"https://{host}/api/v2/summary.json")
        if scode == 200 and sbody[:1] == b"{":
            try:
                if "status" in json.loads(sbody):
                    return "statuspage", {"base": f"https://{host}", "aliases": [b]}
            except Exception:
                pass
    return None, {}

_lap("seed + bespoke done")
unk = [v for v in out if v["platform"] in ("unknown-html", "incident.io")]
def _timed_reprobe(v):
    t = _time.time()
    r = _reprobe(v)
    return r, _time.time() - t
with ThreadPoolExecutor(max_workers=32) as ex:
    timed = list(ex.map(_timed_reprobe, unk))
found = [r for r, _ in timed]
print("reprobe slowest:", ", ".join(f"{v['slug']}={t:.0f}s" for v, (_, t) in sorted(zip(unk, timed), key=lambda z: -z[1][1])[:5]))
for v, (plat, extra) in zip(unk, found):
    if plat:
        v["platform"], v["supported"] = plat, True
        v.pop("note", None)
        if "base" in extra:
            v.setdefault("aliases", [])
            v["aliases"] = sorted(set(v["aliases"] + extra.pop("aliases", [])))
        v.update(extra)
    elif v["platform"] == "incident.io":
        v["supported"], v["note"] = False, "incident.io page with no working feed"
print("reprobe rescued:", sum(1 for f, _ in found if f), "of", len(unk), "unknown-html/incident.io")
json.dump(_HTML_CACHE, open(_CACHE_P, "w"), indent=0, sort_keys=True)
_lap("reprobe done")

sio = [v for v in out if v["platform"] == "status.io"]
with ThreadPoolExecutor(max_workers=8) as ex:
    ids = list(ex.map(lambda v: P.statusio_page_id(v["base"]), sio))
_lap("status.io ids done")
for v, pid in zip(sio, ids):
    if pid:
        v["page_id"] = pid
    else:
        v["supported"] = False
        v["note"] = "status.io page id not found"

# --- c131: collapse same-vendor duplicates -----------------------------------
# The seed dedupes on BASE URL only, so a vendor listed under two status URLs
# (1password.statuspage.io + status.1password.com) shipped as two board rows.
# Site review 2026-09-04 called this out by name ("a duplicated 'MongoDB' row")
# and it is a straight credibility hit on a data product's headline table.
#
# Rules, in order, deliberately conservative — we never silently delete a row
# that might be a DIFFERENT company that merely cleans to the same name:
#   winner = supported > unsupported, then vendor-owned host over *.statuspage.io,
#            then shorter host, then alphabetical (fully deterministic).
#   a loser is MERGED AWAY (its URL kept as an alias) only if it shares the
#   winner's registrable domain or lives on *.statuspage.io — i.e. provably the
#   same brand. Any other same-name row is a real, different company: it is KEPT
#   and disambiguated by domain ("Innovo (inriver.com)") rather than dropped.
def _host(u):
    # NB: removeprefix, not lstrip("www.") — lstrip strips a CHARACTER SET, which
    # would turn "wix.com" into "ix.com".
    return re.sub(r"^https?://", "", u or "").split("/")[0].lower().removeprefix("www.")


def _regdom(u):
    return ".".join(_host(u).split(".")[-2:])


_adopt = []  # (old_slug, canonical_slug) pairs whose history file must follow


def _collapse(rows):
    groups, merged, renamed = {}, 0, 0
    for v in rows:
        groups.setdefault(v["name"].strip().lower(), []).append(v)
    keep = []
    for _, g in groups.items():
        if len(g) == 1:
            keep.append(g[0])
            continue
        g.sort(key=lambda v: (not v["supported"],
                              _host(v["base"]).endswith("statuspage.io"),
                              len(_host(v["base"])), _host(v["base"])))
        win, rest = g[0], g[1:]
        # brand token = the name reduced to letters/digits ("ionos", "postman").
        # If it appears in BOTH hosts the two URLs are the same company on two
        # domains (cohere.ai/cohere.com, ionos-status.de/.com, getpostman.com/
        # postman.com) — merge. If it appears in only one, they are different
        # companies that merely clean to the same name (Innovo vs inRiver) — keep.
        tok = re.sub(r"[^a-z0-9]", "", win["name"].lower())
        for lo in rest:
            same_brand = (_regdom(lo["base"]) == _regdom(win["base"])
                          or _host(lo["base"]).endswith("statuspage.io")
                          or (len(tok) >= 4 and tok in _host(lo["base"]).replace("-", "")
                              and tok in _host(win["base"]).replace("-", "")))
            if same_brand:
                win.setdefault("aliases", []).append(lo["base"])
                # Adopt the loser's slug if it is the canonical (unsuffixed) one.
                # Without this, merging away "cohere" in favour of "cohere-2"
                # would silently move a live, sitemapped page from /v/cohere.html
                # to /v/cohere-2.html and orphan history/cohere.json.
                if re.sub(r"-\d+$", "", lo["slug"]) == lo["slug"] and win["slug"] != lo["slug"]:
                    _adopt.append((win["slug"], lo["slug"]))
                    win["slug"] = lo["slug"]
                merged += 1
            else:
                lo["name"] = f'{lo["name"]} ({_regdom(lo["base"])})'
                renamed += 1
                keep.append(lo)
        keep.append(win)
    print(f"dedupe: merged {merged} duplicate rows, disambiguated {renamed} same-name vendors")
    return keep


out = _collapse(out)
# Carry each merged vendor's incident history onto the slug it now lives at,
# keeping whichever file has more recorded incidents. Orphaned files are left in
# place (harmless, and they make the merge auditable) but never re-published.
for _old, _new in _adopt:
    _o, _n = os.path.join("history", _old + ".json"), os.path.join("history", _new + ".json")
    try:
        _no = len(json.load(open(_o)).get("incidents", [])) if os.path.exists(_o) else -1
        _nn = len(json.load(open(_n)).get("incidents", [])) if os.path.exists(_n) else -1
        if _no > _nn:
            os.replace(_o, _n)
            print(f"history: {_old}.json ({_no} incidents) adopted as {_new}.json")
    except Exception as _e:
        print(f"WARN: history merge {_old}->{_new} failed: {_e}")

# Hard assertion: junk fixtures and duplicate display names must never reach the
# board again. Fail the build loudly rather than publish a table nobody trusts.
_bad = [v for v in out
        if re.search(r"^(sg test|own company|test|demo|example|acme)\b", v["name"], re.I)]
if _bad:
    raise SystemExit(f"REFUSING TO PUBLISH: test fixtures in the map: {[v['slug'] for v in _bad]}")
_dupes = [n for n, c in collections.Counter(v["name"].strip().lower() for v in out).items() if c > 1]
if _dupes:
    raise SystemExit(f"REFUSING TO PUBLISH: duplicate vendor names survived dedupe: {_dupes}")

out.sort(key=lambda v: v["slug"])
json.dump({"generated_at": P._now(), "source": "metoro-io/statusphere (MIT) + live probe",
           "count": len(out), "supported": sum(v["supported"] for v in out),
           "vendors": out}, open(OUT, "w"), indent=1)
import collections
print(f"{len(out)} vendors, {sum(v['supported'] for v in out)} supported")
print(collections.Counter(v["platform"] for v in out).most_common())
print("status.io ids resolved:", sum(1 for v in sio if v.get("page_id")), "/", len(sio))
