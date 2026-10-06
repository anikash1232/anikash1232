#!/usr/bin/env python3
"""
Hand-authored SVGs: banner, impact tiles, tech stack, career timeline, project
cards, link buttons, contact card. No third-party services, no network.
Edit the DATA blocks below, then:

    python scripts/make_static_art.py        # writes into ./art/
"""
import json
import os
import textwrap

from theme import (BG, CW, CYAN, FRAME, FRAME2, GOLD, GREEN, INK, MUTED, PANEL, SOFT,
                   esc, fade, frame, head, text_w, write)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "art")
os.makedirs(OUT, exist_ok=True)
W = 860


def out(name):
    return os.path.join(OUT, name)


def wrap(s, px, fs):
    return textwrap.wrap(s, max(10, int(px / (fs * CW))))


# ---------------------------------------------------------------- banner
NAME = "Anirudh Kashyap"
BANNER_LINES = [
    "Computer Science @ UNC Chapel Hill",
    "Co-founder @ Prysma Tech, AI automation consultancy",
    "Applied AI researcher, accessibility tooling",
]


def banner():
    h = 318
    fs = 56
    nw = len(NAME) * fs * CW
    x0, ny = 40, 158
    fr, top = frame(W, h, "ani@github: ~/hello")
    n = len(NAME)
    widths = ";".join(f"{i * fs * CW:.1f}" for i in range(n + 1))
    xs = ";".join(f"{x0 + i * fs * CW:.1f}" for i in range(n + 1))
    dur, begin = 1.5, 0.9
    s = head(W, h) + fr
    s += (f'<clipPath id="nc"><rect x="{x0}" y="{ny - fs}" height="{fs + 20}" width="0">'
          f'<animate attributeName="width" values="{widths}" dur="{dur}s" begin="{begin}s" '
          f'calcMode="discrete" fill="freeze"/></rect></clipPath>')
    s += fade(f'<text x="{x0}" y="{top + 44}" font-size="14" fill="{MUTED}">'
              f'<tspan fill="{GREEN}">ani@github</tspan> ~ $ whoami</text>', 0.1)
    s += (f'<text x="{x0}" y="{ny}" font-size="{fs}" font-weight="700" fill="{INK}" '
          f'textLength="{nw:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#nc)">{esc(NAME)}</text>')
    # cursor: follows the typing, then blinks
    s += (f'<rect y="{ny - fs + 8}" width="{fs * 0.5:.1f}" height="{fs - 6}" fill="{CYAN}" x="{x0}">'
          f'<animate attributeName="x" values="{xs}" dur="{dur}s" begin="{begin}s" calcMode="discrete" fill="freeze"/>'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" '
          f'begin="{begin + dur}s" repeatCount="indefinite"/></rect>')
    y = ny + 56
    for i, line in enumerate(BANNER_LINES):
        s += fade(f'<text x="{x0}" y="{y}" font-size="17" fill="{SOFT}"><tspan fill="{CYAN}">&gt;</tspan> {esc(line)}</text>',
                  2.5 + i * 0.35)
        y += 30
    write(out("banner.svg"), s + "</svg>")


# ---------------------------------------------------------------- impact tiles
IMPACT = [
    ("hours --saved", "200+", "hrs / month", "manual lead sourcing replaced for investment banking clients"),
    ("users --accessibility", "2,500+", "users", "served by the in-house WCAG and PDF-UA alt-text tool"),
    ("users --app-store", "100+", "active", "App Store users on Chiaro, auto-apply at 90%+ success"),
    ("awards --first", "1st", "place", "FidHacks 2025, out of 25+ teams, with Landed"),
]


