# CoinList outage history — every incident their status page has posted

**17 CoinList incidents on record** spanning **2025-08-14** to **2026-02-18**. Status page:
[https://status.coinlist.co](https://status.coinlist.co) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Only **12** CoinList incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what CoinList posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent CoinList incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-02-18 | [NIL withdrawals from old.coinlist.co are temporarily disabled as part of an ongoing migration.](https://stspg.io/21yxpdyq19zp) | maintenance | — |
| 2026-01-05 | [Withdrawal Delays for BDXN, USDT, USDC, ETH, CSPR, SUI, BTC and other assets](https://stspg.io/37dzrvbt5qzc) | minor | 38.4 h |
| 2025-12-08 | [Deposits Disabled for all assets](https://stspg.io/z16zhj0ykjdg) | maintenance | — |
| 2025-11-19 | [Trading Update: Sell Mode Only and limited to USDC and USDT](https://stspg.io/nhf2kmgjv463) | maintenance | — |
| 2025-11-17 | [USDT Deposits Experiencing Delays](https://stspg.io/q1s4b3nl4879) | minor | 5.1 h |
| 2025-10-27 | [SOL Withdrawal Disabled](https://stspg.io/0g1mnbn6g1bm) | none | 7.1 days |
| 2025-10-24 | [Scheduled Maintenance for DOT (Polkadot)](https://stspg.io/5v66x6g7lppz) | none | — |
| 2025-10-23 | [Scheduled maintenance on our custodian (1st November).](https://stspg.io/qv0r28b3jr5n) | none | — |
| 2025-10-21 | [Deposits and Withdrawals for certain assets are experiencing delays due to a partial disruption with our custodian.](https://stspg.io/9ddm5ctp15sl) | minor | 69 min |
| 2025-10-20 | [FIL, eFIL, DOGE and XTZ Deposits and Withdrawals Delay](https://stspg.io/h7xd4xklmsjs) | none | 19.2 h |
| 2025-10-06 | [MOCA Withdrawals Delayed](https://stspg.io/hz1b9w69d0r6) | none | 5.7 h |
| 2025-10-04 | [FIL Deposits, Withdrawals, and Trading Disabled](https://stspg.io/np54dq3zf3hm) | none | 5.9 days |
| 2025-10-02 | [AXL Withdrawals Disabled](https://stspg.io/gc2x39wd29hp) | minor | 61.1 days |
| 2025-09-09 | [PEAQ and MINA Deposit Delays](https://stspg.io/v2dsqn028skl) | minor | 40.3 h |
| 2025-09-05 | [SOL, DOT, and ICP Deposits Disabled](https://stspg.io/7rrn57fy5gr4) | minor | 12.0 days |

Newest 15 of 17. Full machine-readable history:
[`history/coinlist.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/coinlist.json).

## What is counted, and what is not

Of 17 recorded incidents, **12** have a usable length. Excluded:
5 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about CoinList's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/coinlist.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/coinlist.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when CoinList breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [CoinList on the live site](https://approjects-vendor-status-watch.static.hf.space/v/coinlist.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
