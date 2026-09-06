#!/usr/bin/env python3
"""Publish the DERIVED per-incident outage-duration / per-vendor MTTR dataset to
Hugging Face (c182, 2026-09-06).

WHY A SECOND HF DATASET, not another section on the first one:
HF dataset search matches tokens in the repo id (c91, c175). The main mirror,
`saas-vendor-status-pages-outages-incidents-daily`, ranks for "status page" and
"vendor outages"; nobody searching "outage duration", "MTTR", "incident
resolution time" or "time to resolve" reaches it, because those words are not
in that id. HF is the only channel producing measurable strangers for this
venture (68 downloads/30d vs 0 stars), so a second surface aimed at the SRE
vocabulary is the cheapest real distribution available. Same pattern as
warn-feed/product/hf_notice_period.py.

WHAT IT SHIPS:
- data/incident_durations.csv — one row per incident that has BOTH a vendor-
  published start and resolve time, with `duration_minutes`.
- data/vendor_summary.csv — per vendor: measured incidents, median / p90 /
  total minutes, major+critical share, last-90-day counts.
- A card whose every number is computed here from the same staged incidents
  file hf_mirror.py just uploaded, so the two datasets cannot disagree.

HONESTY RAILS (selftest enforces them; it is FATAL in pipeline.sh):
- Excluded, never guessed: scheduled maintenance, incidents with no resolve
  time (still open), resolutions we INFERRED rather than the vendor posting,
  and negative durations. Each exclusion count is printed on the card and the
  buckets must partition the input exactly.
- The card must say that incident count measures how much a vendor
  COMMUNICATES, not how reliable it is, and that history depth differs by
  platform (Statuspage backfills; others accumulate from first watch), so
  cross-vendor counts are not comparable.
- Window and "as of" are anchored on the snapshot's generated_at, never now().

Usage (cwd = product/, AFTER hf_mirror.py has staged hf_staging/):
  python3 hf_outage_duration.py --selftest
  python3 hf_outage_duration.py --dry-run     # stage card + CSVs, upload nothing
  python3 hf_outage_duration.py               # create/update the dataset (HF_TOKEN)
"""
import argparse
import csv
import json
import os
import shutil
import statistics
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hf_staging", "data", "incidents.csv")
SNAP = os.path.join(HERE, "docs", "api", "snapshot.json")
STAGE = os.path.join(HERE, "hf_od_staging")
OUTJSON = os.path.join(HERE, "hf_outage_duration.json")
DATASET_NAME = "saas-vendor-outage-duration-incident-resolution-time-mttr"
REPO_ID = "APProjects/" + DATASET_NAME
MAIN_DS = "https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily"
SITE = "https://approjects-vendor-status-watch.static.hf.space"
REPO = "https://github.com/APVentureEngine/vendor-status-watch"
MIN_FOR_RANK = 20   # vendors ranked by median only with at least this many measured incidents

CAVEAT_COMMS = "how much a vendor communicates"
CAVEAT_DEPTH = "history depth differs by platform"

FRONT = """---
pretty_name: How long SaaS vendor outages last (incident resolution time / MTTR per vendor, from their own status pages)
license: cc-by-4.0
language:
  - en
task_categories:
  - tabular-regression
  - time-series-forecasting
tags:
  - outage
  - outage-duration
  - mttr
  - incident-resolution-time
  - time-to-resolve
  - downtime
  - saas
  - vendor-management
  - sre
  - reliability
  - statuspage
  - incident-management
  - third-party-risk
  - daily-updated
  - tabular
size_categories:
  - 10K<n<100K
configs:
  - config_name: incident_durations
    default: true
    data_files:
      - split: train
        path: data/incident_durations.csv
  - config_name: vendor_summary
    data_files:
      - split: train
        path: data/vendor_summary.csv
---
"""

