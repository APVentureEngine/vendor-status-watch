#!/usr/bin/env bash
# vendor-status-watch — daily pipeline (runs unattended; the engine timer or cron calls it).
# build_map (self-healing vendor map) -> poll_all (history) -> gen_site (docs/) -> commit + push.
# Every step fails loudly: a broken run must never leave a half-regenerated site or a
# stale-but-green board. Exit non-zero on any failure so state/pipelines.json shows it.
set -euo pipefail
cd "$(dirname "$0")"
log() { echo "[$(date -u +%FT%TZ)] $*"; }

log "build_map"
python3 build_map.py "${PROBE_JSON:-probe.json}" vendors.json
python3 - <<'PY'
import json; d=json.load(open("vendors.json"))
assert d["count"] > 1000 and d["supported"] > 700, f"map health: {d['count']} / {d['supported']}"
print("map ok:", d["count"], "vendors,", d["supported"], "supported")
PY

log "poll_all"
python3 poll_all.py            # exits 2 if <60% of supported vendors parsed

log "gen_site"
python3 gen_site.py
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

# ---- publish the LIVE site (Hugging Face static Space) -------------------------
# This is the canonical public surface since 2026-09-04: GitHub Pages stopped
# building for the whole APVentureEngine org and we have no lever over it. This
# step is FATAL on failure — if it fails, the thing strangers read is stale and
# every "rebuilt daily" claim on the page is false. hf_site.py verifies the LIVE
# bytes after upload (a push is not a deploy), so a green line here means a
# stranger really can read today's data.
HFPY="${HF_PYTHON:-$(dirname "$0")/../../warn-feed/product/.venv-hf/bin/python3}"
[ -x "$HFPY" ] || HFPY=python3
log "hf_site (live site)"
"$HFPY" hf_site.py

if [ -d .git ] && [ -n "${GITHUB_ORG_TOKEN:-}" ]; then
  log "commit + push"
  git add -A vendors.json history docs seed_extra.json .indexnow_last 2>/dev/null || git add -A vendors.json history docs seed_extra.json
  if git diff --cached --quiet; then log "nothing to commit"; else
    git -c user.name=vendor-status-watch -c user.email=bot@apventureengine.invalid commit -q -m "daily: $(date -u +%F) $(python3 -c 'import json;r=json.load(open("poll_report.json"));print(r["parsed"],"/",r["polled"],"parsed,",r["states"])')"
    git push -q "https://x-access-token:${GITHUB_ORG_TOKEN}@github.com/APVentureEngine/vendor-status-watch.git" HEAD:main
  fi
else
  log "no git repo / token here — skipped push (pre-creation dry run)"
fi
# IndexNow: only when the URL set changed; needs the key file live, so it naturally waits for the first deploy.
log "indexnow"; python3 indexnow_submit.py || log "indexnow: FAILED (non-fatal)"

# Hugging Face mirror (second discovery surface). Non-fatal: the site is already live; report honestly.
if [ -n "${HF_TOKEN:-}" ]; then
  log "hf_mirror"
  if "$HFPY" hf_mirror.py 2>&1 | grep -v -i warning; then log "hf_mirror: OK"; else log "hf_mirror: FAILED (non-fatal)"; fi
else
  log "hf_mirror: HF_TOKEN absent, skipped"
fi
log "done"
