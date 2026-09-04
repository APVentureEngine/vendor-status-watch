#!/usr/bin/env python3
"""Probe run: prints environment variable NAMES only (never values) and exits 0."""
import os, sys, json, urllib.request
from datetime import datetime, timezone
print("hosted_run probe", datetime.now(timezone.utc).isoformat())
print("env names:", sorted(os.environ.keys()))
try:
    with urllib.request.urlopen("https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json", timeout=20) as r:
        n = len(json.load(r).get("vendors", []))
    print("egress ok, vendors.json rows:", n)
except Exception as e:
    print("egress FAILED:", e)
sys.exit(0)
