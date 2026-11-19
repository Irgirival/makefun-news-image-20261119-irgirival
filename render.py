"""Render the front page for Thursday, 19 November 2026.

Draws a one-page newspaper front page ("THE DAY IN REVIEW") with Pillow:
a gold-on-navy masthead, a full-width lead story, four story panels in a
two-column grid, and an "also today" ticker. All stories are real events
reported on 19 November 2026, gathered from live news sources that day.

Deterministic: no randomness, no time, no network. Running this script
twice produces byte-identical entry.png output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (10, 26, 51)
NAVY_DARK = (7, 18, 36)
NAVY_MID = (16, 42, 78)
GOLD = (212, 164, 65)
GOLD_LIGHT = (232, 196, 110)
CREAM = (247, 242, 231)
CREAM_DIM = (228, 221, 203)
INK = (18, 28, 46)
GREY = (90, 96, 110)
WHITE = (255, 255, 255)
RED = (178, 58, 48)
TEAL = (42, 122, 110)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_kicker(draw, x, y, label, fg=WHITE, bg=NAVY):
    """Small uppercase tag chip; returns (width, height)."""
    fnt = font(SANS_BOLD, 20)
    pad_x, pad_y = 12, 6
    tw = draw.textlength(label, font=fnt)
    w, h = int(tw) + 2 * pad_x, 32
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), label, font=fnt, fill=fg)
    return w, h


def draw_headline(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Wrapped headline; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def draw_body(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def icon_bridge(draw, x, y, s, color):
    """A suspension bridge: deck, two towers, one arc."""
    draw.line([x, y + s * 0.72, x + s, y + s * 0.72], fill=color, width=4)
    draw.line([x + s * 0.22, y + s * 0.2, x + s * 0.22, y + s * 0.72],
              fill=color, width=4)
    draw.line([x + s * 0.78, y + s * 0.2, x + s * 0.78, y + s * 0.72],
              fill=color, width=4)
    draw.arc([x + s * 0.05, y - s * 0.1, x + s * 0.95, y + s * 0.9],
             start=180, end=360, fill=color, width=4)


def icon_flame(draw, x, y, s, color):
    """A stylised flame: teardrop body with a pale inner tongue."""
    pts = [(x + s * 0.5, y),
           (x + s * 0.74, y + s * 0.3),
           (x + s * 0.96, y + s * 0.62),
           (x + s * 0.84, y + s * 0.96),
           (x + s * 0.5, y + s * 1.0),
           (x + s * 0.16, y + s * 0.96),
           (x + s * 0.04, y + s * 0.62),
           (x + s * 0.26, y + s * 0.3)]
    draw.polygon(pts, fill=color)
    inner = [(x + s * 0.5, y + s * 0.48),
             (x + s * 0.66, y + s * 0.68),
             (x + s * 0.6, y + s * 0.88),
             (x + s * 0.5, y + s * 0.92),
             (x + s * 0.4, y + s * 0.88),
             (x + s * 0.34, y + s * 0.68)]
    draw.polygon(inner, fill=CREAM)


def icon_scales(draw, x, y, s, color):
    """Scales of justice: post, beam, two pans."""
    draw.line([x + s * 0.5, y + s * 0.05, x + s * 0.5, y + s * 0.9],
              fill=color, width=4)
    draw.line([x + s * 0.08, y + s * 0.22, x + s * 0.92, y + s * 0.22],
              fill=color, width=4)
    draw.line([x + s * 0.5, y + s * 0.9, x + s * 0.18, y + s * 0.98],
              fill=color, width=4)
    draw.line([x + s * 0.5, y + s * 0.9, x + s * 0.82, y + s * 0.98],
              fill=color, width=4)
    for cx in (0.14, 0.86):
        draw.line([x + s * cx, y + s * 0.22, x + s * cx, y + s * 0.5],
                  fill=color, width=3)
        draw.polygon([(x + s * (cx - 0.14), y + s * 0.5),
                      (x + s * (cx + 0.14), y + s * 0.5),
                      (x + s * cx, y + s * 0.72)], fill=color)


def icon_bars(draw, x, y, s, color):
    """Three rising bars (markets)."""
    bw = s * 0.2
    for i, hfrac in enumerate((0.35, 0.6, 0.9)):
        bx = x + i * s * 0.32
        draw.rectangle([bx, y + s * (1 - hfrac), bx + bw, y + s],
                       fill=color)


def icon_globe(draw, x, y, s, color):
    """A globe: circle with meridians, three gold stars above it."""
    cx, cy, r = x + s / 2, y + s / 2 + 6, s / 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=0, end=360, fill=color, width=3)


def panel(draw, x, y, w, h, kicker, headline, body, icon_fn, accent):
    """One cream story panel with a kicker chip, headline, body, icon."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CREAM)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           outline=GOLD, width=2)
    # Gold spine on the left edge.
    draw.rounded_rectangle([x, y, x + 8, y + h], radius=4, fill=accent)
    px = x + 22
    draw_kicker(draw, px, y + 16, kicker)
    icon_fn(draw, x + w - 78, y + 14, 56, accent)
    hy = y + 56
    hy = draw_headline(draw, px, hy, headline, font(SERIF, 30),
                       w - 118, 36)
    draw_body(draw, px, hy + 6, body, font(SANS, 21), w - 44, 27)


