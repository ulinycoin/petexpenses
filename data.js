// ───────────────────────────────────────────────────────────────
// DATA — breeds, cost tables, recommendations
// Tagged for both dog and cat. Stubbed affiliate offers.
// ───────────────────────────────────────────────────────────────

window.PET_DATA = (function () {
  // ── DOG BREEDS ──────────────────────────────────────────────
  // [size, coat, vetMult, insMult, foodMult, groomMult, note]
  const DOG_BREEDS = {
    'Chihuahua':                    ['small',  'short', 1.1,  1.1,  0.9,  1.0,  'Dental issues common'],
    'Yorkshire Terrier':            ['small',  'long',  1.15, 1.15, 0.9,  1.4,  'Prone to dental & tracheal issues'],
    'Dachshund':                    ['small',  'short', 1.3,  1.3,  0.95, 1.0,  'High risk of back (IVDD) problems'],
    'Shih Tzu':                     ['small',  'long',  1.2,  1.2,  0.95, 1.5,  'Brachycephalic; lots of grooming'],
    'Pomeranian':                   ['small',  'long',  1.1,  1.1,  0.9,  1.3,  'Dental & luxating patella risk'],
    'Maltese':                      ['small',  'long',  1.1,  1.1,  0.9,  1.4,  'Dental & skin issues'],
    'Cavalier King Charles Spaniel':['small',  'long',  1.5,  1.5,  1.0,  1.2,  'High cardiac & neurological risk'],
    'Pug':                          ['small',  'short', 1.6,  1.6,  1.0,  0.9,  'Brachycephalic syndrome'],
    'French Bulldog':               ['small',  'short', 1.7,  1.7,  1.0,  0.9,  'Breathing & spine issues'],
    'Boston Terrier':               ['small',  'short', 1.4,  1.4,  1.0,  0.9,  'Eye & joint issues'],
    'Miniature Schnauzer':          ['small',  'wire',  1.15, 1.15, 1.0,  1.3,  'Pancreatitis & bladder stones'],
    'Jack Russell Terrier':         ['small',  'short', 1.1,  1.1,  1.0,  1.0,  'Very healthy; high energy'],
    'Beagle':                       ['small',  'short', 1.2,  1.2,  1.1,  1.0,  'Obesity & epilepsy risk'],
    'Cocker Spaniel':               ['medium', 'long',  1.25, 1.25, 1.0,  1.4,  'Ear & eye issues'],
    'Miniature Poodle':             ['small',  'wire',  1.1,  1.1,  1.0,  1.4,  'Healthy; needs grooming'],
    'Havanese':                     ['small',  'long',  1.1,  1.1,  0.95, 1.3,  'Joint & eye issues'],
    'Papillon':                     ['small',  'long',  1.05, 1.05, 0.9,  1.1,  'Long-lived, healthy'],
    'Bichon Frise':                 ['small',  'wire',  1.15, 1.15, 0.95, 1.4,  'Skin allergies; needs grooming'],
    'Italian Greyhound':            ['small',  'short', 1.15, 1.15, 0.9,  0.8,  'Fragile bones; dental'],
    'Lhasa Apso':                   ['small',  'long',  1.15, 1.15, 0.95, 1.4,  'Kidney & eye issues'],
    'Rat Terrier':                  ['small',  'short', 1.0,  1.0,  0.95, 0.8,  'Very hardy'],
    'Cockapoo':                     ['small',  'wire',  1.1,  1.1,  0.95, 1.4,  'Ear infections; grooming'],
    'Cavapoo':                      ['small',  'wire',  1.15, 1.15, 0.95, 1.4,  'Possible MVD heart risk'],
    'Labrador Retriever':           ['large',  'short', 1.2,  1.2,  1.1,  1.0,  'Hip dysplasia & obesity risk'],
    'Golden Retriever':             ['large',  'long',  1.25, 1.3,  1.1,  1.2,  'High cancer risk'],
    'German Shepherd':              ['large',  'long',  1.3,  1.3,  1.1,  1.1,  'Hip dysplasia common'],
    'Bulldog':                      ['medium', 'short', 1.8,  1.8,  1.0,  0.9,  'Very high lifetime vet costs'],
    'Poodle':                       ['medium', 'wire',  1.1,  1.1,  1.0,  1.5,  "Addison's disease risk"],
    'Boxer':                        ['large',  'short', 1.4,  1.4,  1.1,  0.9,  'Heart issues & cancer rate'],
    'Siberian Husky':               ['medium', 'long',  1.1,  1.1,  1.2,  1.2,  'Eye & hip issues'],
    'Australian Shepherd':          ['medium', 'long',  1.15, 1.15, 1.1,  1.2,  'MDR1 mutation; epilepsy'],
    'Border Collie':                ['medium', 'long',  1.1,  1.1,  1.1,  1.2,  'Epilepsy & CEA risk'],
    'Shiba Inu':                    ['medium', 'long',  1.1,  1.1,  1.0,  1.1,  'Allergies & hip risk'],
    'Corgi (Pembroke)':             ['small',  'long',  1.2,  1.2,  1.05, 1.1,  'Back & hip; obesity'],
    'Whippet':                      ['medium', 'short', 1.05, 1.05, 1.0,  0.8,  'Very healthy'],
    'Vizsla':                       ['medium', 'short', 1.1,  1.1,  1.1,  0.8,  'Epilepsy & hip risk'],
    'Weimaraner':                   ['large',  'short', 1.2,  1.2,  1.1,  0.9,  'Bloat & hip risk'],
    'Samoyed':                      ['medium', 'long',  1.2,  1.2,  1.1,  1.5,  'Diabetes & heart issues'],
    'Chow Chow':                    ['medium', 'long',  1.3,  1.3,  1.0,  1.4,  'Hip & eye issues'],
    'Akita':                        ['large',  'long',  1.25, 1.25, 1.1,  1.1,  'Autoimmune & kidney'],
    'Rottweiler':                   ['large',  'short', 1.35, 1.35, 1.1,  0.9,  'Hip & high cancer rate'],
    'Doberman Pinscher':            ['large',  'short', 1.3,  1.3,  1.1,  0.9,  'Cardiomyopathy risk'],
    'Bernese Mountain Dog':         ['large',  'long',  1.5,  1.6,  1.1,  1.3,  'Short lifespan ~7–8 yrs'],
    'Dalmatian':                    ['medium', 'short', 1.2,  1.2,  1.0,  0.9,  'Deafness & urinary stones'],
    'Bernedoodle':                  ['large',  'wire',  1.2,  1.25, 1.1,  1.5,  'High grooming needs'],
    'Great Dane':                   ['giant',  'short', 1.4,  1.5,  1.1,  0.9,  'Bloat; lifespan 7–10 yrs'],
    'Saint Bernard':                ['giant',  'long',  1.3,  1.4,  1.2,  1.2,  'Hip & heart issues'],
    'Mastiff':                      ['giant',  'short', 1.3,  1.4,  1.15, 0.9,  'Hip dysplasia; bloat'],
    'Newfoundland':                 ['giant',  'long',  1.3,  1.35, 1.2,  1.3,  'Heart disease (SAS)'],
    'Standard Poodle':              ['large',  'wire',  1.1,  1.1,  1.05, 1.5,  "Addison's; bloat risk"],
    'Cane Corso':                   ['giant',  'short', 1.2,  1.3,  1.15, 0.9,  'Hip; cherry eye risk'],
  };

  // ── CAT BREEDS ──────────────────────────────────────────────
  const CAT_BREEDS = {
    'Domestic Shorthair':           ['medium', 'short', 1.0,  1.0,  1.0,  0.8,  'The classic — generally healthy'],
    'Domestic Longhair':            ['medium', 'long',  1.05, 1.05, 1.0,  1.3,  'Brushing 2–3× per week'],
    'Maine Coon':                   ['large',  'long',  1.25, 1.3,  1.2,  1.4,  'HCM heart condition risk'],
    'Ragdoll':                      ['large',  'long',  1.2,  1.25, 1.1,  1.3,  'HCM & UTI risk; very affectionate'],
    'Persian':                      ['medium', 'long',  1.4,  1.4,  1.0,  1.6,  'Brachycephalic; daily grooming'],
    'Siamese':                      ['medium', 'short', 1.15, 1.15, 1.0,  0.8,  'Dental & respiratory issues'],
    'British Shorthair':            ['medium', 'short', 1.15, 1.2,  1.0,  0.9,  'HCM risk; placid'],
    'Bengal':                       ['medium', 'short', 1.15, 1.15, 1.1,  0.9,  'High energy; HCM risk'],
    'Sphynx':                       ['medium', 'short', 1.4,  1.4,  1.05, 1.2,  'Skin care + weekly bathing'],
    'Scottish Fold':                ['medium', 'short', 1.5,  1.5,  1.0,  1.0,  'Osteochondrodysplasia (joint pain)'],
    'Russian Blue':                 ['medium', 'short', 1.0,  1.0,  1.0,  0.9,  'Very healthy, low-maintenance'],
    'Abyssinian':                   ['medium', 'short', 1.15, 1.15, 1.0,  0.8,  'Renal amyloidosis risk'],
    'Norwegian Forest Cat':         ['large',  'long',  1.2,  1.2,  1.15, 1.4,  'HCM & hip dysplasia'],
    'American Shorthair':           ['medium', 'short', 1.05, 1.05, 1.0,  0.8,  'Generally hardy'],
    'Exotic Shorthair':             ['medium', 'short', 1.35, 1.35, 1.0,  1.0,  'Brachycephalic like Persian'],
    'Burmese':                      ['medium', 'short', 1.2,  1.2,  1.0,  0.8,  'Diabetes & cranial issues'],
    'Birman':                       ['medium', 'long',  1.1,  1.1,  1.0,  1.2,  'Generally healthy'],
    'Oriental Shorthair':           ['medium', 'short', 1.1,  1.1,  1.0,  0.8,  'Dental & cardiac risk'],
    'Devon Rex':                    ['small',  'short', 1.15, 1.15, 0.95, 0.9,  'Patellar luxation'],
    'Cornish Rex':                  ['small',  'short', 1.15, 1.15, 0.95, 0.9,  'HCM & hypotrichosis'],
    'Savannah':                     ['large',  'short', 1.2,  1.25, 1.2,  0.9,  'High energy; pricey vet'],
    'Manx':                         ['medium', 'short', 1.3,  1.3,  1.0,  0.9,  'Manx syndrome (spine)'],
    'Tonkinese':                    ['medium', 'short', 1.1,  1.1,  1.0,  0.8,  'Generally healthy'],
  };

  // ── BASE COST TABLES (annual, USD, US 2026 averages) ────────
  // Numbers cross-referenced with APPA 2026, AVMA, NAPHIA, BLS Feb 2026
  const DOG_COSTS = {
    food:      { small:[360,600],  medium:[600,1000], large:[900,1500], giant:[1200,2000] },
    vet:       { small:[200,500],  medium:[300,700],  large:[400,1000], giant:[500,1200] },
    insurance: { small:[240,480],  medium:[360,720],  large:[480,960],  giant:[600,1200] },
    grooming:  {
      short: { small:[100,200], medium:[150,300], large:[200,400], giant:[250,500] },
      long:  { small:[200,400], medium:[300,500], large:[400,800], giant:[500,1000] },
      wire:  { small:[180,350], medium:[250,450], large:[350,700], giant:[450,900] },
    },
    supplies:  { small:[150,300], medium:[200,400], large:[250,500], giant:[300,600] },
  };

  const CAT_COSTS = {
    food:      { small:[240,420], medium:[300,600],  large:[420,720] },
    vet:       { small:[180,400], medium:[220,500],  large:[300,650] },
    insurance: { small:[180,360], medium:[240,480],  large:[300,540] },
    grooming:  {
      short: { small:[40,120],  medium:[60,150],  large:[80,180] },
      long:  { small:[120,300], medium:[180,400], large:[240,500] },
    },
    supplies:  { small:[120,240], medium:[150,300], large:[200,380] },
  };

  // ── MULTIPLIERS ─────────────────────────────────────────────
  const AGE_MULT = {
    puppy:  { vet: 1.3, supplies: 1.4 },
    adult:  {},
    senior: { vet: 1.6, insurance: 1.4 },
  };
  const ACTIVITY_MULT = {
    low:      { food: 0.9 },
    moderate: {},
    high:     { food: 1.2, supplies: 1.15 },
  };

  // ── STUB OFFERS (placeholder, not real affiliates) ──────────
  const OFFERS = {
    dog: [
      {
        id: 'fresh-food',
        emoji: '🍖',
        sticker: 'FRESH',
        accent: '#6EE7B7',
        accentDark: '#0E9F6E',
        title: 'Fresh Vet-Made Meals',
        partner: 'Partner #1',
        bullet1: 'Human-grade meat & veggies',
        bullet2: 'Portioned for your pup',
        bullet3: '50% off first box',
        priceFrom: '$2/day',
        ratings: '4.9 ★  ·  200k+ pups',
        ctaText: 'Try Fresh →',
      },
      {
        id: 'insurance',
        emoji: '🛡️',
        sticker: 'SAFETY',
        accent: '#A78BFA',
        accentDark: '#6D49C7',
        title: 'Pet Insurance Comparison',
        partner: 'Partner #2',
        bullet1: 'Compare 10+ plans free',
        bullet2: 'Avg payout 80% of vet bill',
        bullet3: 'Covers accidents & illness',
        priceFrom: 'from $14/mo',
        ratings: '★★★★★  ·  Top-rated 2026',
        ctaText: 'Get Quotes →',
      },
      {
        id: 'treats',
        emoji: '🎁',
        sticker: 'FUN',
        accent: '#FFD23F',
        accentDark: '#C9941E',
        title: 'Toy & Treat Box',
        partner: 'Partner #3',
        bullet1: 'Themed box every month',
        bullet2: 'Sized to your dog',
        bullet3: 'Cancel anytime',
        priceFrom: '$23/mo',
        ratings: '4.6 ★  ·  1M+ subscribers',
        ctaText: 'Build My Box →',
      },
    ],
    cat: [
      {
        id: 'fresh-food',
        emoji: '🐟',
        sticker: 'FRESH',
        accent: '#6EE7B7',
        accentDark: '#0E9F6E',
        title: 'Vet-Formulated Wet Food',
        partner: 'Partner #1',
        bullet1: 'Real fish & poultry, no fillers',
        bullet2: 'Portioned per cat',
        bullet3: 'Free first 2 weeks',
        priceFrom: '$1.50/day',
        ratings: '4.8 ★  ·  120k+ cats',
        ctaText: 'Try Fresh →',
      },
      {
        id: 'insurance',
        emoji: '🛡️',
        sticker: 'SAFETY',
        accent: '#A78BFA',
        accentDark: '#6D49C7',
        title: 'Cat Insurance Comparison',
        partner: 'Partner #2',
        bullet1: 'Compare 10+ plans free',
        bullet2: 'Avg payout 80% of vet bill',
        bullet3: 'Dental + chronic covered',
        priceFrom: 'from $11/mo',
        ratings: '★★★★★  ·  Top-rated 2026',
        ctaText: 'Get Quotes →',
      },
      {
        id: 'treats',
        emoji: '🎁',
        sticker: 'FUN',
        accent: '#FFD23F',
        accentDark: '#C9941E',
        title: 'Cat Toy & Treat Box',
        partner: 'Partner #3',
        bullet1: 'Themed enrichment box',
        bullet2: 'Catnip + crinkle toys',
        bullet3: 'Cancel anytime',
        priceFrom: '$18/mo',
        ratings: '4.5 ★  ·  280k+ subs',
        ctaText: 'Build My Box →',
      },
    ],
  };

  // ── DATA SOURCES (cited inline) ─────────────────────────────
  const SOURCES = [
    { name: 'APPA',     full: '2026 State of the Industry Report' },
    { name: 'AVMA',     full: 'Pet Ownership & Demographics 2026' },
    { name: 'NAPHIA',   full: 'Pet Health Insurance Report 2026' },
    { name: 'BLS',      full: 'Veterinary Services CPI · Feb 2026' },
    { name: 'MarketWatch', full: 'Annual cost of pet ownership' },
  ];

  // ── BLOG TEASERS (stubs) ────────────────────────────────────
  const BLOG = [
    {
      tag: 'NEW · MAY 2026',
      title: 'The $4,272 question: where does it all go?',
      body: 'A line-by-line look at the average American pet budget — and the three categories most owners underestimate.',
      mins: 6, accent: '#FF5A3C',
    },
    {
      tag: 'INSURANCE',
      title: 'Is pet insurance worth it? We ran the math on 12 breeds.',
      body: 'For French Bulldogs and Goldens it pays for itself by year three. For others, a high-yield savings account wins.',
      mins: 9, accent: '#A78BFA',
    },
    {
      tag: 'FOOD',
      title: 'Kibble vs fresh vs raw: a real cost comparison',
      body: 'We costed out a year of feeding a 50 lb dog across 8 popular brands. The cheapest option will surprise you.',
      mins: 7, accent: '#6EE7B7',
    },
  ];

  // ── TESTIMONIAL STUBS ───────────────────────────────────────
  const TESTIMONIALS = [
    { who: 'Sara · Brooklyn',     pet: 'French Bulldog, 3 yrs', quote: '"I had no idea Frenchies cost this much. The insurance suggestion saved me a $4k vet bill."', rotate: -2 },
    { who: 'Mike · Austin',       pet: 'Labrador, 1 yr',         quote: '"Bookmarked. Sent to my partner. Now we agree on the food budget."', rotate: 1.5 },
    { who: 'Priya · Chicago',     pet: 'Maine Coon, 5 yrs',       quote: '"Honest answer about my cat\'s yearly bill. No paywall, no email-grab."', rotate: -1 },
    { who: 'Diego · Los Angeles', pet: 'Rescue mutt, 7 yrs',      quote: '"Calculator caught a vet category I\'d been ignoring for years."', rotate: 2.5 },
  ];

  return { DOG_BREEDS, CAT_BREEDS, DOG_COSTS, CAT_COSTS, AGE_MULT, ACTIVITY_MULT, OFFERS, SOURCES, BLOG, TESTIMONIALS };
})();
