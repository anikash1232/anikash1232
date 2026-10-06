#!/usr/bin/env python3
"""
Your 5 latest public commits (across your own public repos) -> data/commits.json.
Skips bot noise ([skip ci], merges). Keeps the previous file on any failure.
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests

USER = os.environ.get("GH_PROFILE_USER", "anikash1232")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "commits.json")
N, REPOS = 5, 12

H = {"Accept": "application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    H["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get(url, **kw):
    r = requests.get(url, headers=H, timeout=30, **kw)
    r.raise_for_status()
    return r.json()


try:
    repos = get(f"https://api.github.com/users/{USER}/repos",
                params={"per_page": 100, "type": "owner", "sort": "pushed"})
    repos = [r for r in repos if not r["fork"] and not r["private"]][:REPOS]
    found = []
    for r in repos:
        try:
            commits = get(f"https://api.github.com/repos/{USER}/{r['name']}/commits",
                          params={"author": USER, "per_page": 6})
        except Exception as e:  # empty repos return 409; skip them instead of aborting
            print(f"  skip {r['name']}: {e}", file=sys.stderr)
            continue
        for c in commits:
            msg = c["commit"]["message"].splitlines()[0].strip()
            if "[skip ci]" in msg or msg.lower().startswith("merge"):
                continue
            found.append({"hash": c["sha"][:7], "msg": msg, "repo": r["name"],
                          "date": c["commit"]["author"]["date"]})
    found.sort(key=lambda c: c["date"], reverse=True)
    if not found:
        raise RuntimeError("no commits found")
    with open(OUT, "w") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "commits": found[:N]}, f, indent=1)
    print(f"commits: {len(found[:N])} written")
except Exception as e:
    print(f"fetch_commits: skipped ({e})", file=sys.stderr)
