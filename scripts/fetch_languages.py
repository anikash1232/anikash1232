#!/usr/bin/env python3
"""
Top languages across your own public, non-fork repos -> data/languages.json.
Uses GITHUB_TOKEN when present (Actions provides it) for a higher rate limit.
On any failure it keeps the previous file so the daily run never breaks.
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests

USER = os.environ.get("GH_PROFILE_USER", "anikash1232")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "languages.json")
SKIP = {"HTML", "CSS", "SCSS", "Makefile", "Dockerfile", "Jupyter Notebook", "Batchfile"}
TOP = 4

H = {"Accept": "application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    H["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get(url, **kw):
    r = requests.get(url, headers=H, timeout=30, **kw)
    r.raise_for_status()
    return r.json()


try:
    repos, page = [], 1
    while True:
        chunk = get(f"https://api.github.com/users/{USER}/repos",
                    params={"per_page": 100, "page": page, "type": "owner"})
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    totals = {}
    for r in repos:
        if r["fork"] or r["private"]:
            continue
        try:
            langs = get(r["languages_url"])
        except Exception as e:
            print(f"  skip {r['name']}: {e}", file=sys.stderr)
            continue
        for lang, n in langs.items():
            if lang not in SKIP:
                totals[lang] = totals.get(lang, 0) + n
    if not totals:
        raise RuntimeError("no language data found")
    s = sum(totals.values())
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    langs = [{"n": k, "pct": round(100 * v / s)} for k, v in ranked[:TOP]]
    rest = 100 - sum(l["pct"] for l in langs)
    if rest > 0 and len(ranked) > TOP:
        langs.append({"n": "Other", "pct": rest})
    else:
        langs[0]["pct"] += rest  # absorb rounding drift
    with open(OUT, "w") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "langs": langs}, f, indent=1)
    print("languages:", ", ".join(f"{l['n']} {l['pct']}%" for l in langs))
except Exception as e:  # keep last good data
    print(f"fetch_languages: skipped ({e})", file=sys.stderr)
