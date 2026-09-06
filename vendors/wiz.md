# Wiz outage history — every incident their status page has posted

**50 Wiz incidents on record** spanning **2025-08-27** to **2026-09-03**. Status page:
[https://status.wiz.io](https://status.wiz.io) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Median incident length: **3.1 h** across 49 incidents where Wiz posted both a start and a resolve time.

This page republishes what Wiz posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Wiz incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-03 | [We are investigating an issue affecting some Wiz services for tenants hosted in the AWS us-west-2 region, related to an ongoing AWS service disruption](https://stspg.io/cjy9c5mbcp22) | none | 79 min |
| 2026-07-23 | [Portal and API Service Degradation Across Multiple US Data Centers](https://stspg.io/mdzw0vl74ch0) | none | 5.1 h |
| 2026-07-10 | [Elevated error rates due to an upstream dependency](https://stspg.io/vk313x3z9pth) | none | 73 min |
| 2026-06-22 | [We are currently investigating an issue affecting Tenable Cloud integrations, where asset fetching may not complete for some customers, and are working with the relevant teams to restore normal operation.](https://stspg.io/44dhlqysl353) | none | 4.9 h |
| 2026-06-20 | [We are currently seeing delays and possible data loss in sensor ATM ingestion, including RED ingestion and VIR.](https://stspg.io/d31x4x7wzkyg) | none | 6.0 h |
| 2026-06-17 | [Intermittent login failures](https://stspg.io/3h7wwqvrd1q5) | major | 28 min |
| 2026-06-08 | [Starting at 08:30 UTC, a subset of audit events may not have been recorded as expected.](https://stspg.io/t2jrbshpxhlx) | none | 77 min |
| 2026-05-20 | [Wiz Sensor and Wiz Defend on prod-us54 may be experiencing delayed data ingestion of approximately one hour. Our team is investigating and working to restore normal processing.](https://stspg.io/f8ckf7x0q7vs) | none | 14.2 h |
| 2026-05-11 | [Degraded performance of Security Graph in DC US48](https://stspg.io/yb81qdz1pmm8) | minor | 2.2 h |
| 2026-05-08 | [AWS infrastructure issues in us-east-1 are currently impacting our backend processing and portal search functionality. Users may see delays in data updates and search results while AWS works on a resolution](https://stspg.io/gcpcb2xhp76m) | none | 3.1 h |
| 2026-04-27 | [Intermittent login failures affecting prod-eu24 only](https://stspg.io/rb7c00l3kx83) | major | 68 min |
| 2026-04-17 | [The GitHub streaming integration has stopped sending events.](https://stspg.io/d8kbxfvnp9ql) | none | 19.3 h |
| 2026-04-14 | [Intermittent Performance Issues Affecting EU4](https://stspg.io/c84f731w7p21) | none | 26 min |
| 2026-04-03 | [Some customers may see critical issues created from incorrectly classified vulnerability findings for CVE-2026-4800, CVE-2026-33937, CVE-2026-33938, and CVE-2026-33940](https://stspg.io/s5s19c5z4yxz) | none | 27.5 h |
| 2026-03-24 | [We are investigating an issue causing false positive issues on controls wc-id-3088, wc-id-3089, wc-id-3090, wc-id-3091, and wc-id-3092 related to leaked cloud keys. These issues can be ignored and do not require investigation at this time.](https://stspg.io/trmzk7svv7zx) | none | 2.4 days |

Newest 15 of 50. Full machine-readable history:
[`history/wiz.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/wiz.json).

## What is counted, and what is not

Of 50 recorded incidents, **49** have a usable length. Excluded:
0 maintenance, 1 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Wiz's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/wiz.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/wiz.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Wiz breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Wiz on the live site](https://approjects-vendor-status-watch.static.hf.space/v/wiz.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