def impact():
    gap, tw, th = 16, (W - 16) / 2, 150
    h = th * 2 + gap
    s = head(W, h)
    for i, (cmd, num, unit, label) in enumerate(IMPACT):
        x, y = (i % 2) * (tw + gap), (i // 2) * (th + gap)
        g = (f'<rect x="{x + .5}" y="{y + .5}" width="{tw - 1}" height="{th - 1}" rx="12" fill="{PANEL}" stroke="{FRAME}"/>'
             f'<text x="{x + 24}" y="{y + 32}" font-size="12" fill="{MUTED}">$ {esc(cmd)}</text>'
             f'<text x="{x + 24}" y="{y + 78}" font-size="40" font-weight="700" fill="{GREEN}">{esc(num)}'
             f'<tspan font-size="15" font-weight="400" fill="{MUTED}"> {esc(unit)}</tspan></text>')
        for j, ln in enumerate(wrap(label, tw - 48, 13)[:2]):
            g += f'<text x="{x + 24}" y="{y + 106 + j * 18}" font-size="13" fill="{SOFT}">{esc(ln)}</text>'
        s += fade(g, 0.1 + i * 0.18, "p")
    write(out("impact.svg"), s + "</svg>")


# ---------------------------------------------------------------- tech tiles
def icon_markup(ic, cx, cy, size):
    """Brand icon centred at (cx, cy), or a text mark when no logo is available."""
    if ic["d"]:
        k = size / 24
        return (f'<g transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({k:.3f})">'
                f'<path d="{ic["d"]}" fill="{ic["c"]}"/></g>')
    fs = size * 0.42 if len(ic["t"]) > 2 else size * 0.5
    return (f'<text x="{cx}" y="{cy + fs * 0.35:.1f}" font-size="{fs:.1f}" font-weight="700" '
            f'text-anchor="middle" fill="{ic["c"]}">{esc(ic["t"])}</text>')


def tech():
    data = json.load(open(os.path.join(HERE, "icons.json")))
    icons = data["icons"]
    pad, gap = 24, 12
    inner = W - pad * 2
    s_parts, y, k = [], 34, 0
    s_parts.append(fade(f'<text x="{pad}" y="{y}" font-size="12" fill="{GOLD}">daily drivers</text>', 0.05))
    y += 16
    n = len(data["drivers"])
    tw = (inner - gap * (n - 1)) / n
    for i, name in enumerate(data["drivers"]):
        ic, x = icons[name], pad + i * (tw + gap)
        g = (f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="104" rx="12" fill="{ic["c"]}" fill-opacity=".09" '
             f'stroke="{ic["c"]}" stroke-opacity=".5"/>'
             f'{icon_markup(ic, x + tw / 2, y + 40, 38)}'
             f'<text x="{x + tw / 2:.1f}" y="{y + 86}" font-size="13" font-weight="700" fill="{INK}" '
             f'text-anchor="middle">{esc(name)}</text>')
        s_parts.append(fade(g, 0.2 + k * 0.08, "p"))
        k += 1
    y += 104 + 30
    for grp in data["groups"]:
        s_parts.append(fade(f'<text x="{pad}" y="{y}" font-size="12" fill="{MUTED}">{esc(grp["g"])}</text>', 0.2 + k * 0.05))
        y += 14
        x = pad
        for name in grp["items"]:
            ic = icons[name]
            w = 12 + 20 + 10 + text_w(name, 12) + 14
            if x + w > pad + inner:
                x, y = pad, y + 46
            g = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="38" rx="10" fill="{BG}" stroke="{FRAME}"/>'
                 f'<g opacity=".88">{icon_markup(ic, x + 22, y + 19, 20)}</g>'
                 f'<text x="{x + 42:.1f}" y="{y + 24}" font-size="12" fill="{SOFT}">{esc(name)}</text>')
            s_parts.append(fade(g, 0.2 + k * 0.05, "p"))
            k += 1
            x += w + 10
        y += 46 + 20
    h = y - 10
    fr, _ = frame(W, h)
    write(out("tech.svg"), head(W, h) + fr + "".join(s_parts) + "</svg>")


# ---------------------------------------------------------------- career timeline
CAREER = [
    ("Co-Founder & Software Engineer", "Prysma Tech", "May 2026 - now"),
    ("Applied AI Researcher", "UNC Computer Science", "Jan 2026 - now"),
    ("Software Developer", "Chiaro", "Apr 2026 - Jun 2026"),
    ("Software Engineer Intern", "Integrus (Investment Bank)", "Jan 2026 - May 2026"),
    ("Teaching Assistant, COMP 210 and COMP 301", "UNC Dept. of Computer Science", "Spring 2026 - now"),
]


def career():
    row, pad = 64, 28
    h = row * len(CAREER) + 20
    fr, _ = frame(W, h)
    s = head(W, h) + fr
    x = pad + 5
    s += f'<line x1="{x}" y1="{36}" x2="{x}" y2="{h - 44}" stroke="{FRAME}" stroke-width="2"/>'
    for i, (role, org, when) in enumerate(CAREER):
        y = 40 + i * row
        g = (f'<circle cx="{x}" cy="{y}" r="5" fill="{CYAN}"/>'
             f'<text x="{pad + 28}" y="{y - 2}" font-size="15" font-weight="700" fill="{INK}">{esc(role)}</text>'
             f'<text x="{pad + 28}" y="{y + 20}" font-size="13" fill="{CYAN}">{esc(org)}</text>'
             f'<text x="{W - pad}" y="{y + 2}" font-size="12" fill="{MUTED}" text-anchor="end">{esc(when)}</text>')
        if i < len(CAREER) - 1:
            g += f'<line x1="{pad + 28}" y1="{y + 38}" x2="{W - pad}" y2="{y + 38}" stroke="{FRAME2}"/>'
        s += fade(g, 0.1 + i * 0.2)
    write(out("career.svg"), s + "</svg>")


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("UNCWorkflows", "used by 60+ CS professors",
     "Unifies GitHub Classroom, Gradescope, Canvas and Google Sheets into one master roster, plus a seating chart generator and automated test conversion.",
     ["Next.js", "TypeScript", "Claude API"]),
    ("Syllabus-to-Calendar", "selected for production over 40+ projects",
     "Upload a syllabus, get a structured course calendar with .ics export. LLM extraction runs on a queue so long documents never time out.",
     ["Python", "FastAPI", "Dramatiq", "Angular"]),
    ("Landed", "1st place, FidHacks 2025",
     "Financial guidance for international students building US credit from zero history, with streamed, personalized roadmaps.",
     ["React", "TypeScript", "FastAPI", "Claude API"]),
    ("pipeline-automation", "unattended lead generation",
     "Pick an industry and metros in a web form. It scrapes Google Maps across US metro areas and emails back a Google Sheet.",
     ["React", "Python", "Apify", "Railway"]),
]


