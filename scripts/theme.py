"""Shared look for every generated SVG: terminal colours, fonts, window chrome."""
import html

BG, BG2 = "#0d1117", "#111722"
PANEL = "#161b22"
FRAME = "#30363d"
FRAME2 = "#21262d"
MUTED = "#7d8590"
INK = "#e6edf3"
SOFT = "#c9d1d9"
CYAN = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CW = 0.6  # monospace glyph width as a fraction of font size


def esc(s):
    return html.escape(str(s), quote=True)


def head(w, h, extra_css=""):
    """Opening <svg>, shared CSS (fade-in classes, reduced-motion), gradient defs."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}">'
        "<style>"
        ".f{opacity:0;animation:f .55s ease-out both}"
        "@keyframes f{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}"
        ".p{opacity:0;animation:p .45s cubic-bezier(.2,.9,.3,1.2) both;transform-box:fill-box;transform-origin:center}"
        "@keyframes p{0%{opacity:0;transform:scale(.88)}100%{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion: reduce){.f,.p{opacity:1!important;transform:none!important;animation:none!important}}"
        f"{extra_css}"
        "</style>"
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>'
    )


def frame(w, h, title=None, grad=True, rx=12):
    """Card background + optional macOS-style titlebar. Returns (svg_fragment, content_top_y)."""
    fill = "url(#bg)" if grad else BG
    out = (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
           f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{FRAME}"/>')
    top = 0
    if title is not None:
        top = 34
        out += f'<line x1="0" y1="{top}" x2="{w}" y2="{top}" stroke="{FRAME}"/>'
        for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
            out += f'<circle cx="{20 + i*16}" cy="{top/2}" r="5" fill="{c}"/>'
        out += (f'<text x="{w/2}" y="{top/2 + 4}" fill="{MUTED}" font-size="12" '
                f'text-anchor="middle">{esc(title)}</text>')
    return out, top


def fade(inner, delay, cls="f"):
    return f'<g class="{cls}" style="animation-delay:{delay:.2f}s">{inner}</g>'


def text_w(s, fs):
    return len(s) * fs * CW


def write(path, svg):
    with open(path, "w") as f:
        f.write(svg)
    print(f"wrote {path}: {len(svg)//1024 or 1} KB")
