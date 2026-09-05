#!/usr/bin/env python3
"""gh_release.py — publish each daily refresh as a GitHub Release (c150, ported from warn-feed).

Why this exists
---------------
GitHub Pages is frozen for the whole org (A024) and the repo shows 0 stars / 0 views, so this
venture has NO usage meter at all: the Space host exposes no analytics and HF dataset
downloads are the only number we can read. A Release is a repo surface that (a) shows in
the right-hand sidebar with a freshness stamp, (b) reaches everyone who Watches the repo,
(c) gives every asset a stable alias
    https://github.com/APVentureEngine/vendor-status-watch/releases/latest/download/vendors.json
and (d) carries a per-asset DOWNLOAD COUNT — attributable to a file, hard to inflate.

Behaviour
---------
  python3 gh_release.py            create/refresh today's release `data-YYYY-MM-DD` (idempotent:
                                   same day replaces assets + notes), then prune releases older
                                   than KEEP_DAYS after recording their counts.
  python3 gh_release.py --stats    print per-release/per-asset download counts, append a line
                                   to ../release_downloads.jsonl (outside the public repo)
  python3 gh_release.py --dry-run  build notes + tarball, touch nothing on GitHub
  python3 gh_release.py --selftest offline assertions on the notes builder

Rails: token only from env ($GITHUB_ORG_TOKEN), never printed. Non-fatal in pipeline.sh.
"""
import datetime as dt
import glob
import json
import mimetypes
import os
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "APVentureEngine/vendor-status-watch"
TEMPLATE_REPO = "APVentureEngine/vendor-status-watch-template"
API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
KEEP_DAYS = 60
TAG_PREFIX = "data-"
TOP_WINDOW_DAYS = 14
OUT_DIR = os.path.join(HERE, "..", "release_out")   # download-count log; OUTSIDE the public repo
HISTORY_TGZ = "incident_history.tar.gz"
import tempfile
TGZ_DIR = os.path.join(tempfile.gettempdir(), "vsw-release")   # 2 MB tarball: never inside any git tree
ASSETS = [  # (path, label). Paths are relative to HERE unless absolute (the tarball).
    ("docs/api/vendors.json", "The vendor map: every status page we know, platform, feed URL, supported flag"),
    ("docs/api/snapshot.json", "Current state of every polled vendor as of this refresh (ok / degraded / major / maintenance)"),
    ("docs/api/stats.json", "Headline counts for this refresh (machine-readable)"),
    (os.path.join(TGZ_DIR, HISTORY_TGZ), "Per-vendor incident history, one JSON per vendor (title, impact, started/updated, source URL)"),
]

try:
    CFG = json.load(open(os.path.join(HERE, "site_config.json")))
except Exception:
    CFG = {}
SITE = (CFG.get("site_url") or "https://approjects-vendor-status-watch.static.hf.space").rstrip("/") + "/"
DIGEST_URL = CFG.get("digest_url") or "https://approj.gumroad.com/l/vendor-digest"
DIGEST_PRICE = CFG.get("digest_price", "$19/year")
HF_DATASET = "https://huggingface.co/datasets/APProjects/saas-vendor-status-incidents-daily"


def _token():
    t = os.environ.get("GITHUB_ORG_TOKEN", "").strip()
    if not t:
        raise SystemExit("gh_release: GITHUB_ORG_TOKEN not in env — skipped")
    return t


def gh(method, url, data=None, ctype="application/json", raw=False):
    body = None
    if data is not None:
        body = data if raw else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", "Bearer " + _token())
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "vendor-status-watch")
    if body is not None:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            txt = r.read().decode() if r.status != 204 else ""
            return r.status, (json.loads(txt) if txt else None)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode())
        except Exception:
            msg = {}
        return e.code, msg


# --------------------------------------------------------------------------- data
def state_counts(snapshot):
    c = {}
    for v in snapshot.get("vendors", []):
        s = v.get("state") or "unknown"
        c[s] = c.get(s, 0) + 1
    return c


