#!/usr/bin/env python3
"""
Hand-authored neofetch-style info card (terminal window SVG). Rows fade and
slide in one after another, then freeze. Edit the ROWS list below, then:

    python scripts/make_info_card.py            # writes info-card.svg
    STATIC=1 python scripts/make_info_card.py   # frozen frame for previews

Canvas is 840 x 880 so it lines up with stats.svg when both are shown at equal
widths in the README table.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 840, 880
PAD = 28
TITLEBAR_H = 30

BG, BG2 = "#0d1117", "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
KEY = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"

USER = "ani"
HOST = "github"

# (key, value). value can be a list of lines. EDIT THESE.
ROWS = [
    ("Name", "Anirudh Kashyap"),
    ("School", "UNC Chapel Hill, BS Computer Science '28"),
    ("Now", ["Co-founder, Prysma Tech (AI + CRM)",
             "Contract SWE, Integrus",
             "Senior TA, COMP 210 (Data Structures)"]),
    ("Research", "ADA Accessibility Tool, Prof. Goodwin"),
    ("Stack", ["Python, TypeScript, React, SQL",
               "AWS, GitHub Actions, automation"]),
    ("Certs", ["AWS Cloud Practitioner", "DealCloud Platform Manager"]),
    ("Looking", "SWE internships, Summer 2027"),
    ("Where", "Chapel Hill, NC"),
]

KEY_COL_W = 190
FS = 22           # font size for rows
LINE_H = 40
STAGGER = 0.22

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>'
    '.l{opacity:0;animation:in .5s ease-out both}'
    '@keyframes in{0%{opacity:0;transform:translateX(-10px)}100%{opacity:1;transform:translateX(0)}}'
    '@media (prefers-reduced-motion: reduce){.l{opacity:1!important;transform:none!important;animation:none!important}}'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD - 8 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{USER}@{HOST}: ~$ neofetch</text>')

n = 0


def line(y, inner):
    global n
    cls = "" if STATIC else ' class="l"'
    style = "" if STATIC else f' style="animation-delay:{n * STAGGER:.2f}s"'
    n += 1
    parts.append(f'<g{cls}{style}>{inner}</g>')


y = TITLEBAR_H + 70
line(y, f'<text x="{PAD}" y="{y}" font-size="{FS + 6}" font-weight="700">'
        f'<tspan fill="{GREEN}">{USER}</tspan><tspan fill="{MUTED}">@</tspan>'
        f'<tspan fill="{GREEN}">{HOST}</tspan></text>')
y += 22
line(y, f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{MUTED}">{"-" * 24}</text>')
y += LINE_H + 8

for key, val in ROWS:
    vals = val if isinstance(val, list) else [val]
    for i, v in enumerate(vals):
        assert len(v) * FS * 0.6 < W - PAD * 2 - KEY_COL_W, f'row too long: {v}'
        k = f'<tspan fill="{KEY}" font-weight="700">{html.escape(key)}</tspan>' if i == 0 else ""
        inner = (f'<text x="{PAD}" y="{y}" font-size="{FS}">{k}</text>'
                 f'<text x="{PAD + KEY_COL_W}" y="{y}" font-size="{FS}" fill="{INK}">{html.escape(v)}</text>')
        line(y, inner)
        y += LINE_H
    y += 10

# colour swatches, like neofetch
y += 10
sw = ["#ff5f56", "#ffbd2e", "#27c93f", "#22d3ee", "#1f6feb", "#bc8cff", "#e6edf3", "#7d8590"]
rects = "".join(f'<rect x="{PAD + i*46}" y="{y - 24}" width="40" height="28" rx="4" fill="{c}"/>'
                for i, c in enumerate(sw))
line(y, rects)

# blinking prompt at the bottom
py = H - 36
parts.append(f'<text x="{PAD}" y="{py}" font-size="{FS - 4}" fill="{MUTED}">{USER}@{HOST}:~$ </text>')
parts.append(f'<rect x="{PAD + 14 * (FS - 4) * 0.6:.1f}" y="{py - 18}" width="12" height="22" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" '
             f'repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
assert y < H - 60, f"content overflows card (y={y}); trim ROWS"
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