CARD = FRONT + """
# How long do SaaS vendor outages last? Incident resolution time per vendor, rebuilt daily

**As of {as_of}.** For every incident a vendor posted on its own public status
page with BOTH an opened time and a resolved time, this dataset computes

`duration_minutes = resolved_at - started_at`

and rolls it up per vendor. It is derived, every day, from the incident table in
[{main_name}]({main_ds}); the two are rebuilt by the same job and cannot
disagree.

## The headline, over {measured:,} measured incidents across {vendors:,} vendors

| | |
|---|---|
| Incidents with both times, vendor-posted | **{measured:,}** |
| **Median** time from opened to resolved | **{median_h}** |
| 90th percentile | **{p90_h}** |
| Resolved in **under 1 hour** | {under1h:,} ({under1h_pct:.1f}%) |
| Open for **more than 24 hours** | {over24h:,} ({over24h_pct:.1f}%) |
| Major or critical impact | {majcrit:,} — median **{majcrit_median_h}** |

## Excluded, and counted rather than guessed

| bucket | rows |
|---|---|
| Included (both times, vendor-posted, non-negative) | {measured:,} |
| Scheduled maintenance (not an outage) | {x_maint:,} |
| Still open / no resolve time posted | {x_open:,} |
| Resolve time we inferred (vendor never posted one) | {x_inferred:,} |
| Resolved before opened (vendor data error) | {x_negative:,} |
| **Total incidents in the source table** | **{total:,}** |

## Most incidents in the last 90 days (to {as_of_date})

Incident count measures **{caveat_comms}**, not how reliable it is: a vendor that
posts every blip ranks "worse" here than one that posts nothing. Read it with
the median next to it.

| vendor | incidents, 90d | median minutes, 90d | all-time measured |
|---|---|---|---|
{top90_table}{cap_note}

## Slowest and fastest to resolve (vendors with at least {min_rank} measured incidents)

| slowest median | minutes | | fastest median | minutes |
|---|---|---|---|---|
{slow_fast_table}

## What is in the files

`data/incident_durations.csv` — **{measured:,} rows**, one per measured incident:

| column | meaning |
|---|---|
| `vendor_slug` | stable id; incident history page at `{site}/v/<vendor_slug>.html` |
| `vendor` | vendor display name |
| `platform` | status-page platform the vendor uses |
| `incident_id` | the vendor's own incident id |
| `title` | incident title as posted |
| `impact` | vendor-declared impact (`none`, `minor`, `major`, `critical`) |
| `started_at` / `resolved_at` | ISO-8601, exactly as the vendor published them |
| `duration_minutes` | `resolved_at - started_at`, integer minutes |
| `url` | the incident's permalink on the vendor's status page |

`data/vendor_summary.csv` — **{vendors:,} rows**, one per vendor with at least one
measured incident: `incidents_measured`, `first_incident`, `last_incident`,
`median_minutes`, `p90_minutes`, `mean_minutes`, `total_minutes`,
`major_critical_count`, `major_critical_median_minutes`, `incidents_90d`,
`minutes_90d`.

```python
import pandas as pd
d = pd.read_csv("https://huggingface.co/datasets/{repo_id}/resolve/main/data/incident_durations.csv")
d.groupby("vendor")["duration_minutes"].median().sort_values().tail(20)   # slowest to resolve
```

## Method, and what it does NOT say

- Times are the vendor's own, as posted on its status page. This is **posted
  incident duration**, not measured downtime: a vendor can open the incident
  late, resolve it early, or never post one at all. It is not an uptime or SLA
  figure and must not be read as one.
- **{caveat_depth_cap}**: Atlassian Statuspage exposes a public incident
  archive that we back-fill (capped at 50 incidents per vendor by that API);
  other platforms accumulate only from the day we first watched them
  ({first_watch}). Cross-vendor counts are therefore not comparable; medians
  are more robust than counts.
- Scheduled maintenance is excluded because a planned window is not an outage.
- Where a resolve time is missing, or where we had to infer resolution from the
  incident disappearing, the incident is excluded — never estimated.
- Impact labels are the vendor's; "major" at one vendor is not "major" at
  another.

## Freshness

Rebuilt daily by an automated pipeline from {n_vendors_map:,} vendor status
pages; source snapshot generated `{generated_at}`. A static copy of this table
is wrong within a week, which is why it is published here rather than once.

## Related

- [{main_name}]({main_ds}) — the full incident and vendor tables this is derived from.
- [{site_host}]({site}) — the live board, per-vendor history pages, RSS and JSON.
- [Source and MIT template]({repo}) — watch your own vendors from GitHub Actions.

## License

CC BY 4.0. Underlying incidents are the vendors' own public status-page posts.
Attribution: "Vendor Status Watch, {site}".

*Not affiliated with any vendor named here.*
"""