def render():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Subtle vertical shading + gold frame.
    for i in range(0, H, 4):
        shade = int(2 * (1 - i / H))
        d.line([0, i, W, i], fill=(NAVY[0] + shade, NAVY[1] + shade,
                                   NAVY[2] + shade))
    d.rectangle([10, 10, W - 11, H - 11], outline=GOLD, width=3)
    d.rectangle([18, 18, W - 19, H - 19], outline=GOLD, width=1)

    # ---- Masthead ----
    cx = W // 2
    title = "THE DAY IN REVIEW"
    tf = font(SERIF, 66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=GOLD_LIGHT)
    d.line([60, 122, W - 60, 122], fill=GOLD, width=2)
    d.line([60, 128, W - 60, 128], fill=GOLD, width=1)
    date_line = "THURSDAY, NOVEMBER 19, 2026  •  THE WORLD'S NEWS IN ONE PAGE"
    df = font(SANS_BOLD, 24)
    dw = d.textlength(date_line, font=df)
    d.text(((W - dw) / 2, 140), date_line, font=df, fill=WHITE)

    # ---- Lead story (full width) ----
    lx, ly, lw, lh = 36, 182, W - 72, 256
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12, fill=CREAM)
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12,
                        outline=GOLD, width=3)
    d.rounded_rectangle([lx, ly, lx + 10, ly + lh], radius=5, fill=RED)
    draw_kicker(d, lx + 28, ly + 18, "LEAD  •  SHENZHEN, CHINA")
    icon_globe(d, lx + lw - 150, ly + 20, 118, NAVY_MID)
    hy = draw_headline(d, lx + 28, ly + 62,
                       "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                       font(SERIF, 46), lw - 200, 54)
    draw_body(d, lx + 28, hy + 10,
              "The US, Chinese and Russian leaders hold their first "
              "three-way summit on the APEC sidelines — nuclear arms, "
              "Ukraine and Iran on the agenda.",
              font(SANS, 23), lw - 56, 31)

    # ---- Two-column grid, four stories ----
    gx, gy = 36, 452
    gw, gh, gap = (W - 72 - 20) // 2, 200, 20
    stories = [
        ("UKRAINE", "BRIDGE HIT FOR THE THIRD TIME",
         "Ukraine strikes the Crimean Bridge again; traffic is halted.",
         icon_bridge, NAVY_MID),
        ("MIDDLE EAST", "IRAN HITS BACK ACROSS THE GULF",
         "Tehran hits Gulf states after US strikes on Qeshm island.",
         icon_flame, RED),
        ("JUSTICE  •  THE HAGUE", "WORLD COURT RULES ON ROHINGYA",
         "The ICJ delivers its judgment in the case against Myanmar.",
         icon_scales, TEAL),
        ("MARKETS", "ANTHROPIC'S RECORD DEBUT",
         "The AI lab raises a record amount in its stock-market debut.",
         icon_bars, NAVY_MID),
    ]
    for i, (kick, head, body, icon_fn, accent) in enumerate(stories):
        px = gx + (i % 2) * (gw + gap)
        py = gy + (i // 2) * (gh + gap)
        panel(d, px, py, gw, gh, kick, head, body, icon_fn, accent)

    # ---- "Also today" ticker ----
    ty = gy + 2 * gh + gap + 14
    d.rounded_rectangle([36, ty, W - 36, ty + 62], radius=8, fill=NAVY_DARK)
    d.rounded_rectangle([36, ty, W - 36, ty + 62], radius=8,
                        outline=GOLD, width=2)
    d.text((52, ty + 16), "ALSO TODAY", font=font(SANS_BOLD, 22),
           fill=GOLD_LIGHT)
    tick_fnt = font(SANS, 19)
    d.text((52 + 168, ty + 8),
           "GTA VI begins its global rollout  •  IAEA: North Korea "
           "expanded enrichment",
           font=tick_fnt, fill=WHITE)
    d.text((52 + 168, ty + 33),
           "Jeffries set to be first Black Speaker  •  EU backs a €45bn "
           "loan for Ukraine",
           font=tick_fnt, fill=WHITE)

    # ---- Footer ----
    foot = ("Every story above was reported on Thursday, 19 November 2026  •  "
            "make.fun news-image-20261119")
    ff = font(SANS, 18)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, H - 52), foot, font=ff, fill=CREAM_DIM)

    return img


def main():
    img = render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
