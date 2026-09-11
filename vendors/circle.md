# Circle outage history — every incident their status page has posted

**52 Circle incidents on record** spanning **2026-06-08** to **2026-09-11**. Status page:
[https://status.circle.com](https://status.circle.com) · platform:
`statuspage` · last polled **2026-09-11 12:29 UTC**, last observed
state **`degraded`**.

Median incident length: **2.2 h** across 50 incidents where Circle posted both a start and a resolve time.

This page republishes what Circle posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Circle incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-11 | [Delayed mint/burn on STMT due to chain outage](https://stspg.io/px83rbxsn70m) | major | — |
| 2026-09-10 | [Circle is discontinuing support for USDC and CCTP V1 on Noble in a phased transition](https://stspg.io/xrjgxv9slr2c) | none | — |
| 2026-09-02 | [Circle Mint deposits and outbound CCTP attestations on Linea delayed](https://stspg.io/5crvmzq95fcj) | major | 3.0 days |
| 2026-09-02 | [CCTP Attestations on HyperEVM Delayed](https://stspg.io/v2p63ttp6lz4) | major | 3 min |
| 2026-08-31 | [USDC and CCTP on Injective — Delayed mints, burns, and transfers](https://stspg.io/c9dr5wm4ytm4) | major | 26.9 h |
| 2026-08-30 | [Cronos Mainnet outage](https://stspg.io/nktyvbh7pwr9) | critical | 3.3 days |
| 2026-08-30 | [USDC on Linea — Delayed mints](https://stspg.io/zn0z842xhbms) | major | 28.9 h |
| 2026-08-28 | [USDC on Stellar Testnet — Delayed mints, burns, and faucet requests](https://stspg.io/620kmj3nkth9) | major | 4.1 days |
| 2026-08-24 | [Circle xReserve on Stacks Mainnet — Delays and degraded performance](https://stspg.io/32sbk0zmwqvn) | major | 24 min |
| 2026-08-24 | [CCTP Attestations on Ink Delayed](https://stspg.io/2p3xt1tfwqq0) | major | 81 min |
| 2026-08-22 | [USDC and CCTP on HyperEVM — Delayed mints, burns, and transfers](https://stspg.io/2vtryf3l74z1) | major | 57 min |
| 2026-08-22 | [Programmable Wallets - Delays/Degraded Performance](https://stspg.io/w2drxjz30931) | critical | 7.7 h |
| 2026-08-16 | [USDC on Stellar — Delayed mints and burns](https://stspg.io/hx6d925rf1sw) | major | 29 min |
| 2026-08-14 | [CCTP Attestations on Base Delayed](https://stspg.io/cwpdrnnd3s5z) | major | 98 min |
| 2026-08-13 | [Circle xReserve on Stacks Testnet - Deposits and withdrawals delayed](https://stspg.io/w84gp915ps1x) | major | 2.6 days |

Newest 15 of 52. Full machine-readable history:
[`history/circle.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/circle.json).

## What is counted, and what is not

Of 52 recorded incidents, **50** have a usable length. Excluded:
0 maintenance, 2 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Circle's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/circle.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/circle.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Circle breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Circle on the live site](https://approjects-vendor-status-watch.static.hf.space/v/circle.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