def parse_ts(s):
    s = (s or "").strip()
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def is_maintenance(r):
    t = (r.get("title") or "").lower()
    return (r.get("impact") or "").lower() == "maintenance" or (r.get("state") or "").lower() == "maintenance" \
        or "scheduled maintenance" in t or t.startswith("maintenance")


def classify(rows):
    """Partition source rows into buckets. Returns (measured_rows, counts)."""
    c = {"maint": 0, "open": 0, "inferred": 0, "negative": 0}
    measured = []
    for r in rows:
        if is_maintenance(r):
            c["maint"] += 1
            continue
        if str(r.get("resolved_inferred", "")).lower() == "true":
            c["inferred"] += 1
            continue
        a, b = parse_ts(r.get("started_at")), parse_ts(r.get("resolved_at"))
        if a is None or b is None:
            c["open"] += 1
            continue
        mins = int((b - a).total_seconds() // 60)
        if mins < 0:
            c["negative"] += 1
            continue
        measured.append({
            "vendor_slug": r["vendor_slug"], "vendor": r["vendor"], "platform": r["platform"],
            "incident_id": r["incident_id"], "title": r["title"], "impact": (r.get("impact") or "").lower(),
            "started_at": r["started_at"], "resolved_at": r["resolved_at"],
            "duration_minutes": mins, "url": r.get("url", ""),
            "_start": a,
        })
    return measured, c


def pct(vals, q):
    if not vals:
        return 0
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(round(q * (len(s) - 1)))))
    return s[k]


def fmt_h(mins):
    if mins < 120:
        return f"{mins} min"
    if mins < 48 * 60:
        return f"{mins / 60:.1f} h"
    return f"{mins / 1440:.1f} days"


def summarise(measured, anchor, src_rows=()):
    d90 = anchor - timedelta(days=90)
    # Statuspage's public incident API returns at most 50 incidents. A vendor sitting at
    # that cap whose archive STARTS inside the 90-day window has an UNKNOWN 90-day count,
    # not a low one; flag it as a floor ("≥"). Same rule as hf_mirror.py / gen_site.CENSORED_90.
    src_tot, src_oldest = {}, {}
    for r in src_rows:
        sl = r["vendor_slug"]
        src_tot[sl] = src_tot.get(sl, 0) + 1
        st = parse_ts(r.get("started_at"))
        if st is not None:
            src_oldest[sl] = min(src_oldest.get(sl, st), st)
    by = {}
    for m in measured:
        by.setdefault(m["vendor_slug"], []).append(m)
    out = []
    for slug, ms in by.items():
        censored = src_tot.get(slug, 0) >= 50 and slug in src_oldest and src_oldest[slug] > d90
        durs = [m["duration_minutes"] for m in ms]
        mc = [m["duration_minutes"] for m in ms if m["impact"] in ("major", "critical")]
        n90 = [m for m in ms if m["_start"] >= d90]
        out.append({
            "vendor_slug": slug, "vendor": ms[0]["vendor"], "platform": ms[0]["platform"],
            "incidents_measured": len(ms),
            "first_incident": min(m["started_at"] for m in ms),
            "last_incident": max(m["started_at"] for m in ms),
            "median_minutes": int(statistics.median(durs)),
            "p90_minutes": int(pct(durs, 0.9)),
            "mean_minutes": int(statistics.mean(durs)),
            "total_minutes": int(sum(durs)),
            "major_critical_count": len(mc),
            "major_critical_median_minutes": int(statistics.median(mc)) if mc else "",
            "incidents_90d": len(n90),
            "minutes_90d": int(sum(m["duration_minutes"] for m in n90)),
            "incidents_90d_is_floor": censored,
            "_median_90d": int(statistics.median([m["duration_minutes"] for m in n90])) if n90 else "",
        })
    out.sort(key=lambda r: (-r["incidents_measured"], r["vendor_slug"]))
    return out


