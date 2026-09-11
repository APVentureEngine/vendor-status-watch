# Dbt Cloud outage history — every incident their status page has posted

**30 Dbt Cloud incidents on record** spanning **2026-06-19** to **2026-09-10**. Status page:
[https://status.getdbt.com](https://status.getdbt.com) · platform:
`statuspage` · last polled **2026-09-11 12:29 UTC**, last observed
state **`ok`**.

Median incident length: **2.0 h** across 27 incidents where Dbt Cloud posted both a start and a resolve time.

This page republishes what Dbt Cloud posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Dbt Cloud incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-10 | Intermittent errors on the Discovery API | minor | 2.3 h |
| 2026-09-10 | Increased error rates associated with dbt MCP and dbt Wizard | minor | 41 min |
| 2026-09-10 | State usage metrics not being ingested | major | 72 min |
| 2026-09-08 | User Login Sessions Terminated | major | 4.5 h |
| 2026-09-04 | dbt Platform not responding | critical | 91 min |
| 2026-09-03 | New user onboarding issue for trial sign-ups | none | 1 min |
| 2026-09-02 | Delayed metadata ingestion and Discovery API latency | minor | 2.9 h |
| 2026-08-26 | support@getdbt.com address not found | minor | 5.8 h |
| 2026-08-25 | Intermittent Databricks connection Errors | minor | 36 min |
| 2026-08-24 | Degraded Discovery API performance | minor | — |
| 2026-08-18 | Studio AI assistant (Wizard) tool errors | minor | 2.0 h |
| 2026-08-17 | Git Failures in dbt Platform | major | 6.3 h |
| 2026-08-13 | ai-codegen-api-increased-error-rate | minor | 3.2 h |
| 2026-08-10 | Potential intermittent admin APIs requests failing | minor | 2.0 h |
| 2026-08-09 | Fusion Stable: BigQuery incremental model builds affected | minor | 77 min |

Newest 15 of 30. Full machine-readable history:
[`history/dbt-cloud.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/dbt-cloud.json).

## What is counted, and what is not

Of 30 recorded incidents, **27** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 3 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Dbt Cloud's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/dbt-cloud.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/dbt-cloud.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Dbt Cloud breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Dbt Cloud on the live site](https://approjects-vendor-status-watch.static.hf.space/v/dbt-cloud.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
