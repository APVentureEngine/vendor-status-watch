# Stacker outage history — every incident their status page has posted

**5 Stacker incidents on record** spanning **2026-02-03** to **2026-07-10**. Status page:
[https://status.stacker.app](https://status.stacker.app) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Only **4** Stacker incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Stacker posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Stacker incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-10 | [Astra outage from failed deployment](https://stspg.io/5wvj3qpr5py5) | critical | 9 min |
| 2026-06-26 | [Unscheduled database manitenance](https://stspg.io/c11v0rjwcx74) | major | 34 min |
| 2026-03-20 | [Unscheduled database restart](https://stspg.io/c4nvpjyjs9hv) | maintenance | — |
| 2026-02-20 | [Unable to access Stacker apps](https://stspg.io/3p0rff75lp0k) | critical | 3.3 h |
| 2026-02-03 | [Stacker Access Down](https://stspg.io/tqt5txgff5x1) | critical | 5 min |

Newest 5 of 5. Full machine-readable history:
[`history/stacker.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/stacker.json).

## What is counted, and what is not

Of 5 recorded incidents, **4** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Stacker's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/stacker.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/stacker.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Stacker breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Stacker on the live site](https://approjects-vendor-status-watch.static.hf.space/v/stacker.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
