#!/usr/bin/env python3
"""gen_vendor_md.py — per-vendor MARKDOWN outage-history pages in the repo (c189).

WHY THIS EXISTS (read before deleting it):

This venture's website is unreachable to search engines twice over. Its bound
GitHub Pages URL is a 404 (the account is flagged, A024), and the working mirror
sits on *.static.hf.space, a host that serves its own /robots.txt and silently
discards ours. Both fixes are parked on an unanswered human unlock. Meanwhile the
repo — github.com/APVentureEngine/vendor-status-watch — is crawled constantly,
has real domain authority, and we push to it on every pipeline run.

The catch: GitHub renders .md as a page and .html as escaped source, so copying
docs/v/<slug>.html across would produce unreadable blobs. Markdown is the only
format that becomes an indexable page there. Hence this script.

Target query shape: "<vendor> outage history", "is <vendor> down", "<vendor>
status page incidents" — long-tail, low-competition, and answerable only by
someone who has been recording the vendor's own status posts for a while.

HONESTY RAILS:
  * Every incident shown is the VENDOR's own post, linked back to their status
    page. We republish; we do not judge.
  * Durations come from hf_outage_duration.classify() — the dataset's own
    classifier, not a re-implementation (learning 2026-09-06). Maintenance,
    still-open, inferred-resolution and negative-interval rows are excluded and
    the exclusion counts are printed on the page.
  * A median is printed only for vendors clearing MIN_FOR_RANK measured
    incidents; below that the page says so and shows the count instead.
  * "Incidents on record" is explicitly since first_watched / backfill, never
    presented as the vendor's whole history.

Inputs : vendors.json, history/*.json, site_config.json
Outputs: vendors/<slug>.md, vendors/README.md, and a link block injected into
         README.md between sentinels.
Run    : from pipeline.sh, after the history files are refreshed.
Selftest: python3 gen_vendor_md.py --selftest
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "vendors")
HIST = os.path.join(HERE, "history")

sys.path.insert(0, HERE)
from hf_outage_duration import classify, fmt_h, MIN_FOR_RANK  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "site_config.json"), encoding="utf-8"))
REPO = CFG["repo_url"]
RAW = REPO.replace("github.com", "raw.githubusercontent.com") + "/main"
BLOB = REPO + "/blob/main"
SITE = CFG["site_url"].rstrip("/")
HF = "https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily"

MIN_INCIDENTS = 3        # below this a page is thin content and not worth indexing
RECENT = 15              # incidents listed per page

START = "<!-- VENDOR_MD_INDEX:START -->"
END = "<!-- VENDOR_MD_INDEX:END -->"


def load_vendor(slug):
    p = os.path.join(HIST, slug + ".json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (ValueError, OSError):
        return None


def rows_for(d):
    """Reshape a history file's incidents into the row shape classify() expects."""
    out = []
    for iid, r in (d.get("incidents") or {}).items():
        out.append({
            "vendor_slug": d.get("slug", ""), "vendor": d.get("vendor", ""),
            "platform": d.get("platform", ""), "incident_id": iid,
            "title": r.get("title") or "", "impact": r.get("impact") or "",
            "state": r.get("state") or "", "started_at": r.get("started_at") or "",
            "resolved_at": r.get("resolved_at") or "",
            "resolved_inferred": r.get("resolved_inferred", False),
            "url": r.get("url") or "", "first_seen": r.get("first_seen") or "",
        })
    return out


