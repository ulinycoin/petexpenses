#!/usr/bin/env python3
"""
Premium Facebook Ad Banner Generator.
Creates ad-quality banners with hero photo, typography, and CTA.
Fully parameterised — works for any blog post.

Usage:
  python3 scripts/generate_fb_banner.py \\
    --photo /tmp/fb_breed_photo.png \\
    --badge "DOG FOOD" \\
    --headline "Kibble vs Fresh vs Raw" \\
    --subhead 'Kibble: $200/yr | Fresh: $2,800/yr | Raw: $3,500+/yr' \\
    --stat "Which is worth it?" \\
    --cta "See the comparison →" \\
    --output /tmp/fb_banner_kibble.png
"""

import os
import sys
import argparse
import ssl
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ssl._create_default_https_context = ssl._create_unverified_context

WIDTH = 1200
HEIGHT = 630

INK = (27, 19, 64)
CORAL = (255, 90, 60)
CREAM = (255, 247, 232)
WHITE = (255, 255, 255)
MUTED = (107, 100, 144)


def find_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                if path.endswith('.ttc'):
                    for idx in [0, 1]:
                        try:
                            return ImageFont.truetype(path, size, index=idx)
                        except:
                            continue
                else:
                    return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def cover_resize(img, tw, th):
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return resized.crop((x, y, x + tw, y + th))


