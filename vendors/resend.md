# Resend outage history — every incident their status page has posted

**26 Resend incidents on record** spanning **2026-06-15** to **2026-09-04**. Status page:
[https://resend-status.com](https://resend-status.com) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Only **17** Resend incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Resend posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Resend incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-04 | Delays in background processes are affecting webhooks, domain verifications, and other important features | minor | 32 min |
| 2026-09-03 | Delay in contact webhooks delivery | minor | 39 min |
| 2026-08-20 | Increased latency across API endpoints | minor | 24 min |
| 2026-08-18 | Contact webhook events are delayed in delivery | minor | 14.1 h |
| 2026-08-16 | API instability | minor | — |
| 2026-08-13 | Errors during the domain creation process | major | — |
| 2026-08-09 | Delayed contact webhook events | none | 38 min |
| 2026-08-08 | Increased API and SMTP Error Rates | major | 42 min |
| 2026-08-07 | Delayed contact related webhook events | minor | 24 min |
| 2026-08-04 | Contact webhook delivery backlog | minor | — |
| 2026-08-04 | Test domain resend.dev failing test emails | minor | — |
| 2026-07-30 | Increased failure rate in Domain verifications | minor | — |
| 2026-07-29 | Elevated error rates on email sending, API, and dashboard | major | 7 min |
| 2026-07-29 | Increased returned error rates | major | 83 min |
| 2026-07-22 | Errors creating domains and API keys | minor | — |

Newest 15 of 26. Full machine-readable history:
[`history/resend.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/resend.json).

## What is counted, and what is not

Of 26 recorded incidents, **17** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 9 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Resend's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/resend.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/resend.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Resend breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Resend on the live site](https://approjects-vendor-status-watch.static.hf.space/v/resend.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
