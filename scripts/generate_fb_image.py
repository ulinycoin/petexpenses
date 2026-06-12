#!/usr/bin/env python3
"""
Facebook Post Image Generator.

Generates branded 1200×630 pixel images for Facebook posts.
Layout modes:
- blog: blog post title + excerpt + CTA (default)
- calculator: calculator promo card
- tip: tip/statistic card

Usage:
  python3 scripts/generate_fb_image.py --layout blog --title "Is Pet Insurance Worth It?" --output /tmp/fb_post.png
  python3 scripts/generate_fb_image.py --layout tip --tip_text "Pet insurance saves up to 90%" --badge "DID YOU KNOW"
"""

import os
import sys
import argparse
import urllib.request
import urllib.error
import json
import ssl

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("Error: Pillow required. Install: pip install Pillow", file=sys.stderr)
    sys.exit(1)

ssl._create_default_https_context = ssl._create_unverified_context

# ── Brand Constants ──────────────────────────────────────────────────
WIDTH = 1200
HEIGHT = 630
COLOR_CREAM = (255, 247, 232)
COLOR_INK = (27, 19, 64)
COLOR_CORAL = (255, 90, 60)
COLOR_WHITE = (255, 255, 255)
COLOR_MUTED = (107, 100, 144)

# ── Font Helper ──────────────────────────────────────────────────────
def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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
                        except (OSError, IOError):
                            continue
                else:
                    return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = font.getbbox(test_line)
            if bbox[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines


def cover_resize(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    img_w, img_h = image.size
    scale = max(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x = (new_w - target_w) // 2
    y = (new_h - target_h) // 2
    return resized.crop((x, y, x + target_w, y + target_h))


def draw_gradient(draw: ImageDraw.ImageDraw, colors: list[tuple], vertical: bool = True):
    """Draw a gradient across the image."""
    w, h = draw._image.size
    if vertical:
        for y in range(h):
            progress = y / h
            idx = min(int(progress * (len(colors) - 1)), len(colors) - 2)
            local_progress = (progress * (len(colors) - 1)) - idx
            c1, c2 = colors[idx], colors[idx + 1]
            r = int(c1[0] * (1 - local_progress) + c2[0] * local_progress)
            g = int(c1[1] * (1 - local_progress) + c2[1] * local_progress)
            b = int(c1[2] * (1 - local_progress) + c2[2] * local_progress)
            draw.line([(0, y), (w, y)], fill=(r, g, b))


# ── Background fetch ─────────────────────────────────────────────────
def fetch_breed_image_url(breed_name: str, species: str) -> str | None:
    """Fetch a breed image for the background."""
    query = breed_name.lower().replace(" (pembroke)", "").replace(" pembroke", "")
    query = query.replace("-", " ")
    candidates = []

    if species.lower() == "dog":
        parts = query.split()
        if len(parts) >= 2:
            dog_url = f"https://dog.ceo/api/breed/{parts[-1]}/{parts[0]}/images"
        else:
            dog_url = f"https://dog.ceo/api/breed/{parts[0]}/images"
        try:
            req = urllib.request.Request(dog_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get("status") == "success":
                    all_urls = data["message"]
                    for img_url in all_urls[:10]:
                        try:
                            hreq = urllib.request.Request(img_url, method="HEAD")
                            with urllib.request.urlopen(hreq, timeout=2) as hresp:
                                size = int(hresp.headers.get("Content-Length", 0))
                                candidates.append((size, img_url))
                        except:
                            candidates.append((0, img_url))
        except:
            pass

    if not candidates and species.lower() == "cat":
        try:
            url = "https://api.thecatapi.com/v1/images/search?limit=3&size=full"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                images = json.loads(resp.read().decode('utf-8'))
                for img in images:
                    w = img.get("width", 0)
                    h = img.get("height", 0)
                    candidates.append((w * h, img["url"]))
        except:
            pass

    if candidates:
        best = max(candidates, key=lambda c: c[0])
        return best[1]
    return None


# ── Layout Renders ───────────────────────────────────────────────────

def render_blog(base_img: Image.Image, draw: ImageDraw.ImageDraw,
                bg_img: Image.Image | None,
                title: str, excerpt: str, url: str, badge: str):
    """Layout: blog post promo — title + excerpt + CTA."""

    # Background
    if bg_img:
        bg_img = cover_resize(bg_img, WIDTH, HEIGHT)
        tint = Image.new('RGBA', (WIDTH, HEIGHT), COLOR_INK + (55,))
        bg_img = Image.alpha_composite(bg_img, tint)
        enhancer = ImageEnhance.Brightness(bg_img)
        bg_img = enhancer.enhance(0.75)
        base_img.alpha_composite(bg_img, (0, 0))

        # Gradient overlays
        grad = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(grad)
        for y in range(HEIGHT):
            if y < HEIGHT // 3:
                a = int(160 * (1 - y / (HEIGHT // 3)))
                gdraw.line([(0, y), (WIDTH, y)], fill=COLOR_INK[:3] + (a,))
            elif y > HEIGHT * 2 // 3:
                a = int(160 * ((y - HEIGHT * 2 // 3) / (HEIGHT // 3)))
                gdraw.line([(0, y), (WIDTH, y)], fill=COLOR_INK[:3] + (a,))
        base_img.alpha_composite(grad, (0, 0))

        # Badge
        if badge:
            font_badge = find_font(18, bold=True)
            bbox = font_badge.getbbox(badge)
            badge_w = bbox[2] + 30
            badge_h = 34
            draw.rounded_rectangle([(40, 30), (40 + badge_w, 30 + badge_h)],
                                   radius=17, fill=COLOR_CORAL)
            draw.text((40 + 15, 30 + (badge_h - bbox[3]) // 2 - 1),
                      badge, fill=COLOR_WHITE, font=font_badge)

        # Title
        font_title = find_font(44, bold=True)
        title_lines = wrap_text(title.upper(), font_title, WIDTH - 120)
        title_y = HEIGHT // 2 - len(title_lines) * 28
        for i, line in enumerate(title_lines):
            bbox = font_title.getbbox(line)
            x = 60
            y = title_y + i * 56
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 160), font=font_title)
            draw.text((x, y), line, fill=COLOR_WHITE, font=font_title)

        # Excerpt
        if excerpt:
            font_exc = find_font(20, bold=False)
            exc_lines = wrap_text(excerpt, font_exc, WIDTH - 140)
            exc_y = title_y + len(title_lines) * 56 + 20
            for i, line in enumerate(exc_lines[:2]):
                bbox = font_exc.getbbox(line)
                draw.text((60, exc_y + i * 28), line, fill=COLOR_CREAM, font=font_exc)

        # URL bar
        font_url = find_font(18, bold=True)
        url_text = url.replace("https://", "")
        bbox = font_url.getbbox(url_text)
        url_bar_y = HEIGHT - 60
        draw.rounded_rectangle([(40, url_bar_y - 15), (40 + bbox[2] + 40, url_bar_y + bbox[3] + 5)],
                               radius=22, fill=COLOR_WHITE + (200,))
        draw.text((40 + 20, url_bar_y), url_text, fill=COLOR_INK, font=font_url)

    else:
        # Flat: brand gradient background + card
        draw_gradient(draw, [COLOR_INK, COLOR_INK, COLOR_CREAM, COLOR_CREAM])

        # Logo area
        font_logo = find_font(20, bold=True)
        logo_text = "petexpenses.com"
        bbox = font_logo.getbbox(logo_text)
        draw.text((40, 35), logo_text, fill=COLOR_CREAM, font=font_logo)

        # Card
        card_margin = 80
        draw.rounded_rectangle(
            [(card_margin, 60), (WIDTH - card_margin, HEIGHT - 50)],
            radius=32, fill=COLOR_WHITE, outline=COLOR_INK, width=4
        )

        # Badge
        if badge:
            font_badge = find_font(16, bold=True)
            bbox = font_badge.getbbox(badge)
            badge_w = bbox[2] + 24
            badge_h = 28
            cx = (WIDTH - badge_w) // 2
            draw.rounded_rectangle([(cx, card_margin + 30), (cx + badge_w, card_margin + 30 + badge_h)],
                                   radius=14, fill=COLOR_CORAL)
            draw.text((cx + 12, card_margin + 30 + (badge_h - bbox[3]) // 2 - 1),
                      badge, fill=COLOR_WHITE, font=font_badge)

        # Title
        font_title = find_font(38, bold=True)
        title_lines = wrap_text(title.upper(), font_title, WIDTH - 220)
        title_y = 160
        for i, line in enumerate(title_lines):
            bbox = font_title.getbbox(line)
            x = (WIDTH - bbox[2]) // 2
            draw.text((x, title_y + i * 50), line, fill=COLOR_INK, font=font_title)

        # Excerpt
        if excerpt:
            font_exc = find_font(18, bold=False)
            exc_lines = wrap_text(excerpt, font_exc, WIDTH - 240)
            exc_y = title_y + len(title_lines) * 50 + 16
            for i, line in enumerate(exc_lines[:2]):
                bbox = font_exc.getbbox(line)
                draw.text(((WIDTH - bbox[2]) // 2, exc_y + i * 26), line, fill=COLOR_MUTED, font=font_exc)

        # URL CTA
        font_cta = find_font(20, bold=True)
        cta = f"Read more at petexpenses.com →"
        bbox = font_cta.getbbox(cta)
        pill_w = bbox[2] + 60
        pill_h = bbox[3] + 30
        pill_y = HEIGHT - 140
        draw.rounded_rectangle(
            [((WIDTH - pill_w) // 2, pill_y), ((WIDTH - pill_w) // 2 + pill_w, pill_y + pill_h)],
            radius=22, fill=COLOR_CORAL
        )
        draw.text(((WIDTH - bbox[2]) // 2, pill_y + (pill_h - bbox[3]) // 2 - 1),
                  cta, fill=COLOR_WHITE, font=font_cta)


def render_calculator(base_img: Image.Image, draw: ImageDraw.ImageDraw,
                      species: str = "Dog"):
    """Layout: calculator promo with big CTA."""

    draw_gradient(draw, [COLOR_CORAL, COLOR_CREAM, COLOR_CREAM])

    # Large decorative circle
    draw.ellipse([(WIDTH // 2 - 250, -100), (WIDTH // 2 + 50, 200)],
                 fill=COLOR_INK + (20,))

    # Icon
    icon = "●"
    font_icon = find_font(60, bold=True)
    bbox = font_icon.getbbox(icon)
    draw.text(((WIDTH - bbox[2]) // 2, 80), icon, fill=COLOR_CORAL, font=font_icon)

    # Title
    font_title = find_font(56, bold=True)
    title = f"{species} Cost Calculator"
    bbox = font_title.getbbox(title)
    draw.text(((WIDTH - bbox[2]) // 2, 170), title, fill=COLOR_INK, font=font_title)

    # Subtitle
    font_sub = find_font(22, bold=False)
    subtitle = "Estimate food, vet, insurance, grooming & more"
    bbox = font_sub.getbbox(subtitle)
    draw.text(((WIDTH - bbox[2]) // 2, 230), subtitle, fill=COLOR_MUTED, font=font_sub)

    # CTA
    font_cta = find_font(28, bold=True)
    cta = f"Calculate Now →"
    bbox = font_cta.getbbox(cta)
    pill_w = bbox[2] + 60
    pill_h = bbox[3] + 30
    pill_y = 320
    draw.rounded_rectangle(
        [((WIDTH - pill_w) // 2, pill_y), ((WIDTH - pill_w) // 2 + pill_w, pill_y + pill_h)],
        radius=25, fill=COLOR_INK
    )
    draw.text(((WIDTH - bbox[2]) // 2, pill_y + (pill_h - bbox[3]) // 2 - 1),
              cta, fill=COLOR_WHITE, font=font_cta)

    # URL
    font_url = find_font(22, bold=True)
    url = "petexpenses.com"
    bbox = font_url.getbbox(url)
    draw.text(((WIDTH - bbox[2]) // 2, 420), url, fill=COLOR_INK, font=font_url)


def render_tip(base_img: Image.Image, draw: ImageDraw.ImageDraw,
               bg_img: Image.Image | None,
               tip_text: str, badge: str = "PET TIP", source: str = "petexpenses.com"):
    """Layout: tip card with bold statistic or advice."""

    if bg_img:
        bg_img = cover_resize(bg_img, WIDTH, HEIGHT)
        tint = Image.new('RGBA', (WIDTH, HEIGHT), COLOR_INK + (70,))
        bg_img = Image.alpha_composite(bg_img, tint)
        enhancer = ImageEnhance.Brightness(bg_img)
        bg_img = enhancer.enhance(0.65)
        base_img.alpha_composite(bg_img, (0, 0))

        grad = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(grad)
        for y in range(HEIGHT):
            if y < HEIGHT // 3:
                a = int(140 * (1 - y / (HEIGHT // 3)))
                gdraw.line([(0, y), (WIDTH, y)], fill=COLOR_INK[:3] + (a,))
            elif y > HEIGHT * 2 // 3:
                a = int(100 * ((y - HEIGHT * 2 // 3) / (HEIGHT // 3)))
                gdraw.line([(0, y), (WIDTH, y)], fill=COLOR_INK[:3] + (a,))
        base_img.alpha_composite(grad, (0, 0))

        # Badge
        font_badge = find_font(18, bold=True)
        bbox = font_badge.getbbox(badge)
        badge_w = bbox[2] + 30
        badge_h = 34
        cx = (WIDTH - badge_w) // 2
        draw.rounded_rectangle([(cx, 30), (cx + badge_w, 30 + badge_h)],
                               radius=17, fill=COLOR_CORAL)
        draw.text((cx + 15, 30 + (badge_h - bbox[3]) // 2 - 1),
                  badge, fill=COLOR_WHITE, font=font_badge)

        # Tip text
        font_tip = find_font(40, bold=True)
        tip_lines = wrap_text(tip_text.upper(), font_tip, WIDTH - 120)
        tip_y = HEIGHT // 2 - len(tip_lines) * 25
        for i, line in enumerate(tip_lines):
            bbox = font_tip.getbbox(line)
            x = (WIDTH - bbox[2]) // 2
            y = tip_y + i * 52
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 160), font=font_tip)
            draw.text((x, y), line, fill=COLOR_WHITE, font=font_tip)

        # Source
        font_src = find_font(18, bold=False)
        bbox = font_src.getbbox(source)
        draw.text(((WIDTH - bbox[2]) // 2, HEIGHT - 70), source, fill=COLOR_CREAM, font=font_src)

    else:
        # Flat version
        draw_gradient(draw, [COLOR_INK, COLOR_CREAM, COLOR_CREAM])

        # Badge
        font_badge = find_font(18, bold=True)
        bbox = font_badge.getbbox(badge)
        badge_w = bbox[2] + 30
        badge_h = 34
        cx = (WIDTH - badge_w) // 2
        draw.rounded_rectangle([(cx, 50), (cx + badge_w, 50 + badge_h)],
                               radius=17, fill=COLOR_CORAL)
        draw.text((cx + 15, 50 + (badge_h - bbox[3]) // 2 - 1),
                  badge, fill=COLOR_WHITE, font=font_badge)

        # Tip text
        font_tip = find_font(36, bold=True)
        tip_lines = wrap_text(tip_text.upper(), font_tip, WIDTH - 140)
        tip_y = 160
        for i, line in enumerate(tip_lines):
            bbox = font_tip.getbbox(line)
            draw.text(((WIDTH - bbox[2]) // 2, tip_y + i * 48), line, fill=COLOR_INK, font=font_tip)

        # Source
        font_src = find_font(18, bold=False)
        bbox = font_src.getbbox(source)
        draw.text(((WIDTH - bbox[2]) // 2, HEIGHT - 80), source, fill=COLOR_MUTED, font=font_src)

        # CTA pill
        font_cta = find_font(22, bold=True)
        cta = "Learn more at petexpenses.com →"
        bbox = font_cta.getbbox(cta)
        pill_w = bbox[2] + 50
        pill_h = bbox[3] + 25
        pill_y = HEIGHT - 150
        draw.rounded_rectangle(
            [((WIDTH - pill_w) // 2, pill_y), ((WIDTH - pill_w) // 2 + pill_w, pill_y + pill_h)],
            radius=20, fill=COLOR_INK
        )
        draw.text(((WIDTH - bbox[2]) // 2, pill_y + (pill_h - bbox[3]) // 2 - 1),
                  cta, fill=COLOR_WHITE, font=font_cta)


# ── Main Entry ───────────────────────────────────────────────────────
def create_fb_image(layout: str = "blog",
                    title: str = "", excerpt: str = "",
                    species: str = "Dog",
                    tip_text: str = "", badge: str = "",
                    bg_image_path: str = None,
                    output_path: str = "/tmp/fb_post.png") -> str:
    """Generate branded Facebook post image."""

    temp_bg_path = None
    if not bg_image_path and layout == "blog" and species in ("Dog", "Cat"):
        print(f"Fetching {species} photo...", file=sys.stderr)
        url = fetch_breed_image_url(title.split(":")[0].strip(), species)
        if url:
            try:
                temp_bg_path = "/tmp/fb_downloaded_bg.png"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    with open(temp_bg_path, "wb") as f:
                        f.write(resp.read())
                bg_image_path = temp_bg_path
                print(f"  Downloaded OK", file=sys.stderr)
            except Exception as e:
                print(f"  Download failed: {e}", file=sys.stderr)

    base_img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_CREAM)

    bg_img = None
    if bg_image_path and os.path.exists(bg_image_path):
        try:
            bg_img = Image.open(bg_image_path).convert("RGBA")
        except Exception as e:
            print(f"  Warning: Could not open bg: {e}", file=sys.stderr)

    draw = ImageDraw.Draw(base_img)

    url = "https://petexpenses.com"

    if layout == "calculator":
        render_calculator(base_img, draw, species)
    elif layout == "tip":
        tip = tip_text or "Pet Insurance Can Save Up to 90% on Vet Bills"
        bdg = badge or "PET TIP"
        render_tip(base_img, draw, bg_img, tip, bdg, "petexpenses.com")
    else:
        # Default: blog
        t = title or "Pet Expenses Calculator"
        e = excerpt or "Compare costs across breeds and save money"
        bdg = badge or "BLOG POST"
        render_blog(base_img, draw, bg_img, t, e, url, bdg)

    final_img = base_img.convert("RGB")
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    final_img.save(output_path, "PNG")
    print(f"✅ FB image saved: {output_path}", file=sys.stderr)

    if temp_bg_path and os.path.exists(temp_bg_path):
        try: os.remove(temp_bg_path)
        except: pass

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Facebook post image")
    parser.add_argument("--layout", default="blog", choices=["blog", "calculator", "tip"])
    parser.add_argument("--title", default="", help="Post title")
    parser.add_argument("--excerpt", default="", help="Short description")
    parser.add_argument("--species", default="Dog", choices=["Dog", "Cat"])
    parser.add_argument("--tip_text", default="", help="Tip text")
    parser.add_argument("--badge", default="", help="Badge label")
    parser.add_argument("--bg_image", default=None, help="Background image path")
    parser.add_argument("--output", default="/tmp/fb_post.png", help="Output PNG path")
    args = parser.parse_args()

    path = create_fb_image(
        layout=args.layout, title=args.title, excerpt=args.excerpt,
        species=args.species, tip_text=args.tip_text, badge=args.badge,
        bg_image_path=args.bg_image, output_path=args.output
    )
    print(path)


if __name__ == "__main__":
    main()
