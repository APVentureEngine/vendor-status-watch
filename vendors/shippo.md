# Shippo outage history — every incident their status page has posted

**56 Shippo incidents on record** spanning **2026-06-26** to **2026-09-08**. Status page:
[https://status.goshippo.com](https://status.goshippo.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **2.2 h** across 55 incidents where Shippo posted both a start and a resolve time.

This page republishes what Shippo posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Shippo incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-08 | [Elevated error rates for the Lasership Transaction services](https://stspg.io/kn1nm71yvq3k) | major | 89 min |
| 2026-09-06 | [USPS Maintenance](https://stspg.io/d1ph3yd6w36c) | maintenance | — |
| 2026-09-05 | [APG Tracking disruption](https://stspg.io/r6pnprz2zjr7) | major | 2.5 h |
| 2026-09-05 | [Elevated error rate on Royal Mail SF Shipment API](https://stspg.io/yhcxtk278mr3) | major | 8.4 h |
| 2026-09-05 | [Elevated error rate on FedEx Shipment API](https://stspg.io/gmrc8jn43582) | major | 15.4 h |
| 2026-09-05 | [Elevated error rate on UPS Shipment API](https://stspg.io/0wy129btj0d7) | major | 8.6 h |
| 2026-09-02 | [Elevated errors on FedEx rating and label purchase](https://stspg.io/zfnml76fxlhz) | minor | 17.0 h |
| 2026-09-02 | [Elevated error rate on UPS Shipment Service](https://stspg.io/xhnkn128z151) | minor | 45 min |
| 2026-09-01 | [Elevated error rates for the FedEX Transaction services](https://stspg.io/hmxt68t9p9ql) | major | 32 min |
| 2026-09-01 | [Elevated error rate on Canada Post Shipment API](https://stspg.io/83c89p5xjs9p) | major | 2.0 h |
| 2026-09-01 | [Elevated error rate on Colissimo Transaction API](https://stspg.io/68x1ll2bptm1) | major | 58 min |
| 2026-09-01 | [Elevated error rate on Canada Post Shipment](https://stspg.io/ncd8gs15gxys) | major | 42 min |
| 2026-08-31 | [Elevated error rate on Deutsche Post Transaction API](https://stspg.io/1gh1yk2th55t) | major | 70 min |
| 2026-08-31 | [Elevated error rate on Colissimo Transaction](https://stspg.io/dtn4k84scm5w) | minor | 30 min |
| 2026-08-31 | [Observing Interruption in Receiving USPS Tracking Events](https://stspg.io/1bkgbs98ryp4) | minor | 5.2 h |

Newest 15 of 56. Full machine-readable history:
[`history/shippo.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/shippo.json).

## What is counted, and what is not

Of 56 recorded incidents, **55** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Shippo's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/shippo.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/shippo.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Shippo breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Shippo on the live site](https://approjects-vendor-status-watch.static.hf.space/v/shippo.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
