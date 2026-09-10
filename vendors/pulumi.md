# Pulumi outage history — every incident their status page has posted

**14 Pulumi incidents on record** spanning **2025-09-08** to **2026-08-17**. Status page:
[https://status.pulumi.com](https://status.pulumi.com) · platform:
`statuspage` · last polled **2026-09-10 12:15 UTC**, last observed
state **`ok`**.

Only **14** Pulumi incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Pulumi posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Pulumi incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-17 | [GitHub services failing](https://stspg.io/j4x31fkfln5m) | none | 3.0 h |
| 2026-07-23 | [Some Team Access Token operations failing](https://stspg.io/l7bcf3c3nlll) | minor | 88 min |
| 2026-07-08 | [Degraded performance for Pulumi Cloud login](https://stspg.io/77hyhyl7gg0b) | minor | 35 min |
| 2026-06-22 | [Degraded performance on Pulumi APIs](https://stspg.io/543hm3nmjzws) | minor | 106 min |
| 2026-06-11 | [Bitbucket authentication failures affecting sign-in and Bitbucket-backed accounts](https://stspg.io/rzb7vqbvn2s9) | minor | 117 min |
| 2026-05-12 | [Elevated API error rates and latency](https://stspg.io/8h5nw99l4q3y) | minor | 2.1 h |
| 2026-04-20 | [Elevated errors when decrypting ESC environments](https://stspg.io/wzttk9fjyfzh) | none | 0 min |
| 2026-04-15 | [Bitbucket Authentication Unavailable](https://stspg.io/jnxvqwprct96) | major | 4.5 h |
| 2026-04-10 | [Slowed API response times](https://stspg.io/s5btc5s8h75p) | minor | 11 min |
| 2026-03-06 | [Machine tokens unable to open referenced environments when running stack previews.](https://stspg.io/x1s1kcgtqqs1) | minor | 22 min |
| 2026-02-03 | [Errors when creating new Pulumi Neo tasks](https://stspg.io/gm02zqk22v7z) | major | 6 min |
| 2025-11-18 | [get.pulumi.com unreachable](https://stspg.io/lycqkv6m2n2r) | none | 2.0 h |
| 2025-10-20 | [AWS outage](https://stspg.io/6k0bcch81k1d) | major | 12.3 h |
| 2025-09-08 | [Issue displaying some previews in Pulumi Cloud](https://stspg.io/tft7jwkz60g0) | minor | 114 min |

Newest 14 of 14. Full machine-readable history:
[`history/pulumi.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/pulumi.json).

## What is counted, and what is not

Of 14 recorded incidents, **14** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Pulumi's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/pulumi.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/pulumi.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Pulumi breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Pulumi on the live site](https://approjects-vendor-status-watch.static.hf.space/v/pulumi.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
