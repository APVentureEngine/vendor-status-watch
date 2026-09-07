# Spacelift outage history — every incident their status page has posted

**13 Spacelift incidents on record** spanning **2025-08-07** to **2026-07-29**. Status page:
[https://spacelift.statuspage.io](https://spacelift.statuspage.io) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Only **13** Spacelift incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Spacelift posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Spacelift incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-29 | [AWS connectivity for runs using hashicorp/aws v6.57.0](https://stspg.io/jx79l6fcqgmp) | none | 2.1 h |
| 2026-07-13 | [External symlink configuration issue](https://stspg.io/wbhfh8ml7ppl) | none | 3.0 days |
| 2026-06-01 | [Runs failing on workers](https://stspg.io/81yrrmdk5fr2) | major | 2.3 h |
| 2026-04-20 | [Terraform runs failing due to expired HashiCorp signing key](https://stspg.io/r338b6b7dqgx) | major | 21.6 h |
| 2026-04-17 | [Git clone operations failing with VCS agents](https://stspg.io/d7dymh200ygb) | major | 77 min |
| 2026-04-14 | [Issues resolving correct module configuration when creating a new module version](https://stspg.io/blcqknk06m2f) | major | 48 min |
| 2026-03-31 | [Spacelift Terraform Provider v1.47.0 incorrect signature](https://stspg.io/mgmf2bc7dd8c) | minor | 20 min |
| 2026-03-16 | [Environment disruptions (app.us.spacelift.io)](https://stspg.io/7wjgqw8bx6rg) | major | 3.6 h |
| 2026-03-02 | [Trivy plugin failing with 404 error](https://stspg.io/q8vcktjghbgp) | minor | 64 min |
| 2025-11-18 | [Elevated GitHub Error Rate](https://stspg.io/wm6p8pls3q5q) | major | 48 min |
| 2025-10-30 | [Event Processing Delays](https://stspg.io/hvdkdmbh235v) | minor | 55 min |
| 2025-10-17 | [Elevated API Errors](https://stspg.io/3q2btcm8ggwl) | major | 11 min |
| 2025-08-07 | [Spacelift unavailable](https://stspg.io/p9hnpths2vm4) | critical | 8 min |

Newest 13 of 13. Full machine-readable history:
[`history/spacelift.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/spacelift.json).

## What is counted, and what is not

Of 13 recorded incidents, **13** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Spacelift's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/spacelift.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/spacelift.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Spacelift breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Spacelift on the live site](https://approjects-vendor-status-watch.static.hf.space/v/spacelift.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
