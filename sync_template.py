#!/usr/bin/env python3
"""Keep the PUBLIC template repo byte-identical to product/template/ (c143).

Why this exists: the workflow a forker runs exists in FOUR places and they drift
silently —

  1. product/template/.github/workflows/watch.yml   (source of truth, in this repo)
  2. vendor-status-watch-template/watch.yml         (repo ROOT, not .github/ — see below)
  3. the urlencoded `value=` blob inside that repo's README.md one-click link
  4. product/watch.py + product/template/watch.py   (guarded by test_watch.py instead)

(2) is at the root because $GITHUB_ORG_TOKEN lacks the `workflows` permission and
GitHub returns 403 for ANY write under `.github/workflows/` (verified again c143;
A021 asks for the permission and is unanswered). The README works around it with a
`../../new/main?filename=.github%2Fworkflows%2Fwatch.yml&value=<urlencoded>` link
that opens GitHub's editor pre-filled in the READER'S OWN repo — two clicks. That
link is a copy of the workflow, so editing the workflow without regenerating the
link ships forkers a stale one. This script reconciles (2) and (3) from (1).

Direction is one-way: local template/ -> GitHub, via the Contents API (no clone).
Files already identical are skipped, so a quiet day makes zero writes.

Usage:  python3 sync_template.py [--dry-run]
Exit:   0 in sync (or synced), 1 could not read/write GitHub. Non-fatal in the
        pipeline — a failed sync must not stop today's data from publishing.
"""
import base64, hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request

REPO = "APVentureEngine/vendor-status-watch-template"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "template")
WORKFLOW_REL = ".github/workflows/watch.yml"
# local path under template/  ->  path in the public repo
REMAP = {WORKFLOW_REL: "watch.yml"}
DRY = "--dry-run" in sys.argv

tok = os.environ.get("GITHUB_ORG_TOKEN")
if not tok:
    print("sync_template: GITHUB_ORG_TOKEN absent — skipped")
    sys.exit(0)
HDR = {"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json",
       "User-Agent": "vendor-status-watch"}


def api(path, data=None, method=None):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/{path}",
                                 data=json.dumps(data).encode() if data else None,
                                 headers={**HDR, "Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def blob_sha(b):
    """git's blob hash — what the Contents API reports as `sha`."""
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def put(rel, body, sha, why):
    if DRY:
        return
    payload = {"message": why, "content": base64.b64encode(body).decode(),
               "committer": {"name": "vendor-status-watch", "email": "bot@apventureengine.invalid"}}
    if sha:
        payload["sha"] = sha
    try:
        api(f"contents/{rel}", payload, method="PUT")
    except urllib.error.HTTPError as e:
        print(f"sync_template: PUT {rel} HTTP {e.code}: {e.read()[:200]!r}")
        sys.exit(1)


def local_files():
    """Every file under template/, recursively, as (repo_path, bytes)."""
    out = []
    for root, _dirs, names in os.walk(SRC):
        if "__pycache__" in root:
            continue
        for n in names:
            if n.endswith(".pyc"):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, SRC).replace(os.sep, "/")
            out.append((REMAP.get(rel, rel), open(p, "rb").read()))
    return sorted(out)


changed, checked = [], 0
for rel, body in local_files():
    checked += 1
    if rel.startswith(".github/workflows/"):
        print(f"sync_template: refusing {rel} — the token cannot write workflow files (403); "
              f"it ships as {REMAP.get(rel, '?')} plus the README one-click link")
        continue
    try:
        cur = api(f"contents/{rel}")
        if isinstance(cur, list):
            print(f"sync_template: {rel} is a directory upstream — skipping")
            continue
        if cur.get("sha") == blob_sha(body):
            continue
        sha = cur.get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"sync_template: GET {rel} HTTP {e.code} — aborting")
            sys.exit(1)
        sha = None                                    # new file
    changed.append(rel)
    put(rel, body, sha, f"sync {rel} from vendor-status-watch/product/template")

# ---- (3) the README's pre-filled one-click link must carry TODAY'S workflow ----
wf = open(os.path.join(SRC, WORKFLOW_REL), "rb").read().decode()
want_value = urllib.parse.quote_plus(wf)
try:
    meta = api("contents/README.md")
    readme = base64.b64decode(meta["content"]).decode()
except urllib.error.HTTPError as e:
    print(f"sync_template: GET README.md HTTP {e.code} — cannot check the one-click link")
    sys.exit(1)
pat = re.compile(r"(\(\.\./\.\./new/main\?filename=[^&\s]+&value=)([^)\s]*)(\))")
m = pat.search(readme)
if not m:
    print("sync_template: WARNING — no pre-filled workflow link found in README.md; "
          "a forker has no one-click path to .github/workflows/watch.yml")
elif m.group(2) == want_value:
    print("sync_template: README one-click link matches the current workflow")
else:
    new = readme[:m.start(2)] + want_value + readme[m.end(2):]
    changed.append("README.md (one-click workflow link)")
    put("README.md", new.encode(), meta["sha"],
        "regenerate the pre-filled workflow link so forkers get the current watch.yml")

# ---- (4) c148: the README's headline numbers must match today's site ----
# "a daily-rebuilt map of **1,130 vendor status pages** (792 with a machine-readable feed) and
# **14,672 incidents**" was typed once and drifted from the site within a day. gen_site.py
# writes docs/api/stats.json from the variables the site uses; rewrite the sentence from it.
stats_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "api", "stats.json")
if os.path.exists(stats_p):
    st = json.load(open(stats_p))
    try:
        meta = api("contents/README.md")          # re-read: step (3) may have changed it
        readme = base64.b64decode(meta["content"]).decode()
    except urllib.error.HTTPError as e:
        print(f"sync_template: GET README.md HTTP {e.code} — numbers not synced")
        readme = None
    if readme is not None:
        subs = [
            (r"(map of \*\*)[\d,]+( vendor status pages\*\*)", rf"\g<1>{st['vendors_mapped']:,}\g<2>"),
            (r"(\()[\d,]+( with a machine-readable\s+feed\))", rf"\g<1>{st['vendors_supported']:,}\g<2>"),
            (r"(\*\*)[\d,]+( incidents\*\* of history)", rf"\g<1>{st['incidents']:,}\g<2>"),
        ]
        new = readme
        for pat, rep in subs:
            new, n = re.subn(pat, rep, new, count=1)
            if n == 0:
                print(f"sync_template: label not found for {pat[:30]!r} — number NOT synced")
        if new != readme:
            changed.append("README.md (headline numbers)")
            put("README.md", new.encode(), meta["sha"],
                f"README: headline numbers from today's map ({st['vendors_mapped']:,} vendors, {st['incidents']:,} incidents)")
        else:
            print("sync_template: README headline numbers already current")
else:
    print("sync_template: docs/api/stats.json missing — run gen_site.py first; numbers not synced")

if not changed:
    print(f"sync_template: {checked} file(s) already identical upstream")
else:
    print(f"sync_template: {'would update' if DRY else 'updated'} {len(changed)}: {', '.join(changed)}")
