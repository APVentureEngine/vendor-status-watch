# Rollbar outage history — every incident their status page has posted

**13 Rollbar incidents on record** spanning **2025-09-03** to **2026-09-01**. Status page:
[http://status.rollbar.com](http://status.rollbar.com) · platform:
`statuspage` · last polled **2026-09-10 12:15 UTC**, last observed
state **`ok`**.

Only **11** Rollbar incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Rollbar posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Rollbar incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | Widespread incident impacting multiple parts of our platform caused by an incident within our cloud provider | minor | 73 min |
| 2026-06-25 | Increased occurrence processing pipeline latency | minor | 29 min |
| 2026-05-18 | Currently experiencing LOGIN issues | major | 12.1 h |
| 2026-05-09 | Item Processing impact for RUBY and PHY SDKs | none | — |
| 2026-04-20 | Increased occurrence processing pipeline latency | minor | 2.5 h |
| 2026-04-08 | Increased processing pipeline latency | minor | — |
| 2026-03-06 | Web app errors, primarily on Item Detail | major | 57 min |
| 2026-01-27 | Web application page loading issues | minor | 96 min |
| 2025-11-20 | Database Maintenance | minor | 9.7 h |
| 2025-11-18 | Web application page loading issues | minor | 3.5 h |
| 2025-10-20 | Increased occurrence processing pipeline latency | critical | 8.1 h |
| 2025-10-20 | Service Disruption Across Infrastructure | critical | 3.7 h |
| 2025-09-03 | Elevated API error rate | minor | 4.2 h |

Newest 13 of 13. Full machine-readable history:
[`history/rollbar.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/rollbar.json).

## What is counted, and what is not

Of 13 recorded incidents, **11** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 2 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Rollbar's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/rollbar.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/rollbar.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Rollbar breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Rollbar on the live site](https://approjects-vendor-status-watch.static.hf.space/v/rollbar.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
