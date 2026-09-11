# hCaptcha outage history — every incident their status page has posted

**8 hCaptcha incidents on record** spanning **2025-08-21** to **2026-08-27**. Status page:
[https://www.hcaptchastatus.com](https://www.hcaptchastatus.com) · platform:
`statuspage` · last polled **2026-09-11 12:29 UTC**, last observed
state **`ok`**.

Only **6** hCaptcha incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what hCaptcha posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent hCaptcha incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-27 | [Enterprise: Analytics queries under maintenance](https://stspg.io/wzl08dk0b91y) | maintenance | — |
| 2026-07-29 | [Increased 429 rates on several ASNs](https://stspg.io/7hz1jyr4mg69) | none | 0 min |
| 2026-05-05 | [Increased error rate on API loads](https://stspg.io/2hk8wfn6mcmk) | none | 0 min |
| 2025-12-19 | [Increased latency on API calls in some regions](https://stspg.io/r30rx588kh2j) | minor | 0 min |
| 2025-10-21 | [hCaptcha is completely unaffected by the AWS outages](https://stspg.io/90bymck493bm) | none | 0 min |
| 2025-10-08 | [Maintenance to Passkey support](https://stspg.io/710w6lpb1p0l) | none | — |
| 2025-09-08 | [Elevated P99 times in South America (Brazil) regions](https://stspg.io/8slwldy29gh6) | minor | 0 min |
| 2025-08-21 | [Elevated latency in IAD region for connections from AWS us-east-1](https://stspg.io/vtl4hy1sk2y8) | minor | 7 min |

Newest 8 of 8. Full machine-readable history:
[`history/hcaptcha.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/hcaptcha.json).

## What is counted, and what is not

Of 8 recorded incidents, **6** have a usable length. Excluded:
2 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about hCaptcha's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/hcaptcha.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/hcaptcha.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when hCaptcha breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [hCaptcha on the live site](https://approjects-vendor-status-watch.static.hf.space/v/hcaptcha.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
