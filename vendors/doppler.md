# Doppler outage history — every incident their status page has posted

**4 Doppler incidents on record** spanning **2025-08-20** to **2026-07-16**. Status page:
[https://www.dopplerstatus.com](https://www.dopplerstatus.com) · platform:
`statuspage` · last polled **2026-09-11 12:29 UTC**, last observed
state **`degraded`**.

Only **4** Doppler incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Doppler posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Doppler incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-16 | [CLI Downloads failing](https://stspg.io/50mq9yk1xmj5) | none | 5 min |
| 2025-11-20 | [Background job delays impacting sync, webhook and email delivery](https://stspg.io/m9f4qljcp5mf) | major | 3.8 h |
| 2025-11-18 | [System Outage](https://stspg.io/ym9ydy0mgtw3) | critical | 3.2 h |
| 2025-08-20 | [Background job delays impacting sync and email delivery](https://stspg.io/zjcknwfkkngy) | critical | 66 min |

Newest 4 of 4. Full machine-readable history:
[`history/doppler.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/doppler.json).

## What is counted, and what is not

Of 4 recorded incidents, **4** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Doppler's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/doppler.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/doppler.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Doppler breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Doppler on the live site](https://approjects-vendor-status-watch.static.hf.space/v/doppler.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
