#!/usr/bin/env python3
"""Generate the org profile hero banners (dark + light).

All type is baked to outlines: GitHub serves README images through its
camo proxy, where an SVG has no webfont access. Animation is SMIL, which
survives <img> rendering in every major browser (CSS keyframes do too,
but SMIL keeps every element on one shared clock).

    python build.py <fonts-dir> <out-dir>

fonts-dir holds the Geist / Geist Mono latin woff2 files from
@fontsource/geist-sans and @fontsource/geist-mono. Needs fonttools + brotli.
"""

import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(sys.argv[1])
OUT = Path(sys.argv[2])

W, H = 1280, 600
LOOP = "7s"

FACES = {
    "sans400": "geist-sans-latin-400-normal.woff2",
    "sans500": "geist-sans-latin-500-normal.woff2",
    "sans600": "geist-sans-latin-600-normal.woff2",
    "mono400": "geist-mono-latin-400-normal.woff2",
    "mono500": "geist-mono-latin-500-normal.woff2",
}
_fonts = {}


def font(face):
    if face not in _fonts:
        _fonts[face] = TTFont(FONTS / FACES[face])
    return _fonts[face]


def text_width(s, face, size, tracking=0.0):
    f = font(face)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    w = sum(hmtx[cmap[ord(c)]][0] for c in s) * size / upm
    return w + tracking * size * max(len(s) - 1, 0)


