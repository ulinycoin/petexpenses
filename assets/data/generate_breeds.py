#!/usr/bin/env python3
"""Generate breed pages for petexpenses.com — dogs AND cats.

Usage:
  python3 generate_breeds.py                     # All dogs
  python3 generate_breeds.py --cats              # All cats
  python3 generate_breeds.py --all               # Dogs + cats
  python3 generate_breeds.py --breed "Maine Coon"  # Single breed
"""

import os, sys, re, urllib.parse
from breeds_data import DOG_BREEDS, CAT_BREEDS, BREED_HOOKS, BREED_SAVINGS

# ─── COST TABLES (synced with index.html PET_DATA) ───────

DOG_COSTS = {
    'food': {'small': [360,600], 'medium': [600,1000], 'large': [900,1500], 'giant': [1200,2000]},
    'vet': {'small': [200,500], 'medium': [300,700], 'large': [400,1000], 'giant': [500,1200]},
    'insurance': {'small': [240,480], 'medium': [360,720], 'large': [480,960], 'giant': [600,1200]},
    'grooming': {
        'short': {'small': [100,200], 'medium': [150,300], 'large': [200,400], 'giant': [250,500]},
        'long': {'small': [200,400], 'medium': [300,500], 'large': [400,800], 'giant': [500,1000]},
        'wire': {'small': [180,350], 'medium': [250,450], 'large': [350,700], 'giant': [450,900]},
    },
    'supplies': {'small': [150,300], 'medium': [200,400], 'large': [250,500], 'giant': [300,600]},
}

# ─── CATS ────────────────────────────────────────────────

CAT_COSTS = {
    'food': {'small': [240,420], 'medium': [300,600], 'large': [420,720]},
    'vet': {'small': [180,400], 'medium': [220,500], 'large': [300,650]},
    'insurance': {'small': [180,360], 'medium': [240,480], 'large': [300,540]},
    'grooming': {
        'short': {'small': [40,120], 'medium': [60,150], 'large': [80,180]},
        'long': {'small': [120,300], 'medium': [180,400], 'large': [240,500]},
    },
    'supplies': {'small': [120,240], 'medium': [150,300], 'large': [200,380]},
}

CAT_PRIORITY = sorted(CAT_BREEDS.keys())
DOG_PRIORITY = sorted(DOG_BREEDS.keys())

# ══════════════════════════════════════════════════════════

def _variant_index(name, n):
    return sum(ord(c) for c in name) % n

def get_intro_hook(name, bp, species, sd, health_note, cl, ch):
    if name in BREED_HOOKS:
        return BREED_HOOKS[name]
    species_word = 'cat' if species == 'cat' else 'dog'
    templates = [
        f'Before you fall for a {name} puppy photo, run the annual math. Most owners underestimate {species_word} costs by 30–40% in the first year alone.',
        f'{bp} sit in the {sd} category for {species_word} ownership costs. Health profile ({health_note.lower()}) is the variable that swings your budget most.',
        f'Planning a {name} budget? The range ${cl:,}–${ch:,}/year covers a healthy adult in a mid-cost US city — but breed-specific vet issues can push you toward the top of that range fast.',
        f'Unlike generic pet cost guides, this breakdown is tuned to {bp}: size, coat type, and known health risks all change the line items below.',
    ]
    return templates[_variant_index(name, len(templates))]

def get_food_text(name, bp, species_title, species, fl, fh, food_extra, coat):
    young = 'kittens' if species == 'cat' else 'puppies'
    variants = [
        f'Food is usually the biggest recurring line item for {bp}. Budget ${fl:,}–${fh:,}/year for quality {species_title.lower()} food. Sensitive stomachs or grain-free formulas can add {food_extra}.',
        f'Expect ${fl:,}–${fh:,}/year on food alone. {bp} with allergies or weight issues often need prescription diets that sit at the top of this range.',
        f'Annual food for {bp} runs ${fl:,}–${fh:,}. {young.capitalize()} cost more per month; seniors may need joint or kidney support formulas that push food spending {food_extra} above baseline.',
    ]
    if coat == 'long':
        variants.append(f'Nutrition affects coat quality too — {bp} on omega-rich diets may spend ${fl:,}–${fh:,}/year, with premium kibble or fresh food at the higher end.')
    return variants[_variant_index(name, len(variants))]

def get_supplies_text(species, bp, sl, sh):
    if species == 'cat':
        items = [
            f'Annual supplies — litter, litter box, scratching post, carrier, bed, bowls, toys — typically run ${sl:,}–${sh:,}. Litter alone can be $150–$400/year depending on clumping vs. natural formulas.',
            f'Budget ${sl:,}–${sh:,}/year for cat essentials: litter subscriptions, replacement scratchers, and occasional carrier upgrades. First-year setup costs more because you buy the litter box and tree once.',
            f'Cat supplies (${sl:,}–${sh:,}/year) break down to litter (~40%), enrichment toys (~25%), and replaceable items like beds and bowls. Smart litter boxes raise the top end but cut daily chore time.',
        ]
    else:
        items = [
            f'Annual supplies — leash, collar, harness, bed, bowls, crate, toys, waste bags — run ${sl:,}–${sh:,}. Chew-heavy breeds burn through toys faster, pushing costs toward the top of the range.',
            f'Dog gear costs ${sl:,}–${sh:,}/year after the first-year crate-and-collar splurge. Durable harnesses and orthopedic beds last longer but cost more upfront.',
            f'Plan ${sl:,}–${sh:,}/year for supplies. Active {bp.lower()} need replaced toys, grooming tools, and weather gear more often than couch-potato breeds.',
        ]
    return items[_variant_index(bp, len(items))]

def get_savings_html(name, species, species_plural, il, health_note):
    if name in BREED_SAVINGS:
        tips = BREED_SAVINGS[name]
        lines = ['      <ul>']
        for title, body in tips:
            lines.append(f'        <li><strong>{title}.</strong> {body}</li>')
        lines.append('      </ul>')
        return '\n'.join(lines)

    hi = health_note.lower()
    sets = [
        [
            ('Shop pet insurance before age 2', f'Premiums jump after the first birthday. Accident-only plans start around ${il}/year — compare at least three carriers.'),
            ('Batch-buy food on auto-ship', f'Subscribe-and-save cuts {species_plural} food costs 10–15%. Store bulk bags in airtight bins to keep kibble fresh.'),
            ('Don\'t skip the annual wellness exam', 'One $50–$80 checkup catches $2,000 problems early. Vaccine clinics at shelters are cheaper than emergency rooms.'),
            ('Brush teeth at home', f'Dental cleanings under anesthesia cost $300–$800. Daily dental chews or brushing adds years of cheap prevention for most {species_plural}.'),
            ('Buy durable, not cute', 'A $40 chew toy that lasts six months beats four $12 toys destroyed in a week.'),
        ],
        [
            ('Use a pet-specific HSA mindset', 'Set aside $50/month in a dedicated savings account. When the emergency hits, you pay cash instead of credit-card interest.'),
            ('Negotiate vet bills', 'Many clinics offer payment plans or 5–10% discounts for cash pay. Ask before the procedure, not after.'),
            ('Generic preventatives work', 'Ask your vet about generic flea, tick, and heartworm options — same active ingredient, lower price.'),
            ('Groom at home between pro visits', f'YouTube tutorials plus a $30 tool kit can halve grooming spend for {species_plural} that need regular coat care.'),
            ('Price-check prescriptions online', 'Vet markup on medications runs 100–200%. Chewy, Costco, and 1800PetMeds often beat in-clinic pricing.'),
        ],
        [
            ('Adopt from a rescue with known history', 'Shelter dogs and cats often come vaccinated, spayed, and microchipped — saving $500–$1,200 in first-year costs.'),
            ('Weight management is free medicine', f'Obesity adds $500+/year in joint, diabetes, and heart costs. Measuring food portions costs nothing.'),
            ('Community clinics for basics', 'Low-cost vaccine and microchip events run in most US cities every month. Check your local humane society calendar.'),
            ('Pet insurance only if the math works', f'For healthy {species_plural}, a dedicated savings fund may beat insurance. For breeds prone to {hi}, insurance often pays off by year three.'),
            ('Buy once, cry once on gear', 'A steel crate, ceramic bowls, and a washable bed outlast five rounds of cheap replacements.'),
        ],
        [
            ('Track spending for 90 days', 'Most owners guess wrong on where money goes. Log every vet, food, and supply purchase — food is usually 30% higher than expected.'),
            ('Seasonal sales on food and litter', 'Black Friday and Amazon Prime Day drop premium pet food 20–30%. Stock up with a six-month supply if you have storage space.'),
            ('Learn basic first aid', f'A pet first-aid course ($40–$80) helps you decide what needs an ER visit vs. a wait-and-see call — saving hundreds in unnecessary trips.'),
            ('Spay/neuter early', 'Unplanned litter costs dwarf the one-time surgery fee. Many shelters offer $50–$150 spay/neuter vouchers.'),
            ('Share pet-sitting instead of boarding', f'Boarding runs $30–$60/night. A trusted neighbor swap costs a thank-you bottle of wine.'),
        ],
        [
            ('Choose your vet by transparency', 'Clinics that publish price lists upfront tend to cost less than "boutique" vets with hidden fees.'),
            ('DIY enrichment beats store-bought', f'Cardboard boxes, frozen Kongs, and sniff walks cost $0 but cut destructive behavior that leads to replacement furniture.'),
            ('Review insurance annually', 'Premiums creep up 10–15%/year. Switching carriers at renewal can save $200+ without losing coverage.'),
            ('Prevent breed-specific problems early', f'For {name}, addressing {hi} in the first year costs a fraction of treating it in an emergency.'),
            ('Tax deductions for working animals', 'Service and farm dogs may qualify for business expense deductions. Ask your accountant if your situation applies.'),
        ],
    ]
    tips = sets[_variant_index(name, len(sets))]
    lines = ['      <ul>']
    for title, body in tips:
        lines.append(f'        <li><strong>{title}.</strong> {body}</li>')
    lines.append('      </ul>')
    return '\n'.join(lines)

