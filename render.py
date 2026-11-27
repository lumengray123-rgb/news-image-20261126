#!/usr/bin/env python3
"""Draw 'THE WORLD TODAY' — a newspaper front page summing up
Thursday 26 November 2026, in code (PIL, no image assets).

Layout (1024x1024, newspaper paper), vertical budget:
  masthead 0-190 | lead 200-470 | row 2 492-746 | row 3 762-985 | footer 992
All art is drawn with PIL primitives. All six stories were verified
against at least two news sources dated 26 November 2026.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (164, 30, 34)
NAVY = (31, 58, 95)
GREY = (74, 85, 104)
GOLD = (176, 132, 30)
SKY = (28, 42, 74)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap by measured width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; returns y after the last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(d, x0, y, x1, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def burst(d, cx, cy, r1, r2, n=12, color=(255, 170, 40)):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def art_kuwait(d, x0, y0, x1, y1):
    """Night skyline, drone, explosion burst."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    for sx, sy in [(30, 18), (90, 40), (160, 12), (240, 34), (320, 20),
                   (400, 44), (60, 70), (200, 62), (360, 70), (430, 16)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(240, 230, 180))
    base = y1
    towers = [(0, 150, 46), (52, 110, 40), (98, 170, 52), (156, 95, 44),
              (206, 140, 48), (260, 120, 42), (308, 165, 46), (360, 105, 40),
              (406, 150, 44)]
    for tx, th, tw in towers:
        d.rectangle([x0 + tx, base - th, x0 + tx + tw, base], fill=(12, 18, 34))
        for wy in range(base - th + 10, base - 8, 18):
            for wx in range(x0 + tx + 6, x0 + tx + tw - 4, 12):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 210, 110))
    burst(d, x0 + 180, base - 150, 46, 20, color=(255, 170, 40))
    burst(d, x0 + 180, base - 150, 26, 12, color=(255, 90, 30))
    d.ellipse([x0 + 168, base - 162, x0 + 192, base - 138], fill=(255, 230, 150))
    dx, dy = x0 + 380, y0 + 42
    d.ellipse([dx - 16, dy - 8, dx + 16, dy + 8], fill=(200, 200, 200))
    d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(60, 60, 60))
    for rx in (-24, 24):
        d.line([(dx + rx - 12, dy - 10), (dx + rx + 12, dy - 10)],
               fill=(220, 220, 220), width=3)
        d.ellipse([dx + rx - 6, dy - 14, dx + rx + 6, dy - 6],
                  outline=(220, 220, 220), width=2)


def art_tariffs(d, x0, y0, x1, y1):
    """Bar chart: China 20, EU 15, Japan 15, S. Korea 15."""
    d.rectangle([x0, y0, x1, y1], fill=(235, 228, 210))
    labels = [("CHINA", 20, RED), ("EU", 15, NAVY), ("JAPAN", 15, NAVY),
              ("S. KOREA", 15, NAVY)]
    bw, gap = 72, 34
    bx = x0 + 26
    base = y1 - 24
    max_h = (y1 - y0) - 24 - 30 - 6
    for name, val, col in labels:
        h = int(max_h * val / 20)
        d.rectangle([bx, base - h, bx + bw, base], fill=col)
        f = font(SANS_B, 26)
        t = f"{val}%"
        tw = d.textlength(t, font=f)
        d.text((bx + (bw - tw) / 2, base - h - 30), t, font=f, fill=INK)
        f2 = font(SANS_B, 15)
        tw2 = d.textlength(name, font=f2)
        d.text((bx + (bw - tw2) / 2, base + 5), name, font=f2, fill=INK)
        bx += bw + gap
    d.line([(x0 + 14, base), (x1 - 14, base)], fill=INK, width=2)