def median(vals):
    if not vals:
        return None
    v = sorted(vals)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def page(d, rows, measured, counts):
    name = d.get("vendor") or d.get("slug")
    slug = d["slug"]
    total = len(rows)
    durs = [m["duration_minutes"] for m in measured]
    med = median(durs)
    dated = sorted([r for r in rows if r["started_at"]],
                   key=lambda r: r["started_at"], reverse=True)
    span = ""
    if dated:
        span = (f" spanning **{dated[-1]['started_at'][:10]}** to "
                f"**{dated[0]['started_at'][:10]}**")

    if med is not None and len(durs) >= MIN_FOR_RANK:
        med_line = (f"Median incident length: **{fmt_h(int(med))}** across "
                    f"{len(durs)} incidents where {name} posted both a start and a "
                    f"resolve time.")
    elif durs:
        med_line = (f"Only **{len(durs)}** {name} incidents carry both a vendor-posted "
                    f"start and resolve time — below the {MIN_FOR_RANK}-incident floor "
                    f"this dataset requires before publishing a median, so none is "
                    f"quoted here.")
    else:
        med_line = (f"No {name} incident carries both a vendor-posted start and resolve "
                    f"time, so no duration statistic is available.")

    ex = counts
    excl = (f"{ex['maint']} maintenance, {ex['open']} still open or missing a timestamp, "
            f"{ex['inferred']} whose resolution time we inferred rather than read, "
            f"{ex['negative']} with a resolve time before the start time")

    tbl = ["| Started | Incident | Impact | Length |",
           "| --- | --- | --- | ---: |"]
    bym = {m["incident_id"]: m for m in measured}
    for r in dated[:RECENT]:
        t = (r["title"] or "—").replace("|", "\\|").strip()
        t = f"[{t}]({r['url']})" if r["url"] else t
        m = bym.get(r["incident_id"])
        length = fmt_h(m["duration_minutes"]) if m else "—"
        tbl.append(f"| {r['started_at'][:10]} | {t} | {(r['impact'] or '—').lower()} "
                   f"| {length} |")

    state = (d.get("last_state") or "unknown").lower()
    checked = (d.get("last_checked") or "")[:16].replace("T", " ")

    return f"""# {name} outage history — every incident their status page has posted

**{total} {name} incidents on record**{span}. Status page:
[{d.get('status_url') or 'n/a'}]({d.get('status_url') or SITE}) · platform:
`{d.get('platform') or 'unknown'}` · last polled **{checked} UTC**, last observed
state **`{state}`**.

{med_line}

This page republishes what {name} posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent {name} incidents

{chr(10).join(tbl)}

Newest {min(RECENT, len(dated))} of {total}. Full machine-readable history:
[`history/{slug}.json`]({RAW}/history/{slug}.json).

## What is counted, and what is not

Of {total} recorded incidents, **{len(measured)}** have a usable length. Excluded:
{excl}. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**{(d.get('first_watched') or 'n/a')[:10]}** — it is not a claim about {name}'s
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/{slug}.json`]({RAW}/history/{slug}.json) |
| All vendors, all incidents (dataset) | [Hugging Face]({HF}) |
| The vendor map (1,100+ status feeds) | [`vendors.json`]({RAW}/vendors.json) |
| Alert your Slack/Discord when {name} breaks | [free MIT GitHub Actions template]({CFG['template_url']}) |
| Weekly digest of your vendors | [Vendor Status Digest]({CFG['digest_url']}) · [free tier]({CFG['digest_free_url']}) |
| Browsable board with charts | [{name} on the live site]({SITE}/v/{slug}.html) |

---

[← all vendors]({BLOB}/vendors/README.md) · [repository home]({REPO}) ·
MIT licence · rebuilt daily by an automated pipeline.
"""


def build(write=True):
    vendors = json.load(open(os.path.join(HERE, "vendors.json"), encoding="utf-8"))["vendors"]
    made, index = 0, []
    for v in vendors:
        d = load_vendor(v["slug"])
        if not d:
            continue
        rows = rows_for(d)
        if len(rows) < MIN_INCIDENTS:
            continue
        measured, counts = classify(rows)
        assert len(measured) + sum(counts.values()) == len(rows), \
            f"{v['slug']}: buckets must partition the incidents"
        if write:
            os.makedirs(OUTDIR, exist_ok=True)
            open(os.path.join(OUTDIR, v["slug"] + ".md"), "w", encoding="utf-8").write(
                page(d, rows, measured, counts))
        durs = [m["duration_minutes"] for m in measured]
        med = median(durs)
        index.append({
            "slug": v["slug"], "name": d.get("vendor") or v["name"],
            "n": len(rows), "measured": len(durs),
            "median": fmt_h(int(med)) if med is not None and len(durs) >= MIN_FOR_RANK else "—",
            "last": max((r["started_at"][:10] for r in rows if r["started_at"]), default="—"),
        })
        made += 1
    return made, index, len(vendors)