def get_first_year_items(species, name):
    if species == 'cat':
        sets = [
            ['Initial vet exam, FVRCP vaccines, and microchip', 'Spay/neuter surgery ($150–$500)', 'Litter box, carrier, scratching post, bed, bowls, starter litter'],
            ['Kitten wellness package at a local clinic', 'FeLV/FIV test and deworming', 'Tall scratching tree, enclosed litter box, food/water fountains'],
            ['First-year vaccinations and rabies shot', 'Neuter/spay plus post-op cone and meds', 'Carrier for vet trips, window perch, interactive toys'],
        ]
    else:
        sets = [
            ['Puppy wellness exam, DHPP vaccines, and microchip', 'Spay/neuter surgery ($200–$600)', 'Crate, bed, leash, harness, bowls, chew toys, training treats'],
            ['Initial vet package plus flea/tick prevention', 'Spay/neuter and recovery supplies', 'Puppy training classes ($100–$300), crate, gates, enrichment toys'],
            ['Vaccination series and deworming rounds', 'Neuter/spay surgery and cone', 'Size-appropriate crate, collar, ID tag, bed, starter food supply'],
        ]
    items = sets[_variant_index(name, len(sets))]
    return '\n'.join(f'        <li>{item}</li>' for item in items)

def get_page_title(name, species):
    if species == 'cat' and name in ('Sphynx', 'Maine Coon', 'Siamese', 'British Shorthair', 'Persian', 'Ragdoll', 'Bengal'):
        return f'How Much Does a {name} Cat Cost? (2026 Annual Guide)'
    if species == 'dog' and name in ('Bulldog', 'Siberian Husky', 'Rottweiler', 'Dachshund', 'Pomeranian', 'Boxer', 'French Bulldog', 'Golden Retriever', 'Labrador Retriever', 'German Shepherd', 'Chihuahua', 'Beagle', 'Boston Terrier'):
        return f'How Much Does a {name} Cost? (2026 Annual Guide)'
    return f'{name} Annual Cost (2026) — petexpenses.com'

def get_page_h1(name, species, article):
    if species == 'cat' and name in ('Sphynx', 'Maine Coon', 'Siamese', 'British Shorthair'):
        return f'How Much Does a {name} Cat Cost?'
    if species == 'dog' and name in ('Bulldog', 'Siberian Husky', 'Rottweiler', 'Dachshund', 'Pomeranian', 'Boxer'):
        return f'How Much Does a {name} Cost?'
    return f'How Much Does {article} {name} Cost Per Year?'

