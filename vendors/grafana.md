# Grafana outage history — every incident their status page has posted

**53 Grafana incidents on record** spanning **2026-07-08** to **2026-09-04**. Status page:
[https://grafanalabs.statuspage.io](https://grafanalabs.statuspage.io) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Median incident length: **113 min** across 53 incidents where Grafana posted both a start and a resolve time.

This page republishes what Grafana posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Grafana incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-04 | [Degradation of Hosted Grafana in US Central Region](https://stspg.io/7n6x5qw9x9d5) | major | 3.6 h |
| 2026-09-04 | [US Central Region Instability](https://stspg.io/b3b4ppnkx23p) | minor | 6.2 h |
| 2026-09-04 | [Alert rule creation, deletion, and update degradation in prod-us-east-2](https://stspg.io/8gw4nt4mmp09) | minor | 2.9 h |
| 2026-09-03 | [Tempo and Mimir Read and Write Failures](https://stspg.io/kw7xrpjrg134) | minor | 2.7 h |
| 2026-09-03 | [High Latency in prod-ap-south-1](https://stspg.io/f6h7k3lq3v62) | major | 3.3 h |
| 2026-09-02 | [Elevated Latency in Grafana Cloud Logs (prod-ap-south-1)](https://stspg.io/39bjpwxypjqn) | none | 0 min |
| 2026-09-01 | [Investigating issues in US Central (prod-us-central-0, prod-us-central-5)](https://stspg.io/jvcf7d0j5x37) | minor | 4.9 h |
| 2026-08-28 | [Partial Logs Write Outage](https://stspg.io/zc28d5qtcwdf) | major | 89 min |
| 2026-08-28 | [Some Grafana UI features may be unavailable or reverting to legacy behaviour](https://stspg.io/lj9v7hbqc7gp) | minor | 102 min |
| 2026-08-27 | [Elevated error rates affecting metrics writes in prod-us-central-0](https://stspg.io/75v8n623y4jn) | minor | 56 min |
| 2026-08-27 | [Mimir Writes Incident in prod-us-central-0](https://stspg.io/cz0zxwg004tf) | none | 0 min |
| 2026-08-25 | [Incident Management unavailable in US Central](https://stspg.io/kdhyw5xk6r56) | minor | 23 min |
| 2026-08-18 | [Cloud Logs read path outage on eu-west-2](https://stspg.io/1g4dpsdmf2cf) | critical | 0 min |
| 2026-08-13 | [K6 Test Outage](https://stspg.io/tv8plq4gysv5) | critical | 82 min |
| 2026-08-10 | [Metrics: Elevated Error Rates Reads/Writes](https://stspg.io/0svqkyqmlzxl) | minor | 0 min |

Newest 15 of 53. Full machine-readable history:
[`history/grafana.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/grafana.json).

## What is counted, and what is not

Of 53 recorded incidents, **53** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Grafana's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/grafana.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/grafana.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Grafana breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Grafana on the live site](https://approjects-vendor-status-watch.static.hf.space/v/grafana.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
