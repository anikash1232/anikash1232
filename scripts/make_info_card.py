#!/usr/bin/env python3
"""
The "Now" card: what Ani is doing right now, a live top-languages bar, and
a few things to ask him about. Rows fade in one after another, then freeze.

    python scripts/make_info_card.py              # writes info-card.svg
    LANG_SAMPLE=1 python scripts/make_info_card.py  # preview with sample language data

Canvas is 840 x 880 so it matches ani-ascii.svg at equal widths in the README table.
Language data comes from data/languages.json (refreshed daily by the Action).
"""
import json
import os

from theme import (BG, CW, CYAN, FRAME, GOLD, GREEN, INK, MUTED, SOFT,
                   esc, fade, frame, head, text_w, write)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W, H = 840, 880
PAD = 32
FS = 28
LINE_H = 40
KEY_W = 210

# EDIT THESE ---------------------------------------------------------------
ROWS = [
    ("Building", ["Lead-sourcing + CRM systems",
                  "WCAG + PDF/UA accessibility tool",
                  "Course admin tooling"]),
    ("Teaching", ["COMP 210 + COMP 301 (TA)"]),
    ("Certs", ["AWS Cloud Practitioner", "DealCloud Platform Manager"]),
    ("Where", ["Chapel Hill, NC"]),
]
ASKS = [
    "turning messy documents into structured data",
    "WCAG + PDF/UA accessibility at scale",
    "winning FidHacks 2025 with Landed",
]
# --------------------------------------------------------------------------

LANG_COLORS = {"Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
               "Java": "#f89820", "C++": "#f34b7d", "C": "#a8b9cc", "Go": "#00ADD8",
               "C#": "#68c46b", "Shell": "#89e051", "R": "#2a7fd4", "Other": "#7d8590"}
FALLBACK = ["#bc8cff", "#ff9d5c", "#4ade80", "#f472b6"]


def load_langs():
    if os.environ.get("LANG_SAMPLE"):
        return [{"n": "Python", "pct": 38}, {"n": "TypeScript", "pct": 30}, {"n": "Java", "pct": 14},
                {"n": "C++", "pct": 10}, {"n": "Other", "pct": 8}]
    try:
        return json.load(open(os.path.join(ROOT, "data", "languages.json")))["langs"]
    except (OSError, ValueError, KeyError):
        return []


langs = load_langs()
fr, top = frame(W, H, "ani@github: ~$ ./now.sh")
parts = [head(W, H), fr]
k = 0


def add(inner):
    global k
    parts.append(fade(inner, 0.1 + k * 0.2))
    k += 1


y = top + 56
add(f'<text x="{PAD}" y="{y}" font-size="{FS + 6}" font-weight="700">'
    f'<tspan fill="{GREEN}">ani</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{GREEN}">now</tspan></text>')
y += 28
add(f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{FRAME}">{"-" * 24}</text>')
y += LINE_H + 4

for key, vals in ROWS:
    for i, v in enumerate(vals):
        assert text_w(v, FS) < W - PAD * 2 - KEY_W, f"row too long: {v}"
        kk = f'<text x="{PAD}" y="{y}" font-size="{FS}" font-weight="700" fill="{CYAN}">{esc(key)}</text>' if i == 0 else ""
        add(f'{kk}<text x="{PAD + KEY_W}" y="{y}" font-size="{FS}" fill="{INK}">{esc(v)}</text>')
        y += LINE_H
    y += 8

# live languages bar
y += 14
add(f'<text x="{PAD}" y="{y}" font-size="{FS}" font-weight="700" fill="{CYAN}">Top langs</text>'
    f'<text x="{PAD + KEY_W}" y="{y}" font-size="20" fill="{MUTED}">public repos, daily</text>')
y += 22
bar_w, bar_h, gap = W - PAD * 2, 22, 4
if langs:
    avail = bar_w - gap * (len(langs) - 1)
    x = PAD
    seg = ""
    for i, l in enumerate(langs):
        w = max(8, avail * l["pct"] / 100)
        c = LANG_COLORS.get(l["n"], FALLBACK[i % len(FALLBACK)])
        l["c"] = c
        seg += (f'<rect x="{x:.1f}" y="{y}" width="0" height="{bar_h}" rx="5" fill="{c}">'
                f'<animate attributeName="width" from="0" to="{w:.1f}" dur=".7s" begin="{0.1 + k * 0.2 + i * 0.12:.2f}s" fill="freeze"/></rect>')
        x += w + gap
    parts.append(seg)
else:
    parts.append(f'<rect x="{PAD}" y="{y}" width="{bar_w}" height="{bar_h}" rx="5" fill="{FRAME}" opacity=".5"/>')
k += 1
y += bar_h + 34
if langs:
    x = PAD
    leg = ""
    for l in langs:
        label = f'{l["n"]} {l["pct"]}%'
        w = 20 + text_w(label, 20) + 20
        if x + w > W - PAD:
            x, y = PAD, y + 34
        leg += (f'<circle cx="{x + 7}" cy="{y - 7}" r="7" fill="{l["c"]}"/>'
                f'<text x="{x + 22}" y="{y}" font-size="20" fill="{SOFT}">{esc(label)}</text>')
        x += w
    add(leg)
else:
    add(f'<text x="{PAD}" y="{y}" font-size="22" fill="{MUTED}">refreshing on the next daily run</text>')
y += 40

# ask me about
parts.append(fade(f'<line x1="{PAD}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{FRAME}" stroke-dasharray="6 6"/>', 0.1 + k * 0.2))
y += 46
add(f'<text x="{PAD}" y="{y}" font-size="{FS}" font-weight="700" fill="{CYAN}">Ask me about</text>')
y += 42
for a in ASKS:
    assert text_w(a, 25) < W - PAD * 2 - 36, f"ask too long: {a}"
    add(f'<text x="{PAD}" y="{y}" font-size="25" fill="{GOLD}">?</text>'
        f'<text x="{PAD + 36}" y="{y}" font-size="25" fill="{INK}">{esc(a)}</text>')
    y += 38

assert y < H - 20, f"content overflows card (y={y})"
write(os.path.join(ROOT, "info-card.svg"), "".join(parts) + "</svg>")