def art_storm(d, x0, y0, x1, y1):
    """Storm cloud, rain, lightning."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 226, 232))
    cx, cy = (x0 + x1) // 2 - 60, y0 + 38
    for ox, oy, r in [(-58, 8, 32), (-18, -10, 40), (28, 6, 34), (62, 12, 26)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=GREY)
    d.rectangle([cx - 90, cy + 6, cx + 94, cy + 30], fill=GREY)
    for i in range(9):
        rx = x0 + 30 + i * 48
        d.line([(rx, y0 + 88), (rx - 12, y0 + 116)], fill=(90, 120, 160),
               width=4)
    bx, by = x0 + 330, y0 + 20
    bolt = [(bx, by), (bx - 22, by + 42), (bx - 7, by + 42),
            (bx - 25, by + 88), (bx + 10, by + 38), (bx - 5, by + 38)]
    d.polygon(bolt, fill=(255, 200, 40), outline=(200, 140, 0))


def art_ecb(d, x0, y0, x1, y1):
    """Bank pediment and columns."""
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    cx = (x0 + x1) // 2
    d.polygon([(cx - 118, y0 + 34), (cx + 118, y0 + 34), (cx, y0 + 6)],
              fill=NAVY)
    d.rectangle([x0 + 24, y0 + 34, x1 - 24, y0 + 40], fill=NAVY)
    for i in range(4):
        colx = x0 + 24 + i * 81
        d.rectangle([colx, y0 + 40, colx + 28, y1 - 6], fill=(188, 176, 142),
                    outline=NAVY, width=2)
    d.rectangle([x0 + 24, y1 - 6, x1 - 24, y1 - 2], fill=NAVY)


def art_jazan(d, x0, y0, x1, y1):
    """Refinery towers with flame and smoke."""
    d.rectangle([x0, y0, x1, y1], fill=(30, 30, 34))
    base = y1 - 6
    for tx, tw, th in [(24, 34, 50), (70, 26, 64), (108, 34, 44),
                       (154, 26, 58), (192, 34, 40)]:
        d.rectangle([x0 + tx, base - th, x0 + tx + tw, base], fill=(90, 90, 96))
        d.rectangle([x0 + tx + 6, base - th - 8, x0 + tx + tw - 6, base - th],
                    fill=(120, 120, 126))
    fx, fy = x0 + 150, base - 66
    d.polygon([(fx, fy - 22), (fx + 15, fy + 4), (fx + 6, fy + 1),
               (fx + 10, fy + 15), (fx, fy + 5), (fx - 10, fy + 15),
               (fx - 6, fy + 1), (fx - 15, fy + 4)], fill=(255, 140, 30))
    d.polygon([(fx, fy - 11), (fx + 8, fy + 6), (fx, fy + 1),
               (fx - 8, fy + 6)], fill=(255, 220, 90))
    for sx, sy, r in [(96, 12, 9), (122, 6, 11), (158, 4, 9)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(140, 140, 145))


def art_hiv(d, x0, y0, x1, y1):
    """Horizontal syringe on a teal panel."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 235, 228))
    cy = (y0 + y1) // 2
    # plunger
    d.line([(x0 + 52, cy), (x0 + 30, cy)], fill=(60, 60, 60), width=5)
    d.line([(x0 + 30, cy - 14), (x0 + 30, cy + 14)], fill=(60, 60, 60),
           width=5)
    # barrel
    d.rounded_rectangle([x0 + 52, cy - 17, x1 - 66, cy + 17], radius=8,
                        fill=(240, 250, 245), outline=NAVY, width=4)
    d.line([(x0 + 66, cy), (x1 - 110, cy)], fill=(200, 60, 60), width=6)
    # measurement ticks
    for i in range(1, 5):
        tx = x0 + 52 + i * (x1 - 66 - x0 - 52) // 5
        d.line([(tx, cy - 17), (tx, cy - 8)], fill=NAVY, width=2)
    # needle
    d.line([(x1 - 66, cy), (x1 - 26, cy)], fill=(90, 90, 90), width=4)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (auto-fit so the title never clips) ----
    size = 96
    while True:
        mf = font(SERIF_B, size)
        if d.textlength("THE WORLD TODAY", font=mf) <= 980 or size <= 60:
            break
        size -= 2
    tw = d.textlength("THE WORLD TODAY", font=mf)
    d.text(((W - tw) / 2, 14), "THE WORLD TODAY", font=mf, fill=INK)
    rule(d, 20, 128, W - 20, 3)
    d.rectangle([20, 138, W - 20, 180], fill=INK)
    df = font(SANS_B, 30)
    date = "THURSDAY, 26 NOVEMBER 2026"
    tw = d.textlength(date, font=df)
    d.text(((W - tw) / 2, 146), date, font=df, fill=(255, 255, 255))
    rule(d, 20, 192, W - 20, 2)

    # ---- lead story: Kuwait ----
    ly = 200
    art_kuwait(d, 20, ly, 500, ly + 270)
    kx = 524
    d.text((kx, ly + 2), "THE GULF", font=font(SANS_B, 22), fill=RED)
    y = para(d, kx, ly + 36, "DRONE ATTACK ON KUWAIT KILLS TWO ITALIANS",
             font(SERIF_B, 40), 480, 46)
    para(d, kx, y + 8,
         "Tehran denies any role as Gulf tensions rise after the strike on a military site.",
         font(SANS, 22), 480, 28)

    # ---- row 2 ----
    ry = 492
    rule(d, 20, ry - 10, W - 20, 2)
    art_tariffs(d, 20, ry, 500, ry + 128)
    art_storm(d, 524, ry, 1004, ry + 128)
    d.text((20, ry + 136), "TRADE", font=font(SANS_B, 20), fill=RED)
    d.text((524, ry + 136), "WEATHER", font=font(SANS_B, 20), fill=RED)
    y = para(d, 20, ry + 162, "U.S. PROPOSES NEW TARIFFS ON 14 PARTNERS",
             font(SERIF_B, 31), 480, 36)
    para(d, 20, y + 4, "20% on China; 15% cap for allies.",
         font(SANS, 20), 480, 26)
    y = para(d, 524, ry + 162, "THANKSGIVING STORMS CUT POWER TO 800,000",
             font(SERIF_B, 31), 480, 36)
    para(d, 524, y + 4, "Macy's 100th parade put off to Saturday.",
         font(SANS, 20), 480, 26)

    # ---- row 3 ----
    by = 762
    rule(d, 20, by - 10, W - 20, 2)
    cols = [
        (20, 340, art_ecb, "EUROPE", "DE COS TO LEAD THE ECB",
         "Succeeds Lagarde in February."),
        (352, 672, art_jazan, "THE RED SEA", "HOUTHIS STRIKE SAUDI REFINERY",
         "Worker killed; Riyadh hits back."),
        (684, 1004, art_hiv, "HEALTH", "$40 HIV JAB REACHES AFRICA",
         "Generic jab lands in Zambia."),
    ]
    for x0, x1, art, kick, head, dek in cols:
        art(d, x0, by, x1, by + 80)
        d.text((x0, by + 88), kick, font=font(SANS_B, 18), fill=RED)
        y = para(d, x0, by + 112, head, font(SERIF_B, 25), x1 - x0, 29)
        para(d, x0, y + 2, dek, font(SANS, 18), x1 - x0, 23)

    # ---- footer ----
    rule(d, 20, 992, W - 20, 2)
    ff = font(SANS, 17)
    foot = "All six stories first reported Thursday 26 November 2026"
    tw = d.textlength(foot, font=ff)
    d.text(((W - tw) / 2, 998), foot, font=ff, fill=GREY)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, optimize=True)
    print("wrote", out)