def make_slug(name):
    slug = name.lower()
    slug = slug.replace(' (pembroke)', '-pembroke')
    slug = slug.replace("'", '')
    slug = slug.replace(' & ', '-and-')
    slug = re.sub(r'[^a-z0-9-]', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug + '-cost'

def get_similar_breeds(breed_name, breed_data, breed_dict, count=5):
    size = breed_data[0]
    similar = []
    for name, data in breed_dict.items():
        if name == breed_name: continue
        if data[0] == size:
            similar.append(name)
        if len(similar) >= count: break
    return similar

def get_offers_html(species, size, coat, breed_name, breed_plural, health_issues, ins_low, ins_high):
    bp = breed_plural
    hi_lc = health_issues.lower()
    is_healthy = any(word in hi_lc for word in ['healthy', 'hardy', 'classic', 'none'])
    
    insurance_p = f"Although {bp} are generally healthy, unexpected accidents or illnesses can still happen. Odie covers up to 90% of your vet bills for accidents, illnesses, and emergency treatments." if is_healthy else f"{bp} are prone to {hi_lc}, which can lead to expensive emergency treatments. Odie covers up to 90% of your vet bills for accidents, illnesses, and breed-specific conditions."

    # 1. Odie Pet Insurance (для всех)
    odie_html = f'''<section class="offers-section">
  <h2>Protect Your {breed_name} with Pet Insurance</h2>
  <div class="article-body">
    <div class="highlight-card hc-lav" style="border-color:var(--lav-dk);box-shadow:4px 4px 0 var(--lav-dk)">
      <div class="hc-label">Odie Pet Insurance</div>
      <p><strong>Customizable pet insurance plans.</strong> {insurance_p}</p>
      <p>Customizable limits &bull; 24/7 vet access &bull; Premium estimate: ${ins_low}–${ins_high}/year</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=68990&amp;id=2900805&amp;ued=https%3A%2F%2Fgetodie.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--lav-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Get Odie Quote &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 2. Dutch Vet Telehealth (для слабых здоровьем пород)
    dutch_html = f'''<section class="offers-section">
  <h2>24/7 Veterinary Support for Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-pink" style="border-color:var(--pink-dk);box-shadow:4px 4px 0 var(--pink-dk)">
      <div class="hc-label">Dutch Vet Telehealth</div>
      <p><strong>Unlimited online vet visits &amp; prescription delivery.</strong> {bp} frequently experience health issues like {hi_lc}. With Dutch, you get round-the-clock access to licensed vets from the comfort of your home, saving you stressful and costly clinic trips.</p>
      <p>24/7 chat &amp; video &bull; Custom treatment plans &bull; Direct prescription delivery</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=78166&amp;id=2900805&amp;ued=https%3A%2F%2Fdutch.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--pink-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Consult a Vet Online &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 3. PrettyLitter (кошачий наполнитель с индикацией здоровья)
    prettylitter_html = f'''<section class="offers-section">
  <h2>Monitor Your {breed_name}&rsquo;s Health with Smart Litter</h2>
  <div class="article-body">
    <div class="highlight-card hc-mint" style="border-color:var(--mint-dk);box-shadow:4px 4px 0 var(--mint-dk)">
      <div class="hc-label">PrettyLitter Health-Monitoring Litter</div>
      <p><strong>Color-changing silica litter that detects illnesses early.</strong> {bp} have a known risk for urinary tract infections (UTIs) or kidney issues. PrettyLitter changes color based on urine pH, helping you catch potential health problems before they become emergency vet bills.</p>
      <p>Odor control &bull; Low dust &bull; Color-changing health indicator</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=126553&amp;id=2900805&amp;ued=https%3A%2F%2Fprettylitter.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--mint-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop PrettyLitter &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 4. Tuft & Paw Tofu Litter (для кошек)
    tuft_html = f'''<section class="offers-section">
  <h2>Try Low-Tracking Litter for Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-coral" style="border-color:var(--coral);box-shadow:4px 4px 0 var(--coral)">
      <div class="hc-label">Tuft &amp; Paw Tofu Litter</div>
      <p><strong>Really Great Cat Litter &mdash; ultra low-tracking and 100% flushable.</strong> Natural tofu pellets do not stick to your {breed_name}&rsquo;s {coat}-haired coat or paw pads, keeping your floors clean. Dust-free and biodegradable.</p>
      <p>4.4 stars from 11,000+ reviews &bull; 50% off first subscription box</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=59149&amp;id=2900805&amp;ued=https%3A%2F%2Fwww.tuftandpaw.com%2Fproducts%2Freally-great-cat-litter" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--coral);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Tuft &amp; Paw &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 5. MeoWant Self-Cleaning Litter Box (для кошек)
    meowant_html = f'''<section class="offers-section">
  <h2>Upgrade Your {breed_name} to a Smart Litter Box</h2>
  <div class="article-body">
    <div class="highlight-card hc-lav" style="border-color:var(--lav-dk);box-shadow:4px 4px 0 var(--lav-dk)">
      <div class="hc-label">MeoWant Self-Cleaning Litter Box</div>
      <p><strong>App-controlled automatic cleaning litter box.</strong> Great for {bp}, this automatic box tracks your cat&rsquo;s weight and toilet visits to monitor health. Safe, odor-destroying, and holds up to 6 cats.</p>
      <p>4.2 stars from 4,000+ reviews &bull; 30-day risk-free trial</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=55213&amp;id=2900805&amp;ued=https%3A%2F%2Fmeowant.com%2Fcollections%2Fself-cleaning-litter-box" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--lav-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop MeoWant &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 6. Hide & Scratch Cardboard Scratcher (для кошек)
    scratch_html = f'''<section class="offers-section">
  <h2>Protect Your Furniture with a Premium Scratcher</h2>
  <div class="article-body">
    <div class="highlight-card hc-pink" style="border-color:var(--pink-dk);box-shadow:4px 4px 0 var(--pink-dk)">
      <div class="hc-label">Hide &amp; Scratch Toy</div>
      <p><strong>Stylish, enclosed cardboard scratcher that cats love.</strong> Keep your active {breed_name} entertained and save your sofas from scratches. Combining a cozy hideout with a durable scratching surface.</p>
      <p>Amazon #1 best seller &bull; Eco-friendly cardboard &bull; Reversible pads</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=105745&amp;id=2900805&amp;ued=https%3A%2F%2Fhideandscratch.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--pink-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Scratcher &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 7. PetPlate Fresh Dog Food (для собак с аллергией / пищевыми проблемами)
    petplate_html = f'''<section class="offers-section">
  <h2>Fresh Vet-Formulated Meals for Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-coral" style="border-color:var(--coral);box-shadow:4px 4px 0 var(--coral)">
      <div class="hc-label">PetPlate Fresh Dog Food</div>
      <p><strong>Personalized fresh meal plans designed by veterinary nutritionists.</strong> Ideal for {bp} dealing with allergies, skin flare-ups, or sensitive stomachs. Made with human-grade ingredients and cooked fresh.</p>
      <p>Aids digestion &bull; Improves coat shine &bull; 50% off your first box</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=70899&amp;id=2900805&amp;ued=https%3A%2F%2Fpetplate.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--coral);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Order Fresh Meals &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 8. Badlands Ranch (для мелких собак)
    badlands_html = f'''<section class="offers-section">
  <h2>Premium Superfood Complete for Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-mint" style="border-color:var(--mint-dk);box-shadow:4px 4px 0 var(--mint-dk)">
      <div class="hc-label">Badlands Ranch Dog Food</div>
      <p><strong>Premium air-dried dog food packed with superfoods.</strong> Created by Katherine Heigl. Because {bp} eat smaller portions, feed them the highest quality nutrient-dense raw diet without the freezer mess.</p>
      <p>100% human-grade meats &bull; No artificial preservatives &bull; Up to 35% off subscriptions</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=75220&amp;id=2900805&amp;ued=https%3A%2F%2Fbadlandsranch.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--mint-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Badlands Ranch &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 9. Raw Paws (для крупных собак / сыроедение в объемах)
    raw_paws_html = f'''<section class="offers-section">
  <h2>Save on Your {breed_name}&rsquo;s Food</h2>
  <div class="article-body">
    <div class="highlight-card hc-mint" style="border-color:var(--mint-dk);box-shadow:4px 4px 0 var(--mint-dk)">
      <div class="hc-label">Raw Paws Pet Food</div>
      <p><strong>Frozen raw dog food, made fresh and shipped bulk.</strong> {bp} on raw diets often experience better digestion, cleaner teeth, and healthier weight. Free shipping nationwide on bulk orders.</p>
      <p>4.8 stars from 2,000+ reviews &bull; Deep bulk discounts &bull; Auto-ship saving</p>
      <p style="margin-top:12px"><a href="https://www.dpbolvw.net/click-101748061-17234885" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--mint-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Raw Paws &rarr;</a> <a href="https://www.anrdoezrs.net/click-101748061-17234936" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;margin-left:8px;background:var(--ink);color:var(--cream);border-radius:var(--radius-pill);font-weight:600;text-decoration:none">Auto-Ship &amp; Save</a></p>
    </div>
  </div>
</section>'''

    # 10. Fi Smart GPS Collar (для активных собак)
    fi_html = f'''<section class="offers-section">
  <h2>Track Your Active {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-coral" style="border-color:var(--coral);box-shadow:4px 4px 0 var(--coral)">
      <div class="hc-label">Fi Smart GPS Collar</div>
      <p><strong>Real-time GPS tracking + LTE activity monitor.</strong> Prevent escapes and monitor sleep or activity level for your active {breed_name}. Waterproof, rugged, and fits dogs from 5 lbs up.</p>
      <p>4.7 stars from 10,000+ reviews &bull; Long battery life &bull; Escape alerts</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=123222&amp;id=2900805&amp;ued=https%3A%2F%2Ftryfi.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--coral);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Fi Collar &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 11. Petcube Smart Camera (для домашних собак, которых оставляют дома)
    petcube_html = f'''<section class="offers-section">
  <h2>Stay Connected with Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-pink" style="border-color:var(--pink-dk);box-shadow:4px 4px 0 var(--pink-dk)">
      <div class="hc-label">Petcube Smart Camera</div>
      <p><strong>Treat-tossing smart camera for {bp}.</strong> See, talk, and play with your {breed_name} from anywhere. Features 1080p HD video, night vision, and 24/7 access to online vets.</p>
      <p>4.5 stars from 60,000+ reviews &bull; Treat dispenser built-in</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=33889&amp;id=2900805&amp;ued=https%3A%2F%2Fpetcube.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--pink-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Petcube &rarr;</a></p>
    </div>
  </div>
</section>'''

    # 12. Chi Dog US (для собак, свежий корм по рецептам ветеринаров - Joined)
    chidog_html = f'''<section class="offers-section">
  <h2>Vet-Owned Fresh Food for Your {breed_name}</h2>
  <div class="article-body">
    <div class="highlight-card hc-mint" style="border-color:var(--mint-dk);box-shadow:4px 4px 0 var(--mint-dk)">
      <div class="hc-label">Chi Dog Food</div>
      <p><strong>Fresh, customized meals created by holistic veterinarians.</strong> Chi Dog diets are based on Eastern medicine theory to help {bp} overcome allergies, digestive issues, and maintain a healthy weight. Human-grade ingredients, cooked fresh.</p>
      <p>Recommended by vets &bull; Custom diet plans &bull; Free consultation online</p>
      <p style="margin-top:12px"><a href="https://www.awin1.com/awclick.php?mid=124742&amp;id=2900805&amp;ued=https%3A%2F%2Fchidog.com%2F" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--mint-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Get Chi Dog Diet &rarr;</a></p>
    </div>
  </div>
</section>'''

    selected_offers = []
    
    # ------------------ CATS ------------------
    if species == 'cat':
        # Оффер 1: Всегда страховка Odie (Joined)
        selected_offers.append(odie_html)
        
        # Оффер 2: Наполнитель Tuft & Paw (Joined)
        selected_offers.append(tuft_html)
        # Note: Вернуть PrettyLitter (126553) когда одобрят:
        # if any(w in hi_lc for w in ['kidney', 'renal', 'uti', 'urinary']):
        #     selected_offers.append(prettylitter_html)
        # else:
        #     selected_offers.append(tuft_html)
            
        # Оффер 3: MeoWant Smart Litter Box (Joined) ИЛИ Petcube Camera (Joined)
        if size == 'large' or any(w in hi_lc for w in ['diabetes', 'weight', 'hcm', 'heart']) or breed_name in ['Bengal', 'Sphynx', 'Persian', 'Scottish Fold']:
            selected_offers.append(meowant_html)
        else:
            selected_offers.append(petcube_html) # Petcube вместо Hide & Scratch (Not Joined)

    # ------------------ DOGS ------------------
    else:
        # Оффер 1: Страховка Odie (Joined)
        selected_offers.append(odie_html)
        
        # Оффер 2: Корм (Chi Dog [Joined] / Raw Paws [Active CJ])
        if any(w in hi_lc for w in ['allergy', 'allergies', 'stomach', 'digestive', 'pancreatitis', 'skin']):
            selected_offers.append(chidog_html) # Chi Dog вместо PetPlate (Not Joined)
        elif size == 'small':
            selected_offers.append(chidog_html) # Chi Dog вместо Badlands Ranch (Not Joined)
        else:
            selected_offers.append(raw_paws_html) # Raw Paws (Active CJ)
            
        # Оффер 3: Гаджет / Забота (Petcube [Joined] - временно заменяет Dutch и Fi Collar)
        selected_offers.append(petcube_html)
        # Note: Вернуть Dutch / Fi Collar когда одобрят:
        # if breed_name in ['French Bulldog', 'Pug', 'Bulldog', 'Boston Terrier', 'Yorkshire Terrier', 'Cavalier King Charles Spaniel', 'Cavapoo']:
        #     selected_offers.append(dutch_html)
        # elif size in ['large', 'giant'] or breed_name in ['Siberian Husky', 'Border Collie', 'Australian Shepherd', 'Shiba Inu', 'Beagle', 'Jack Russell Terrier', 'Vizsla']:
        #     selected_offers.append(fi_html)
        # else:
        #     selected_offers.append(petcube_html)
            
    return '\n\n'.join(selected_offers)

def build_args(name, data, species):
    """species = 'dog' or 'cat'"""
    size = data[0]
    coat = data[1]
    multi = data[2]
    health_note = data[6]
    slug = make_slug(name)

    costs = DOG_COSTS if species == 'dog' else CAT_COSTS
    breed_dict = DOG_BREEDS if species == 'dog' else CAT_BREEDS

    sizes = {'dog': ['small','medium','large','giant'], 'cat': ['small','medium','large']}

    food = costs['food'][size]
    vet = costs['vet'][size]
    ins = costs['insurance'][size]
    groom = costs['grooming'][coat][size]
    supp = costs['supplies'][size]

    cl = int((food[0] + vet[0] + ins[0] + groom[0] + supp[0]) * multi)
    ch = int((food[1] + vet[1] + ins[1] + groom[1] + supp[1]) * multi)
    fl = int(food[0] * multi); fh = int(food[1] * multi)
    vl = int(vet[0] * multi); vh = int(vet[1] * multi)
    il = int(ins[0] * multi); ih = int(ins[1] * multi)
    gl = int(groom[0] * multi); gh = int(groom[1] * multi)
    sl = int(supp[0]); sh = int(supp[1])
    ml = cl // 12; mh = ch // 12

    def pct(a, b):
        return round(((a + b) / (cl + ch)) * 100) if (cl + ch) else 0

    sd_map = {'small': 'small', 'medium': 'medium-sized', 'large': 'large', 'giant': 'giant'}
    sd = sd_map[size]
    cd_map = {'short': 'short-haired', 'long': 'long-haired', 'wire': 'wire-haired'}
    cd = cd_map[coat]

    # Plural
    if name.endswith('s') or name.endswith('x') or name.endswith('sh') or name.endswith('ch'):
        bp = name + 'es'
    else:
        bp = name + 's'

    dw_map = {'dog': {'small': 12, 'medium': 35, 'large': 65, 'giant': 110},
              'cat': {'small': 6, 'medium': 11, 'large': 18}}
    dw = dw_map[species][size]
    art = 'an' if name.lower()[0] in 'aeiou' else 'a'

    health_issues = health_note.split(';')[0].strip() if ';' in health_note else health_note.split(',')[0].strip()
    hi_lc = health_issues.lower()

    # Species title
    species_title = 'Cat' if species == 'cat' else 'Dog'
    species_plural_lc = 'cats' if species == 'cat' else 'dogs'

    # Health extended & insurance/FAQ sentences
    is_healthy_breed = any(word in hi_lc for word in ['healthy', 'hardy', 'classic', 'none', 'very healthy'])
    
    if 'hcm' in hi_lc or 'heart' in hi_lc:
        he = f'{bp} are prone to hypertrophic cardiomyopathy (HCM), a serious heart condition that requires regular veterinary monitoring and can significantly increase healthcare costs.'
    elif 'brachycephalic' in hi_lc:
        he = f'{bp} are brachycephalic (flat-faced), which means they are prone to breathing difficulties, eye problems, and may need specialized veterinary care.'
    elif 'kidney' in hi_lc or 'renal' in hi_lc:
        he = f'{bp} have a higher risk of kidney issues, which require specialized diets and regular check-ups to manage effectively.'
    elif 'dental' in hi_lc:
        he = f'{bp} are prone to dental issues, which may require professional cleanings and at-home dental care to prevent more serious health problems.'
    elif 'skin' in hi_lc:
        he = f'{bp} require special skin care due to their unique coat or skin type, which can add to annual grooming and vet costs.'
    elif 'diabetes' in hi_lc:
        he = f'{bp} have a higher risk of developing diabetes, which requires ongoing medication, special diets, and regular veterinary monitoring.'
    elif 'spine' in hi_lc or 'joint' in hi_lc or 'hip' in hi_lc or 'ivdd' in hi_lc or 'back' in hi_lc:
        he = f'{bp} are prone to joint and spinal issues, which may require ongoing supplements, medications, or even surgical intervention.'
    elif 'lifetime' in hi_lc or 'vet cost' in hi_lc:
        he = f'{bp} are known for {hi_lc.lower()}, with emergency and specialist visits stacking up faster than most breeds.'
    elif is_healthy_breed:
        he = f'{bp} are generally healthy, hardy, and have low risks of major breed-specific genetic diseases.'
    else:
        he = f'{bp} are generally healthy but can be prone to {hi_lc}.'

    art_capital = art.capitalize()
    if is_healthy_breed:
        ins_reason_json = f"Yes — although {bp} are generally healthy, unexpected emergency surgeries can cost $2,000–$5,000. Pet insurance typically costs ${il}–${ih}/year and can cover 70-90% of eligible costs."
        ins_reason_html = f"Pet insurance for {art} {name} costs ${il}–${ih} per year. Although {bp} are generally healthy, unexpected accidents or illnesses can still happen. Insurance is worth considering since an emergency visit can cost $2,000 to $5,000 — far more than a year's premiums."
        faq_health_text = f"{bp} are generally healthy and hardy, with relatively low risk of genetic conditions. However, like all pets, they still require routine vaccinations, dental care, and preventative vet visits."
    else:
        ins_reason_json = f"Yes — {bp} are prone to {hi_lc}, which can lead to expensive vet bills. One emergency surgery can cost $2,000–$5,000. Pet insurance typically costs ${il}–${ih}/year and can cover 70-90% of eligible costs."
        ins_reason_html = f"Pet insurance for {art} {name} costs ${il}–${ih} per year. Given the breed's predisposition to {hi_lc}, insurance is worth considering. An emergency visit can cost $2,000 to $5,000 — far more than a year's premiums."
        faq_health_text = f"{bp} are prone to {hi_lc}. These conditions can require ongoing medication, special diets, or surgery — increasing annual veterinary costs beyond the routine care baseline."

    # Grooming text
    if coat == 'long':
        gt = f'{bp} have a gorgeous {cd} coat that needs regular brushing 2-3 times per week and occasional professional grooming. Annual grooming costs: ${gl}–${gh}. Regular grooming prevents matting and hairballs.'
    elif coat == 'wire':
        gt = f'{bp} have a distinctive wiry coat that needs professional grooming. Budget ${gl}–${gh}/year for grooming, plus regular at-home brushing.'
    else:
        gt = f'{bp} have a short, low-maintenance coat. Weekly brushing is plenty. Professional grooming is rarely needed — annual costs are just ${gl}–${gh}, mainly for nail trims.'

    # Cost comparison
    avgs = {'dog': 2800, 'cat': 1450}
    avg = avgs[species]
    diff = ((cl + ch) / 2) - avg
    if diff > 300:
        cc = 'More'; cc_lc = 'more'; cr = f'their {sd} size, breed-specific health needs, and care requirements'
    elif diff < -300:
        cc = 'Less'; cc_lc = 'less'; cr = f'their {sd} size, generally good health, and low-maintenance needs'
    else:
        cc = 'About Average'; cc_lc = 'about average'; cr = f'their {sd} size and moderate health profile'
    comp_heading = f'Why {bp} Cost {cc} Than Average' if cc in ['More', 'Less'] else f'Why {bp} Cost About Average'

    cl_label = 'more' if cc == 'More' else 'less'
    avg_cost_str = f'${avg:,}'
    hf = f'{bp} cost {cl_label} than the average {species_title.lower()} primarily because of their {sd} size and breed-specific health considerations. {he} Additionally, {bp.lower()} have {cd} coats, which affects annual grooming costs.'

    if cc == 'About Average':
        comp_sentence = f'{bp} cost about the same as the average {species_title.lower()}. A typical {species_title.lower()} costs around {avg_cost_str} per year, and {bp.lower()} at ${cl:,}–${ch:,}/year fall right in line due to {cr}.'
    elif cc == 'More':
        comp_sentence = f'{bp} are more expensive than average to own. A typical {species_title.lower()} costs around {avg_cost_str} per year, while {bp.lower()} at ${cl:,}–${ch:,}/year cost more due to {cr}.'
    else:
        comp_sentence = f'{bp} are less expensive than average to own. A typical {species_title.lower()} costs around {avg_cost_str} per year, while {bp.lower()} at ${cl:,}–${ch:,}/year cost less due to {cr}.'

    fye = int((cl + ch) / 2 * 0.4)

    # Similar breeds
    sim = get_similar_breeds(name, data, breed_dict, 4)
    sim_links = ''
    for sib in sim:
        ss = make_slug(sib)
        sim_links += f'<a href="/breeds/{ss}">🐾 {sib}</a>\n    '

    md = f'See the real annual cost of owning a {name} in 2026. Food, vet, insurance, grooming & supplies: ${cl:,}–${ch:,}/year. Free breed-specific calculator.'[:160]

    # Article (H1)
    h1_article = art
    for special in ['australian shepherd']:
        if name.lower() == special:
            h1_article = 'an'

    # Cat-specific: accent color pink, emoji fish
    accent = '#FF8FB1' if species == 'cat' else '#FF5A3C'
    accent_dk = '#E55E89' if species == 'cat' else '#E03812'

    # ------------------ IN-CONTENT BANNERS ------------------
    if species == 'dog':
        if size == 'small' or any(w in hi_lc for w in ['allergy', 'allergies', 'stomach', 'digestive', 'pancreatitis', 'skin']):
            in_content_banner = f'''<a href="https://www.awin1.com/awclick.php?mid=124742&amp;id=2900805&amp;ued=https%3A%2F%2Fchidog.com%2F" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--mint-soft)">🍖</div>
  <div class="nb-info">
    <div class="nb-title">Vet-Owned Fresh Food for {bp}</div>
    <div class="nb-desc">Customized human-grade fresh diets designed by holistic veterinarians. Formulated to improve digestion, heal skin allergies, and manage weight naturally.</div>
  </div>
  <div class="nb-cta">Get Chi Dog &rarr;</div>
