# Plaid outage history — every incident their status page has posted

**25 Plaid incidents on record** spanning **2026-05-21** to **2026-08-24**. Status page:
[https://status.plaid.com](https://status.plaid.com) · platform:
`statuspage` · last polled **2026-09-08 12:29 UTC**, last observed
state **`ok`**.

Median incident length: **3.1 h** across 24 incidents where Plaid posted both a start and a resolve time.

This page republishes what Plaid posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Plaid incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-24 | Elevated API errors | minor | 15.6 h |
| 2026-08-16 | Service Disruption Impacting Navy Federal Credit Union connections | minor | 3.6 h |
| 2026-08-12 | Service Disruption Impacting Navy Federal Credit Union connections | none | 8.3 h |
| 2026-08-05 | Delayed Capital One Transactions Updates | none | 5.7 days |
| 2026-08-02 | Service Disruption Impacting Bank of America connections | major | 22.0 h |
| 2026-08-01 | python SDK degraded on Identity Verification APIs | minor | 82 min |
| 2026-07-27 | Virtual Account perfomance degradation (UK and Europe) | none | 16.1 h |
| 2026-07-23 | Transfer Status Upates Delays | none | 82 min |
| 2026-07-23 | Payouts/Refunds API degraded | none | 2.9 h |
| 2026-07-22 | Transaction Updates Delayed | minor | 43.0 h |
| 2026-07-17 | Link performance degradation | none | 99 min |
| 2026-07-16 | Elevated dashboard.plaid.com error rates | major | 102 min |
| 2026-07-12 | Elevated API errors | none | 2.9 h |
| 2026-07-12 | Service Disruption Impacting Chase connections | major | 2 min |
| 2026-07-11 | Service Disruption Impacting Wells Fargo connections | major | 19 min |

Newest 15 of 25. Full machine-readable history:
[`history/plaid.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/plaid.json).

## What is counted, and what is not

Of 25 recorded incidents, **24** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 1 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Plaid's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/plaid.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/plaid.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Plaid breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Plaid on the live site](https://approjects-vendor-status-watch.static.hf.space/v/plaid.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
