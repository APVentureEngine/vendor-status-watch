# Cloudera outage history — every incident their status page has posted

**6 Cloudera incidents on record** spanning **2025-08-13** to **2026-09-03**. Status page:
[https://status.cloudera.com](https://status.cloudera.com) · platform:
`statuspage` · last polled **2026-09-11 12:29 UTC**, last observed
state **`ok`**.

Only **6** Cloudera incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Cloudera posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Cloudera incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-03 | [Cloudera Management Console not accessible in US Control Plane](https://stspg.io/jzl2h2lmr01s) | minor | 3.5 h |
| 2026-05-11 | [Intermittent Performance Issues - US Control Plane](https://stspg.io/6t0hy3kcj8g0) | none | 0 min |
| 2026-03-10 | [Intermittent Management Console Access Issues Across US, EU, and AP Regions](https://stspg.io/2f2l4x28khkx) | minor | 0 min |
| 2025-09-25 | [FreeIPA connectivity issues](https://stspg.io/5ts1ff98nf42) | minor | 6.6 h |
| 2025-09-24 | [Intermittent Performance and Access Issues with the Cloudera Management Console](https://stspg.io/sk4jg5x4pjxb) | minor | 21.3 h |
| 2025-08-13 | [DataHubs, DataLakes and FreeIPA are unreachable in US region](https://stspg.io/kjv7xw15yn3n) | minor | 44 min |

Newest 6 of 6. Full machine-readable history:
[`history/cloudera.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/cloudera.json).

## What is counted, and what is not

Of 6 recorded incidents, **6** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Cloudera's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/cloudera.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/cloudera.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Cloudera breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Cloudera on the live site](https://approjects-vendor-status-watch.static.hf.space/v/cloudera.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
