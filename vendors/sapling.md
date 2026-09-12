# Sapling outage history — every incident their status page has posted

**13 Sapling incidents on record** spanning **2025-09-27** to **2026-09-11**. Status page:
[https://sapling.statuspage.io](https://sapling.statuspage.io) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Only **12** Sapling incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Sapling posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Sapling incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-11 | [Sporadic downtime in previous hour due to database migration](https://stspg.io/qnlwjkp5c79w) | none | 0 min |
| 2026-07-12 | [DNS server update downtime](https://stspg.io/7pvc1w7q9xt5) | maintenance | — |
| 2026-07-06 | [Website unexpected instance reboot](https://stspg.io/vjk444r00ygc) | major | 6 min |
| 2026-06-15 | [/edits model downtime](https://stspg.io/l92pcwmlxntr) | major | 3.6 h |
| 2026-01-25 | [linkerd expired anchors led to cluster downtime](https://stspg.io/6cfscv658ch8) | critical | 0 min |
| 2026-01-16 | [Chrome 144 breaking change for runtime.onMessage](https://stspg.io/gzqlvjbjxwnp) | major | 8.7 days |
| 2025-12-30 | [/edits and /spellcheck APIs team_id argument error](https://stspg.io/5jl8ymc0y9wm) | major | 0 min |
| 2025-11-26 | [AI detect downtime](https://stspg.io/qvy88zdj2chw) | major | 0 min |
| 2025-11-11 | [Downtime due to new AWS AMI upgrade](https://stspg.io/sfrrgdchw6c2) | critical | 0 min |
| 2025-11-07 | [AI detector pods overloaded](https://stspg.io/7r38v6t1s26y) | minor | 4.6 h |
| 2025-10-08 | [Spellcheck latency](https://stspg.io/4cm379ptv7h8) | minor | 14 min |
| 2025-10-07 | [Spellcheck API / service request failures](https://stspg.io/1y6qlzh439d1) | none | 0 min |
| 2025-09-27 | [High latency](https://stspg.io/630zfd0drp9t) | major | 0 min |

Newest 13 of 13. Full machine-readable history:
[`history/sapling.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/sapling.json).

## What is counted, and what is not

Of 13 recorded incidents, **12** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Sapling's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/sapling.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/sapling.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Sapling breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Sapling on the live site](https://approjects-vendor-status-watch.static.hf.space/v/sapling.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
