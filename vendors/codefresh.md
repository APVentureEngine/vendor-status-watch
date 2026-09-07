# Codefresh outage history — every incident their status page has posted

**16 Codefresh incidents on record** spanning **2025-10-13** to **2026-08-24**. Status page:
[http://status.codefresh.io](http://status.codefresh.io) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Only **16** Codefresh incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Codefresh posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Codefresh incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-24 | [Some customers report classic builds remain in the pending state](https://stspg.io/vb77m7x7bt6j) | major | 2.8 h |
| 2026-07-06 | [g.codefresh.io is intermittently unreachable for some users](https://stspg.io/gpntsjgwkvml) | minor | 3.2 h |
| 2026-07-06 | [Codefresh Classic SaaS builds may be delayed](https://stspg.io/k4yvc7kx0tqy) | minor | 4.0 h |
| 2026-06-05 | [BitBucket SSO and OAuth integrations: degraded performance](https://stspg.io/w51md5fk2rv1) | minor | 33 min |
| 2026-05-12 | [Maven repository rate limit (429 Errors) on SaaS builds.](https://stspg.io/fn3tkmznjxj5) | none | 2.8 h |
| 2026-04-21 | [OAuth Bitbucket integrations and triggers are facing rate limit issues](https://stspg.io/g27hxgvmx88y) | minor | 16.1 days |
| 2026-04-03 | [Some accounts may encounter delays and slow response times when viewing GitOps Dashboards data.](https://stspg.io/w2m1mcxxfrf6) | minor | 2.7 h |
| 2026-03-30 | [Codefresh CI Pipeline Runs Failing Due to Image Pull Failure](https://stspg.io/qdq037cdsnty) | major | 10.1 h |
| 2026-02-16 | [Performance issues with the Codefresh platform](https://stspg.io/bqmh1r68byxp) | minor | 75 min |
| 2025-12-29 | [Some accounts may experience issues with viewing the audit data](https://stspg.io/l5w0htjyxqf7) | minor | 3.7 h |
| 2025-11-18 | [GitHub upstream outage impacting Classic Pipelines (and other GH dependent services)](https://stspg.io/kdqzjvnqnvb3) | major | 40 min |
| 2025-11-18 | [codefresh.io is intermittently unreachable for some users](https://stspg.io/rd5y8ywq34k4) | minor | 12.6 h |
| 2025-11-05 | [Free-tier Codefresh Classic users unable to run classic pipeline builds on SaaS.](https://stspg.io/qthlll26v5sw) | minor | 59 min |
| 2025-10-26 | [GitOps UI Slowness](https://stspg.io/9wpz3nbq3p5v) | minor | 36 min |
| 2025-10-20 | [An ongoing AWS US East outage is causing platform degradation](https://stspg.io/yy0m7x4n5nyj) | minor | 9.6 h |

Newest 15 of 16. Full machine-readable history:
[`history/codefresh.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/codefresh.json).

## What is counted, and what is not

Of 16 recorded incidents, **16** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Codefresh's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/codefresh.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/codefresh.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Codefresh breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Codefresh on the live site](https://approjects-vendor-status-watch.static.hf.space/v/codefresh.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