def load_source():
    if not os.path.exists(SRC):
        sys.exit(f"hf_outage_duration: {SRC} missing — run hf_mirror.py first")
    with open(SRC, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    snap = json.load(open(SNAP, encoding="utf-8"))
    gen = (snap.get("generated_at") or "")[:19]
    anchor = datetime.strptime(gen, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    first_watch = min((r.get("first_seen") or "9999" for r in rows), default="")[:10]
    return rows, snap, gen, anchor, first_watch


def render(rows, snap, gen, anchor, first_watch):
    measured, c = classify(rows)
    total = len(rows)
    assert len(measured) + sum(c.values()) == total, "buckets must partition the source rows"
    durs = [m["duration_minutes"] for m in measured]
    mc = [m["duration_minutes"] for m in measured if m["impact"] in ("major", "critical")]
    summary = summarise(measured, anchor, rows)
    m = {
        "total": total, "measured": len(measured), "vendors": len(summary),
        "median": int(statistics.median(durs)) if durs else 0,
        "p90": int(pct(durs, 0.9)),
        "under1h": sum(1 for d in durs if d < 60),
        "over24h": sum(1 for d in durs if d > 1440),
        "majcrit": len(mc), "majcrit_median": int(statistics.median(mc)) if mc else 0,
        "x_maint": c["maint"], "x_open": c["open"], "x_inferred": c["inferred"], "x_negative": c["negative"],
        "generated_at": gen + "Z", "first_watch": first_watch,
        "n_vendors_map": len(snap.get("vendors", [])),
    }
    top90 = sorted([s for s in summary if s["incidents_90d"] > 0],
                   key=lambda s: (-s["incidents_90d"], s["vendor_slug"]))[:25]
    top90_table = "\n".join(
        f"| [{s['vendor']}]({SITE}/v/{s['vendor_slug']}.html) | {'≥ ' if s['incidents_90d_is_floor'] else ''}{s['incidents_90d']} | {s['_median_90d']} | {s['incidents_measured']} |"
        for s in top90) or "| (none yet) | | | |"
    n_floor = sum(1 for s in top90 if s["incidents_90d_is_floor"])
    m["n_floor"] = n_floor
    cap_note = (f"\n\n**\u201c\u2265\u201d on {n_floor} row(s):** the source status-page API returns at most 50 "
                f"incidents per vendor, and these vendors' archives begin inside the 90-day window, so the "
                f"count is a floor rather than a total. The median beside it is over the incidents we can see."
                if n_floor else "")
    ranked = [s for s in summary if s["incidents_measured"] >= MIN_FOR_RANK]
    slow = sorted(ranked, key=lambda s: (-s["median_minutes"], s["vendor_slug"]))[:10]
    fast = sorted(ranked, key=lambda s: (s["median_minutes"], s["vendor_slug"]))[:10]
    sf_rows = []
    for i in range(max(len(slow), len(fast))):
        a = slow[i] if i < len(slow) else None
        b = fast[i] if i < len(fast) else None
        sf_rows.append(
            f"| {a['vendor'] if a else ''} | {a['median_minutes'] if a else ''} | | "
            f"{b['vendor'] if b else ''} | {b['median_minutes'] if b else ''} |")
    slow_fast_table = "\n".join(sf_rows) or "| (fewer than %d incidents everywhere) | | | | |" % MIN_FOR_RANK
    card = CARD.format(
        as_of=gen[:16].replace("T", " ") + " UTC", as_of_date=gen[:10],
        main_name="saas-vendor-status-pages-outages-incidents-daily", main_ds=MAIN_DS,
        measured=m["measured"], vendors=m["vendors"],
        median_h=fmt_h(m["median"]), p90_h=fmt_h(m["p90"]),
        under1h=m["under1h"], under1h_pct=100.0 * m["under1h"] / max(1, m["measured"]),
        over24h=m["over24h"], over24h_pct=100.0 * m["over24h"] / max(1, m["measured"]),
        majcrit=m["majcrit"], majcrit_median_h=fmt_h(m["majcrit_median"]),
        x_maint=m["x_maint"], x_open=m["x_open"], x_inferred=m["x_inferred"], x_negative=m["x_negative"],
        total=m["total"], caveat_comms=CAVEAT_COMMS, caveat_depth_cap=CAVEAT_DEPTH[0].upper() + CAVEAT_DEPTH[1:],
        top90_table=top90_table, cap_note=cap_note, min_rank=MIN_FOR_RANK, slow_fast_table=slow_fast_table,
        site=SITE, site_host=SITE.split("//")[1], repo_id=REPO_ID, repo=REPO,
        first_watch=first_watch, generated_at=m["generated_at"], n_vendors_map=m["n_vendors_map"],
    )
    return measured, summary, m, card


def _assert_card_honest(card, m, measured):
    assert CAVEAT_COMMS in card, "card must say counts measure communication, not reliability"
    assert CAVEAT_DEPTH.lower() in card.lower(), "card must say history depth differs by platform"
    flat = " ".join(card.split())
    assert "not an uptime or SLA figure" in flat, "card must disclaim uptime/SLA"
    assert f"{m['x_negative']:,}" in card and f"{m['x_inferred']:,}" in card, "exclusion counts must be printed"
    assert f"{m['total']:,}" in card and f"{m['measured']:,}" in card
    assert m["measured"] + m["x_maint"] + m["x_open"] + m["x_inferred"] + m["x_negative"] == m["total"]
    assert all(x["duration_minutes"] >= 0 for x in measured), "no negative durations may ship"
    assert not any(is_maintenance(x) for x in measured), "maintenance rows may not ship"
    assert "{" not in card.replace("{{", "").replace("}}", "") or "```" in card  # format placeholders resolved
    for tok in ("{as_of}", "{measured", "{top90_table}", "{slow_fast_table}", "{cap_note}"):
        assert tok not in card, f"unresolved placeholder {tok}"
    if m.get("n_floor"):
        assert "floor rather than a total" in card, "capped 90d counts must be explained on the card"
        assert card.count("| \u2265 ") == m["n_floor"], "every floor row must carry the \u2265 mark"


def stage(measured, summary, card):
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(os.path.join(STAGE, "data"))
    icols = ["vendor_slug", "vendor", "platform", "incident_id", "title", "impact",
             "started_at", "resolved_at", "duration_minutes", "url"]
    with open(os.path.join(STAGE, "data", "incident_durations.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=icols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(measured, key=lambda r: (r["started_at"], r["vendor_slug"], r["incident_id"])):
            w.writerow(r)
    scols = ["vendor_slug", "vendor", "platform", "incidents_measured", "first_incident", "last_incident",
             "median_minutes", "p90_minutes", "mean_minutes", "total_minutes", "major_critical_count",
             "major_critical_median_minutes", "incidents_90d", "incidents_90d_is_floor", "minutes_90d"]
    with open(os.path.join(STAGE, "data", "vendor_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=scols, extrasaction="ignore")
        w.writeheader()
        for r in summary:
            w.writerow(r)
    with open(os.path.join(STAGE, "README.md"), "w", encoding="utf-8") as f:
        f.write(card)


def build(dry_run=False):
    rows, snap, gen, anchor, first_watch = load_source()
    measured, summary, m, card = render(rows, snap, gen, anchor, first_watch)
    _assert_card_honest(card, m, measured)
    stage(measured, summary, card)
    with open(OUTJSON, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=1, sort_keys=True)
    print(f"hf_outage_duration: staged {m['measured']:,} durations across {m['vendors']:,} vendors "
          f"(median {m['median']} min, p90 {m['p90']} min), card {len(card):,} bytes -> {STAGE}")
    if dry_run:
        print("hf_outage_duration: --dry-run, nothing uploaded")
        return 0
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("hf_outage_duration: HF_TOKEN not set — staged only")
        return 0
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    api.create_repo(REPO_ID, repo_type="dataset", exist_ok=True)
    api.upload_folder(folder_path=STAGE, repo_id=REPO_ID, repo_type="dataset",
                      commit_message=f"daily rebuild {gen[:10]}")
    info = api.dataset_info(REPO_ID)
    assert any(s.rfilename == "data/incident_durations.csv" for s in info.siblings), "upload did not land"
    print(f"hf_outage_duration: uploaded -> https://huggingface.co/datasets/{REPO_ID} (files: {len(info.siblings)})")
    return 0


def selftest():
    # synthetic partition test
    rows = [
        {"vendor_slug": "a", "vendor": "A", "platform": "statuspage", "incident_id": "1", "title": "Down",
         "impact": "major", "state": "resolved", "started_at": "2026-01-01T00:00:00Z",
         "resolved_at": "2026-01-01T01:30:00Z", "resolved_inferred": "False", "url": "", "first_seen": "2026-01-02"},
        {"vendor_slug": "a", "vendor": "A", "platform": "statuspage", "incident_id": "2", "title": "Scheduled Maintenance",
         "impact": "maintenance", "state": "maintenance", "started_at": "2026-01-01T00:00:00Z",
         "resolved_at": "2026-01-01T02:00:00Z", "resolved_inferred": "False", "url": "", "first_seen": "2026-01-02"},
        {"vendor_slug": "a", "vendor": "A", "platform": "statuspage", "incident_id": "3", "title": "Open",
         "impact": "minor", "state": "investigating", "started_at": "2026-01-01T00:00:00Z",
         "resolved_at": "", "resolved_inferred": "False", "url": "", "first_seen": "2026-01-02"},
        {"vendor_slug": "a", "vendor": "A", "platform": "statuspage", "incident_id": "4", "title": "Inferred",
         "impact": "minor", "state": "resolved", "started_at": "2026-01-01T00:00:00Z",
         "resolved_at": "2026-01-01T00:10:00Z", "resolved_inferred": "True", "url": "", "first_seen": "2026-01-02"},
        {"vendor_slug": "a", "vendor": "A", "platform": "statuspage", "incident_id": "5", "title": "Reversed",
         "impact": "minor", "state": "resolved", "started_at": "2026-01-01T05:00:00Z",
         "resolved_at": "2026-01-01T00:10:00Z", "resolved_inferred": "False", "url": "", "first_seen": "2026-01-02"},
    ]
    measured, c = classify(rows)
    assert len(measured) == 1 and measured[0]["duration_minutes"] == 90, (measured, c)
    assert c == {"maint": 1, "open": 1, "inferred": 1, "negative": 1}, c
    # real data end-to-end, no upload
    rows, snap, gen, anchor, first_watch = load_source()
    measured, summary, m, card = render(rows, snap, gen, anchor, first_watch)
    _assert_card_honest(card, m, measured)
    assert m["measured"] > 1000, "unexpectedly few measured incidents"
    assert sum(s["incidents_measured"] for s in summary) == m["measured"]
    print(f"hf_outage_duration selftest ok ({m['measured']:,} of {m['total']:,} rows measured, "
          f"{m['vendors']:,} vendors, {len(card):,}-byte card)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        sys.exit(0)
    sys.exit(build(dry_run=a.dry_run))
