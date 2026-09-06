#!/usr/bin/env bash
# vendor-status-watch — daily pipeline (runs unattended; the engine timer or cron calls it).
# build_map (self-healing vendor map) -> poll_all (history) -> gen_site (docs/) -> commit + push.
# Every step fails loudly: a broken run must never leave a half-regenerated site or a
# stale-but-green board. Exit non-zero on any failure so state/pipelines.json shows it.
set -euo pipefail
cd "$(dirname "$0")"
HERE="$(pwd -P)"   # absolute; "$(dirname "$0")" is RELATIVE to the caller's cwd and is wrong after this cd
log() { echo "[$(date -u +%FT%TZ)] $*"; }

# c144: the engine's timer run on 2026-09-04 05:30 PT died at its hard 900s limit and left NO
# evidence of which stage stalled (capture_output only survives a normal exit). Two fixes:
# (1) single-flight — a founder cycle's by-hand run overlapping the timer's run meant two
#     poll_all processes and two concurrent Space commits with delete_patterns=["*"];
# (2) every stage line also goes to pipeline.log, and each network-heavy stage runs under
#     `timeout` so a stalled upload fails loudly inside the budget instead of eating it.
#     Budget sums to < 900s: build_map 150 + poll 420 + hf_site 180 + hf_mirror 90 + misc.
exec 9>.pipeline.lock
if ! flock -n 9; then log "another run holds .pipeline.lock — skipped"; exit 0; fi
exec > >(tee -a pipeline.log) 2>&1
log "==== pipeline start (pid $$)"
trap 'log "==== pipeline end (exit $?)"' EXIT
T() { timeout --foreground "$@"; }   # T <seconds> <cmd...>

# PUBLISH_ONLY=1 bash pipeline.sh  -> skip the map rebuild + 7-minute poll and just
# re-render + publish (copy fixes between daily runs). Data stays whatever the last
# poll wrote, so the "Data as of" stamp on the page is still the poll's, not now's.
if [ "${PUBLISH_ONLY:-0}" = "1" ]; then
  log "PUBLISH_ONLY=1: skipping build_map + poll_all (re-render + publish only)"
else
log "build_map"
T 120 python3 build_map.py "${PROBE_JSON:-probe.json}" vendors.json
python3 - <<'PY'
import json; d=json.load(open("vendors.json"))
assert d["count"] > 1000 and d["supported"] > 700, f"map health: {d['count']} / {d['supported']}"
print("map ok:", d["count"], "vendors,", d["supported"], "supported")
PY

log "poll_all"
T 400 python3 poll_all.py      # exits 2 if <60% of supported vendors parsed; T kills it at 400s (its own stall cap is 7 min)
fi

# ---- DAILY DIGEST tier fulfilment (c140) --------------------------------------
# The paid offer that needs no 5-minute runner: reads Gumroad sales of the digest listing,
# posts one message per buyer to THEIR webhook, keeps per-sale state in ../digest_state.json
# (outside this public repo). Runs after the poll so it reports today's data; runs even in
# PUBLISH_ONLY mode because a missed digest is a broken promise. Non-fatal for the site
# build, but its line in the log is the delivery evidence — read it.
if [ -n "${GUMROAD_ACCESS_TOKEN:-}" ]; then
  log "digest"; T 45 python3 digest.py || log "digest: FAILED (non-fatal for the site; buyers may have missed today's message)"
else
  log "digest: GUMROAD_ACCESS_TOKEN absent, skipped"
fi

# The file forkers actually run is template/watch.py; test_watch.py imports the
# product/ copy. They drifted (c143: product/ still pointed SITE at the dead
# github.io host and printed a /vendors/ URL HF 302s off-site), so the test now
# asserts they are byte-identical. Fatal: shipping a template with a dead link in
# it is the one thing a free-distribution venture cannot afford.
log "test_watch (shipped-copy guard + diff engine + end-to-end)"
python3 test_watch.py > /dev/null

log "gen_site"
python3 gen_site.py
# c189: per-vendor MARKDOWN outage-history pages inside the repo. docs/ is
# invisible to search engines twice over — the bound Pages URL is a 404 (flagged
# account, A024) and the working mirror is on *.static.hf.space, which serves its
# own robots.txt and discards ours. github.com is crawlable and we push here every
# run; GitHub renders .md as a page and .html as source, so Markdown is the only
# format that works. Selftest is fatal: it gates the median sample floor and the
# requirement that the dataset's own classifier partitions every incident.
log "gen_vendor_md"
python3 gen_vendor_md.py --selftest && python3 gen_vendor_md.py \
  || log "gen_vendor_md: FAILED (non-fatal)"
