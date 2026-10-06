#!/usr/bin/env python3
"""data/commits.json -> commits.svg (a `git log --oneline` panel)."""
import json
import os
from datetime import datetime

from theme import FRAME2, GOLD, INK, MUTED, SOFT, esc, fade, frame, head, text_w, write

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W, ROW, PAD = 860, 44, 28
FS = 14

try:
    commits = json.load(open(os.path.join(ROOT, "data", "commits.json")))["commits"]
except (OSError, ValueError, KeyError):
    commits = []

h = max(1, len(commits)) * ROW + 36
fr, _ = frame(W, h)
s = head(W, h) + fr
if not commits:
    s += f'<text x="{PAD}" y="{h/2 + 5}" font-size="{FS}" fill="{MUTED}">waiting for the first daily refresh...</text>'
for i, c in enumerate(commits):
    y = 40 + i * ROW
    when = datetime.fromisoformat(c["date"].replace("Z", "+00:00")).strftime("%b %d")
    right = f'{c["repo"]} · {when}'
    room = W - PAD * 2 - 7 * FS * 0.6 - 24 - text_w(right, 12) - 24
    maxc = int(room / (FS * 0.6))
    msg = c["msg"] if len(c["msg"]) <= maxc else c["msg"][:maxc - 3].rstrip() + "..."
    g = (f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{GOLD}">{esc(c["hash"])}</text>'
         f'<text x="{PAD + 7 * FS * 0.6 + 24:.1f}" y="{y}" font-size="{FS}" fill="{INK}">{esc(msg)}</text>'
         f'<text x="{W - PAD}" y="{y}" font-size="12" fill="{MUTED}" text-anchor="end">{esc(right)}</text>')
    s += fade(g, 0.1 + i * 0.18)
write(os.path.join(ROOT, "art", "commits.svg"), s + "</svg>")