def busiest(history_dir, today, k=5):
    """Vendors with the most incidents whose start date falls in the last TOP_WINDOW_DAYS.
    Ranked by started_at (the vendor's own timestamp), NOT first_seen — first_seen is mostly
    backfill in a scraped dataset (warn-feed learning 2026-09-04)."""
    cutoff = (today - dt.timedelta(days=TOP_WINDOW_DAYS)).isoformat()
    rows = []
    for p in glob.glob(os.path.join(history_dir, "*.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        inc = d.get("incidents") or {}
        vals = inc.values() if isinstance(inc, dict) else inc
        n = 0
        for i in vals:
            sa = (i.get("started_at") or "")[:10]
            if sa and cutoff <= sa <= today.isoformat():
                n += 1
        if n:
            rows.append((d.get("vendor") or d.get("slug") or os.path.basename(p)[:-5], d.get("slug") or "", n))
    rows.sort(key=lambda x: (-x[2], x[0].lower()))
    return rows[:k]


def build_notes(stats, counts, day, top=None):
    """Notes from docs/api/stats.json + snapshot.json of the SAME run — no rounded figures."""
    mapped = int(stats.get("vendors_mapped", 0))
    sup = int(stats.get("vendors_supported", 0))
    inc = int(stats.get("incidents", 0))
    inc30 = int(stats.get("incidents_30d", 0))
    with_hist = int(stats.get("vendors_with_history", 0))
    polled = sum(counts.values())
    not_ok = sum(n for s, n in counts.items() if s not in ("ok", "unknown"))
    lines = [
        f"**{mapped:,} SaaS status pages mapped · {sup:,} machine-readable · {inc:,} incidents of history · refreshed {day}**",
        "",
        f"{polled:,} vendors polled this refresh; {not_ok:,} reporting something other than \"all systems operational\" "
        f"({', '.join(f'{s}: {n}' for s, n in sorted(counts.items(), key=lambda x: -x[1]))}). "
        f"{inc30:,} incidents opened in the last 30 days across {with_hist:,} vendors with history.",
        "",
        "## Files",
        "",
    ]
    for path, label in ASSETS:
        lines.append(f"- `{os.path.basename(path)}` — {label}")
    lines += [
        "",
        "Stable alias for scripts (always the newest release): "
        f"`https://github.com/{REPO}/releases/latest/download/vendors.json` "
        f"(same for `snapshot.json`, `stats.json`, `{HISTORY_TGZ}`)",
        "",
        "## Same data, other shapes",
        "",
        f"- Live board + per-vendor pages: {SITE}",
        f"- JSON API (no key): {SITE}api.html · RSS of new incidents: {SITE}feed.xml",
        f"- Hugging Face (`load_dataset` / pandas): {HF_DATASET}",
        f"- Alert your own Slack / Discord / Teams from GitHub Actions, free, MIT: https://github.com/{TEMPLATE_REPO}",
        "",
        "## Don't want to run the template yourself?",
        "",
        f"- [Daily vendor-status digest to your webhook — {DIGEST_PRICE}]({DIGEST_URL}) — name your vendors at checkout; "
        "one message a day from this same pipeline.",
    ]
    if top:
        lines += ["", f"## Vendors with the most incidents started in the last {TOP_WINDOW_DAYS} days", ""]
        lines += [f"- {name} — {n} incident{'s' if n != 1 else ''}" + (f" ({SITE}v/{slug}.html)" if slug else "")
                  for name, slug, n in top]
    lines += ["", "_Published automatically by the daily pipeline. Counts come from `stats.json` and `snapshot.json` of the same run._"]
    return "\n".join(lines)


def build_tarball(history_dir, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    n = 0
    with tarfile.open(dest, "w:gz") as tf:
        for p in sorted(glob.glob(os.path.join(history_dir, "*.json"))):
            tf.add(p, arcname="history/" + os.path.basename(p))
            n += 1
    return n


# --------------------------------------------------------------------------- releases
def list_releases():
    out, page = [], 1
    while True:
        st, d = gh("GET", f"{API}/repos/{REPO}/releases?per_page=100&page={page}")
        if st != 200 or not d:
            break
        out += d
        if len(d) < 100:
            break
        page += 1
    return out


def stats(write=True):
    rels = list_releases()
    rec = {"ts": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "releases": []}
    total = 0
    for r in rels:
        assets = {a["name"]: a["download_count"] for a in r.get("assets", [])}
        total += sum(assets.values())
        rec["releases"].append({"tag": r["tag_name"], "published_at": r.get("published_at"), "assets": assets})
        print(f"{r['tag_name']}: " + (", ".join(f"{k}={v}" for k, v in assets.items()) if assets else "(no assets)"))
    rec["total_downloads"] = total
    print(f"release assets: {len(rels)} releases, {total} downloads total")
    if write:
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(os.path.join(OUT_DIR, "release_downloads.jsonl"), "a") as f:
            f.write(json.dumps(rec) + "\n")
    return rec


def prune(rels, today):
    cutoff = today - dt.timedelta(days=KEEP_DAYS)
    for r in rels:
        tag = r["tag_name"]
        if not tag.startswith(TAG_PREFIX):
            continue
        try:
            d = dt.date.fromisoformat(tag[len(TAG_PREFIX):])
        except ValueError:
            continue
        if d < cutoff:
            st, _ = gh("DELETE", f"{API}/repos/{REPO}/releases/{r['id']}")
            st2, _ = gh("DELETE", f"{API}/repos/{REPO}/git/refs/tags/{tag}")
            print(f"pruned {tag}: release {st}, tag {st2}")


def publish(dry=False):
    today = dt.datetime.now(dt.timezone.utc).date()
    day = today.isoformat()
    tag = TAG_PREFIX + day
    st_json = json.load(open(os.path.join(HERE, "docs", "api", "stats.json")))
    snap = json.load(open(os.path.join(HERE, "docs", "api", "snapshot.json")))
    counts = state_counts(snap)
    n_hist = build_tarball(os.path.join(HERE, "history"), os.path.join(TGZ_DIR, HISTORY_TGZ))
    notes = build_notes(st_json, counts, day, busiest(os.path.join(HERE, "history"), today))
    name = f"Vendor status map + incident history — refresh {day}"
    if dry:
        print(notes)
        print(f"\n[dry-run] tarball: {n_hist} vendor histories -> {os.path.join(TGZ_DIR, HISTORY_TGZ)}")
        return 0
    st, ref = gh("GET", f"{API}/repos/{REPO}/git/ref/heads/main")
    if st != 200:
        print(f"gh_release: cannot read main ref (HTTP {st}) — skipped")
        return 1
    sha = ref["object"]["sha"]
    rels = list_releases()
    existing = next((r for r in rels if r["tag_name"] == tag), None)
    payload = {"tag_name": tag, "target_commitish": sha, "name": name, "body": notes,
               "draft": False, "prerelease": False, "make_latest": "true"}
    if existing:
        st, rel = gh("PATCH", f"{API}/repos/{REPO}/releases/{existing['id']}", payload)
        for a in existing.get("assets", []):
            gh("DELETE", f"{API}/repos/{REPO}/releases/assets/{a['id']}")
    else:
        st, rel = gh("POST", f"{API}/repos/{REPO}/releases", payload)
    if st not in (200, 201):
        print(f"gh_release: create/update failed HTTP {st}: {json.dumps(rel)[:300]}")
        return 1
    upload_url = rel["upload_url"].split("{")[0]
    ok = 0
    for path, _label in ASSETS:
        full = path if os.path.isabs(path) else os.path.join(HERE, path)
        if not os.path.exists(full):
            print(f"gh_release: missing {path}, skipped")
            continue
        fname = os.path.basename(path)
        ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
        with open(full, "rb") as f:
            data = f.read()
        st, a = gh("POST", f"{upload_url}?{urllib.parse.urlencode({'name': fname})}", data, ctype=ctype, raw=True)
        if st == 201:
            ok += 1
        else:
            print(f"gh_release: asset {fname} upload HTTP {st}: {json.dumps(a)[:200]}")
    print(f"gh_release: {'updated' if existing else 'created'} {tag} ({ok}/{len(ASSETS)} assets) -> {rel.get('html_url')}")
    stats(write=True)
    prune(rels, today)
    return 0 if ok == len(ASSETS) else 1


# --------------------------------------------------------------------------- selftest
def selftest():
    st_json = {"vendors_mapped": 1127, "vendors_supported": 799, "incidents": 14707, "incidents_30d": 2197,
               "vendors_with_history": 650}
    counts = {"ok": 686, "maintenance": 24, "degraded": 39, "partial": 12, "major": 4, "unknown": 48}
    n = build_notes(st_json, counts, "2026-09-05", [("Slack", "slack", 3), ("Acme", "", 1)])
    for must in ("1,127 SaaS status pages mapped", "799 machine-readable", "14,707 incidents of history",
                 "813 vendors polled", "79 reporting something other", "2,197 incidents opened in the last 30 days",
                 "650 vendors with history", "releases/latest/download/vendors.json", "`snapshot.json`",
                 f"`{HISTORY_TGZ}`", DIGEST_URL, HF_DATASET, TEMPLATE_REPO,
                 "Slack — 3 incidents (" + SITE + "v/slack.html)", "Acme — 1 incident\n"):
        assert must in n, must
    assert "github.io" not in n, "notes must not name the frozen Pages host"
    for bad in ("TODO", "lorem", "None", "{"):
        assert bad not in n, bad
    n0 = build_notes({}, {}, "2026-09-05")
    assert "0 SaaS status pages" in n0 and "most incidents" not in n0
    # busiest(): ranks by started_at inside the window, ignores first_seen, skips undated/future
    import tempfile
    t = dt.date(2026, 9, 5)
    tmpd = tempfile.mkdtemp()
    json.dump({"vendor": "Old", "slug": "old", "incidents": {"a": {"started_at": "2024-01-01", "first_seen": "2026-09-04T00:00:00Z"}}},
              open(os.path.join(tmpd, "old.json"), "w"))
    json.dump({"vendor": "Busy", "slug": "busy", "incidents": {"a": {"started_at": "2026-09-01T10:00:00Z"},
                                                                 "b": {"started_at": "2026-09-03T10:00:00-07:00"},
                                                                 "c": {"started_at": ""}, "d": {"started_at": "2026-12-01"}}},
              open(os.path.join(tmpd, "busy.json"), "w"))
    json.dump({"vendor": "One", "slug": "one", "incidents": {"a": {"started_at": "2026-08-30"}}},
              open(os.path.join(tmpd, "one.json"), "w"))
    b = busiest(tmpd, t)
    assert b == [("Busy", "busy", 2), ("One", "one", 1)], b
    tgz = os.path.join(tmpd, "h.tgz")
    assert build_tarball(tmpd, tgz) == 3
    with tarfile.open(tgz) as tf:
        assert sorted(tf.getnames()) == ["history/busy.json", "history/old.json", "history/one.json"]
    print("gh_release selftest: OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
    elif "--stats" in a:
        stats(write="--no-write" not in a)
    else:
        sys.exit(publish(dry="--dry-run" in a))