test -s docs/index.html && test -s docs/api/snapshot.json && test -s docs/sitemap.xml
grep -q '@media' docs/index.html
python3 - <<'PY'
import json
n = json.load(open("docs/api/vendors.json"))["count"]
html = open("docs/index.html").read()
assert f"{n:,} SaaS vendors" in html, f"api/vendors.json says {n} vendors but index.html does not — two public surfaces disagree"
print("surface check ok:", n, "vendors on both api/vendors.json and index.html")
PY
# NOTE: gen_site writes docs/api/vendors.json itself (alias-collapsed). Do not cp the raw map over it.

# ...and the PUBLIC template repo is a fourth copy nobody was reconciling. Pushes
# watch.py/platforms.py/config.json, regenerates the README's pre-filled one-click
# workflow link, and (c148) rewrites the README's headline numbers from
# docs/api/stats.json — which is why this runs AFTER gen_site. Non-fatal.
log "sync_template"; T 30 python3 sync_template.py || log "sync_template: FAILED (non-fatal)"
# c151: the reusable Action (APVentureEngine/vendor-status-watch-action) ships the same
# watch.py/platforms.py. Force-pushing main keeps a forked-action user on current code;
# release TAGS (v1, v1.0.0) are cut by hand so a breaking change never lands on @v1.
log "sync_action"; T 45 python3 sync_action.py || log "sync_action: FAILED (non-fatal)"

# ---- publish the LIVE site (Hugging Face static Space) -------------------------
# This is the canonical public surface since 2026-09-04: GitHub Pages stopped
# building for the whole APVentureEngine org and we have no lever over it. This
# step is FATAL on failure — if it fails, the thing strangers read is stale and
# every "rebuilt daily" claim on the page is false. hf_site.py verifies the LIVE
# bytes after upload (a push is not a deploy), so a green line here means a
# stranger really can read today's data.
# c136: was "$(dirname "$0")/../../warn-feed/…", which only resolved when the caller's cwd
# was already product/ — `bash product/pipeline.sh` from the venture root silently fell back
# to system python3 (no huggingface_hub) and the Space upload FAILED while the run stayed green.
HFPY="${HF_PYTHON:-$HERE/../../warn-feed/product/.venv-hf/bin/python3}"
if [ ! -x "$HFPY" ] || ! "$HFPY" -c 'import huggingface_hub' 2>/dev/null; then
  log "hf_site: no python with huggingface_hub at $HFPY — FATAL (the live Space would go stale)"
  exit 3
fi
log "hf_site (live site)"
# c156: 120s was killed (exit 124) at 12:16Z when warn-feed's publish.sh was uploading 3,993
# files to HF at the same minute (both timers fire 12:15Z); a normal run takes ~16s. 240s
# absorbs a contended upload; everything after this step (push, release, indexnow, hf_mirror)
# is lost when it dies, so a generous bound is cheaper than a half-published run.
T 240 "$HFPY" hf_site.py

# c172: Netlify copy — the first host without HF's injected canonical header
# (which voids the 1,146 per-vendor pages for search). Only runs once
# NETLIFY_AUTH_TOKEN is unlocked (A029); non-fatal so the Space still ships.
if [ -n "${NETLIFY_AUTH_TOKEN:-}" ]; then
  log "netlify_site (controlled host)"
  T 300 python3 netlify_site.py || log "WARN: netlify deploy failed (non-fatal)"
else
  log "netlify_site: skipped (NETLIFY_AUTH_TOKEN not set)"
fi

