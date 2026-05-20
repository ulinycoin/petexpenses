#!/usr/bin/env python3
"""Generate breed pages for petexpenses.com — dogs AND cats.

Usage:
  python3 generate_breeds.py                     # All dogs
  python3 generate_breeds.py --cats              # All cats
  python3 generate_breeds.py --all               # Dogs + cats
  python3 generate_breeds.py --breed "Maine Coon"  # Single breed
"""

import os, sys, re, urllib.parse

# ─── DOGS ────────────────────────────────────────────────

DOG_BREEDS = {
    'Chihuahua': ['small','short',1.1,1.1,.9,1,'Dental issues common'],
    'Yorkshire Terrier': ['small','long',1.15,1.15,.9,1.4,'Prone to dental & tracheal issues'],
    'Dachshund': ['small','short',1.3,1.3,.95,1,'High risk of back (IVDD) problems'],
    'Shih Tzu': ['small','long',1.2,1.2,.95,1.5,'Brachycephalic; lots of grooming'],
    'Pomeranian': ['small','long',1.1,1.1,.9,1.3,'Dental & luxating patella risk'],
    'Maltese': ['small','long',1.1,1.1,.9,1.4,'Dental & skin issues'],
    'Pug': ['small','short',1.6,1.6,1,.9,'Brachycephalic syndrome'],
    'French Bulldog': ['small','short',1.7,1.7,1,.9,'Breathing & spine issues'],
    'Boston Terrier': ['small','short',1.4,1.4,1,.9,'Eye & joint issues'],
    'Miniature Schnauzer': ['small','wire',1.15,1.15,1,1.3,'Pancreatitis & bladder stones'],
    'Jack Russell Terrier': ['small','short',1.1,1.1,1,1,'Very healthy; high energy'],
    'Beagle': ['small','short',1.2,1.2,1.1,1,'Obesity & epilepsy risk'],
    'Cocker Spaniel': ['medium','long',1.25,1.25,1,1.4,'Ear & eye issues'],
    'Miniature Poodle': ['small','wire',1.1,1.1,1,1.4,'Healthy; needs grooming'],
    'Havanese': ['small','long',1.1,1.1,.95,1.3,'Joint & eye issues'],
    'Papillon': ['small','long',1.05,1.05,.9,1.1,'Long-lived, healthy'],
    'Bichon Frise': ['small','wire',1.15,1.15,.95,1.4,'Skin allergies; needs grooming'],
    'Italian Greyhound': ['small','short',1.15,1.15,.9,.8,'Fragile bones; dental'],
    'Lhasa Apso': ['small','long',1.15,1.15,.95,1.4,'Kidney & eye issues'],
    'Rat Terrier': ['small','short',1,1,.95,.8,'Very hardy'],
    'Cockapoo': ['small','wire',1.1,1.1,.95,1.4,'Ear infections; grooming'],
    'Cavapoo': ['small','wire',1.15,1.15,.95,1.4,'Possible MVD heart risk'],
    'Labrador Retriever': ['large','short',1.2,1.2,1.1,1,'Hip dysplasia & obesity risk'],
    'Golden Retriever': ['large','long',1.25,1.3,1.1,1.2,'High cancer risk'],
    'German Shepherd': ['large','long',1.3,1.3,1.1,1.1,'Hip dysplasia common'],
    'Bulldog': ['medium','short',1.8,1.8,1,.9,'Very high lifetime vet costs'],
    'Poodle': ['medium','wire',1.1,1.1,1,1.5,"Addison's disease risk"],
    'Boxer': ['large','short',1.4,1.4,1.1,.9,'Heart issues & cancer rate'],
    'Siberian Husky': ['medium','long',1.1,1.1,1.2,1.2,'Eye & hip issues'],
    'Australian Shepherd': ['medium','long',1.15,1.15,1.1,1.2,'MDR1 mutation; epilepsy'],
    'Border Collie': ['medium','long',1.1,1.1,1.1,1.2,'Epilepsy & CEA risk'],
    'Shiba Inu': ['medium','long',1.1,1.1,1,1.1,'Allergies & hip risk'],
    'Corgi (Pembroke)': ['small','long',1.2,1.2,1.05,1.1,'Back & hip; obesity'],
    'Whippet': ['medium','short',1.05,1.05,1,.8,'Very healthy'],
    'Vizsla': ['medium','short',1.1,1.1,1.1,.8,'Epilepsy & hip risk'],
    'Weimaraner': ['large','short',1.2,1.2,1.1,.9,'Bloat & hip risk'],
    'Samoyed': ['medium','long',1.2,1.2,1.1,1.5,'Diabetes & heart issues'],
    'Chow Chow': ['medium','long',1.3,1.3,1,1.4,'Hip & eye issues'],
    'Akita': ['large','long',1.25,1.25,1.1,1.1,'Autoimmune & kidney'],
    'Rottweiler': ['large','short',1.35,1.35,1.1,.9,'Hip & high cancer rate'],
    'Doberman Pinscher': ['large','short',1.3,1.3,1.1,.9,'Cardiomyopathy risk'],
    'Bernese Mountain Dog': ['large','long',1.5,1.6,1.1,1.3,'Short lifespan ~7–8 yrs'],
    'Dalmatian': ['medium','short',1.2,1.2,1,.9,'Deafness & urinary stones'],
    'Bernedoodle': ['large','wire',1.2,1.25,1.1,1.5,'High grooming needs'],
    'Great Dane': ['giant','short',1.4,1.5,1.1,.9,'Bloat; lifespan 7–10 yrs'],
    'Saint Bernard': ['giant','long',1.3,1.4,1.2,1.2,'Hip & heart issues'],
    'Mastiff': ['giant','short',1.3,1.4,1.15,.9,'Hip dysplasia; bloat'],
    'Newfoundland': ['giant','long',1.3,1.35,1.2,1.3,'Heart disease (SAS)'],
    'Standard Poodle': ['large','wire',1.1,1.1,1.05,1.5,"Addison's; bloat risk"],
    'Cane Corso': ['giant','short',1.2,1.3,1.15,.9,'Hip; cherry eye risk'],
}

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