def project_cards():
    w, h = 424, 240
    for i, (name, badge, desc, tags) in enumerate(PROJECTS):
        fr, _ = frame(w, h)
        s = head(w, h) + fr
        s += (f'<text x="24" y="44" font-size="17" font-weight="700" fill="{INK}">{esc(name)}</text>'
              f'<text x="{w - 24}" y="44" font-size="12" fill="{CYAN}" text-anchor="end">view &#8594;</text>'
              f'<text x="24" y="70" font-size="12" fill="{GOLD}">{esc(badge)}</text>')
        lines = wrap(desc, w - 48, 13)
        assert len(lines) <= 5, f"{name}: description too long"
        for j, ln in enumerate(lines):
            s += f'<text x="24" y="{102 + j * 20}" font-size="13" fill="{SOFT}">{esc(ln)}</text>'
        x = 24
        for t in tags:
            tw = text_w(t, 11) + 20
            s += (f'<rect x="{x:.1f}" y="{h - 48}" width="{tw:.1f}" height="26" rx="13" fill="{BG}" stroke="{FRAME}"/>'
                  f'<text x="{x + tw / 2:.1f}" y="{h - 31}" font-size="11" fill="{MUTED}" text-anchor="middle">{esc(t)}</text>')
            x += tw + 8
        write(out(f"project-{i + 1}.svg"), s + "</svg>")


# ---------------------------------------------------------------- link buttons + contact card
BUTTONS = [
    ("btn-linkedin.svg", "LinkedIn", False),
    ("btn-github.svg", "GitHub", False),
    ("btn-email.svg", "Email", False),
    ("btn-unc.svg", "UNC CS", False),
    ("btn-contact-email.svg", "anirudh.vpk@gmail.com", True),
    ("btn-contact-linkedin.svg", "linkedin.com/in/anikash1", False),
]


def buttons():
    for fname, label, primary in BUTTONS:
        w, h = int(text_w(label, 13) + 40), 44
        fill, stroke, ink, wt = (CYAN, CYAN, BG, "700") if primary else (PANEL, FRAME, INK, "400")
        s = head(w, h) + (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="{fill}" stroke="{stroke}"/>'
                          f'<text x="{w / 2}" y="{h / 2 + 4.5}" font-size="13" font-weight="{wt}" fill="{ink}" '
                          f'text-anchor="middle">{esc(label)}</text></svg>')
        write(out(fname), s)


def contact():
    h = 190
    fr, _ = frame(W, h)
    s = head(W, h) + fr
    s += fade(f'<text x="40" y="52" font-size="14" fill="{MUTED}"><tspan fill="{GREEN}">ani@github</tspan> ~ $ ./contact.sh</text>', 0.1)
    s += fade(f'<text x="40" y="104" font-size="30" font-weight="700" fill="{INK}">Let\'s build something together.</text>', 0.4)
    s += fade(f'<text x="40" y="142" font-size="15" fill="{SOFT}">Open to software engineering roles.</text>', 0.7)
    write(out("contact.svg"), s + "</svg>")


def more_repos():
    h = 56
    fr, _ = frame(W, h)
    s = head(W, h) + fr
    s += (f'<text x="28" y="{h / 2 + 5}" font-size="14" fill="{MUTED}"><tspan fill="{GREEN}">ani@github</tspan> ~ $ ls ./more-repos'
          f'<tspan fill="{CYAN}">   (C++, C, Java, web)</tspan></text>'
          f'<text x="{W - 28}" y="{h / 2 + 5}" font-size="13" fill="{GOLD}" text-anchor="end">click to expand</text>')
    write(out("more-repos.svg"), s + "</svg>")


if __name__ == "__main__":
    more_repos(); banner(); impact(); tech(); career(); project_cards(); buttons(); contact()
