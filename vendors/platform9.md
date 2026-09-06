# Platform9 outage history — every incident their status page has posted

**3 Platform9 incidents on record** spanning **2025-09-28** to **2026-07-24**. Status page:
[https://status.platform9.com](https://status.platform9.com) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Only **3** Platform9 incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Platform9 posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Platform9 incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-24 | [PCD, PMK, PMO Control Plane is experience degradation](https://stspg.io/nrc0jdlvyrv1) | none | 15 min |
| 2026-04-22 | [PMK Control Plane is experience degradation](https://stspg.io/hdvbbw2d2p0s) | major | 6.3 h |
| 2025-09-28 | [PCD Kuberenetes Outage](https://stspg.io/t20h1l43961n) | critical | 35.2 h |

Newest 3 of 3. Full machine-readable history:
[`history/platform9.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/platform9.json).

## What is counted, and what is not

Of 3 recorded incidents, **3** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Platform9's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/platform9.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/platform9.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Platform9 breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Platform9 on the live site](https://approjects-vendor-status-watch.static.hf.space/v/platform9.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