</a>'''
        else:
            in_content_banner = f'''<a href="https://www.awin1.com/awclick.php?mid=68990&amp;id=2900805&amp;ued=https%3A%2F%2Fgetodie.com%2F" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--lav-soft)">🛡️</div>
  <div class="nb-info">
    <div class="nb-title">Protect Your {name} &amp; Save on Vet Bills</div>
    <div class="nb-desc">Get customizable pet insurance from Odie. Covers up to 90% of emergency treatments, illnesses, and breed-specific conditions. Free 24/7 vet chat included.</div>
  </div>
  <div class="nb-cta">Get Free Quote &rarr;</div>
</a>'''
    else:
        if coat == 'long':
            in_content_banner = f'''<a href="https://www.awin1.com/awclick.php?mid=59149&amp;id=2900805&amp;ued=https%3A%2F%2Fwww.tuftandpaw.com%2Fproducts%2Freally-great-cat-litter" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--pink-soft)">🌿</div>
  <div class="nb-info">
    <div class="nb-title">Flushable Low-Tracking Litter for {bp}</div>
    <div class="nb-desc">Tuft &amp; Paw Really Great Cat Litter is dust-free, fully flushable, and doesn&rsquo;t stick to long fur. 100% natural, odor-destroying tofu pellets.</div>
  </div>
  <div class="nb-cta">Shop Tuft &amp; Paw &rarr;</div>
