# Octopus outage history — every incident their status page has posted

**19 Octopus incidents on record** spanning **2025-09-04** to **2026-07-31**. Status page:
[https://status.octopus.com](https://status.octopus.com) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Only **19** Octopus incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Octopus posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Octopus incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-31 | [https://g.octopushq.com Certificate issues](https://stspg.io/jch14qntcrn4) | major | 91 min |
| 2026-07-23 | [Service connectivity issues due to upstream Azure outage](https://stspg.io/6mjw4268d4d6) | minor | 4.3 h |
| 2026-07-03 | [Bicep deployments may fail after upgrading to 2026.3.4658 or later](https://stspg.io/pyyh2y43ljbm) | major | 32.5 days |
| 2026-05-29 | [Ability to deploy in West US 2 might be affected](https://stspg.io/2njlj5pnsppk) | minor | 18.5 h |
| 2026-05-15 | [Amazon ECS Service Steps fail with 'Container.image contains invalid cha...](https://stspg.io/xp9qxttg4ym1) | major | 2.9 days |
| 2026-05-05 | [Dynamic Worker issues in West US 2](https://stspg.io/1f20tgkzq23j) | major | 41.4 h |
| 2026-04-01 | [AWS Deployment Failures for Cloud Customers](https://stspg.io/slpby92g6q6f) | major | 6.8 days |
| 2026-03-30 | [Deployments using AWS-dependent resources may fail with “No RegionEndpoint or ServiceURL configured.”](https://stspg.io/hjv0y0z6scrx) | major | 0 min |
| 2026-03-24 | [gRPC port (8443) shows Octopus Cloud instance is Undergoing Maintenance](https://stspg.io/jpwpyx1n49ww) | major | 25.9 h |
| 2026-02-26 | [Emails are currently not being delivered](https://stspg.io/h6972d163hcg) | major | 3.9 h |
| 2026-02-02 | [Ubuntu Dynamic Workers are failing to lease](https://stspg.io/czrr4lws5zww) | critical | 24.1 h |
| 2025-11-25 | [OctopusID signin intermittent for cloud customers](https://stspg.io/m72cwhzx3pmx) | major | 2.4 h |
| 2025-11-18 | [GitHub upstream outage causing issues with VCS-backed elements](https://stspg.io/7l33709ml2wq) | major | 3.6 h |
| 2025-10-29 | [Octopus.com and billing portal may be unavailable in certain regions](https://stspg.io/13fnd1fgrzky) | critical | 8.7 h |
| 2025-10-20 | [Docker Hub is down](https://stspg.io/r8500hm0c5sf) | major | 17.6 h |

Newest 15 of 19. Full machine-readable history:
[`history/octopus.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/octopus.json).

## What is counted, and what is not

Of 19 recorded incidents, **19** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Octopus's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/octopus.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/octopus.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Octopus breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Octopus on the live site](https://approjects-vendor-status-watch.static.hf.space/v/octopus.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
