# Kraken outage history — every incident their status page has posted

**60 Kraken incidents on record** spanning **2026-05-24** to **2026-09-09**. Status page:
[https://status.kraken.com](https://status.kraken.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`degraded`**.

Median incident length: **5.8 h** across 51 incidents where Kraken posted both a start and a resolve time.

This page republishes what Kraken posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Kraken incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-09 | [Moonbeam (GLMR) and Moonriver (MOVR) Funding Delays](https://stspg.io/6glmcvd69pjj) | minor | — |
| 2026-09-08 | [Funding Limits and Deposit Delays](https://stspg.io/f9q8cd781w77) | none | 33 min |
| 2026-09-08 | [Funding Delays - Withdrawals Stuck](https://stspg.io/5d4rdc445vfj) | none | 16 min |
| 2026-09-08 | [Delayed Historical Balance Data](https://stspg.io/2yqmgclztspf) | minor | 9.8 h |
| 2026-09-07 | [PEAQ (PEAQ) Funding Delays](https://stspg.io/bdblfq0bq4zl) | minor | 2.4 h |
| 2026-09-05 | [Kaspa (KAS) Withdrawals Delays](https://stspg.io/kwlscwg348mv) | minor | 72 min |
| 2026-09-05 | [EUR and GBP Funding Maintenance](https://stspg.io/s11xgblc9lp1) | maintenance | — |
| 2026-09-04 | [Funding delays for select blockchain networks](https://stspg.io/qkr4w76jtq70) | minor | — |
| 2026-09-04 | [FIX API Maintenance](https://stspg.io/4k2qrf80wh7t) | maintenance | — |
| 2026-09-04 | [Delayed EUR Withdrawals via Banking Circle](https://stspg.io/w9z996h83zmr) | minor | 5.8 h |
| 2026-09-02 | [Monad (MON) Funding Delays](https://stspg.io/bkhvg2g83nwh) | minor | — |
| 2026-09-02 | [Document upload issues](https://stspg.io/2ks1bd9p4khs) | minor | 49 min |
| 2026-09-01 | [Monad (MON) Funding Delays](https://stspg.io/fvql4fyxt0bm) | minor | 8.7 h |
| 2026-08-31 | [Injective (INJ) Funding Delays](https://stspg.io/1tsw7fwzff23) | minor | 18.9 h |
| 2026-08-30 | [Cronos (CRO) Funding Disruptions](https://stspg.io/cxw7t4n1zqz6) | minor | 8.8 days |

Newest 15 of 60. Full machine-readable history:
[`history/kraken.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/kraken.json).

## What is counted, and what is not

Of 60 recorded incidents, **51** have a usable length. Excluded:
3 maintenance, 6 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Kraken's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/kraken.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/kraken.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Kraken breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Kraken on the live site](https://approjects-vendor-status-watch.static.hf.space/v/kraken.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