def index_page(index, n_vendors):
    index.sort(key=lambda r: -r["n"])
    body = "\n".join(
        f"| [{r['name']}]({r['slug']}.md) | {r['n']:,} | {r['measured']:,} | "
        f"{r['median']} | {r['last']} |" for r in index)
    total = sum(r["n"] for r in index)
    return f"""# SaaS vendor outage history, vendor by vendor

Public status-page incidents for **{len(index)} vendors** with at least
{MIN_INCIDENTS} recorded incidents — **{total:,} incidents** in all, out of
{n_vendors:,} vendor status feeds this project polls. Every page republishes what
the vendor itself posted, links back to the original, and is rebuilt daily.

A median is shown only where the vendor posted both a start and a resolve time
for at least {MIN_FOR_RANK} incidents; "—" means the sample is too small to
publish one, not that the vendor is fast.

Some rows below are identical by construction, because the two products share one
status page — Twilio and SendGrid post to the same feed, as do Cherwell and Ivanti
Cloud. That is not a duplicate row; it is what the vendors publish.

| Vendor | Incidents on record | With a measurable length | Median length | Latest |
| --- | ---: | ---: | ---: | --- |
{body}

Want to be told when one of these breaks, instead of reading a table?
The [free MIT GitHub Actions template]({CFG['template_url']}) polls your vendors
every 5 minutes and posts to your Slack, Discord or Teams.

[← repository home]({REPO}) · MIT licence · data also on
[Hugging Face]({HF}).
"""


def inject_readme(n_pages):
    p = os.path.join(HERE, "README.md")
    src = open(p, encoding="utf-8").read()
    picks = ["aws", "cloudflare", "github", "slack", "stripe", "openai", "zoom", "atlassian"]
    have = [s for s in picks if os.path.exists(os.path.join(OUTDIR, s + ".md"))]
    block = (f"{START}\n**Per-vendor outage history, readable right here on GitHub:** "
             f"[all {n_pages} vendors]({BLOB}/vendors/README.md)"
             + ("".join(f" · [{s}]({BLOB}/vendors/{s}.md)" for s in have))
             + f"\n{END}")
    if START in src and END in src:
        src = src.split(START, 1)[0] + block + src.split(END, 1)[1]
    else:
        anchor = "## Why this exists"
        if anchor not in src:
            return False
        src = src.replace(anchor, block + "\n\n" + anchor, 1)
    open(p, "w", encoding="utf-8").write(src)
    return True


def selftest():
    made, index, n = build(write=False)
    assert made > 0, "no vendor cleared the incident floor — check history/"
    # a median must never be published below the floor
    for r in index:
        if r["median"] != "—":
            assert r["measured"] >= MIN_FOR_RANK, f"{r['slug']}: median below floor"
    # the classifier must be the dataset's, and partition every incident
    d = load_vendor(index[0]["slug"])
    rows = rows_for(d)
    measured, counts = classify(rows)
    assert len(measured) + sum(counts.values()) == len(rows)
    pg = page(d, rows, measured, counts)
    assert "republishes what" in pg, "attribution sentence missing"
    assert "is not a claim about" in pg, "coverage caveat missing"
    print(f"gen_vendor_md selftest: OK ({made} pages would be written, "
          f"floor={MIN_INCIDENTS} incidents, median floor={MIN_FOR_RANK})")


def main():
    made, index, n = build(write=True)
    open(os.path.join(OUTDIR, "README.md"), "w", encoding="utf-8").write(
        index_page(index, n))
    ok = inject_readme(made)
    print(f"gen_vendor_md: wrote {made} vendor pages + index; README injected={ok}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