def wrap_text(text, font, max_width):
    lines = []
    for para in text.split('\n'):
        words = para.split()
        cur = ""
        for w in words:
            test = f"{cur} {w}".strip()
            bb = font.getbbox(test)
            if bb[2] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def create_banner(photo_path, output_path,
                  badge_text="PET INSURANCE",
                  headline="IS PET INSURANCE WORTH IT?",
                  sub_lines=None,
                  stat_text="Premium: $300–$900/year",
                  cta_text="Read Full Analysis →",
                  highlight_sub=None):
    """Create a premium Facebook ad banner with full text control."""

    if sub_lines is None:
        sub_lines = [
            "We ran the math on 12 breeds.",
            "French Bulldogs & Goldens:",
            "it pays for itself."
        ]
    if highlight_sub is None:
        highlight_sub = 2  # index of the emphasised sub line

    # Load and process photo
    photo = Image.open(photo_path).convert("RGBA")
    photo = cover_resize(photo, WIDTH, HEIGHT)

    # Colour grade — warm
    r, g, b, a = photo.split()
    r = r.point(lambda i: min(255, int(i * 1.05)))
    g = g.point(lambda i: min(255, int(i * 1.02)))
    b = b.point(lambda i: max(0, int(i * 0.90)))
    photo = Image.merge("RGBA", (r, g, b, a))

    enhancer = ImageEnhance.Contrast(photo)
    photo = enhancer.enhance(1.08)

    base = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    base.paste(photo, (0, 0))
    draw = ImageDraw.Draw(base)

    # ── Left-side dark gradient overlay ──
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    fade_width = int(WIDTH * 0.68)
    for x in range(fade_width):
        progress = 1 - (x / fade_width)
        alpha = int(245 * (progress ** 1.5))
        odraw.rectangle([(x, 0), (x, HEIGHT)], fill=INK[:3] + (alpha,))
    for y in range(HEIGHT - 120, HEIGHT):
        progress = (y - (HEIGHT - 120)) / 120
        alpha = int(160 * progress)
        odraw.rectangle([(0, y), (WIDTH, y)], fill=INK[:3] + (alpha,))
    base.alpha_composite(overlay, (0, 0))

    # ── Text zone ──
    x0 = 48

    # Badge
    font_badge = find_font(16, bold=True)
    bb = font_badge.getbbox(badge_text)
    badge_w = bb[2] + 28
    badge_h = 30
    bx, by = x0, 48
    draw.rounded_rectangle([(bx, by), (bx + badge_w, by + badge_h)], radius=15, fill=CORAL)
    draw.text((bx + 14, by + (badge_h - bb[3]) // 2 - 1), badge_text, fill=WHITE, font=font_badge)

    # Headline
    font_h1 = find_font(50, bold=True)
    h1_lines = wrap_text(headline.upper(), font_h1, 580)
    h1_y = 120
    for i, line in enumerate(h1_lines):
        draw.text((x0, h1_y + i * 60), line, fill=WHITE, font=font_h1)
        draw.text((x0 + 2, h1_y + i * 60 + 2), line, fill=(0, 0, 0, 120), font=font_h1)

    # Subhead
    font_sub = find_font(19, bold=True)  # bold for readability on photo
    font_sub_bold = find_font(19, bold=True)
    sub_y = h1_y + len(h1_lines) * 60 + 16
    for i, line in enumerate(sub_lines):
        fnt = font_sub_bold if i == highlight_sub else font_sub
        clr = WHITE if i == highlight_sub else CREAM
        draw.text((x0, sub_y + i * 30), line, fill=clr, font=fnt)

    # Stat pill
    font_stat = find_font(32, bold=True)
    bb = font_stat.getbbox(stat_text)
    pill_w = bb[2] + 50
    pill_h = bb[3] + 28
    pill_x, pill_y = x0, sub_y + len(sub_lines) * 30 + 16
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=20, fill=CORAL)
    draw.text((pill_x + 25, pill_y + (pill_h - bb[3]) // 2 - 2), stat_text, fill=WHITE, font=font_stat)

    # CTA
    font_cta = find_font(22, bold=True)
    bb = font_cta.getbbox(cta_text)
    cta_w = bb[2] + 44
    cta_h = bb[3] + 28
    cta_x, cta_y = x0, pill_y + pill_h + 22
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=22, fill=WHITE)
    draw.text((cta_x + 22, cta_y + (cta_h - bb[3]) // 2 - 1), cta_text, fill=INK, font=font_cta)

    # URL
    font_url = find_font(18, bold=False)
    url_text = "petexpenses.com"
    bb = font_url.getbbox(url_text)
    draw.text((x0, HEIGHT - 52), url_text, fill=CREAM, font=font_url)

    # Save
    final = base.convert("RGB")
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    final.save(output_path, "PNG")
    print(f"✅ Banner saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate premium Facebook banner")
    parser.add_argument("--photo", default="/tmp/fb_breed_photo.png", help="Path to hero photo")
    parser.add_argument("--output", default="/tmp/fb_banner.png", help="Output PNG path")
    parser.add_argument("--badge", default="PET INSURANCE", help="Badge label")
    parser.add_argument("--headline", default="IS PET INSURANCE WORTH IT?", help="Main headline")
    parser.add_argument("--subhead", nargs="*", default=None,
                        help="Subhead lines (pass multiple values or use --subhead-line for each)")
    parser.add_argument("--highlight", type=int, default=2,
                        help="Index of emphasised subhead line")
    parser.add_argument("--stat", default="Premium: $300–$900/year", help="Stat pill text")
    parser.add_argument("--cta", default="Read Full Analysis →", help="CTA button text")

    # Alternative: pass subhead as comma-separated
    parser.add_argument("--subhead-csv", default=None, help="Subhead as comma-separated lines")

    args = parser.parse_args()

    # Resolve subhead
    sub_lines = None
    if args.subhead_csv:
        sub_lines = [s.strip() for s in args.subhead_csv.split(",")]
    elif args.subhead:
        sub_lines = args.subhead
    else:
        # Default for pet insurance
        sub_lines = [
            "We ran the math on 12 breeds.",
            "French Bulldogs & Goldens:",
            "it pays for itself."
        ]

    if not os.path.exists(args.photo):
        print(f"❌ Photo not found: {args.photo}")
        sys.exit(1)

    create_banner(
        photo_path=args.photo,
        output_path=args.output,
        badge_text=args.badge,
        headline=args.headline,
        sub_lines=sub_lines,
        stat_text=args.stat,
        cta_text=args.cta,
        highlight_sub=args.highlight,
    )
    print(args.output)


if __name__ == "__main__":
    main()
