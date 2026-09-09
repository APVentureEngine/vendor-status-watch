# Meridian outage history — every incident their status page has posted

**6 Meridian incidents on record** spanning **2025-09-08** to **2026-06-02**. Status page:
[http://status.meridiankiosks.com](http://status.meridiankiosks.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Only **6** Meridian incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Meridian posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Meridian incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-06-02 | [Reporting endpoint maintenance](https://stspg.io/hbtmntdvpbhk) | none | 81 min |
| 2026-03-20 | [Investigating Connectivity Issue](https://stspg.io/r467kv8qppv1) | none | 8 min |
| 2025-12-11 | [Data Processing Delays - Reporting Tools Affected](https://stspg.io/vy065cdv8qdh) | none | 0 min |
| 2025-10-20 | [SMS Outage](https://stspg.io/1ng06psmmp0d) | major | 8.9 h |
| 2025-10-09 | [Payment Processing - Potential Service Interruption](https://stspg.io/br3hvsxc9rgs) | major | 17.9 h |
| 2025-09-08 | [Chase Payment Processing incident (Resolved)](https://stspg.io/f29z5jmv17r8) | none | 0 min |

Newest 6 of 6. Full machine-readable history:
[`history/meridian.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/meridian.json).

## What is counted, and what is not

Of 6 recorded incidents, **6** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Meridian's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/meridian.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/meridian.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Meridian breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Meridian on the live site](https://approjects-vendor-status-watch.static.hf.space/v/meridian.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
