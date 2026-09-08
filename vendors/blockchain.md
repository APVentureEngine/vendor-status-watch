# Blockchain outage history — every incident their status page has posted

**6 Blockchain incidents on record** spanning **2025-11-10** to **2026-08-08**. Status page:
[https://www.blockchain-status.com](https://www.blockchain-status.com) · platform:
`statuspage` · last polled **2026-09-08 12:29 UTC**, last observed
state **`ok`**.

Only **6** Blockchain incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Blockchain posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Blockchain incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-08 | Withdrawals temporarily unavailable | none | 24.6 h |
| 2026-05-20 | Arbitrum Block Processing delayed | minor | 14.1 h |
| 2026-01-14 | Naira (NGN) deposit issue | none | 20.6 h |
| 2026-01-12 | USD Wires temporarily disabled | none | 14.0 days |
| 2025-11-21 | Cardano deposits/withdrawals delayed | minor | 2.2 days |
| 2025-11-10 | Polkadot deposits/withdrawals delayed | critical | 27.1 h |

Newest 6 of 6. Full machine-readable history:
[`history/blockchain.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/blockchain.json).

## What is counted, and what is not

Of 6 recorded incidents, **6** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Blockchain's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/blockchain.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/blockchain.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Blockchain breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Blockchain on the live site](https://approjects-vendor-status-watch.static.hf.space/v/blockchain.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