</a>'''
        else:
            in_content_banner = f'''<a href="https://www.awin1.com/awclick.php?mid=55213&amp;id=2900805&amp;ued=https%3A%2F%2Fmeowant.com%2Fcollections%2Fself-cleaning-litter-box" target="_blank" rel="noopener" class="native-banner">
  <div class="nb-icon" style="background:var(--lav-soft)">🤖</div>
  <div class="nb-info">
    <div class="nb-title">Upgrade Your {name} to a Smart Litter Box</div>
    <div class="nb-desc">The MeoWant automatic self-cleaning litter box tracks your cat&rsquo;s weight and health visits automatically. Clean, safe, and odorless. Holds up to 6 cats.</div>
  </div>
  <div class="nb-cta">Shop MeoWant &rarr;</div>
</a>'''

    offers_html = get_offers_html(species, size, coat, name, bp, health_issues, il, ih)

    food_extra = '$200–$400' if multi > 1.4 else ('$100–$200' if multi > 1.2 else '$0–$100')
    page_title = get_page_title(name, species)
    page_h1 = get_page_h1(name, species, h1_article)
    intro_hook = get_intro_hook(name, bp, species, sd, health_note, cl, ch)
    food_text = get_food_text(name, bp, species_title, species, fl, fh, food_extra, coat)
    supplies_text = get_supplies_text(species, bp, sl, sh)
    savings_html = get_savings_html(name, species, species_plural_lc, il, health_note)
    first_year_items = get_first_year_items(species, name)
    compare_label = 'dogs' if species == 'dog' else 'cats'

    return {
        'IN_CONTENT_BANNER': in_content_banner,
        'OFFERS_HTML': offers_html,
        'SPECIES': species,
        'SPECIES_TITLE': species_title,
        'SPECIES_PLURAL': species_plural_lc,
        'BREED': name,
        'BREED_PLURAL': bp,
        'BREED_PLURAL_LC': bp.lower(),
        'SLUG': slug,
        'META_DESC': md,
        'COST_LOW': f'{cl:,}',
        'COST_HIGH': f'{ch:,}',
        'MONTHLY_LOW': str(ml),
        'MONTHLY_HIGH': str(mh),
        'FOOD_LOW': str(fl), 'FOOD_HIGH': str(fh),
        'FOOD_MONTHLY_LOW': str(fl // 12), 'FOOD_MONTHLY_HIGH': str(fh // 12),
        'FOOD_PCT': str(pct(fl, fh)),
        'VET_LOW': str(vl), 'VET_HIGH': str(vh),
        'VET_MONTHLY_LOW': str(vl // 12), 'VET_MONTHLY_HIGH': str(vh // 12),
        'VET_PCT': str(pct(vl, vh)),
        'INS_LOW': str(il), 'INS_HIGH': str(ih),
        'INS_MONTHLY_LOW': str(il // 12), 'INS_MONTHLY_HIGH': str(ih // 12),
        'INS_PCT': str(pct(il, ih)),
        'GROOM_LOW': str(gl), 'GROOM_HIGH': str(gh),
        'GROOM_MONTHLY_LOW': str(gl // 12), 'GROOM_MONTHLY_HIGH': str(gh // 12),
        'GROOM_PCT': str(pct(gl, gh)),
        'SUPP_LOW': str(sl), 'SUPP_HIGH': str(sh),
        'SUPP_MONTHLY_LOW': str(sl // 12), 'SUPP_MONTHLY_HIGH': str(sh // 12),
        'SUPP_PCT': str(pct(sl, sh)),
        'SIZE_DESC': sd,
        'COAT_DESC': cd,
        'DEFAULT_WEIGHT': str(dw),
        'COAT': coat,
        'HEALTH_NOTE': health_note,
        'HEALTH_ISSUES': health_issues,
        'HEALTH_ISSUES_LC': hi_lc,
        'HEALTH_NOTE_EXTENDED': he,
        'INSURANCE_REASON_JSON': ins_reason_json,
        'INSURANCE_REASON_HTML': ins_reason_html,
        'FAQ_HEALTH_TEXT': faq_health_text,
        'GROOMING_TEXT': gt,
        'COST_COMPARISON': cc,
        'COST_COMPARISON_LC': cc_lc,
        'COMPARISON_REASON': cr,
        'COMPARISON_SENTENCE': comp_sentence,
        'HEALTH_FACTORS_SECTION': hf,
        'FOOD_ALLERGY_EXTRA': '$200–$400' if multi > 1.4 else ('$100–$200' if multi > 1.2 else '$0–$100'),
        'FIRST_YEAR_EXTRA': f'${fye:,}',
        'SIMILAR_LINKS': sim_links,
        'BREED_URL_ENCODED': urllib.parse.quote(name),
        'ARTICLE': h1_article,
        'ACCENT': accent,
        'ACCENT_DK': accent_dk,
        'FOOD_EMOJI': '🐟' if species == 'cat' else '🍖',
        'SPECIES_EMOJI': '🐈' if species == 'cat' else '🐕',
        'AVG_COST': str(avg),
        'COMP_HEADING': comp_heading,
        'PAGE_TITLE': page_title,
        'PAGE_H1': page_h1,
        'INTRO_HOOK': intro_hook,
        'FOOD_TEXT': food_text,
        'SUPPLIES_TEXT': supplies_text,
        'SAVINGS_HTML': savings_html,
        'FIRST_YEAR_ITEMS': first_year_items,
        'COMPARE_LABEL': compare_label,
    }

def fill_template(template, args):
    result = template
    for key, val in args.items():
        result = result.replace(f'!{key}!', str(val))
    return result

# ══════════════════════════════════════════════════════════
# HTML TEMPLATE
# ══════════════════════════════════════════════════════════

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="p:domain_verify" content="dcfb2a50a6d5a6fadb45c1820157944e"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>!PAGE_TITLE!</title>
<meta name="description" content="!META_DESC!">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://petexpenses.com/"},
        {"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://petexpenses.com/compare"},
        {"@type": "ListItem", "position": 3, "name": "!BREED! Cost", "item": "https://petexpenses.com/breeds/!SLUG!"}
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How much does a !BREED! cost per year?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The annual cost of owning a !BREED! ranges from $!COST_LOW! to $!COST_HIGH! per year in 2026, depending on age, weight, diet, and location. This includes food, vet care, pet insurance, grooming, and supplies."
          }
        },
        {
          "@type": "Question",
          "name": "Is !BREED! pet insurance worth it?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "!INSURANCE_REASON_JSON!"
          }
        },
        {
          "@type": "Question",
          "name": "What is the most expensive part of owning a !BREED!?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Food and veterinary care are the largest expenses for !BREED!s. Food costs $!FOOD_LOW!–$!FOOD_HIGH!/year, while vet care ranges from $!VET_LOW!–$!VET_HIGH!/year including routine check-ups and breed-specific health concerns."
          }
        }
      ]
    },
    {
      "@type": "WebPage",
      "name": "!BREED! Annual Cost (2026)",
      "url": "https://petexpenses.com/breeds/!SLUG!",
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [".article-h1", ".highlight-card"]
      }
    },
    {
      "@type": "Dataset",
      "name": "!BREED! Pet Expenses 2026",
      "description": "Annual cost data for owning a !BREED! in the United States, 2026. Includes food, veterinary care, insurance, grooming, and supplies cost ranges by breed, size, age, and activity level.",
      "url": "https://petexpenses.com/breeds/!SLUG!",
      "creator": {"@type": "Organization", "name": "petexpenses.com"},
      "datePublished": "2026-05-01",
      "dateModified": "2026-05-21",
      "temporalCoverage": "2026-01-01/2026-12-31",
      "spatialCoverage": {
        "@type": "Place",
        "name": "United States"
      }
    }
  ]
}
</script>
<meta property="og:title" content="!BREED! Annual Cost (2026) — petexpenses.com">
<meta property="og:description" content="See the real annual cost of owning a !BREED! in 2026. Food, vet, insurance, grooming & supplies breakdown. Free calculator included.">
<meta property="og:image" content="https://petexpenses.com/og-!SPECIES!.jpg">
<meta property="og:url" content="https://petexpenses.com/breeds/!SLUG!">
<meta property="og:type" content="website">
<meta property="og:site_name" content="petexpenses.com">
<meta property="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://petexpenses.com/breeds/!SLUG!">
<link rel="ai-summary" href="https://petexpenses.com/ai-summary.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap"></noscript>
<style>
:root{--ink:#1B1340;--ink-soft:#4A3F6F;--ink-mute:#6B6490;--coral:#FF5A3C;--coral-dk:#E03812;--coral-soft:#FFE3DA;--pink:#FF8FB1;--pink-dk:#E55E89;--pink-soft:#FFE2EC;--sun:#FFD23F;--sun-dk:#C9941E;--sun-soft:#FFF1B8;--mint:#6EE7B7;--mint-dk:#0E9F6E;--mint-soft:#C7F4DD;--lavender:#A78BFA;--lav-dk:#6D49C7;--lav-soft:#E6DCFF;--cream:#FFF7E8;--cream-2:#FBEFD6;--paper:#FFF;--radius-xl:28px;--radius-lg:20px;--radius:14px;--radius-sm:10px;--radius-pill:999px;--shadow-sm:0 1px 0 rgba(27,19,64,.05),0 1px 3px rgba(27,19,64,.06);--shadow:0 2px 0 rgba(27,19,64,.06),0 8px 22px -8px rgba(27,19,64,.18);--shadow-lg:0 4px 0 rgba(27,19,64,.10),0 22px 50px -16px rgba(27,19,64,.30);--display:'Bricolage Grotesque','Geist',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;--body:'Geist',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;--mono:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:var(--body);color:var(--ink);background:var(--cream);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--coral);font-weight:600}a:hover{text-decoration:underline}
.site-nav{display:flex;align-items:center;gap:24px;padding:16px 32px;position:sticky;top:0;z-index:100;background:rgba(255,247,232,.85);backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid rgba(27,19,64,.07)}
.site-brand{display:inline-flex;align-items:center;gap:10px;font-family:var(--display);font-weight:800;font-size:1.15rem;letter-spacing:-.02em;white-space:nowrap;color:var(--ink);text-decoration:none}
.brand-dot{color:var(--coral)}
.site-nav-mid{display:flex;align-items:center;gap:6px;margin:0 auto}
.site-nav-mid a{padding:8px 14px;border-radius:var(--radius-pill);font-size:.92rem;font-weight:500;color:var(--ink-soft);transition:background .15s,color .15s;text-decoration:none}
.site-nav-mid a:hover{background:rgba(27,19,64,.05);color:var(--ink)}
.site-nav-mid a.active{background:var(--ink);color:var(--cream)}
.site-cta{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;background:var(--ink);color:var(--cream);border-radius:var(--radius-pill);font-weight:600;font-size:.92rem;transition:transform .15s,background .15s;white-space:nowrap;text-decoration:none}
.site-cta:hover{background:var(--coral);transform:translateY(-1px)}
@media(max-width:800px){.site-nav-mid{display:none}.site-cta{padding:8px 14px;font-size:.85rem}}
.article-wrap{max-width:780px;margin:0 auto;padding:48px 24px 64px}
.article-header{margin-bottom:40px}
.article-tag{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-mute);background:var(--cream-2);padding:5px 12px;border-radius:6px;margin-bottom:16px}
.article-h1{font-family:var(--display);font-weight:800;font-size:clamp(2.2rem,4.5vw,3.6rem);line-height:1.05;letter-spacing:-.03em;font-variation-settings:"wdth" 92;margin-bottom:12px}
.article-meta{display:flex;align-items:center;gap:16px;font-family:var(--mono);font-size:12px;color:var(--ink-mute);padding-bottom:24px;border-bottom:1.5px dashed rgba(27,19,64,.1)}
.article-body{font-size:1.05rem;color:var(--ink)}
.article-body h2{font-family:var(--display);font-weight:800;font-size:1.6rem;letter-spacing:-.02em;margin:40px 0 16px;line-height:1.15}
.article-body h3{font-family:var(--display);font-weight:700;font-size:1.2rem;margin:28px 0 12px}
.article-body p{margin-bottom:18px}
.article-body ul,.article-body ol{margin:0 0 18px 24px}
.article-body li{margin-bottom:8px}
.article-body blockquote{border-left:4px solid var(--coral);background:var(--coral-soft);padding:16px 20px;margin:24px 0;border-radius:0 var(--radius) var(--radius) 0;font-style:italic}
.article-body .highlight-card{background:var(--paper);border:2.5px solid var(--ink);border-radius:var(--radius-xl);padding:24px 28px;margin:24px 0;box-shadow:4px 4px 0 var(--ink)}
.article-body .highlight-card.hc-coral{border-color:var(--coral);box-shadow:4px 4px 0 var(--coral)}
.article-body .highlight-card.hc-mint{border-color:var(--mint-dk);box-shadow:4px 4px 0 var(--mint-dk)}
.article-body .highlight-card.hc-lav{border-color:var(--lav-dk);box-shadow:4px 4px 0 var(--lav-dk)}
.article-body .highlight-card.hc-pink{border-color:var(--pink);box-shadow:4px 4px 0 var(--pink)}
.hc-label{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-mute);font-weight:700;margin-bottom:8px}
.article-body .highlight-card p:last-child{margin-bottom:0}
.article-body table{width:100%;border-collapse:collapse;margin:24px 0;font-size:.95rem;word-break:break-word}
.article-body th{background:var(--ink);color:var(--cream);padding:10px 14px;text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.article-body td{padding:10px 14px;border-bottom:1px solid rgba(27,19,64,.08)}
.article-body tr:nth-child(even) td{background:var(--cream-2)}
.article-body .footnote{font-size:.85rem;color:var(--ink-mute);margin-top:4px}
.offers-section{max-width:780px;margin:40px auto 0;padding:0 24px}
.offers-section h2{font-family:var(--display);font-weight:800;font-size:1.6rem;letter-spacing:-.02em;margin-bottom:20px;line-height:1.15}
.calc-promo{max-width:780px;margin:40px auto 0;padding:32px 24px;background:var(--paper);border:2.5px solid var(--ink);border-radius:var(--radius-xl);box-shadow:6px 6px 0 var(--ink);text-align:center}
.calc-promo h3{font-family:var(--display);font-weight:800;font-size:1.3rem;margin-bottom:12px}
.calc-promo p{margin-bottom:16px;color:var(--ink-soft)}
.calc-promo a{display:inline-block;padding:12px 28px;background:var(--coral);color:var(--cream);border-radius:var(--radius-pill);font-weight:700;font-size:1.05rem;text-decoration:none;transition:transform .15s;white-space:nowrap}
.calc-promo a:hover{background:var(--coral-dk);transform:translateY(-2px)}
.similar-breeds{max-width:780px;margin:48px auto 0;padding:0 24px}
.similar-breeds h2{font-family:var(--display);font-weight:800;font-size:1.6rem;letter-spacing:-.02em;margin-bottom:20px;line-height:1.15}
.similar-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.similar-grid a{display:flex;align-items:center;gap:8px;padding:14px 18px;background:var(--paper);border:2px solid var(--ink);border-radius:var(--radius);font-weight:600;font-size:.95rem;color:var(--ink);text-decoration:none;transition:transform .15s,box-shadow .15s}
.similar-grid a:hover{transform:translateY(-2px);box-shadow:3px 3px 0 var(--ink)}
.cost-table-wrap{overflow-x:auto;margin:24px 0}
.cost-table{width:100%;border-collapse:collapse;font-size:.95rem}
.cost-table th{background:var(--ink);color:var(--cream);padding:10px 14px;text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;word-break:break-word}
.cost-table td{padding:10px 14px;border-bottom:1px solid rgba(27,19,64,.08);word-break:break-word}
.cost-table tr:nth-child(even) td{background:var(--cream-2)}
.cost-table .total-row td{font-weight:700;background:var(--coral-soft)}
.site-footer{background:var(--ink);color:var(--cream);padding:40px 24px 28px;margin-top:48px}
.footer-inner{max-width:780px;margin:0 auto;display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:rgba(255,247,232,.6)}
.footer-inner a{color:var(--sun);text-decoration:none}
.native-banner{display:flex;flex-wrap:wrap;align-items:center;gap:20px;background:var(--paper);border:2.5px solid var(--ink);border-radius:var(--radius-lg);padding:20px 24px;margin:32px 0;box-shadow:4px 4px 0 var(--ink);transition:transform .15s,box-shadow .15s;text-decoration:none;color:var(--ink)}
.native-banner:hover{transform:translateY(-2px);box-shadow:6px 6px 0 var(--ink);text-decoration:none}
.nb-icon{font-size:2rem;display:flex;align-items:center;justify-content:center;width:56px;height:56px;background:var(--cream-2);border-radius:50%;flex-shrink:0}
.nb-info{flex:1;min-width:260px}
.nb-title{font-family:var(--display);font-weight:800;font-size:1.1rem;margin-bottom:4px;color:var(--ink)}
.nb-desc{font-size:.92rem;color:var(--ink-soft);line-height:1.4}
.nb-cta{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;background:var(--ink);color:var(--cream);border-radius:var(--radius-pill);font-weight:700;font-size:.9rem;white-space:nowrap;transition:background .15s}
.native-banner:hover .nb-cta{background:var(--coral);color:var(--cream)}
</style>
</head>
<body>

<nav class="site-nav">
  <a class="site-brand" href="https://petexpenses.com">
    <svg viewBox="0 0 40 40" width="26" height="26"><circle cx="20" cy="24" r="10" fill="#FF5A3C"/><circle cx="8" cy="14" r="4.5" fill="#FF5A3C"/><circle cx="32" cy="14" r="4.5" fill="#FF5A3C"/><circle cx="14" cy="5" r="3.6" fill="#FF5A3C"/><circle cx="26" cy="5" r="3.6" fill="#FF5A3C"/></svg>
    <span>petexpenses<span class="brand-dot">.</span>com</span>
  </a>
  <div class="site-nav-mid">
    <a href="https://petexpenses.com">Calculator</a>
    <a href="https://petexpenses.com/compare">Compare</a>
    <a href="https://petexpenses.com/blog/">Blog</a>
    <a href="https://petexpenses.com/#faq">FAQ</a>
  </div>
  <a href="https://petexpenses.com" class="site-cta">Run the math &rarr;</a>
</nav>

<div class="article-wrap">
  <article>
    <header class="article-header">
      <span class="article-tag">!BREED!</span>
      <h1 class="article-h1">!PAGE_H1!</h1>
      <div class="article-meta">
        <span>Last updated May 2026</span>
        <span>Data: APPA, AVMA, NAPHIA</span>
        <span>!SPECIES_TITLE! guide</span>
      </div>
    </header>

    <div class="article-disclosure" style="font-family:var(--mono);font-size:11px;color:var(--ink-mute);margin-bottom:24px;padding:10px 14px;background:var(--cream-2);border-radius:var(--radius-sm);line-height:1.4">
      <strong>Affiliate Disclosure:</strong> petexpenses.com is reader-supported. We may earn a small commission from our partners when you click links on our site, at no extra cost to you.
    </div>

    <div class="article-body">

      <div class="highlight-card hc-!SPECIES!">
        <div class="hc-label">Quick Answer</div>
        <p>The average annual cost of owning a !BREED! in the US ranges from <strong>$!COST_LOW! to $!COST_HIGH! per year</strong> ($!MONTHLY_LOW!–$!MONTHLY_HIGH!/month). This includes food, routine vet care, pet insurance, grooming, and supplies. Actual costs depend on your !SPECIES_TITLE!&rsquo;s age, weight, diet, activity level, and location.</p>
      </div>

      <blockquote>!INTRO_HOOK!</blockquote>

      <h2>Annual Cost Breakdown for !BREED_PLURAL!</h2>
      <p>Here&rsquo;s how the average !BREED! owner&rsquo;s annual budget breaks down across five key categories. !BREED_PLURAL! are a <strong>!SIZE_DESC!</strong> !SPECIES_TITLE! breed with a <strong>!COAT_DESC!</strong> coat.</p>

      <div class="cost-table-wrap">
        <table class="cost-table">
          <thead>
            <tr><th>Category</th><th>Annual Range</th><th>Monthly Range</th><th>% of Total</th></tr>
          </thead>
          <tbody>
            <tr><td>!FOOD_EMOJI! Food</td><td>$!FOOD_LOW!–$!FOOD_HIGH!</td><td>$!FOOD_MONTHLY_LOW!–$!FOOD_MONTHLY_HIGH!</td><td>!FOOD_PCT!%</td></tr>
            <tr><td> Vet Care</td><td>$!VET_LOW!–$!VET_HIGH!</td><td>$!VET_MONTHLY_LOW!–$!VET_MONTHLY_HIGH!</td><td>!VET_PCT!%</td></tr>
            <tr><td> Insurance</td><td>$!INS_LOW!–$!INS_HIGH!</td><td>$!INS_MONTHLY_LOW!–$!INS_MONTHLY_HIGH!</td><td>!INS_PCT!%</td></tr>
            <tr><td> Grooming</td><td>$!GROOM_LOW!–$!GROOM_HIGH!</td><td>$!GROOM_MONTHLY_LOW!–$!GROOM_MONTHLY_HIGH!</td><td>!GROOM_PCT!%</td></tr>
            <tr><td> Supplies</td><td>$!SUPP_LOW!–$!SUPP_HIGH!</td><td>$!SUPP_MONTHLY_LOW!–$!SUPP_MONTHLY_HIGH!</td><td>!SUPP_PCT!%</td></tr>
            <tr class="total-row"><td> Total</td><td>$!COST_LOW!–$!COST_HIGH!</td><td>$!MONTHLY_LOW!–$!MONTHLY_HIGH!</td><td>100%</td></tr>
          </tbody>
        </table>
      </div>

      !IN_CONTENT_BANNER!

      <h3>Food</h3>
      <p>!FOOD_TEXT!</p>

      <h3>Veterinary Care</h3>
      <p>Routine veterinary care for !BREED_PLURAL! costs $!VET_LOW!–$!VET_HIGH! per year. This covers annual check-ups, vaccinations, and preventative treatments. !HEALTH_NOTE_EXTENDED! Unexpected emergencies can add thousands in a single visit.</p>

      <h3>Pet Insurance</h3>
      <p>!INSURANCE_REASON_HTML!</p>

      <h3>Grooming</h3>
      <p>!GROOMING_TEXT!</p>

      <h3>Supplies</h3>
      <p>!SUPPLIES_TEXT!</p>

      <h2>!COMP_HEADING!</h2>
      <p>!HEALTH_FACTORS_SECTION!</p>

      <h2>How to Save on !BREED! Ownership</h2>
!SAVINGS_HTML!

      <h2>First-Year vs. Annual Costs</h2>
      <p>Your first year with a !BREED! will be more expensive. Expect to spend an extra !FIRST_YEAR_EXTRA! on:</p>
      <ul>
!FIRST_YEAR_ITEMS!
      </ul>

      <h2>FAQ About !BREED! Costs</h2>

      <details>
        <summary>How much does a !BREED! cost per month?</summary>
        <div class="faq-a">
          <p>Monthly costs for a !BREED! range from <strong>$!MONTHLY_LOW! to $!MONTHLY_HIGH!</strong>. This includes food, vet care, insurance, grooming, and supplies. !SPECIES_TITLE!s and seniors typically cost more than healthy adults.</p>
        </div>
      </details>

      <details>
        <summary>Is a !BREED! expensive to own compared to other !COMPARE_LABEL!?</summary>
        <div class="faq-a">
          <p>!COMPARISON_SENTENCE!</p>
        </div>
      </details>

      <details>
        <summary>What health issues do !BREED_PLURAL! have?</summary>
        <div class="faq-a">
          <p>!FAQ_HEALTH_TEXT!</p>
        </div>
      </details>

    </div>
  </article>
</div>

<div class="calc-promo">
  <h3>Get Your Exact !BREED! Cost</h3>
  <p>Every !SPECIES_TITLE! is different. Use our free calculator to adjust for your !BREED!&rsquo;s age, weight, and activity level.</p>
  <a href="/?breed=!BREED_URL_ENCODED!&weight=!DEFAULT_WEIGHT!&age=adult&coat=!COAT!&species=!SPECIES!">Open !BREED! Calculator</a>
</div>

<section class="similar-breeds">
  <h2>Similar Breeds to Compare</h2>
  <div class="similar-grid">
    !SIMILAR_LINKS!
    <a href="/compare">Compare all breeds</a>
  </div>
</section>

!OFFERS_HTML!

<footer class="site-footer">
  <div class="footer-inner">
    <span>&copy; 2026 <a href="https://petexpenses.com">petexpenses.com</a></span>
    <span>Data: APPA, AVMA, NAPHIA, BLS</span>
    <span><a href="https://petexpenses.com">Back to calculator &rarr;</a></span>
  </div>
</footer>

<script>
window.addEventListener('load',function(){
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=!0}(document,window.posthog||[]);
  posthog.init('phc_6iTpA8vFIxlQ8HxmPsoMmtj4sqgCUWiZQMOpfSfyvxe',{api_host:'https://eu.posthog.com'});
});
</script>
</body>
</html>'''

