# Replicate outage history — every incident their status page has posted

**25 Replicate incidents on record** spanning **2025-12-18** to **2026-08-26**. Status page:
[https://replicatestatus.com](https://replicatestatus.com) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Median incident length: **3.1 h** across 25 incidents where Replicate posted both a start and a resolve time.

This page republishes what Replicate posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Replicate incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-26 | A100 hardware partial outage | major | 3.1 h |
| 2026-08-10 | Delayed scaling due to node failure | minor | 40 min |
| 2026-08-05 | Significant degradation | none | 2.0 h |
| 2026-08-02 | API degraded for A100s | none | 8 min |
| 2026-07-31 | Degraded scale-out due to failed setups pulling from huggingface | minor | 2.2 h |
| 2026-07-22 | Hitting GPU Capacity for H100s creating large queue times for some models | minor | 26.5 h |
| 2026-07-16 | HuggingFace download issues | none | 7.5 h |
| 2026-07-13 | H100 GPU shortage resulting in high queue times | minor | 25.0 h |
| 2026-07-10 | High contention on H100 hardware | minor | 8.2 h |
| 2026-06-30 | Limited H100 capacity | minor | 5.6 h |
| 2026-06-03 | We're seeing long setup times and high contention for models on some L40S and H200 clusters. | major | 66 min |
| 2026-05-28 | Degraded performance on flux-2-klein-4b | minor | 107 min |
| 2026-05-21 | Prediction and Training status updates delayed | minor | 110 min |
| 2026-05-21 | Constrained H100 capacity | major | 6.9 h |
| 2026-05-12 | Constrained capacity for H100 hardware | minor | 4.3 h |

Newest 15 of 25. Full machine-readable history:
[`history/replicate.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/replicate.json).

## What is counted, and what is not

Of 25 recorded incidents, **25** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Replicate's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/replicate.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/replicate.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Replicate breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Replicate on the live site](https://approjects-vendor-status-watch.static.hf.space/v/replicate.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