CAT_BREEDS = {
    'Domestic Shorthair': ['medium','short',1,1,1,.8,'The classic — generally healthy'],
    'Domestic Longhair': ['medium','long',1.05,1.05,1,1.3,'Brushing 2–3× per week'],
    'Maine Coon': ['large','long',1.25,1.3,1.2,1.4,'HCM heart condition risk'],
    'Ragdoll': ['large','long',1.2,1.25,1.1,1.3,'HCM & UTI risk; very affectionate'],
    'Persian': ['medium','long',1.4,1.4,1,1.6,'Brachycephalic; daily grooming'],
    'Siamese': ['medium','short',1.15,1.15,1,.8,'Dental & respiratory issues'],
    'British Shorthair': ['medium','short',1.15,1.2,1,.9,'HCM risk; placid'],
    'Bengal': ['medium','short',1.15,1.15,1.1,.9,'High energy; HCM risk'],
    'Sphynx': ['medium','short',1.4,1.4,1.05,1.2,'Skin care + weekly bathing'],
    'Scottish Fold': ['medium','short',1.5,1.5,1,1,'Osteochondrodysplasia (joint pain)'],
    'Russian Blue': ['medium','short',1,1,1,.9,'Very healthy, low-maintenance'],
    'Abyssinian': ['medium','short',1.15,1.15,1,.8,'Renal amyloidosis risk'],
    'Norwegian Forest Cat': ['large','long',1.2,1.2,1.15,1.4,'HCM & hip dysplasia'],
    'American Shorthair': ['medium','short',1.05,1.05,1,.8,'Generally hardy'],
    'Exotic Shorthair': ['medium','short',1.35,1.35,1,1,'Brachycephalic like Persian'],
    'Burmese': ['medium','short',1.2,1.2,1,.8,'Diabetes & cranial issues'],
    'Birman': ['medium','long',1.1,1.1,1,1.2,'Generally healthy'],
    'Oriental Shorthair': ['medium','short',1.1,1.1,1,.8,'Dental & cardiac risk'],
    'Devon Rex': ['small','short',1.15,1.15,.95,.9,'Patellar luxation'],
    'Cornish Rex': ['small','short',1.15,1.15,.95,.9,'HCM & hypotrichosis'],
    'Savannah': ['large','short',1.2,1.25,1.2,.9,'High energy; pricey vet'],
    'Manx': ['medium','short',1.3,1.3,1,.9,'Manx syndrome (spine)'],
    'Tonkinese': ['medium','short',1.1,1.1,1,.8,'Generally healthy'],
}

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

