import os

CSS_BLOCK = """
.native-banner{display:flex;flex-wrap:wrap;align-items:center;gap:20px;background:var(--paper);border:2.5px solid var(--ink);border-radius:var(--radius-lg);padding:20px 24px;margin:32px 0;box-shadow:4px 4px 0 var(--ink);transition:transform .15s,box-shadow .15s;text-decoration:none;color:var(--ink)}
.native-banner:hover{transform:translateY(-2px);box-shadow:6px 6px 0 var(--ink);text-decoration:none}
.nb-icon{font-size:2rem;display:flex;align-items:center;justify-content:center;width:56px;height:56px;background:var(--cream-2);border-radius:50%;flex-shrink:0}
.nb-info{flex:1;min-width:260px}
.nb-title{font-family:var(--display);font-weight:800;font-size:1.1rem;margin-bottom:4px;color:var(--ink)}
.nb-desc{font-size:.92rem;color:var(--ink-soft);line-height:1.4}
.nb-cta{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;background:var(--ink);color:var(--cream);border-radius:var(--radius-pill);font-weight:700;font-size:.9rem;white-space:nowrap;transition:background .15s}
.native-banner:hover .nb-cta{background:var(--coral);color:var(--cream)}
"""

BANNERS = {
    "odie": """<a href="https://www.awin1.com/awclick.php?mid=68990&amp;id=2900805&amp;ued=https%3A%2F%2Fgetodie.com%2F" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--lav-soft)">🛡️</div>
  <div class="nb-info">
    <div class="nb-title">Protect Your Pet &amp; Save on Vet Bills</div>
    <div class="nb-desc">Get customizable pet insurance from Odie. Covers up to 90% of emergency treatments, illnesses, and accidents. Free 24/7 vet chat included.</div>
  </div>
  <div class="nb-cta">Get Free Quote &rarr;</div>
</a>""",
    "chidog": """<a href="https://www.awin1.com/awclick.php?mid=124742&amp;id=2900805&amp;ued=https%3A%2F%2Fchidog.com%2F" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--mint-soft)">🍖</div>
  <div class="nb-info">
    <div class="nb-title">Vet-Owned Fresh Dog Food Delivery</div>
    <div class="nb-desc">Customized human-grade fresh diets designed by holistic veterinarians based on Eastern medicine. Formulated to heal allergies and improve digestion.</div>
  </div>
  <div class="nb-cta">Get Chi Dog &rarr;</div>
</a>""",
    "tuft": """<a href="https://www.awin1.com/awclick.php?mid=59149&amp;id=2900805&amp;ued=https%3A%2F%2Fwww.tuftandpaw.com%2Fproducts%2Freally-great-cat-litter" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--pink-soft)">🌿</div>
  <div class="nb-info">
    <div class="nb-title">Flushable Low-Tracking Litter for Cats</div>
    <div class="nb-desc">Tuft &amp; Paw Really Great Cat Litter is dust-free, fully flushable, and doesn't stick to long fur. 100% natural, odor-destroying tofu pellets.</div>
  </div>
  <div class="nb-cta">Shop Tuft &amp; Paw &rarr;</div>
</a>""",
    "meowant": """<a href="https://www.awin1.com/awclick.php?mid=55213&amp;id=2900805&amp;ued=https%3A%2F%2Fmeowant.com%2Fcollections%2Fself-cleaning-litter-box" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--lav-soft)">🤖</div>
  <div class="nb-info">
    <div class="nb-title">Upgrade to MeoWant Smart Litter Box</div>
    <div class="nb-desc">The MeoWant automatic self-cleaning litter box tracks your cat's weight and health visits automatically. Clean, safe, and odorless. Holds up to 6 cats.</div>
  </div>
  <div class="nb-cta">Shop MeoWant &rarr;</div>
</a>""",
    "petcube": """<a href="https://www.awin1.com/awclick.php?mid=33889&amp;id=2900805&amp;ued=https%3A%2F%2Fpetcube.com%2F" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--pink-soft)">📷</div>
  <div class="nb-info">
    <div class="nb-title">Stay Connected with Your Pet</div>
    <div class="nb-desc">Treat-tossing smart camera for dogs and cats. See, talk, and play with your pet from anywhere. Features 1080p HD video and 24/7 vet access.</div>
  </div>
  <div class="nb-cta">Shop Petcube &rarr;</div>
</a>"""
}

