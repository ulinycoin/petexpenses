"""
Facebook Page Auto-Poster for PetExpenses.
Usage:
  python3 scratch/facebook_post.py                          # interactive — pick a post
  python3 scratch/facebook_post.py --post pet-insurance     # specific post
  python3 scratch/facebook_post.py --all                    # post all unpublished articles
  python3 scratch/facebook_post.py --list                   # list available blog posts

Requires FACEBOOK_PAGE_ID and FACEBOOK_PAGE_TOKEN in .env
"""

import os
import json
import urllib.request
import urllib.error
import ssl
import sys
import glob

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
LOG_FILE = os.path.join(BASE_DIR, "scratch", "facebook_published.json")

# ─── Env loader ──────────────────────────────────────────────────────────────

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

load_env(os.path.join(BASE_DIR, '.env'))

PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")

# ─── Blog post index ─────────────────────────────────────────────────────────

BLOG_POSTS = {
    "pet-insurance": {
        "title": "Is Pet Insurance Worth It? (2026 Analysis)",
        "url": "https://petexpenses.com/blog/pet-insurance-worth-it",
        "file": "pet-insurance-worth-it.html",
        "message": "Is pet insurance actually worth the monthly premium? I ran the numbers on 12 breeds. For French Bulldogs — yes, absolutely. For others — depends on your risk tolerance. Here's the full breakdown ⬇️"
    },
    "new-puppy": {
        "title": "New Puppy First Year Cost (2026)",
        "url": "https://petexpenses.com/blog/new-puppy-first-year-cost",
        "file": "new-puppy-first-year-cost.html",
        "message": "Bringing home a puppy? The first year can cost $1,500–$5,000+ depending on breed. Here's exactly where the money goes — from vaccinations to crate training. Budget smart ⬇️"
    },
    "cheapest-breeds": {
        "title": "Cheapest Dog Breeds to Own (2026)",
        "url": "https://petexpenses.com/blog/cheapest-dog-breeds-to-own",
        "file": "cheapest-dog-breeds-to-own.html",
        "message": "Not all dogs cost the same. Some breeds cost under $1,000/year while others hit $3,500+. Here are the most budget-friendly breeds and why they're cheaper ⬇️"
    },
    "vet-visit-costs": {
        "title": "Dog Vet Visit Costs (2026 Guide)",
        "url": "https://petexpenses.com/blog/dog-vet-visit-costs",
        "file": "dog-vet-visit-costs.html",
        "message": "A routine vet visit runs $50–$250. An emergency? Can hit $5,000 overnight. Here's what 12 common procedures actually cost and how pet insurance changes the math ⬇️"
    },
    "kibble-vs-fresh": {
        "title": "Kibble vs Fresh vs Raw Dog Food: Cost Showdown",
        "url": "https://petexpenses.com/blog/kibble-vs-fresh-vs-raw",
        "file": "kibble-vs-fresh-vs-raw.html",
        "message": "Kibble: $200/year. Fresh: $2,800/year. Raw: $3,500+/year. Is the pricier food worth it or is kibble fine? I compared costs, nutrition, and vet opinions ⬇️"
    },
    "dog-food-recalls": {
        "title": "Dog Food Recalls 2026 — Brands to Avoid",
        "url": "https://petexpenses.com/blog/dog-food-recalls-2026",
        "file": "dog-food-recalls-2026.html",
        "message": "50+ dog food recalls in 2026 so far. Some of the biggest brands made the list. Here's which ones had issues and safer alternatives with clean track records ⬇️"
    },
    "litter-box-cost": {
        "title": "Self-Cleaning Litter Box Cost: Is It Worth the Hype?",
        "url": "https://petexpenses.com/blog/self-cleaning-litter-box-cost",
        "file": "self-cleaning-litter-box-cost.html",
        "message": "Automatic litter boxes cost $200–$800 upfront but save on litter over time. I tested a MeoWant and crunched the 3-year cost vs traditional boxes ⬇️"
    },
    "understanding-costs": {
        "title": "Understanding Pet Costs — Complete Guide 2026",
        "url": "https://petexpenses.com/blog/understanding-pet-costs",
        "file": "understanding-pet-costs.html",
        "message": "Americans spend $1,000–$5,000/year on a single pet. Most people underestimate costs by 40%. Here's a complete breakdown of every expense category ⬇️"
    }
}

# ─── Facebook Graph API ───────────────────────────────────────────────────────

def post_to_facebook(post_key):
    if not PAGE_ID or not PAGE_TOKEN:
        print("❌ FACEBOOK_PAGE_ID and FACEBOOK_PAGE_TOKEN must be set in .env")
        return False

    post = BLOG_POSTS.get(post_key)
    if not post:
        print(f"❌ Unknown post key: {post_key}")
        return False

    # Check if already published
    published = load_published_log()
    if post_key in published:
        print(f"⚠️  Already published on {published[post_key]} — skipping (remove from scratch/facebook_published.json to repost)")
        return False

    url = f"https://graph.facebook.com/v22.0/{PAGE_ID}/feed"
    data = {
        "message": post["message"],
        "link": post["url"],
        "access_token": PAGE_TOKEN
    }

    print(f"📤 Posting to Facebook: \"{post['title']}\"")
    print(f"   URL: {post['url']}")
    print(f"   Message: {post['message'][:80]}...")

    req = urllib.request.Request(url, method="POST")
    req.data = urllib.parse.urlencode(data).encode('utf-8')
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            post_id = result.get("id", "unknown")
            print(f"✅ Published! Post ID: {post_id}")
            print(f"   https://www.facebook.com/{PAGE_ID}/posts/{post_id.split('_')[-1]}")
            mark_published(post_key)
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"❌ HTTP {e.code}: {body}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ─── Published log ────────────────────────────────────────────────────────────

def load_published_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def mark_published(post_key):
    from datetime import datetime
    log = load_published_log()
    log[post_key] = datetime.now().isoformat()
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def list_posts():
    published = load_published_log()
    print("Available blog posts for Facebook:\n")
    for key, post in BLOG_POSTS.items():
        status = "✅ published" if key in published else "⬜ not yet"
        print(f"  {key:20s} — {post['title'][:50]:52s} {status}")
    print()

def post_all():
    for key in BLOG_POSTS:
        post_to_facebook(key)
        print()

if __name__ == "__main__":
    import urllib.parse

    if not PAGE_ID or not PAGE_TOKEN:
        print("⚠️  Facebook not configured. Edit .env:\n")
        print(f"  FACEBOOK_PAGE_ID=your_page_id")
        print(f"  FACEBOOK_PAGE_TOKEN=your_page_access_token\n")

    if "--list" in sys.argv:
        list_posts()
    elif "--all" in sys.argv:
        post_all()
    elif "--post" in sys.argv:
        idx = sys.argv.index("--post") + 1
        if idx < len(sys.argv):
            post_to_facebook(sys.argv[idx])
        else:
            print("Usage: --post <key>")
            list_posts()
    else:
        # Interactive mode
        list_posts()
        print("Which post to publish? (key name, or 'all', or 'q' to quit)")
        choice = input("> ").strip()
        if choice == 'all':
            post_all()
        elif choice in BLOG_POSTS:
            post_to_facebook(choice)
        elif choice != 'q':
            print(f"Unknown: {choice}")
