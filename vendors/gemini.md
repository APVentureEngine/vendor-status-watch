# Gemini outage history — every incident their status page has posted

**50 Gemini incidents on record** spanning **2026-04-08** to **2026-09-04**. Status page:
[https://status.gemini.com](https://status.gemini.com) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`degraded`**.

Median incident length: **6.3 h** across 49 incidents where Gemini posted both a start and a resolve time.

This page republishes what Gemini posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Gemini incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-04 | [Delayed order completion email notifications](https://stspg.io/k9183r5b5k9d) | none | 3.7 h |
| 2026-08-26 | [BSC Network Delays](https://stspg.io/w4fzx71w1g4f) | minor | 99 min |
| 2026-08-19 | [Websockets (wss://ws.gemini.com) connectivity issues](https://stspg.io/r3h8gc52mq1d) | minor | 18 min |
| 2026-08-17 | [TON deposits, withdrawals and trading capabilities are temporarily unavailable](https://stspg.io/z4drhw8mhg5j) | minor | — |
| 2026-08-14 | [Outage for Deposits and Withdrawals for Cosmos](https://stspg.io/j38z68vggh55) | major | 32.5 h |
| 2026-08-12 | [Outage for Sui deposits and withdrawals](https://stspg.io/d6qr8tftj4mk) | minor | 10.6 h |
| 2026-08-05 | [Singapore Withdrawals Temporarily Unavailable](https://stspg.io/43z9tc5jh2sy) | minor | 30 min |
| 2026-08-04 | [Delays in account balances updating after transactions](https://stspg.io/x7g0rcx8rywl) | minor | 38 min |
| 2026-07-31 | [Ripple Ledger Transfers Currently Unavailable](https://stspg.io/xktpfrxbdjqk) | major | 5.1 h |
| 2026-07-29 | [Delayed Solana Deposits and Withdrawals](https://stspg.io/b4dtkf6c1nfy) | minor | 6.2 h |
| 2026-07-10 | [Sui Deposits and Withdrawals Delayed](https://stspg.io/fxw0kxsz12cf) | minor | 3.4 h |
| 2026-07-09 | [TON Deposits and Withdrawals Delayed](https://stspg.io/nt2jrs9yz7xm) | minor | 3.4 h |
| 2026-07-02 | [Delays for Filecoin Deposits and Withdrawals](https://stspg.io/cgn09qwnygc0) | major | 16.5 h |
| 2026-07-01 | [Delayed Solana Withdrawals](https://stspg.io/ltz4v6c00387) | minor | 2.4 h |
| 2026-06-29 | [Delays to Solana deposits and withdrawals](https://stspg.io/0ksbv12r96r5) | minor | 86 min |

Newest 15 of 50. Full machine-readable history:
[`history/gemini.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/gemini.json).

## What is counted, and what is not

Of 50 recorded incidents, **49** have a usable length. Excluded:
0 maintenance, 1 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Gemini's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/gemini.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/gemini.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Gemini breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Gemini on the live site](https://approjects-vendor-status-watch.static.hf.space/v/gemini.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
