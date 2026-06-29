#!/usr/bin/env python3
"""Generate complete sitemap.xml for petexpenses.com from actual HTML files."""
import os
from datetime import datetime

ROOT = "/Users/aleksejs/Desktop/dog-cost-tool"
TODAY = datetime.now().strftime("%Y-%m-%d")

EXCLUDE_DIRS = {"petexpenses-new", "aura-designer-tool", "node_modules", ".hermes", "research", ".git", ".wrangler"}
EXCLUDE_FILES = {"404.html"}
EXCLUDE_PATHS = {"embed", "widget"}

# Priority map
PRIORITY = {
    "": 1.0,
    "compare": 0.9,
    "sources": 0.85,
    "about": 0.6,
    "contact": 0.4,
    "privacy": 0.3,
    "terms": 0.3,
    "blog": 0.7,
    "breeds": 0.7,
}

def get_priority(url_path):
    parts = url_path.strip("/").split("/")
    for p in parts:
        if p in PRIORITY:
            return PRIORITY[p]
    return 0.5

def is_excluded(path):
    rel = path.replace(ROOT + "/", "")
    parts = rel.split("/")
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def file_to_url(fp):
    url = fp.replace(ROOT + "/", "")
    if url in EXCLUDE_FILES:
        return None
    # Check if URL path matches any exclude pattern
    url_without_ext = url.replace(".html", "").replace("/index.html", "/").rstrip("/")
    for path in url_without_ext.split("/"):
        if path in EXCLUDE_PATHS:
            return None
    if url.endswith("/index.html"):
        url = url.replace("/index.html", "/")
    elif url == "index.html":
        url = ""
    else:
        url = url.replace(".html", "")
    return f"https://petexpenses.com/{url}"

# Collect URLs
urls = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip excluded dirs
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        if is_excluded(fp):
            continue
        url = file_to_url(fp)
        if url:
            urls.add(url)

urls = sorted(urls)

# Generate XML
xml_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url in urls:
    path = url.replace("https://petexpenses.com", "")
    pri = get_priority(path)
    xml_parts.append("  <url>")
    xml_parts.append(f"    <loc>{url}</loc>")
    xml_parts.append(f"    <lastmod>{TODAY}</lastmod>")
    xml_parts.append(f"    <changefreq>monthly</changefreq>")
    xml_parts.append(f"    <priority>{pri}</priority>")
    xml_parts.append("  </url>")

xml_parts.append("</urlset>")
xml_content = "\n".join(xml_parts) + "\n"

# Write to root
output_path = os.path.join(ROOT, "sitemap.xml")
with open(output_path, "w") as f:
    f.write(xml_content)

print(f"✅ Generated sitemap.xml with {len(urls)} URLs")
print(f"   Path: {output_path}")
print()
for url in urls:
    print(f"  {url}")