CAT_PRIORITY = [
    'Maine Coon', 'Persian', 'Ragdoll', 'Bengal', 'Siamese',
    'Sphynx', 'British Shorthair', 'Scottish Fold', 'Russian Blue',
    'Abyssinian', 'Norwegian Forest Cat', 'Exotic Shorthair',
    'American Shorthair', 'Burmese', 'Birman', 'Oriental Shorthair',
    'Devon Rex', 'Cornish Rex', 'Savannah', 'Domestic Shorthair',
    'Domestic Longhair', 'Manx', 'Tonkinese',
]

DOG_PRIORITY = [
    'French Bulldog', 'Labrador Retriever', 'Golden Retriever', 'German Shepherd',
    'Bulldog', 'Poodle', 'Beagle', 'Rottweiler', 'Dachshund', 'Siberian Husky',
    'Pomeranian', 'Great Dane', 'Chihuahua', 'Yorkshire Terrier', 'Boxer',
    'Shih Tzu', 'Boston Terrier', 'Corgi (Pembroke)', 'Australian Shepherd',
    'Bernese Mountain Dog',
]

# ══════════════════════════════════════════════════════════

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

    # Health extended
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
    elif 'spine' in hi_lc or 'joint' in hi_lc or 'hip' in hi_lc:
        he = f'{bp} are prone to joint and spinal issues, which may require ongoing supplements, medications, or even surgical intervention.'
    else:
        he = f'{bp} are generally healthy but can be prone to {hi_lc}.'

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

    return {
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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How Much Does a !BREED! Cost Per Year? (2026 Guide) — petexpenses.com</title>
<meta name="description" content="!META_DESC!">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://petexpenses.com/"},
        {"@type": "ListItem", "position": 2, "name": "Breeds", "item": "https://petexpenses.com/breeds"},
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
            "text": "Yes — !BREED!s are prone to !HEALTH_ISSUES_LC!, which can lead to expensive vet bills. One emergency surgery can cost $2,000–$5,000. Pet insurance typically costs $!INS_LOW!–$!INS_HIGH!/year and can cover 70-90% of eligible costs."
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
    }
  ]
}
</script>
<meta property="og:title" content="How Much Does a !BREED! Cost Per Year? (2026 Guide)">
<meta property="og:description" content="See the real annual cost of owning a !BREED! in 2026. Food, vet, insurance, grooming & supplies breakdown. Free calculator included.">
<meta property="og:image" content="https://petexpenses.com/og-!SPECIES!.jpg">
<meta property="og:url" content="https://petexpenses.com/breeds/!SLUG!">
<meta property="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://petexpenses.com/breeds/!SLUG!">
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
      <h1 class="article-h1">How Much Does !ARTICLE! !BREED! Cost Per Year?</h1>
      <div class="article-meta">
        <span>Last updated May 2026</span>
        <span>Data: APPA, AVMA, NAPHIA</span>
        <span>!SPECIES_TITLE! guide</span>
      </div>
    </header>

    <div class="article-body">

      <div class="highlight-card hc-!SPECIES!">
        <div class="hc-label">Quick Answer</div>
        <p>The average annual cost of owning a !BREED! in the US ranges from <strong>$!COST_LOW! to $!COST_HIGH! per year</strong> ($!MONTHLY_LOW!–$!MONTHLY_HIGH!/month). This includes food, routine vet care, pet insurance, grooming, and supplies. Actual costs depend on your !SPECIES_TITLE!&rsquo;s age, weight, diet, activity level, and location.</p>
      </div>

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

      <h3>Food</h3>
      <p>Food is typically the largest recurring expense for !BREED_PLURAL!. Expect to spend $!FOOD_LOW!–$!FOOD_HIGH! per year on quality !SPECIES_TITLE! food. !BREED_PLURAL! with food sensitivities may need specialized diets, which can add !FOOD_ALLERGY_EXTRA! per year. Larger !BREED_PLURAL! eat more and cost more to feed.</p>

      <h3>Veterinary Care</h3>
      <p>Routine veterinary care for !BREED_PLURAL! costs $!VET_LOW!–$!VET_HIGH! per year. This covers annual check-ups, vaccinations, and preventative treatments. !HEALTH_NOTE_EXTENDED! Unexpected emergencies can add thousands in a single visit.</p>

      <h3>Pet Insurance</h3>
      <p>Pet insurance for a !BREED! costs $!INS_LOW!–$!INS_HIGH! per year. Given the breed&rsquo;s predisposition to !HEALTH_ISSUES_LC!, insurance is worth considering. An emergency visit can cost $2,000 to $5,000 — far more than a year&rsquo;s premiums.</p>

      <h3>Grooming</h3>
      <p>!GROOMING_TEXT!</p>

      <h3>Supplies</h3>
      <p>Annual supplies — litter box, scratching post, bed, bowls, toys — run $!SUPP_LOW!–$!SUPP_HIGH!. Initial setup in the first year costs more due to one-time purchases.</p>

      <h2>Why !BREED_PLURAL! Cost !COST_COMPARISON! Than Average</h2>
      <p>!HEALTH_FACTORS_SECTION!</p>

      <h2>How to Save on !BREED! Ownership</h2>
      <ul>
        <li><strong>Preventative care is cheaper than emergency care.</strong> Regular vet visits catch problems early. Budget for annual check-ups and stay up-to-date on vaccinations.</li>
        <li><strong>Compare pet insurance plans.</strong> Get quotes from at least three providers. Accident-only plans start around $!INS_LOW!/year.</li>
        <li><strong>Buy food and litter in bulk.</strong> Subscribe to auto-ship for discounts. !SPECIES_TITLE! food and litter are significantly cheaper per unit in larger quantities.</li>
        <li><strong>Use preventative dental care.</strong> Dental disease is common in !SPECIES_PLURAL! and can lead to expensive health issues. At-home dental treats and regular check-ups save money long-term.</li>
        <li><strong>Choose high-quality food.</strong> Better nutrition reduces vet visits from urinary issues, obesity, and allergies.</li>
      </ul>

      <h2>First-Year vs. Annual Costs</h2>
      <p>Your first year with a !BREED! will be more expensive. Expect to spend an extra !FIRST_YEAR_EXTRA! on:</p>
      <ul>
        <li>Initial vet visit, vaccinations, and microchipping</li>
        <li>Spay/neuter surgery</li>
        <li>Litter box, bed, bowls, scratching post, toys</li>
      </ul>

      <h2>FAQ About !BREED! Costs</h2>

      <details>
        <summary>How much does a !BREED! cost per month?</summary>
        <div class="faq-a">
          <p>Monthly costs for a !BREED! range from <strong>$!MONTHLY_LOW! to $!MONTHLY_HIGH!</strong>. This includes food, vet care, insurance, grooming, and supplies. !SPECIES_TITLE!s and seniors typically cost more than healthy adults.</p>
        </div>
      </details>

      <details>
        <summary>Is a !BREED! expensive to own compared to other cats?</summary>
        <div class="faq-a">
          <p>!COMPARISON_SENTENCE!</p>
        </div>
      </details>

      <details>
        <summary>What health issues do !BREED_PLURAL! have?</summary>
        <div class="faq-a">
          <p>!BREED_PLURAL! are prone to !HEALTH_ISSUES_LC!. These conditions can require ongoing medication, special diets, or surgery — increasing annual veterinary costs beyond the routine care baseline.</p>
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