# ══════════════════════════════════════════════════════════

def generate_page(name, data, species):
    args = build_args(name, data, species)
    slug = args['SLUG']
    filepath = f'/Users/aleksejs/Desktop/dog-cost-tool/breeds/{slug}.html'
    html = fill_template(TEMPLATE, args)
    with open(filepath, 'w') as f:
        f.write(html)
    print(f'  {slug}.html ({len(html)} bytes)')
    return filepath

def generate_sitemap(generated_dogs, generated_cats):
    import datetime
    today = datetime.date.today().strftime('%Y-%m-%d')
    sitemap_path = '/Users/aleksejs/Desktop/dog-cost-tool/sitemap.xml'
    
    # Базовые страницы
    static_urls = [
        ('', '1.0'),
        ('about', '0.6'),
        ('contact', '0.4'),
        ('privacy', '0.3'),
        ('terms', '0.3'),
        ('compare', '0.9'),
        ('sources', '0.85'),
        ('blog/', '0.7')
    ]
    
    # Статьи в блоге (сканируем папку blog)
    blog_dir = '/Users/aleksejs/Desktop/dog-cost-tool/blog'
    blog_urls = []
    if os.path.exists(blog_dir):
        for f in sorted(os.listdir(blog_dir)):
            if f.endswith('.html') and f != 'index.html':
                slug = f[:-5] # убираем .html
                blog_urls.append(f'blog/{slug}')
                
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Пишем статические страницы
    for slug, priority in static_urls:
        xml.append('  <url>')
        xml.append(f'    <loc>https://petexpenses.com/{slug}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
        
    # Пишем блог
    for slug in blog_urls:
        xml.append('  <url>')
        xml.append(f'    <loc>https://petexpenses.com/{slug}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append('    <priority>0.8</priority>')
        xml.append('  </url>')
        
    # Пишем породы собак
    for name in sorted(generated_dogs):
        slug = make_slug(name)
        xml.append(f'  <url><loc>https://petexpenses.com/breeds/{slug}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.75</priority></url>')
        
    # Пишем породы кошек
    for name in sorted(generated_cats):
        slug = make_slug(name)
        xml.append(f'  <url><loc>https://petexpenses.com/breeds/{slug}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.75</priority></url>')
        
    xml.append('</urlset>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print(f'\n[+] Sitemap сгенерирован: {len(xml)-3} URL адресов записано в {sitemap_path}')

def update_compare_links(generated_dogs, generated_cats):
    compare_path = '/Users/aleksejs/Desktop/dog-cost-tool/compare.html'
    if not os.path.exists(compare_path):
        return
        
    with open(compare_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Генерируем HTML ссылок для собак
    dog_links = []
    for name in sorted(generated_dogs):
        slug = make_slug(name)
        dog_links.append(f'    <a href="/breeds/{slug}" style="display:block;padding:10px 14px;background:var(--paper);border:2px solid var(--ink);border-radius:var(--radius);font-weight:600;font-size:.9rem;color:var(--ink);text-decoration:none;transition:transform .12s">{name} Cost</a>')
    
    dog_html = '\n' + '\n'.join(dog_links) + '\n  '
    
    # Генерируем HTML ссылок для кошек
    cat_links = []
    for name in sorted(generated_cats):
        slug = make_slug(name)
        cat_links.append(f'    <a href="/breeds/{slug}" style="display:block;padding:10px 14px;background:var(--paper);border:2px solid var(--ink);border-radius:var(--radius);font-weight:600;font-size:.9rem;color:var(--ink);text-decoration:none;transition:transform .12s">{name} Cost</a>')
        
    cat_html = '\n' + '\n'.join(cat_links) + '\n  '
    
    # Заменяем блоки в compare.html
    dog_pattern = r'(<div style="display:grid;grid-template-columns:repeat\(auto-fill,minmax\(200px,1fr\)\);gap:10px">)(.*?)(</div>)'
    cat_pattern = r'(<div style="display:grid;grid-template-columns:repeat\(auto-fill,minmax\(200px,1fr\)\);gap:10px;margin-top:10px">)(.*?)(</div>)'
    
    content = re.sub(dog_pattern, rf'\1{dog_html}\3', content, flags=re.DOTALL)
    content = re.sub(cat_pattern, rf'\1{cat_html}\3', content, flags=re.DOTALL)
    
    with open(compare_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f'[+] Ссылки на породы в {compare_path} успешно обновлены!')

def main():
    target_breed = None
    do_cats = False
    do_dogs = False
    do_all = False

    for arg in sys.argv[1:]:
        if arg == '--cats':
            do_cats = True
        elif arg == '--dogs':
            do_dogs = True
        elif arg == '--all':
            do_all = True
        elif arg.startswith('--breed='):
            target_breed = arg.split('=', 1)[1]
        elif arg == '--breed':
            # handled below
            pass

    # Handle --breed NAME
    for i, arg in enumerate(sys.argv):
        if arg == '--breed' and i + 1 < len(sys.argv):
            target_breed = sys.argv[i + 1]

    if target_breed:
        if target_breed in DOG_BREEDS:
            data = DOG_BREEDS[target_breed]
            species = 'dog'
        elif target_breed in CAT_BREEDS:
            data = CAT_BREEDS[target_breed]
            species = 'cat'
        else:
            print(f'Breed "{target_breed}" not found')
            sys.exit(1)
        generate_page(target_breed, data, species)
        return

    if do_all:
        do_dogs = True
        do_cats = True
    elif not do_cats and not do_dogs:
        do_dogs = True  # default

    if do_dogs:
        print(f'\nGenerating {len(DOG_PRIORITY)} dog breed pages...')
        for name in DOG_PRIORITY:
            if name in DOG_BREEDS:
                generate_page(name, DOG_BREEDS[name], 'dog')

    if do_cats:
        print(f'\nGenerating {len(CAT_PRIORITY)} cat breed pages...')
        for name in CAT_PRIORITY:
            if name in CAT_BREEDS:
                generate_page(name, CAT_BREEDS[name], 'cat')

    # Генерируем полный sitemap.xml
    generate_sitemap(DOG_BREEDS.keys(), CAT_BREEDS.keys())

    # Обновляем ссылки в compare.html
    update_compare_links(DOG_BREEDS.keys(), CAT_BREEDS.keys())

    total = (len(DOG_PRIORITY) if do_dogs else 0) + (len(CAT_PRIORITY) if do_cats else 0)
    print(f'\nDone! {total} pages in /breeds/')

if __name__ == '__main__':
    main()
