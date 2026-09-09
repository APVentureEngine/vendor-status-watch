# LaunchDarkly outage history — every incident their status page has posted

**50 LaunchDarkly incidents on record** spanning **2026-02-06** to **2026-08-26**. Status page:
[https://status.launchdarkly.com](https://status.launchdarkly.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **66 min** across 50 incidents where LaunchDarkly posted both a start and a resolve time.

This page republishes what LaunchDarkly posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent LaunchDarkly incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-26 | [Flag delivery errors in Streaming API](https://stspg.io/n8kkgrxbjkdh) | minor | 14 min |
| 2026-08-24 | [Email delivery failure affecting sign-up verification and notification emails](https://stspg.io/cgfs9bf4w12c) | minor | 75 min |
| 2026-08-17 | [Flag Updates via Polling API delayed](https://stspg.io/h8byqm8qtb9p) | minor | 5.4 h |
| 2026-08-14 | [Flag Updates delayed in US Region](https://stspg.io/xg4w7vvnrk63) | minor | 2.0 h |
| 2026-08-07 | [Elevated errors on server-side SDK streaming connections](https://stspg.io/2f7v4bt6s4k3) | minor | 46 min |
| 2026-07-31 | [Investigating - Known Impact](https://stspg.io/rg10v64yrrny) | minor | 5.2 h |
| 2026-07-28 | [Delay in Session Replay and Error ingest](https://stspg.io/4h85388bhst6) | minor | 40 min |
| 2026-07-26 | [Elevated API Latency and Errors (11:32–11:48 PT)](https://stspg.io/sm5vp8lh0nk5) | minor | 0 min |
| 2026-07-10 | [Web application unavailable and flag delivery evaluations have elevated failure rate](https://stspg.io/3zs2g4y0zjhs) | critical | 69 min |
| 2026-07-10 | [Launchdarkly UI is down and flag evaluation errors are occuring](https://stspg.io/5cz51f7pr4jt) | none | 91 min |
| 2026-07-10 | [LaunchDarkly is operational but customer action may be required](https://stspg.io/rgzx37hr3zl0) | minor | 19.1 days |
| 2026-07-08 | [Frequentist experiments cannot be saved or started](https://stspg.io/3xw9y1f2h5qn) | minor | 98 min |
| 2026-07-07 | [Delays in Experimentation and Guarded Rollout results](https://stspg.io/nb74mgrw1279) | none | 0 min |
| 2026-07-06 | [High volume of error alerts related to flag delivery network.](https://stspg.io/2w8p702dlbxs) | major | 51 min |
| 2026-07-06 | [Verification emails not being sent](https://stspg.io/68ggsmfb0zjn) | minor | 79 min |

Newest 15 of 50. Full machine-readable history:
[`history/launchdarkly.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/launchdarkly.json).

## What is counted, and what is not

Of 50 recorded incidents, **50** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about LaunchDarkly's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/launchdarkly.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/launchdarkly.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when LaunchDarkly breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [LaunchDarkly on the live site](https://approjects-vendor-status-watch.static.hf.space/v/launchdarkly.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