def text_path(s, face, size, x, y, tracking=0.0):
    """Outline a string; (x, y) is the left end of the baseline."""
    f = font(face)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]
    k = size / upm
    out = []
    cx = x
    for c in s:
        g = cmap[ord(c)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        d = pen.getCommands()
        if d:
            out.append(d)
        cx += hmtx[g][0] * k + tracking * size
    return " ".join(out)


def t(s, face, size, x, y, fill, tracking=0.0, extra=""):
    d = text_path(s, face, size, x, y, tracking)
    return f'<path d="{d}" fill="{fill}"{extra}/>'


# The Sent mark, from sent-dm-docs/public/sent-logo-mark-white.svg (1000 box).
MARK = [
    "M413.439 275.528C396.838 269.254 388.466 250.709 394.74 234.108L456.845 69.7828C463.119 53.1814 481.664 44.8096 498.265 51.0839L979.217 232.854C995.819 239.128 1004.19 257.672 997.916 274.274L816.146 755.226C809.872 771.827 791.328 780.199 774.726 773.925L610.401 711.82C593.799 705.546 585.428 687.001 591.702 670.4L688.646 413.892C694.92 397.291 686.548 378.746 669.947 372.472L413.439 275.528Z",
    "M20.7828 451.048C4.18136 444.774 -4.19043 426.229 2.08387 409.628L64.1885 245.303C70.4628 228.701 89.0073 220.33 105.609 226.604L586.561 408.374C603.162 414.648 611.534 433.192 605.26 449.794L423.49 930.746C417.216 947.347 398.671 955.719 382.07 949.445L217.744 887.34C201.143 881.066 192.771 862.521 199.046 845.92L295.989 589.412C302.264 572.811 293.892 554.266 277.291 547.992L20.7828 451.048Z",
]


def mark(x, y, size, fill):
    s = size / 1000
    paths = "".join(f'<path d="{d}"/>' for d in MARK)
    return f'<g transform="translate({x} {y}) scale({s})" fill="{fill}">{paths}</g>'


PALETTES = {
    "dark": dict(
        bg="#0e0e0e", bg2="#161616", dot="#ffffff", dot_op="0.07",
        ink="#f5f5f4", muted="#a1a1aa", faint="#52525b", border="#262626",
        card="#121212", card_head="#181818",
        kw="#ff8a5b", str="#86efac", prop="#93c5fd", punct="#71717a", ident="#f5f5f4",
        glow_op="0.22", lane="#2e2e2e", pill="#151515",
    ),
    "light": dict(
        bg="#faf9f5", bg2="#f3f2ec", dot="#18181b", dot_op="0.08",
        ink="#18181b", muted="#52525b", faint="#71717a", border="#e4e2da",
        card="#ffffff", card_head="#f7f6f1",
        kw="#c2410c", str="#15803d", prop="#1d4ed8", punct="#a1a1aa", ident="#18181b",
        glow_op="0.12", lane="#dcdad2", pill="#ffffff",
    ),
}

ORANGE = "#EC3B00"
ORANGE_HI = "#ff7a3d"
ORANGE_LO = "#ffac5a"


def anim(attr, values, key_times):
    return (f'<animate attributeName="{attr}" values="{values}" keyTimes="{key_times}" '
            f'dur="{LOOP}" repeatCount="indefinite"/>')


def build(theme):
    p = PALETTES[theme]
    el = []

    # ---- canvas ---------------------------------------------------------
    el.append(f'''<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{p['dot']}" fill-opacity="{p['dot_op']}"/>
  </pattern>
  <radialGradient id="glow" cx="78%" cy="62%" r="55%">
    <stop offset="0" stop-color="{ORANGE}" stop-opacity="{p['glow_op']}"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{p['bg']}" stop-opacity="0"/>
    <stop offset="1" stop-color="{p['bg']}" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="hl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ORANGE}"/>
    <stop offset="1" stop-color="{ORANGE_LO}"/>
  </linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
</defs>''')
    el.append('<g clip-path="url(#frame)">')
    el.append(f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>')
    el.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    el.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
    el.append(f'<rect y="{H-140}" width="{W}" height="140" fill="url(#fade)"/>')

    # ---- left column: identity + promise --------------------------------
    LX = 72
    el.append(mark(LX, 64, 40, p["ink"]))
    el.append(t("sentdm", "mono500", 18, LX + 54, 92, p["muted"]))

    el.append(t("One API.", "sans600", 76, LX - 3, 238, p["ink"], tracking=-0.035))
    el.append(t("Every channel.", "sans600", 76, LX - 3, 322, "url(#hl)", tracking=-0.035))

    el.append(t("SMS, WhatsApp and RCS behind a single endpoint.",
                "sans400", 20, LX, 378, p["muted"]))
    el.append(t("Routing, compliance and delivery receipts handled for you.",
                "sans400", 20, LX, 408, p["muted"]))

    # SDK chips
    cx = LX
    el.append(t("OFFICIAL SDKS", "mono500", 13, LX, 486, p["faint"], tracking=0.12))
    for lang in ["TypeScript", "Python", "Go", "Java", "C#", "PHP", "Ruby"]:
        w = text_width(lang, "mono400", 15) + 26
        el.append(f'<rect x="{cx:.1f}" y="502" width="{w:.1f}" height="34" rx="17" '
                  f'fill="{p["pill"]}" stroke="{p["border"]}"/>')
        el.append(t(lang, "mono400", 15, cx + 13, 524, p["ink"]))
        cx += w + 8

    # ---- right column: the send call ------------------------------------
    CX, CY, CW, CH = 712, 44, 496, 318
    el.append(f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="14" '
              f'fill="{p["card"]}" stroke="{p["border"]}"/>')
    el.append(f'<path d="M{CX} {CY+14}a14 14 0 0 1 14-14h{CW-28}a14 14 0 0 1 14 14v26h-{CW}z" '
              f'fill="{p["card_head"]}"/>')
    el.append(f'<line x1="{CX}" y1="{CY+40}" x2="{CX+CW}" y2="{CY+40}" stroke="{p["border"]}"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        el.append(f'<circle cx="{CX+22+i*18}" cy="{CY+20}" r="5.5" fill="{c}" fill-opacity="0.85"/>')
    el.append(t("send.ts", "mono400", 14, CX + CW / 2 - text_width("send.ts", "mono400", 14) / 2,
                CY + 25, p["muted"]))

    chans = [
        ("SMS", ORANGE_HI, CX + 70),
        ("WhatsApp", "#25D366", CX + CW / 2),
        ("RCS", "#4F8EF7", CX + CW - 70),
    ]
    # timeline (fractions of LOOP): packet down the trunk, then one
    # recipient at a time is routed to the channel that suits it
    T_TRUNK = (0.02, 0.12)
    starts = [0.14, 0.30, 0.46]
    TRAVEL = 0.12
    HOLD_END, FADE_END = 0.88, 0.94

    K, S, P, PU, I = p["kw"], p["str"], p["prop"], p["punct"], p["ident"]
    code = [
        [("import", K), (" Sent ", I), ("from", K), (' "@sentdm/sentdm"', S), (";", PU)],
        [("const", K), (" sent ", I), ("=", PU), (" new", K), (" Sent", I), ("();", PU)],
        [],
        [("await", K), (" sent", I), (".", PU), ("messages", I), (".", PU), ("send", P), ("({", PU)],
        [("  to", P), (": [", PU)],
        [('    "+15555550100"', S), (",", PU)],
        [('    "+15555550101"', S), (",", PU)],
        [('    "+15555550102"', S), (",", PU)],
        [("  ],", PU)],
        [("  text", P), (": ", PU), ('"Your order has shipped"', S), (",", PU)],
        [("});", PU)],
    ]
    size, lh = 16, 24
    x0, y0 = CX + 24, CY + 72
    # recipient line highlight, in the colour of the channel it lands on
    for i, (_, col, _) in enumerate(chans):
        ln = 5 + i
        s0 = starts[i]
        el.append(f'<rect x="{CX+1}" y="{y0 + ln*lh - 17}" width="{CW-2}" height="{lh}" '
                  f'fill="{col}" opacity="0">'
                  + anim("opacity", "0;0;0.16;0.16;0;0",
                         f"0;{s0-0.02:.3f};{s0:.3f};{HOLD_END:.3f};{FADE_END:.3f};1") + '</rect>')
        el.append(f'<rect x="{CX+1}" y="{y0 + ln*lh - 17}" width="3" height="{lh}" '
                  f'fill="{col}" opacity="0">'
                  + anim("opacity", "0;0;1;1;0;0",
                         f"0;{s0-0.02:.3f};{s0:.3f};{HOLD_END:.3f};{FADE_END:.3f};1") + '</rect>')
    for li, line in enumerate(code):
        x = x0
        for chunk, col in line:
            el.append(t(chunk, "mono400", size, x, y0 + li * lh, col))
            x += text_width(chunk, "mono400", size)
    caret_x = x0 + text_width("});", "mono400", size) + 3
    el.append(f'<rect x="{caret_x:.1f}" y="{y0 + 10*lh - 14}" width="9" height="18" fill="{ORANGE}">'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
              f'dur="1.1s" repeatCount="indefinite"/></rect>')

    # ---- routing diagram ------------------------------------------------
    hub_x, hub_y = CX + CW / 2, 418
    pill_y = 494
    R = 20

    trunk = f"M{hub_x} {CY+CH} L{hub_x} {hub_y-R}"
    el.append(f'<path id="trunk" d="{trunk}" stroke="{p["lane"]}" stroke-width="2" '
              f'stroke-dasharray="4 6" fill="none"/>')
    for i, (_, _, px) in enumerate(chans):
        if abs(px - hub_x) < 1:
            d = f"M{hub_x} {hub_y+R} L{px} {pill_y-20}"
        else:
            d = f"M{hub_x} {hub_y+R} C{hub_x} {hub_y+R+28} {px} {pill_y-50} {px} {pill_y-20}"
        el.append(f'<path id="lane{i}" d="{d}" stroke="{p["lane"]}" stroke-width="2" '
                  f'stroke-dasharray="4 6" fill="none"/>')

    el.append(f'<circle cx="{hub_x}" cy="{hub_y}" r="{R}" fill="{p["card"]}" stroke="{p["border"]}"/>')
    # one pulse per routing decision
    for s0 in starts:
        el.append(f'<circle cx="{hub_x}" cy="{hub_y}" r="{R}" fill="none" stroke="{ORANGE}" '
                  f'stroke-width="2" stroke-opacity="0">'
                  + anim("stroke-opacity", "0;0;0.9;0;0", f"0;{s0-0.01:.3f};{s0:.3f};{s0+0.1:.3f};1")
                  + anim("r", f"{R};{R};{R};{R+14};{R+14}", f"0;{s0-0.01:.3f};{s0:.3f};{s0+0.1:.3f};1")
                  + '</circle>')
    el.append(mark(hub_x - 11, hub_y - 11, 22, p["ink"]))

    a, b = T_TRUNK
    el.append(f'<circle r="5" fill="{ORANGE}" opacity="0">'
              f'<animateMotion dur="{LOOP}" repeatCount="indefinite" keyPoints="0;0;1;1" '
              f'keyTimes="0;{a};{b};1" calcMode="linear"><mpath href="#trunk"/></animateMotion>'
              + anim("opacity", "0;0;1;1;0;0", f"0;{a};{a+0.005:.3f};{b-0.005:.3f};{b};1") + '</circle>')

    for i, (name, col, px) in enumerate(chans):
        s0 = starts[i]
        s1 = s0 + TRAVEL
        el.append(f'<circle r="5" fill="{col}" opacity="0">'
                  f'<animateMotion dur="{LOOP}" repeatCount="indefinite" keyPoints="0;0;1;1" '
                  f'keyTimes="0;{s0:.3f};{s1:.3f};1" calcMode="spline" '
                  f'keySplines="0 0 1 1;0.4 0 0.2 1;0 0 1 1"><mpath href="#lane{i}"/></animateMotion>'
                  + anim("opacity", "0;0;1;1;0;0",
                         f"0;{s0:.3f};{s0+0.005:.3f};{s1-0.005:.3f};{s1:.3f};1") + '</circle>')

        label_w = text_width(name, "sans500", 17)
        pw = max(label_w + 58, 132)
        x = px - pw / 2
        el.append(f'<rect x="{x:.1f}" y="{pill_y-20}" width="{pw:.1f}" height="40" rx="20" '
                  f'fill="{p["pill"]}" stroke="{p["border"]}"/>')
        el.append(f'<rect x="{x:.1f}" y="{pill_y-20}" width="{pw:.1f}" height="40" rx="20" '
                  f'fill="none" stroke="{col}" stroke-width="1.5" stroke-opacity="0">'
                  + anim("stroke-opacity", "0;0;1;1;0;0",
                         f"0;{s1-0.005:.3f};{s1+0.02:.3f};{HOLD_END};{FADE_END};1") + '</rect>')
        el.append(f'<circle cx="{x+20:.1f}" cy="{pill_y}" r="5" fill="{col}"/>')
        el.append(t(name, "sans500", 17, x + 34, pill_y + 6, p["ink"]))

        rw = text_width("delivered", "mono400", 14) + 20
        rx = px - rw / 2
        el.append(f'<g opacity="0">'
                  + anim("opacity", "0;0;1;1;0;0",
                         f"0;{s1+0.01:.3f};{s1+0.05:.3f};{HOLD_END};{FADE_END};1")
                  + f'<path d="M{rx:.1f} {pill_y+40} l4 4 l8 -9" stroke="{col}" stroke-width="2" '
                    f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                  + t("delivered", "mono400", 14, rx + 20, pill_y + 45, p["muted"])
                  + '</g>')

    el.append('</g>')
    el.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="23.5" fill="none" stroke="{p["border"]}"/>')

    body = "\n".join(el)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Sent: one API for SMS, WhatsApp and RCS">\n'
            f'<title>Sent: one API for SMS, WhatsApp and RCS</title>\n{body}\n</svg>\n')


OUT.mkdir(parents=True, exist_ok=True)
for theme in PALETTES:
    (OUT / f"hero-{theme}.svg").write_text(build(theme))
    print("wrote", OUT / f"hero-{theme}.svg")
