# Pinecone outage history — every incident their status page has posted

**48 Pinecone incidents on record** spanning **2025-08-05** to **2026-09-01**. Status page:
[https://status.pinecone.io](https://status.pinecone.io) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **76 min** across 48 incidents where Pinecone posted both a start and a resolve time.

This page republishes what Pinecone posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Pinecone incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | [5xx errors on some control plane operations](https://stspg.io/lhxtyzp0mn82) | major | 4.6 h |
| 2026-08-25 | [[SERVERLESS][GCP][us-central1] 5xx errors on some read and write requests](https://stspg.io/vpzz5nfgp7zm) | major | 21 min |
| 2026-07-21 | [[SERVERLESS][Azure][eastus2] 5xx errors for some namespaces](https://stspg.io/84vynt818w3j) | critical | 29 min |
| 2026-07-20 | [[SERVERLESS][AWS][us-east-1] Increased latency and 5xx errors for some indexes](https://stspg.io/1l6gyphhdwc3) | minor | 75 min |
| 2026-07-12 | [[Serverless][AWS][us-east-1] Increase in freshness lag for some namespaces](https://stspg.io/zbbns3nppvf5) | minor | 4.9 h |
| 2026-07-09 | [[Serverless][Azure][eastus2] 5xx errors on some requests for some indexes](https://stspg.io/5yn0r7x4nj4j) | major | 4.8 h |
| 2026-06-18 | [Some initial queries to infrequently read namespaces incorrectly returning empty results](https://stspg.io/dbnb6cnq0cgn) | minor | 8.4 h |
| 2026-06-16 | [[Serverless][AWS][us-east-1] Metrics tab in the console not showing graphs](https://stspg.io/pzkpk0q3m54f) | none | 4.0 h |
| 2026-06-06 | [[Serverless][AWS][us-west-2] 5xx errors for some requests on some indexes](https://stspg.io/1b7wv45c2zxf) | major | 3.6 h |
| 2026-06-06 | [[Serverless][AWS][us-west-2] Read path operations for some indexes may experience elevated latency and timeouts](https://stspg.io/58n64vnr08r9) | minor | 2.7 h |
| 2026-06-06 | [[AWS][us-east-1] 5xx errors for some requests on some indexes](https://stspg.io/6l695wtjfy0j) | minor | 26 min |
| 2026-05-25 | [[Serverless][AWS][us-west-2] 5xx errors and longer response times on upsert requests for some indexes.](https://stspg.io/z4t7c1tq3w40) | major | 78 min |
| 2026-05-13 | [[AWS][us-east-1] 5xx errors on read and write operations for some indexes](https://stspg.io/0707b83qf179) | major | 61 min |
| 2026-05-06 | [[AWS][us-east-1] 5xx errors for some requests on some indexes](https://stspg.io/t70kz736vzf0) | major | 27 min |
| 2026-05-06 | [Pinecone Console loading slowly for some users](https://stspg.io/9nyjqj9k830d) | minor | 19 min |

Newest 15 of 48. Full machine-readable history:
[`history/pinecone.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/pinecone.json).

## What is counted, and what is not

Of 48 recorded incidents, **48** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Pinecone's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/pinecone.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/pinecone.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Pinecone breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Pinecone on the live site](https://approjects-vendor-status-watch.static.hf.space/v/pinecone.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
