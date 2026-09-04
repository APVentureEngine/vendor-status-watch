#!/usr/bin/env python3
"""Live end-to-end test of platforms.check() against real vendor status pages.
Asserts the normalized contract, then reports coverage + a real state histogram."""
import json, collections, sys, re
from concurrent.futures import ThreadPoolExecutor
import platforms as P

rows = json.load(open("../../research/vendor-status-probe-2026-09-04.json"))["rows"]
PLAT = {"statuspage-html": "statuspage", "instatus-html": "instatus"}
seen, vendors = set(), []
for r in rows:
    base = (r.get("base") or r["url"]).rstrip("/")
    plat = PLAT.get(r["platform"], r["platform"])
    if base in seen or plat not in P.PARSERS:
        continue
    seen.add(base)
    slug = re.sub(r"[^a-z0-9]+", "-", r["name"].lower()).strip("-")
    vendors.append({"name": r["name"], "slug": slug, "platform": plat, "base": base})

SAMPLE = {"statuspage": 60, "instatus": 99, "betterstack": 99, "status.io": 99}
cnt = collections.Counter(); sample = []
for v in vendors:
    if cnt[v["platform"]] < SAMPLE[v["platform"]]:
        cnt[v["platform"]] += 1; sample.append(v)
print(f"pool {len(vendors)} supported vendors; testing {len(sample)}: {dict(cnt)}\n")

with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(P.check, sample))

REQ = {"vendor","slug","platform","status_url","state","description","incidents","checked_at","error"}
bad = 0
for r in res:
    missing = REQ - set(r)
    assert not missing, f"contract: {r['vendor']} missing {missing}"
    assert r["state"] in P.STATES, f"bad state {r['state']} for {r['vendor']}"
    for i in r["incidents"]:
        assert set(i) == {"id","title","state","impact","url","started_at","updated_at","body"}, \
            f"incident contract broken for {r['vendor']}: {sorted(i)}"
    if r["error"]: bad += 1
print("CONTRACT: PASS (all rows normalized, all incidents same shape)\n")

byplat = collections.defaultdict(lambda: collections.Counter())
for r in res: byplat[r["platform"]][r["state"]] += 1
for p in sorted(byplat):
    tot = sum(byplat[p].values()); ok = tot - byplat[p]["unknown"]
    print(f"{p:12} n={tot:3}  parsed={ok:3} ({100*ok//max(tot,1)}%)  {dict(byplat[p])}")

live = [r for r in res if r["incidents"]]
print(f"\nvendors with an OPEN incident/maintenance right now: {len(live)}/{len(res)}")
for r in live[:8]:
    i = r["incidents"][0]
    print(f"  [{r['platform']:11}] {r['vendor'][:22]:22} {r['state']:11} :: {str(i['title'])[:58]}")
errs = collections.Counter((r["platform"], r["error"]) for r in res if r["error"])
print("\nerrors:", dict(errs) if errs else "none")
json.dump(res, open("selftest_live_out.json","w"), indent=1)
print(f"\nwrote selftest_live_out.json ({len(res)} rows)")