if [ -d .git ] && [ -n "${GITHUB_ORG_TOKEN:-}" ]; then
  log "commit + push"
  # c151: this used to stage a hand-typed list of DATA paths only, so README.md — a claim
  # surface whose "opened in the last 30 days" number sync_readme rewrites every run — was
  # regenerated locally and never pushed (public copy sat 6 incidents stale, and the new
  # action link would never have shipped). Stage the sources too; .gitignore holds the
  # excludes. action/ is deliberately ignored here: it has its own repo (sync_action.py).
  # c165: apify/ is the Apify Actor's source (MIT, same parsers) — it ships in this
  # repo so the Store listing has readable source behind it. action/ stays ignored
  # because it has its own repo (sync_action.py); apify/ does not.
  git add -A vendors.json vendors history docs seed_extra.json .indexnow_last \
             README.md space_readme.md site_config.json pipeline.sh template apify ./*.py 2>/dev/null \
    || git add -A vendors.json history docs seed_extra.json
  if git diff --cached --quiet; then log "nothing to commit"; else
    git -c user.name=vendor-status-watch -c user.email=bot@apventureengine.invalid commit -q -m "daily: $(date -u +%F) $(python3 -c 'import json;r=json.load(open("poll_report.json"));print(r["parsed"],"/",r["polled"],"parsed,",r["states"])')"
    git push -q "https://x-access-token:${GITHUB_ORG_TOKEN}@github.com/APVentureEngine/vendor-status-watch.git" HEAD:main
  fi
else
  log "no git repo / token here — skipped push (pre-creation dry run)"
fi
# c150: daily GitHub Release of vendors.json + snapshot.json + stats.json + the incident-history
# tarball. Pages-independent publish surface with a per-asset DOWNLOAD COUNT — the only usage
# meter this venture has (repo traffic reads 0, the Space exposes no analytics). Idempotent per
# day; prunes releases older than 60 d after logging their counts. Non-fatal.
if [ -n "${GITHUB_ORG_TOKEN:-}" ]; then
  log "gh_release"; T 180 python3 gh_release.py || log "gh_release: FAILED (non-fatal)"
fi

# c130: the GitHub repo DESCRIPTION is a claim surface too (warn-feed learning c98) — keep its
# counts equal to the alias-collapsed numbers the page shows. PATCHed only on change; non-fatal.
if [ -n "${GITHUB_ORG_TOKEN:-}" ]; then
python3 - <<'PY' || log "repo description sync: FAILED (non-fatal)"
import json, os, urllib.request
vj = json.load(open("docs/api/vendors.json"))
n, sup = vj["count"], sum(1 for v in vj["vendors"] if v.get("supported"))
want = (f"Vendor Status Watch — live map of {n:,} SaaS status pages ({sup:,} machine-readable, incl. AWS, Azure, "
        f"Google Cloud, Slack, Stripe) + 14k incident histories, rebuilt daily. Free GitHub Actions alerting template.")
hdr = {"Authorization": "Bearer " + os.environ["GITHUB_ORG_TOKEN"], "Accept": "application/vnd.github+json",
       "User-Agent": "vendor-status-watch"}
url = "https://api.github.com/repos/APVentureEngine/vendor-status-watch"
cur = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30)).get("description")
if cur != want:
    req = urllib.request.Request(url, data=json.dumps({"description": want}).encode(), headers=hdr, method="PATCH")
    got = json.load(urllib.request.urlopen(req, timeout=30)).get("description")
    assert got == want, "description PATCH did not land"
    print("repo description updated:", want)
else:
    print("repo description already current")
PY
fi

# IndexNow: only when the URL set changed; needs the key file live, so it naturally waits for the first deploy.
log "indexnow"; T 30 python3 indexnow_submit.py || log "indexnow: FAILED (non-fatal)"

# Hugging Face mirror (second discovery surface). Non-fatal: the site is already live; report honestly.
if [ -n "${HF_TOKEN:-}" ]; then
  log "hf_mirror"
  if T 60 "$HFPY" hf_mirror.py 2>&1 | grep -v -i warning; then log "hf_mirror: OK"; else log "hf_mirror: FAILED (non-fatal)"; fi
  # c182: DERIVED outage-duration / MTTR dataset — a second HF search surface for the SRE
  # vocabulary ("outage duration", "mttr", "incident resolution time") the main mirror's id
  # cannot match. Reads hf_staging/data/incidents.csv that hf_mirror.py just built, so the
  # two cannot disagree. Selftest is FATAL (it guards the exclusion buckets and the
  # communication-not-reliability caveat); the upload is non-fatal.
  log "hf_outage_duration"
  T 30 python3 hf_outage_duration.py --selftest
  if T 60 "$HFPY" hf_outage_duration.py 2>&1 | grep -v -i warning; then log "hf_outage_duration: OK"; else log "hf_outage_duration: FAILED (non-fatal)"; fi
else
  log "hf_mirror: HF_TOKEN absent, skipped"
fi
# c182: HF download/like counts per dataset -> out/hf_downloads.jsonl (public endpoint, stdlib,
# non-fatal). The only stranger channel this venture has, recorded as a series.
log "hf_stats"; T 30 python3 hf_stats.py || log "hf_stats: FAILED (non-fatal)"
log "done"
