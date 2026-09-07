# Cohere outage history — every incident their status page has posted

**11 Cohere incidents on record** spanning **2025-08-07** to **2026-09-01**. Status page:
[https://status.cohere.ai](https://status.cohere.ai) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Only **11** Cohere incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Cohere posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Cohere incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | Multiple Endpoint Disruptions | minor | 4.4 h |
| 2026-08-05 | Documentation Content Loading Issues | major | 57 min |
| 2026-07-23 | Dashboard Login Service Disruption | major | 50 min |
| 2026-06-01 | /audio/transcriptions endpoint returns error for audio files with unexpected sampling rate | none | 2.9 h |
| 2026-04-20 | Docs Platform Degraded Performance | critical | 12 min |
| 2026-04-13 | Multiple Model Disruptions | minor | 84 min |
| 2026-04-11 | Scheduled DB Maintenance: Model authentication and API access momentarily affected | minor | 8 min |
| 2026-02-13 | Some chat models are unresponsive or timing out | major | 77 min |
| 2025-10-18 | Chat models return 503 service error when /v1/chat requests omit message and chat_history while providing tool_results | none | 36 min |
| 2025-10-01 | logprobs param degeraded for `command-a-03-2025` and `command-a-reasoning-08-2025` | minor | 3.8 h |
| 2025-08-07 | Command-a-vision-07-2025 degraded performance | minor | 10 min |

Newest 11 of 11. Full machine-readable history:
[`history/cohere.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/cohere.json).

## What is counted, and what is not

Of 11 recorded incidents, **11** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Cohere's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/cohere.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/cohere.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Cohere breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Cohere on the live site](https://approjects-vendor-status-watch.static.hf.space/v/cohere.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