MODIFICATIONS = [
    {
        "file": "blog/pet-insurance-worth-it.html",
        "css_target": "</style>",
        "banner_target": "<h2>When Insurance Wins</h2>",
        "banner_html": BANNERS["odie"]
    },
    {
        "file": "blog/self-cleaning-litter-box-cost.html",
        "css_target": "</style>",
        "banner_target": "<h2>Why MeoWant?</h2>",
        "banner_html": BANNERS["meowant"]
    },
    {
        "file": "blog/self-cleaning-litter-box-cost.html",
        "css_target": None, # Already added in previous file check
        "banner_target": "<h2>Bottom Line</h2>",
        "banner_html": BANNERS["tuft"]
    },
    {
        "file": "blog/dog-vet-visit-costs.html",
        "css_target": "</style>",
        "banner_target": "<h2>How Pet Insurance Changes the Math</h2>",
        "banner_html": BANNERS["odie"]
    },
    {
        "file": "blog/kibble-vs-fresh-vs-raw.html",
        "css_target": "</style>",
        "banner_target": "<h2>Fresh Food: $2,800&ndash;$2,850/year</h2>",
        "banner_html": BANNERS["chidog"]
    },
    {
        "file": "blog/dog-food-recalls-2026.html",
        "css_target": "</style>",
        "banner_target": "<h2>Safer Alternatives With Clean Track Records</h2>",
        "banner_html": BANNERS["chidog"]
    },
    {
        "file": "blog/dog-food-recalls-2026.html",
        "css_target": None,
        "banner_target": "<h2>Pet Insurance: The Safety Net Your Dog Needs</h2>",
        "banner_html": BANNERS["odie"]
    },
    {
        "file": "blog/new-puppy-first-year-cost.html",
        "css_target": "</style>",
        "banner_target": "<h2>6. Pet Insurance: $200&ndash;$500</h2>",
        "banner_html": BANNERS["odie"]
    },
    {
        "file": "blog/new-puppy-first-year-cost.html",
        "css_target": None,
        "banner_target": "<h2>How to Trim Costs Without Cutting Corners</h2>",
        "banner_html": BANNERS["petcube"]
    },
    {
        "file": "blog/cheapest-dog-breeds-to-own.html",
        "css_target": "</style>",
        "banner_target": "<h2>3 Ways to Lower Your Costs Even Further</h2>",
        "banner_html": BANNERS["odie"]
    }
]

# Run modifications
base_dir = "/Users/aleksejs/Desktop/dog-cost-tool"
modified_files = set()

for mod in MODIFICATIONS:
    file_path = os.path.join(base_dir, mod["file"])
    print(f"Modifying {mod['file']}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Add CSS styles if needed and not already added to this file
    if mod["css_target"] and file_path not in modified_files:
        if CSS_BLOCK.strip() not in content:
            target = mod["css_target"]
            replacement = CSS_BLOCK + target
            content = content.replace(target, replacement, 1)
            modified_files.add(file_path)
            print(f"  Added CSS block to {mod['file']}")
            
    # 2. Add Banner HTML if not already present
    banner_html = mod["banner_html"]
    # Check simple anchor part to prevent duplicate injections
    anchor_part = banner_html.split("class=\"native-banner\"")[0]
    if anchor_part not in content:
        target = mod["banner_target"]
        replacement = banner_html + "\n\n      " + target
        content = content.replace(target, replacement, 1)
        print(f"  Injected banner before {mod['banner_target']}")
    else:
        print(f"  Banner already present before {mod['banner_target']}")
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("All blog articles modified successfully!")
