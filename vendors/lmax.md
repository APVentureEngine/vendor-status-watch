# LMAX outage history — every incident their status page has posted

**17 LMAX incidents on record** spanning **2025-08-18** to **2026-09-10**. Status page:
[https://status.lmax.com](https://status.lmax.com) · platform:
`statuspage` · last polled **2026-09-10 12:15 UTC**, last observed
state **`maintenance`**.

Only **15** LMAX incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what LMAX posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent LMAX incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-10 | [Digital UAT Maintenance](https://stspg.io/hmhj4zfxtn4y) | maintenance | — |
| 2026-09-05 | [Exchange Maintenance](https://stspg.io/qjhxrvkf610l) | maintenance | — |
| 2026-05-22 | [LMAX Perpetual Futures - Pricing Incident](https://stspg.io/7ybq6gqyxptw) | major | 2.5 h |
| 2026-05-18 | [LMAX SWAPS X-Bridge Related incident](https://stspg.io/s861lz2z6fwm) | none | 2.1 h |
| 2026-05-14 | [Prematurely closed UAT Maintenance](https://stspg.io/yc5qxn1zgs3s) | major | 117 min |
| 2026-04-30 | [P1 - INC0024145 - PERPS issue in Prod and Demo](https://stspg.io/7rs0h4tn5jqk) | none | 3.4 h |
| 2026-04-29 | [LMAX Global: Crypto Deposits in Broker](https://stspg.io/7l5ds3zb9c98) | minor | 101 min |
| 2026-03-05 | [UAT Maintenance](https://stspg.io/td171w0hv3dq) | none | 113 min |
| 2026-02-20 | [Internet Connectivity problem](https://stspg.io/081bg7rq8jd4) | none | 56 min |
| 2026-02-02 | [Delays in external emails sent from lmax.com and lmaxdigital.com](https://stspg.io/1jr2pt5ll1bh) | minor | 19.1 h |
| 2026-01-14 | [Perpetual Futures FIX Trading](https://stspg.io/g34d99796dcp) | none | 46 min |
| 2025-12-12 | [PD #1525: Digital broker's custodian 2 integration has stopped detecting deposits after kit44 patch release.](https://stspg.io/cyl70n3dkpdn) | none | 35 min |
| 2025-12-08 | [Java API rejections in London Professional](https://stspg.io/hlw7fnnqmxsv) | minor | 100 min |
| 2025-11-18 | [DFX Trading Portal is unavailable](https://stspg.io/65qh0pc04tsp) | none | 42 min |
| 2025-11-18 | [LMAX Global Trading platform down](https://stspg.io/cf75pgc4y8w4) | minor | 56 min |

Newest 15 of 17. Full machine-readable history:
[`history/lmax.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/lmax.json).

## What is counted, and what is not

Of 17 recorded incidents, **15** have a usable length. Excluded:
2 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about LMAX's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/lmax.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/lmax.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when LMAX breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [LMAX on the live site](https://approjects-vendor-status-watch.static.hf.space/v/lmax.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
