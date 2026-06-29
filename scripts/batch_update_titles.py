#!/usr/bin/env python3
"""Batch-update remaining breed pages with new title/meta/og format."""
import re, os, sys

BREEDS_DIR = '/Users/aleksejs/Desktop/dog-cost-tool/breeds'

# Get list of files without 'Purchase Price'
files = []
for fname in os.listdir(BREEDS_DIR):
    if not fname.endswith('.html'):
        continue
    path = os.path.join(BREEDS_DIR, fname)
    with open(path, 'r') as f:
        content = f.read()
    if 'Purchase Price' not in content:
        files.append(fname)

print(f"Pages without 'Purchase Price': {len(files)}")

cat_keywords = ['cat', 'shorthair', 'rex', 'coon', 'ragdoll', 'persian', 'siamese',
                'bengal', 'burmese', 'tonkinese', 'birman', 'manx', 'savannah',
                'fold', 'blue', 'longhair', 'abyssinian']

done = 0
for fname in files:
    path = os.path.join(BREEDS_DIR, fname)
    with open(path, 'r') as f:
        content = f.read()
    
    # Extract old title
    m_title = re.search(r'<title>(.*?)</title>', content)
    if not m_title:
        print(f"  SKIP {fname}: no <title>")
        continue
    old_title_full = m_title.group(0)
    old_title_text = m_title.group(1)
    
    # Extract old meta
    m_meta = re.search(r'<meta name="description" content="(.*?)">', content)
    if not m_meta:
        print(f"  SKIP {fname}: no meta description")
        continue
    old_meta_full = m_meta.group(0)
    old_meta_text = m_meta.group(1)
    
    # Extract dollar range
    m_dollars = re.search(r'\$([0-9,]+)[–-]\$([0-9,]+)', old_meta_text)
    if not m_dollars:
        print(f"  SKIP {fname}: no dollar range in meta")
        continue
    cost_low, cost_high = m_dollars.group(1), m_dollars.group(2)
    
    # Extract breed name from title
    breed_name = None
    t = old_title_text
    if 'Annual Cost (2026)' in t:
        breed_name = t.split(' Annual Cost')[0].strip()
    elif 'How Much Does' in t:
        m2 = re.search(r'How Much Does an? (.*?) (?:Cat|Dog)?\s*Cost', t)
        if m2:
            breed_name = m2.group(1).strip()
    
    if not breed_name:
        print(f"  SKIP {fname}: can't parse: {t}")
        continue
    
    # Species detection
    species = 'cat' if any(kw in fname.lower() for kw in cat_keywords) else 'dog'
    puppy_word = 'kitten' if species == 'cat' else 'puppy'
    
    new_title = f'{breed_name} Cost in 2026: Purchase Price + ${cost_low}–${cost_high}/Year Ownership'
    new_meta = f'What a {breed_name} really costs in 2026 — {puppy_word} price, annual food & vet bills (${cost_low}–${cost_high}/yr), insurance, and hidden expenses. Free calculator with real data.'
    new_og = f'{breed_name} Cost in 2026: Purchase Price + ${cost_low}–${cost_high}/Year'
    
    # Make replacements
    content = content.replace(old_title_full, f'<title>{new_title}</title>')
    content = content.replace(old_meta_full, f'<meta name="description" content="{new_meta}">')
    
    # Replace og:title
    m_og = re.search(r'<meta property="og:title" content="(.*?)">', content)
    if m_og:
        old_og_full = m_og.group(0)
        content = content.replace(old_og_full, f'<meta property="og:title" content="{new_og}">')
    
    with open(path, 'w') as f:
        f.write(content)
    
    done += 1
    print(f'  OK {fname}: {breed_name} ${cost_low}–${cost_high}')

print(f"\nDone: {done}")

# Final count
remaining = 0
for fname in os.listdir(BREEDS_DIR):
    if not fname.endswith('.html'):
        continue
    with open(os.path.join(BREEDS_DIR, fname)) as f:
        if 'Purchase Price' not in f.read():
            remaining += 1
print(f"Still without 'Purchase Price': {remaining}")
