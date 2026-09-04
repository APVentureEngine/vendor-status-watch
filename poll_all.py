#!/usr/bin/env python3
"""poll_all.py — poll every SUPPORTED vendor in the living map and keep per-vendor history.

This is the daily data step of the pipeline (the hosted poller and the free template
use watch.py; this one feeds the public site). It never invents an "ok": a vendor whose
endpoint fails is recorded as state=unknown with the error string.

Inputs : vendors.json  (from build_map.py)
Outputs: history/<slug>.json   one file per vendor, merged across runs
         snapshot.json         the latest state of every polled vendor (site input)
         poll_report.json      counts + errors for the pipeline log

History model (per vendor):
  incidents: {id: {title, impact, state, started_at, updated_at, resolved_at,
                   resolved_inferred, url, first_seen, last_seen}}
  checks:    [{at, state}]  (last 400 runs)
For Atlassian Statuspage vendors we also read /api/v2/incidents.json (the last ~50
incidents, INCLUDING resolved ones), so their history is real from day one. Other
platforms only expose what is open right now, so their history starts on the day we
first watched them — the vendor page says so.
"""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta

import platforms as P

HERE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(HERE, "history")
KEEP_DAYS = 400
WORKERS = int(os.environ.get("POLL_WORKERS", "24"))


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sp_incidents(base):
    """Statuspage: last ~50 incidents incl. resolved. Returns [] on any failure."""
    code, body = P._get(base.rstrip("/") + "/api/v2/incidents.json")
    if code != 200:
        return []
    try:
        j = json.loads(body)
    except Exception:
        return []
    out = []
    for i in j.get("incidents") or []:
        out.append({
            "id": i.get("id"), "title": i.get("name"), "state": i.get("status"),
            "impact": i.get("impact"), "url": i.get("shortlink"),
            "started_at": i.get("created_at"), "updated_at": i.get("updated_at"),
            "resolved_at": i.get("resolved_at"),
            "body": ((i.get("incident_updates") or [{}])[0]).get("body"),
        })
    return out


def poll_one(v):
    cur = P.check(v)
    hist_inc = _sp_incidents(v["base"]) if v["platform"] == "statuspage" and not cur["error"] else []
    return v, cur, hist_inc


def load_hist(slug):
    p = os.path.join(HIST, slug + ".json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def merge(v, cur, hist_inc, prev, ts):
    h = prev or {"slug": v["slug"], "vendor": v["name"], "platform": v["platform"],
                 "status_url": cur["status_url"], "first_watched": ts,
                 "history_backfilled": False, "incidents": {}, "checks": []}
    h["vendor"], h["platform"], h["status_url"] = v["name"], v["platform"], cur["status_url"]
    h["last_checked"], h["last_state"] = ts, cur["state"]
    h["last_description"], h["last_error"] = cur["description"], cur["error"]
    open_ids = set()
    for src, backfill in ((cur["incidents"], False), (hist_inc, True)):
        for i in src:
            iid = i.get("id")
            if not iid:
                continue
            if not backfill:
                open_ids.add(iid)
            rec = h["incidents"].get(iid) or {"first_seen": ts}
            for k in ("title", "impact", "state", "url", "started_at", "updated_at", "body"):
                if i.get(k) is not None:
                    rec[k] = i[k]
            if i.get("resolved_at"):
                rec["resolved_at"] = i["resolved_at"]
                rec["resolved_inferred"] = False
            rec["last_seen"] = ts
            h["incidents"][iid] = rec
    if hist_inc:
        h["history_backfilled"] = True
    # An incident we saw open earlier and that is no longer listed: resolved at some
    # point since the last run. Say "inferred" rather than pretend we know the minute.
    if not cur["error"]:
        for iid, rec in h["incidents"].items():
            if iid not in open_ids and not rec.get("resolved_at") and rec.get("last_seen") != ts:
                rec["resolved_at"] = ts
                rec["resolved_inferred"] = True
    # Prune
    cutoff = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).isoformat()
    for iid in [k for k, r in h["incidents"].items() if (r.get("started_at") or r.get("first_seen") or "") < cutoff]:
        del h["incidents"][iid]
    h["checks"] = (h["checks"] + [{"at": ts, "state": cur["state"]}])[-400:]
    return h


def main():
    vendors = json.load(open(os.path.join(HERE, "vendors.json")))["vendors"]
    todo = [v for v in vendors if v.get("supported")]
    os.makedirs(HIST, exist_ok=True)
    ts = now_iso()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        results = list(ex.map(poll_one, todo))
    snap, errors = [], {}
    for v, cur, hist_inc in results:
        h = merge(v, cur, hist_inc, load_hist(v["slug"]), ts)
        with open(os.path.join(HIST, v["slug"] + ".json"), "w") as f:
            json.dump(h, f, indent=0, sort_keys=True)
        snap.append({"slug": v["slug"], "vendor": v["name"], "platform": v["platform"],
                     "status_url": cur["status_url"], "state": cur["state"],
                     "description": cur["description"], "open": len(cur["incidents"]),
                     "error": cur["error"], "checked_at": cur["checked_at"]})
        if cur["error"]:
            errors[cur["error"]] = errors.get(cur["error"], 0) + 1
    snap.sort(key=lambda r: r["slug"])
    json.dump({"generated_at": ts, "count": len(snap), "vendors": snap},
              open(os.path.join(HERE, "snapshot.json"), "w"), indent=0)
    parsed = sum(1 for r in snap if not r["error"])
    rep = {"at": ts, "polled": len(snap), "parsed": parsed, "unknown": len(snap) - parsed,
           "seconds": round(time.time() - t0, 1), "errors": errors,
           "states": {s: sum(1 for r in snap if r["state"] == s) for s in P.STATES}}
    json.dump(rep, open(os.path.join(HERE, "poll_report.json"), "w"), indent=1)
    print(json.dumps(rep))
    # Health assertion: a run that parsed <60% of supported vendors is a broken run,
    # not a quiet internet. Exit non-zero so the pipeline notices.
    if parsed < 0.6 * max(len(snap), 1):
        print(f"HEALTH FAIL: parsed {parsed}/{len(snap)}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