<section class="offers-section">
  <h2>Save on Your !BREED!&rsquo;s Food</h2>
  <div class="article-body">
    <div class="highlight-card hc-mint">
      <div class="hc-label">Raw Paws Pet Food</div>
      <p><strong>Frozen raw !SPECIES_TITLE! food, made fresh weekly.</strong> Free shipping nationwide. !BREED_PLURAL! on raw diets often show better digestion and fewer allergy symptoms.</p>
      <p>4.8 stars from 2,000+ reviews &bull; $160 avg order</p>
      <p style="margin-top:12px"><a href="https://www.dpbolvw.net/click-101748061-17234885" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;background:var(--mint-dk);color:#fff;border-radius:var(--radius-pill);font-weight:700;text-decoration:none">Shop Raw Paws</a> <a href="https://www.anrdoezrs.net/click-101748061-17234936" target="_blank" rel="noopener" style="display:inline-block;padding:10px 24px;margin-left:8px;background:var(--ink);color:var(--cream);border-radius:var(--radius-pill);font-weight:600;text-decoration:none">Auto-Ship &amp; Save</a></p>
    </div>
  </div>
</section>

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

    total = (len(DOG_PRIORITY) if do_dogs else 0) + (len(CAT_PRIORITY) if do_cats else 0)
    print(f'\nDone! {total} pages in /breeds/')

if __name__ == '__main__':
    main()
