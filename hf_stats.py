#!/usr/bin/env python3
"""Record Hugging Face dataset download/like counts once per pipeline run (c182, 2026-09-06).

WHY: HF datasets are the ONLY surface in this portfolio that measurably reaches
strangers (c181: 80 + 68 + 34 downloads/30d across three datasets vs 0 GitHub
stars and 0 site conversions). But HF only exposes a rolling 30-day number and
an all-time number; nothing here was recording them, so every cycle re-read the
same "80 downloads" anecdote and could not tell whether a card change, a new
derived dataset or a Bluesky post moved anything. This script appends one line
per run to out/hf_downloads.jsonl so the series is measurable.

WHAT IT MEASURES (and what it cannot): `downloads` is HF's rolling-30-day
count of file downloads via the Hub (dataset loaders + direct resolve URLs);
`downloadsAllTime` is cumulative. Neither is unique visitors. Movement between
consecutive runs of `downloadsAllTime` IS a stranger-action counter, because we
never download our own datasets through the Hub (hf_mirror uploads only).

Standard library only, no token needed (public endpoint). Non-fatal in the
pipeline: a stats miss must never block a data publish.

Usage (cwd = product/):
  python3 hf_stats.py                 # append a line, print deltas vs previous line
  python3 hf_stats.py --out PATH      # elsewhere (vendor-status-watch uses its own out/)
  python3 hf_stats.py --selftest
"""
import argparse
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "out", "hf_downloads.jsonl")
AUTHOR = "APProjects"
API = "https://huggingface.co/api/datasets"


def fetch(author=AUTHOR):
    q = urllib.parse.urlencode(
        [("author", author), ("expand[]", "downloads"), ("expand[]", "downloadsAllTime"),
         ("expand[]", "likes"), ("limit", "100")]
    )
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": "warn-feed hf_stats/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.load(r)
    out = {}
    for d in rows:
        out[d["id"]] = {
            "d30": int(d.get("downloads") or 0),
            "all": int(d.get("downloadsAllTime") or 0),
            "likes": int(d.get("likes") or 0),
        }
    return out


def last_line(path):
    if not os.path.exists(path):
        return None
    last = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                last = line
    return json.loads(last) if last else None


def deltas(prev, cur):
    """Per-dataset change in all-time downloads and likes since the previous line."""
    out = {}
    pd = (prev or {}).get("datasets", {})
    for rid, m in cur.items():
        p = pd.get(rid)
        out[rid] = {
            "all": m["all"] - (p["all"] if p else 0) if p else None,
            "likes": m["likes"] - (p["likes"] if p else 0) if p else None,
        }
    return out


def record(path, cur):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    prev = last_line(path)
    line = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "datasets": cur,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")
    return prev, line


def selftest():
    prev = {"datasets": {"a/x": {"d30": 5, "all": 10, "likes": 0}}}
    cur = {"a/x": {"d30": 6, "all": 13, "likes": 1}, "a/y": {"d30": 0, "all": 0, "likes": 0}}
    d = deltas(prev, cur)
    assert d["a/x"] == {"all": 3, "likes": 1}, d
    assert d["a/y"] == {"all": None, "likes": None}, d
    assert deltas(None, cur)["a/x"]["all"] is None
    print("hf_stats selftest OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--author", default=AUTHOR)
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    try:
        cur = fetch(a.author)
    except Exception as e:  # noqa: BLE001
        print(f"hf_stats: fetch failed ({e}); nothing recorded", file=sys.stderr)
        return 1
    if not cur:
        print("hf_stats: API returned no datasets; nothing recorded", file=sys.stderr)
        return 1
    prev, line = record(a.out, cur)
    d = deltas(prev, cur)
    since = prev["ts"] if prev else "first run"
    print(f"hf_stats: {len(cur)} datasets recorded -> {os.path.relpath(a.out, HERE)} (since {since})")
    for rid in sorted(cur):
        m = cur[rid]
        da = d[rid]["all"]
        mark = f" (+{da} all-time since last run)" if da else ""
        print(f"  {rid}: 30d={m['d30']} all={m['all']} likes={m['likes']}{mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
