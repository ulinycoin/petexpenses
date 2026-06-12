#!/usr/bin/env python3
"""
Facebook Page Posting Script.

Uploads a branded image to Facebook as a photo post with message + link.
Manages state in scratch/fb_published.json to avoid duplicates.

Usage:
  python3 scripts/post_fb.py --image /tmp/fb_post.png --message "Check this out!" --link "https://petexpenses.com/blog/..."
  python3 scripts/post_fb.py --all                              # post all blog articles with generated images
  python3 scripts/post_fb.py --list                             # list published state
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
import ssl
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "scratch", "fb_published.json")

# Blog posts catalogue
BLOG_POSTS = [
    {
        "key": "pet-insurance",
        "title": "Is Pet Insurance Worth It?",
        "url": "https://petexpenses.com/blog/pet-insurance-worth-it",
        "badge": "PET INSURANCE",
        "message": "Is pet insurance actually worth the monthly premium? I ran the numbers on 12 breeds. For French Bulldogs, Goldens, and other high-risk breeds it pays for itself.\n\nRead the full analysis → petexpenses.com/blog/pet-insurance-worth-it"
    },
    {
        "key": "new-puppy",
        "title": "New Puppy First Year Cost",
        "url": "https://petexpenses.com/blog/new-puppy-first-year-cost",
        "badge": "PUPPY BUDGET",
        "message": "Bringing home a puppy? The first year can cost $1,500–$5,000+ depending on breed. Here's exactly where the money goes — vaccinations, crate, training, food, and vet visits.\n\nFull breakdown → petexpenses.com/blog/new-puppy-first-year-cost"
    },
    {
        "key": "cheapest-breeds",
        "title": "Cheapest Dog Breeds to Own",
        "url": "https://petexpenses.com/blog/cheapest-dog-breeds-to-own",
        "badge": "BUDGET BREEDS",
        "message": "Not all dogs cost the same. Some breeds cost under $1,000/year while others hit $3,500+. Here are the most budget-friendly breeds and why they're cheaper.\n\nSee the list → petexpenses.com/blog/cheapest-dog-breeds-to-own"
    },
    {
        "key": "vet-visit-costs",
        "title": "Dog Vet Visit Costs",
        "url": "https://petexpenses.com/blog/dog-vet-visit-costs",
        "badge": "VET COSTS",
        "message": "A routine vet visit runs $50–$250. An emergency? Can hit $5,000 overnight. Here's what 12 common procedures actually cost and how pet insurance changes the math.\n\nFull guide → petexpenses.com/blog/dog-vet-visit-costs"
    },
    {
        "key": "kibble-vs-fresh",
        "title": "Kibble vs Fresh vs Raw: Cost Showdown",
        "url": "https://petexpenses.com/blog/kibble-vs-fresh-vs-raw",
        "badge": "FOOD COSTS",
        "message": "Kibble: $200/year. Fresh: $2,800/year. Raw: $3,500+/year. Is premium food worth it or is kibble fine? I compared costs, nutrition, and vet opinions.\n\nRead the comparison → petexpenses.com/blog/kibble-vs-fresh-vs-raw"
    },
    {
        "key": "dog-food-recalls",
        "title": "Dog Food Recalls 2026 — Brands to Avoid",
        "url": "https://petexpenses.com/blog/dog-food-recalls-2026",
        "badge": "SAFETY ALERT",
        "message": "50+ dog food recalls in 2026 so far. Some of the biggest brands made the list. Here's which ones had issues and safer alternatives with clean track records.\n\nCheck the list → petexpenses.com/blog/dog-food-recalls-2026"
    },
    {
        "key": "litter-box-cost",
        "title": "Self-Cleaning Litter Box Cost",
        "url": "https://petexpenses.com/blog/self-cleaning-litter-box-cost",
        "badge": "CAT GEAR",
        "message": "Automatic litter boxes cost $200–$800 upfront but save on litter over time. I tested a MeoWant and crunched the 3-year cost vs traditional boxes.\n\nSee the math → petexpenses.com/blog/self-cleaning-litter-box-cost"
    },
    {
        "key": "understanding-costs",
        "title": "Understanding Pet Costs — Complete Guide",
        "url": "https://petexpenses.com/blog/understanding-pet-costs",
        "badge": "COST GUIDE",
        "message": "Americans spend $1,000–$5,000/year on a single pet. Most people underestimate costs by 40%. Here's a complete breakdown of every expense category.\n\nRead the guide → petexpenses.com/blog/understanding-pet-costs"
    }
]


def load_env(env_path):
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val


def load_published():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {}


def mark_published(post_key, post_id=None, image_path=None):
    log = load_published()
    log[post_key] = {
        "timestamp": datetime.now().isoformat(),
        "post_id": post_id,
        "image": image_path
    }
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)


def multipart_encode(fields, file_field, file_path, file_mime="image/png"):
    """
    Build multipart/form-data body for Facebook photo upload.
    fields: dict of form fields (message, link, etc.)
    file_field: name of the file field (e.g. 'source')
    file_path: path to the image file
    """
    import uuid
    boundary = uuid.uuid4().hex
    body_parts = []

    for key, val in fields.items():
        body_parts.append(f'--{boundary}'.encode())
        body_parts.append(f'Content-Disposition: form-data; name="{key}"'.encode())
        body_parts.append(b'')
        body_parts.append(val.encode() if isinstance(val, str) else str(val).encode())

    # File
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{os.path.basename(file_path)}"'.encode()
    )
    body_parts.append(f'Content-Type: {file_mime}'.encode())
    body_parts.append(f'Content-Transfer-Encoding: binary'.encode())
    body_parts.append(b'')
    with open(file_path, 'rb') as f:
        body_parts.append(f.read())

    body_parts.append(f'--{boundary}--'.encode())
    body_parts.append(b'')

    body = b'\r\n'.join(body_parts)
    content_type = f'multipart/form-data; boundary={boundary}'
    return body, content_type


def post_to_facebook(post_key, image_path=None, force=False):
    """Post an article to Facebook as a photo post."""

    # Load .env
    load_env(os.path.join(BASE_DIR, '.env'))

    page_id = os.getenv("FACEBOOK_PAGE_ID")
    page_token = os.getenv("FACEBOOK_PAGE_TOKEN")

    if not page_id or not page_token:
        print("❌ FACEBOOK_PAGE_ID and FACEBOOK_PAGE_TOKEN must be set in .env", file=sys.stderr)
        return False

    # Check published state
    published = load_published()
    if post_key in published and not force:
        print(f"⚠️  Already published ({published[post_key]['timestamp']}) — use --force to repost", file=sys.stderr)
        return False

    # Find post data
    post = None
    for p in BLOG_POSTS:
        if p["key"] == post_key:
            post = p
            break
    if not post:
        print(f"❌ Unknown post key: {post_key}", file=sys.stderr)
        return False

    # Ensure image exists
    if not image_path or not os.path.exists(image_path):
        # Try to find a pre-generated image
        possible = [
            image_path,
            f"/tmp/fb_{post_key}.png",
            f"/tmp/fb_post.png",
        ]
        for p in possible:
            if p and os.path.exists(p):
                image_path = p
                break
        if not image_path or not os.path.exists(image_path):
            print(f"❌ Image not found. Generate first:", file=sys.stderr)
            print(f"   python3 scripts/generate_fb_image.py --layout blog \\", file=sys.stderr)
            print(f"     --title \"{post['title']}\" --badge \"{post['badge']}\" \\", file=sys.stderr)
            print(f"     --output /tmp/fb_{post_key}.png", file=sys.stderr)
            return False

    print(f"📤 Posting to Facebook: \"{post['title']}\"")
    print(f"   Image: {image_path}")
    print(f"   URL: {post['url']}")

    # Upload photo with message (link in message body)
    url = f"https://graph.facebook.com/v22.0/{page_id}/photos"
    fields = {
        "message": post["message"],
        "access_token": page_token,
    }

    body, content_type = multipart_encode(fields, "source", image_path)

    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", content_type)

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            post_id = result.get("id", "unknown")
            print(f"✅ Published! Post ID: {post_id}")
            link = f"https://www.facebook.com/{page_id}/posts/{post_id.split('_')[-1]}"
            print(f"   {link}")

            mark_published(post_key, post_id=post_id, image_path=image_path)
            return True

    except urllib.error.HTTPError as e:
        body_resp = e.read().decode('utf-8')
        print(f"❌ HTTP {e.code}: {body_resp}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return False


def generate_and_post(post_key, force=False):
    """Generate image then post to Facebook."""
    post = None
    for p in BLOG_POSTS:
        if p["key"] == post_key:
            post = p
            break
    if not post:
        print(f"❌ Unknown post key: {post_key}", file=sys.stderr)
        return

    image_path = f"/tmp/fb_{post_key}.png"

    # Generate image
    print(f"🎨 Generating image for: {post['title']}")
    import subprocess
    cmd = [
        sys.executable,
        os.path.join(BASE_DIR, "scripts", "generate_fb_image.py"),
        "--layout", "blog",
        "--title", post["title"],
        "--badge", post["badge"],
        "--output", image_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Image generation failed: {result.stderr}", file=sys.stderr)
        return

    # Post
    post_to_facebook(post_key, image_path, force)


def list_status():
    """Show current publication status."""
    published = load_published()
    print(f"{'KEY':<22} {'TITLE':<40} STATUS")
    print("-" * 80)
    for p in BLOG_POSTS:
        key = p["key"]
        title = p["title"][:38]
        if key in published:
            ts = published[key]["timestamp"][:19]
            print(f"  {key:<20} {title:<40} ✅ {ts}")
        else:
            print(f"  {key:<20} {title:<40} ⬜ not yet published")


def post_all(force=False):
    """Generate and post all unpublished (or all if force) blog articles."""
    published = load_published()
    for p in BLOG_POSTS:
        key = p["key"]
        if key in published and not force:
            print(f"⏩ Skipping {key} (already published)")
            continue
        generate_and_post(key, force)
        print()


def main():
    parser = argparse.ArgumentParser(description="Post to Facebook with branded images")
    parser.add_argument("--image", help="Path to pre-generated image (overrides auto-gen)")
    parser.add_argument("--message", help="Custom message (overrides default)")
    parser.add_argument("--link", help="Article URL (overrides default)")
    parser.add_argument("--force", action="store_true", help="Repost even if already published")
    parser.add_argument("--list", action="store_true", help="List publication status")
    parser.add_argument("--all", action="store_true", help="Generate and post all blog articles")
    parser.add_argument("--post", help="Post a specific article by key (e.g. 'pet-insurance')")
    args = parser.parse_args()

    if args.list:
        list_status()
        return

    if args.all:
        post_all(force=args.force)
        return

    if args.post:
        if args.image:
            post_to_facebook(args.post, args.image, args.force)
        else:
            generate_and_post(args.post, args.force)
        return

    # Interactive
    list_status()
    print()
    print("Post key to publish (or 'all'): ", end="")
    choice = input().strip()
    if choice == "all":
        post_all()
    elif any(p["key"] == choice for p in BLOG_POSTS):
        if args.image:
            post_to_facebook(choice, args.image, args.force)
        else:
            generate_and_post(choice, args.force)
    elif choice:
        print(f"Unknown: {choice}")


if __name__ == "__main__":
    main()
