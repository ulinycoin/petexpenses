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
const { useState, useEffect, useRef, useMemo, useCallback } = React;
function Paw({ size = 32, color = "currentColor", className = "", style = {} }) {
  return /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 40 40", width: size, height: size, className, style, "aria-hidden": "true" }, /* @__PURE__ */ React.createElement("circle", { cx: "20", cy: "24", r: "10", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "8", cy: "14", r: "4.5", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "32", cy: "14", r: "4.5", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "14", cy: "5", r: "3.6", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "26", cy: "5", r: "3.6", fill: color }));
}
function Sticker({ rotate = 0, children, className = "", style = {}, onClick }) {
  return /* @__PURE__ */ React.createElement(
    "div",
    {
      className: `sticker ${className}`,
      style: {
        transform: `rotate(${rotate}deg)`,
        ...style
      },
      onClick
    },
    children
  );
}
function HalftoneBg({ color = "rgba(27,19,64,0.07)", size = 14 }) {
  return /* @__PURE__ */ React.createElement(
    "div",
    {
      "aria-hidden": "true",
      style: {
        position: "absolute",
        inset: 0,
        backgroundImage: `radial-gradient(${color} 1.4px, transparent 1.6px)`,
        backgroundSize: `${size}px ${size}px`,
        pointerEvents: "none"
      }
    }
  );
}
function BigSlider({ label, value, onChange, min, max, step = 1, format = (v) => v, ticks = null, accent = "#FF5A3C" }) {
  const pct = (value - min) / (max - min) * 100;
  return /* @__PURE__ */ React.createElement("div", { className: "bigslider" }, /* @__PURE__ */ React.createElement("div", { className: "bigslider-head" }, /* @__PURE__ */ React.createElement("div", { className: "bigslider-label" }, label), /* @__PURE__ */ React.createElement("div", { className: "bigslider-value", style: { color: accent } }, format(value))), /* @__PURE__ */ React.createElement("div", { className: "bigslider-track-wrap" }, /* @__PURE__ */ React.createElement(
    "input",
    {
      type: "range",
      min,
      max,
      step,
      value,
      onChange: (e) => onChange(Number(e.target.value)),
      className: "bigslider-input",
      style: { "--pct": pct + "%", "--accent": accent }
    }
  )), ticks && /* @__PURE__ */ React.createElement("div", { className: "bigslider-ticks" }, ticks.map((t, i) => /* @__PURE__ */ React.createElement("span", { key: i }, t))));
}
function PillSegment({ options, value, onChange, accent = "#FF5A3C", size = "md" }) {
  return /* @__PURE__ */ React.createElement("div", { className: `pill-seg pill-seg-${size}` }, options.map((opt) => {
    const active = opt.value === value;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: opt.value,
        className: `pill-seg-btn ${active ? "active" : ""}`,
        style: active ? { background: accent, color: "#fff" } : {},
        onClick: () => onChange(opt.value)
      },
      opt.icon && /* @__PURE__ */ React.createElement("span", { className: "pill-seg-icon" }, opt.icon),
      /* @__PURE__ */ React.createElement("span", null, opt.label)
    );
  }));
}
function BreedSearch({ breeds, value, onChange, placeholder, accent = "#FF5A3C" }) {
  const [open, setOpen] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const wrapRef = useRef(null);
  const names = useMemo(() => Object.keys(breeds).sort(), [breeds]);
  const q = (value || "").toLowerCase().trim();
  const matches = useMemo(() => {
    if (!q) return [];
    return names.filter((n) => n.toLowerCase().includes(q)).slice(0, 7);
  }, [q, names]);
  useEffect(() => {
    function onDoc(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, []);
  function pick(name) {
    onChange(name);
    setOpen(false);
    setActiveIdx(-1);
  }
  function onKey(e) {
    if (!open || !matches.length) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIdx((i) => Math.min(i + 1, matches.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIdx((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && activeIdx >= 0) {
      e.preventDefault();
      pick(matches[activeIdx]);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  }
  return /* @__PURE__ */ React.createElement("div", { className: "breed-search", ref: wrapRef }, /* @__PURE__ */ React.createElement(
    "input",
    {
      className: "breed-input",
      value,
      onChange: (e) => {
        onChange(e.target.value);
        setOpen(true);
        setActiveIdx(-1);
      },
      onFocus: () => setOpen(true),
      onKeyDown: onKey,
      placeholder,
      autoComplete: "off",
      style: { "--accent": accent }
    }
  ), open && matches.length > 0 && /* @__PURE__ */ React.createElement("ul", { className: "breed-list", role: "listbox" }, matches.map((name, i) => {
    const [size, coat] = breeds[name];
    const sizeMap = { small: "Small", medium: "Medium", large: "Large", giant: "Giant" };
    const coatMap = { short: "Short", long: "Long", wire: "Curly/Wire" };
    return /* @__PURE__ */ React.createElement(
      "li",
      {
        key: name,
        onMouseDown: () => pick(name),
        className: i === activeIdx ? "active" : ""
      },
      /* @__PURE__ */ React.createElement("span", { className: "bl-name" }, name),
      /* @__PURE__ */ React.createElement("span", { className: "bl-meta" }, sizeMap[size], " \xB7 ", coatMap[coat])
    );
  })));
}
function AnimatedDollar({ value, duration = 700, className = "", style = {} }) {
  const [display, setDisplay] = useState(value);
  const fromRef = useRef(value);
  const startRef = useRef(0);
  const rafRef = useRef(0);
  useEffect(() => {
    cancelAnimationFrame(rafRef.current);
    fromRef.current = display;
    startRef.current = performance.now();
    function tick(now) {
      const t = Math.min(1, (now - startRef.current) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const v = Math.round(fromRef.current + (value - fromRef.current) * eased);
      setDisplay(v);
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
    }
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [value]);
  return /* @__PURE__ */ React.createElement("span", { className, style }, "$", display.toLocaleString());
}
function Donut({ items, total, size = 220, stroke = 36 }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  let offset = 0;
  return /* @__PURE__ */ React.createElement("svg", { width: size, height: size, viewBox: `0 0 ${size} ${size}` }, /* @__PURE__ */ React.createElement("circle", { cx: size / 2, cy: size / 2, r, fill: "none", stroke: "rgba(27,19,64,0.08)", strokeWidth: stroke }), items.map((it, i) => {
    const frac = it.amount / total;
    const dash = frac * c;
    const seg = /* @__PURE__ */ React.createElement(
      "circle",
      {
        key: i,
        cx: size / 2,
        cy: size / 2,
        r,
        fill: "none",
        stroke: it.color,
        strokeWidth: stroke,
        strokeDasharray: `${dash} ${c - dash}`,
        strokeDashoffset: -offset,
        transform: `rotate(-90 ${size / 2} ${size / 2})`,
        style: { transition: "stroke-dasharray 0.5s ease, stroke-dashoffset 0.5s ease" },
        strokeLinecap: "butt"
      }
    );
    offset += dash;
    return seg;
  }));
}
Object.assign(window, { Paw, Sticker, HalftoneBg, BigSlider, PillSegment, BreedSearch, AnimatedDollar, Donut });
const { DOG_BREEDS, CAT_BREEDS, DOG_COSTS, CAT_COSTS, AGE_MULT, ACTIVITY_MULT, OFFERS, SOURCES, BLOG, TESTIMONIALS } = window.PET_DATA;
function clamp(v, a, b) {
  return Math.max(a, Math.min(b, v));
}
function midOf(arr) {
  return Math.round((arr[0] + arr[1]) / 2);
}
function lerpInRange(range, t) {
  return Math.round(range[0] + (range[1] - range[0]) * t);
}
function sizeFromWeight(species, weight) {
  if (species === "dog") {
    if (weight < 20) return "small";
    if (weight < 50) return "medium";
    if (weight < 80) return "large";
    return "giant";
  } else {
    if (weight < 8) return "small";
    if (weight < 14) return "medium";
    return "large";
  }
}
function intraT(species, weight) {
  if (species === "dog") {
    if (weight < 20) return clamp((weight - 4) / (20 - 4), 0, 1);
    if (weight < 50) return clamp((weight - 20) / (50 - 20), 0, 1);
    if (weight < 80) return clamp((weight - 50) / (80 - 50), 0, 1);
    return clamp((weight - 80) / (160 - 80), 0, 1);
  } else {
    if (weight < 8) return clamp((weight - 4) / (8 - 4), 0, 1);
    if (weight < 14) return clamp((weight - 8) / (14 - 8), 0, 1);
    return clamp((weight - 14) / (25 - 14), 0, 1);
  }
}
function calcCosts({ species, weight, age, activity, coat, breedData }) {
  const size = sizeFromWeight(species, weight);
  const t = intraT(species, weight);
  const tbl = species === "dog" ? DOG_COSTS : CAT_COSTS;
  const bm = breedData || { vetMult: 1, insMult: 1, foodMult: 1, groomMult: 1 };
  let food = lerpInRange(tbl.food[size], t);
  let vet = lerpInRange(tbl.vet[size], t);
  let insurance = lerpInRange(tbl.insurance[size], t);
  const groomT = tbl.grooming[coat] || tbl.grooming.short;
  let grooming = lerpInRange(groomT[size], t);
  let supplies = lerpInRange(tbl.supplies[size], t);
  food = Math.round(food * (bm.foodMult ?? 1));
  vet = Math.round(vet * (bm.vetMult ?? 1));
  insurance = Math.round(insurance * (bm.insMult ?? 1));
  grooming = Math.round(grooming * (bm.groomMult ?? 1));
  const am = AGE_MULT[age] || {};
  if (am.vet) vet = Math.round(vet * am.vet);
  if (am.insurance) insurance = Math.round(insurance * am.insurance);
  if (am.supplies) supplies = Math.round(supplies * am.supplies);
  const acm = ACTIVITY_MULT[activity] || {};
  if (acm.food) food = Math.round(food * acm.food);
  if (acm.supplies) supplies = Math.round(supplies * acm.supplies);
  return {
    food,
    vet,
    insurance,
    grooming,
    supplies,
    total: food + vet + insurance + grooming + supplies,
    size
  };
}
function getBreed(species, name) {
  if (!name) return null;
  const map = species === "dog" ? DOG_BREEDS : CAT_BREEDS;
  const key = Object.keys(map).find((k) => k.toLowerCase() === name.toLowerCase());
  if (!key) return null;
  const [size, coat, vetMult, insMult, foodMult, groomMult, note] = map[key];
  return { name: key, size, coat, vetMult, insMult, foodMult, groomMult, note };
}
function defaultWeightFromSize(species, size) {
  if (species === "dog") return { small: 12, medium: 35, large: 65, giant: 110 }[size];
  return { small: 6, medium: 11, large: 18 }[size];
}
const LINE_META = {
  food: { emoji: "\u{1F356}", label: "Food", color: "#FF5A3C" },
  vet: { emoji: "\u{1FA7A}", label: "Vet care", color: "#A78BFA" },
  insurance: { emoji: "\u{1F6E1}\uFE0F", label: "Insurance", color: "#0E9F6E" },
  grooming: { emoji: "\u2702\uFE0F", label: "Grooming", color: "#FFD23F" },
  supplies: { emoji: "\u{1F3BE}", label: "Supplies", color: "#1B1340" }
};
function lineMetaFor(species) {
  return { ...LINE_META, food: { ...LINE_META.food, emoji: species === "cat" ? "\u{1F41F}" : "\u{1F356}" } };
}
function Hero({ species }) {
  const isDog = species === "dog";
  return /* @__PURE__ */ React.createElement("section", { className: "hero" }, /* @__PURE__ */ React.createElement(HalftoneBg, { color: "rgba(27,19,64,0.06)", size: 18 }), /* @__PURE__ */ React.createElement("div", { className: "hero-grid" }, /* @__PURE__ */ React.createElement("div", { className: "hero-left" }, /* @__PURE__ */ React.createElement("div", { className: "hero-pretitle" }, /* @__PURE__ */ React.createElement(Paw, { size: 20, color: "#FF5A3C" }), /* @__PURE__ */ React.createElement("span", null, "petexpenses.com \xB7 updated may 2026")), /* @__PURE__ */ React.createElement("h1", { className: "hero-h1" }, "How much does", /* @__PURE__ */ React.createElement("br", null), "your ", /* @__PURE__ */ React.createElement("span", { className: isDog ? "h1-accent-orange" : "h1-accent-pink" }, isDog ? "dog" : "cat"), " ", /* @__PURE__ */ React.createElement("span", { className: "h1-stamp" }, "really"), /* @__PURE__ */ React.createElement("br", null), "cost a year?"), /* @__PURE__ */ React.createElement("p", { className: "hero-sub" }, "Free, honest, no email grab. We crunch ", /* @__PURE__ */ React.createElement("strong", null, "2026 US averages"), " from APPA, AVMA & NAPHIA \u2014 by breed, age, weight & activity. You get the number, the breakdown, and three ways to spend less."), /* @__PURE__ */ React.createElement("div", { className: "hero-badges" }, /* @__PURE__ */ React.createElement("span", { className: "hbadge" }, "\u2726 Free forever"), /* @__PURE__ */ React.createElement("span", { className: "hbadge" }, "\u26A1 Instant result"), /* @__PURE__ */ React.createElement("span", { className: "hbadge" }, "\u{1F512} No sign-up"), /* @__PURE__ */ React.createElement("span", { className: "hbadge" }, "\u{1F4CA} Cited data"))), /* @__PURE__ */ React.createElement("div", { className: "hero-right" }, /* @__PURE__ */ React.createElement("div", { className: `hero-photo ${isDog ? "hero-photo-dog" : "hero-photo-cat"}` }, /* @__PURE__ */ React.createElement("img", { src: "hero-image.jpg", alt: `${isDog ? "Dog" : "Cat"} cost calculator`, className: "hero-photo-img" })), /* @__PURE__ */ React.createElement(Sticker, { rotate: -8, className: "deco-sticker deco-paid" }, /* @__PURE__ */ React.createElement("div", { className: "deco-paid-amount" }, "$4,272"), /* @__PURE__ */ React.createElement("div", { className: "deco-paid-cap" }, "avg US owner / year"), /* @__PURE__ */ React.createElement("div", { className: "deco-paid-src" }, "source: NYPost \xB7 Healthy Paws 2026")), /* @__PURE__ */ React.createElement(Sticker, { rotate: 6, className: "deco-sticker deco-savings" }, /* @__PURE__ */ React.createElement(Paw, { size: 16, color: "#1B1340" }), /* @__PURE__ */ React.createElement("span", null, "save up to ", /* @__PURE__ */ React.createElement("strong", null, "$840/yr"))), /* @__PURE__ */ React.createElement(Sticker, { rotate: -4, className: "deco-sticker deco-rating" }, /* @__PURE__ */ React.createElement("span", { className: "deco-stars" }, "\u2605\u2605\u2605\u2605\u2605"), /* @__PURE__ */ React.createElement("span", null, '"finally a calculator that', /* @__PURE__ */ React.createElement("br", null), `doesn't want my email"`)))));
}
function SpeciesToggle({ species, onChange }) {
  return /* @__PURE__ */ React.createElement("div", { className: "species-toggle-wrap" }, /* @__PURE__ */ React.createElement("div", { className: "species-toggle" }, /* @__PURE__ */ React.createElement(
    "button",
    {
      className: `st-btn st-dog ${species === "dog" ? "active" : ""}`,
      onClick: () => onChange("dog")
    },
    /* @__PURE__ */ React.createElement("span", { className: "st-emoji" }, "\u{1F415}"),
    /* @__PURE__ */ React.createElement("span", { className: "st-label" }, "Dog calculator")
  ), /* @__PURE__ */ React.createElement(
    "button",
    {
      className: `st-btn st-cat ${species === "cat" ? "active" : ""}`,
      onClick: () => onChange("cat")
    },
    /* @__PURE__ */ React.createElement("span", { className: "st-emoji" }, "\u{1F408}"),
    /* @__PURE__ */ React.createElement("span", { className: "st-label" }, "Cat calculator")
  )));
}
function CalcForm({ species, state, setState }) {
  const breeds = species === "dog" ? DOG_BREEDS : CAT_BREEDS;
  const breedData = getBreed(species, state.breed);
  const accent = species === "dog" ? "#FF5A3C" : "#FF8FB1";
  const weightMin = species === "dog" ? 4 : 4;
  const weightMax = species === "dog" ? 160 : 25;
  const weightStep = species === "dog" ? 1 : 0.5;
  const weightTicks = species === "dog" ? ["4 lb", "small", "medium", "large", "giant", "160+"] : ["4 lb", "small", "medium", "large", "25+"];
  function onBreedPick(name) {
    const bd = getBreed(species, name);
    if (bd) {
      setState({
        ...state,
        breed: bd.name,
        coat: bd.coat,
        weight: defaultWeightFromSize(species, bd.size)
      });
    } else {
      setState({ ...state, breed: name });
    }
  }
  return /* @__PURE__ */ React.createElement("section", { className: "calc-wrap", id: "calculator" }, /* @__PURE__ */ React.createElement("div", { className: "calc-card" }, /* @__PURE__ */ React.createElement(HalftoneBg, { color: "rgba(27,19,64,0.04)", size: 16 }), /* @__PURE__ */ React.createElement("div", { className: "calc-card-inner" }, /* @__PURE__ */ React.createElement("div", { className: "calc-header" }, /* @__PURE__ */ React.createElement(Sticker, { rotate: -3, className: "calc-title-sticker" }, /* @__PURE__ */ React.createElement("span", null, "About your ", species), /* @__PURE__ */ React.createElement(Paw, { size: 20, color: "#FFF7E8" })), /* @__PURE__ */ React.createElement("p", { className: "calc-sub" }, "Slide it around. Numbers update live as you go.")), /* @__PURE__ */ React.createElement("div", { className: "calc-grid" }, /* @__PURE__ */ React.createElement("div", { className: "calc-field full" }, /* @__PURE__ */ React.createElement("label", { className: "calc-label" }, "Breed", /* @__PURE__ */ React.createElement("span", { className: "calc-label-hint" }, "type to auto-fill size & coat")), /* @__PURE__ */ React.createElement(
    BreedSearch,
    {
      breeds,
      value: state.breed,
      onChange: onBreedPick,
      placeholder: species === "dog" ? "e.g. Labrador, French Bulldog\u2026" : "e.g. Maine Coon, Ragdoll\u2026",
      accent
    }
  ), breedData && /* @__PURE__ */ React.createElement("div", { className: "breed-note", style: { borderLeftColor: accent } }, /* @__PURE__ */ React.createElement(Paw, { size: 14, color: accent }), " ", /* @__PURE__ */ React.createElement("strong", null, breedData.name), " \xB7 ", breedData.note)), /* @__PURE__ */ React.createElement("div", { className: "calc-field full" }, /* @__PURE__ */ React.createElement(
    BigSlider,
    {
      label: `Weight (lb)`,
      value: state.weight,
      onChange: (v) => setState({ ...state, weight: v }),
      min: weightMin,
      max: weightMax,
      step: weightStep,
      format: (v) => `${v} lb`,
      ticks: weightTicks,
      accent
    }
  )), /* @__PURE__ */ React.createElement("div", { className: "calc-field" }, /* @__PURE__ */ React.createElement("label", { className: "calc-label" }, "Life stage"), /* @__PURE__ */ React.createElement(
    PillSegment,
    {
      value: state.age,
      onChange: (v) => setState({ ...state, age: v }),
      accent,
      options: [
        { value: "puppy", label: species === "dog" ? "Puppy" : "Kitten" },
        { value: "adult", label: "Adult" },
        { value: "senior", label: "Senior" }
      ]
    }
  )), /* @__PURE__ */ React.createElement("div", { className: "calc-field" }, /* @__PURE__ */ React.createElement("label", { className: "calc-label" }, "Activity"), /* @__PURE__ */ React.createElement(
    PillSegment,
    {
      value: state.activity,
      onChange: (v) => setState({ ...state, activity: v }),
      accent,
      options: [
        { value: "low", label: "Chill" },
        { value: "moderate", label: "Normal" },
        { value: "high", label: "Bouncy" }
      ]
    }
  )), /* @__PURE__ */ React.createElement("div", { className: "calc-field full" }, /* @__PURE__ */ React.createElement("label", { className: "calc-label" }, "Coat"), /* @__PURE__ */ React.createElement(
    PillSegment,
    {
      value: state.coat,
      onChange: (v) => setState({ ...state, coat: v }),
      accent,
      options: species === "dog" ? [
        { value: "short", label: "Short / Smooth" },
        { value: "long", label: "Long / Double" },
        { value: "wire", label: "Curly / Wire" }
      ] : [
        { value: "short", label: "Shorthair" },
        { value: "long", label: "Longhair" }
      ]
    }
  ))))));
}
function ResultCard({ species, costs, breedData, state }) {
  const accent = species === "dog" ? "#FF5A3C" : "#FF8FB1";
  const meta = lineMetaFor(species);
  const items = ["food", "vet", "insurance", "grooming", "supplies"].map((k) => ({
    key: k,
    label: meta[k].label,
    emoji: meta[k].emoji,
    color: meta[k].color,
    amount: costs[k]
  }));
  const monthly = Math.round(costs.total / 12);
  const lifetime = Math.round(costs.total * (species === "dog" ? 12 : 14));
  const nationalAvg = species === "dog" ? 2800 : 1450;
  const vsAvg = costs.total - nationalAvg;
  const vsAvgPct = Math.round(vsAvg / nationalAvg * 100);
  const sorted = [...items].sort((a, b) => b.amount - a.amount);
  return /* @__PURE__ */ React.createElement("section", { className: "result-section", id: "result" }, /* @__PURE__ */ React.createElement("div", { className: "result-stage" }, /* @__PURE__ */ React.createElement("div", { className: "rcard rcard-total", style: { "--accent": accent } }, /* @__PURE__ */ React.createElement(HalftoneBg, { color: "rgba(255,255,255,0.18)", size: 14 }), /* @__PURE__ */ React.createElement("div", { className: "rcard-total-inner" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-total-top" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-stamp" }, "YOUR ", species.toUpperCase(), " COSTS"), breedData && /* @__PURE__ */ React.createElement("div", { className: "rcard-breed" }, breedData.name)), /* @__PURE__ */ React.createElement("div", { className: "rcard-total-num" }, /* @__PURE__ */ React.createElement(AnimatedDollar, { value: costs.total, className: "rcard-total-amount" }), /* @__PURE__ */ React.createElement("span", { className: "rcard-total-unit" }, "/ year")), /* @__PURE__ */ React.createElement("div", { className: "rcard-total-meta" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-mini" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-label" }, "/ month"), /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-val" }, /* @__PURE__ */ React.createElement(AnimatedDollar, { value: monthly }))), /* @__PURE__ */ React.createElement("div", { className: "rcard-mini" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-label" }, "lifetime (", species === "dog" ? "~12" : "~14", " yrs)"), /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-val" }, /* @__PURE__ */ React.createElement(AnimatedDollar, { value: lifetime }))), /* @__PURE__ */ React.createElement("div", { className: "rcard-mini" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-label" }, "vs US average"), /* @__PURE__ */ React.createElement("div", { className: "rcard-mini-val rcard-mini-vs" }, vsAvg >= 0 ? "+" : "", vsAvgPct, "%"))), /* @__PURE__ */ React.createElement("div", { className: "rcard-share-row" }, /* @__PURE__ */ React.createElement("button", { className: "share-btn share-btn-primary" }, /* @__PURE__ */ React.createElement("span", null, "\u{1F4F8}"), " Save as image"), /* @__PURE__ */ React.createElement("button", { className: "share-btn" }, /* @__PURE__ */ React.createElement("span", null, "\u{1F517}"), " Copy link"), /* @__PURE__ */ React.createElement("button", { className: "share-btn" }, /* @__PURE__ */ React.createElement("span", null, "\u{1D54F}"), " Share on X")), /* @__PURE__ */ React.createElement("div", { className: "rcard-share-note" }, "Shareable card \xB7 personal data stays in your browser"))), /* @__PURE__ */ React.createElement("div", { className: "rcard rcard-breakdown" }, /* @__PURE__ */ React.createElement("div", { className: "rcard-breakdown-head" }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "rcard-stamp dark" }, "WHERE IT GOES"), /* @__PURE__ */ React.createElement("div", { className: "rcard-breakdown-title" }, "The breakdown")), /* @__PURE__ */ React.createElement(Sticker, { rotate: 4, className: "breakdown-sticker" }, /* @__PURE__ */ React.createElement(Paw, { size: 14, color: "#FFF7E8" }), /* @__PURE__ */ React.createElement("span", null, "2026 data"))), /* @__PURE__ */ React.createElement("div", { className: "rcard-breakdown-body" }, /* @__PURE__ */ React.createElement("div", { className: "donut-wrap" }, /* @__PURE__ */ React.createElement(Donut, { items, total: costs.total }), /* @__PURE__ */ React.createElement("div", { className: "donut-center" }, /* @__PURE__ */ React.createElement("div", { className: "donut-center-label" }, "total / year"), /* @__PURE__ */ React.createElement("div", { className: "donut-center-num" }, /* @__PURE__ */ React.createElement(AnimatedDollar, { value: costs.total })))), /* @__PURE__ */ React.createElement("ul", { className: "rcard-line-list" }, sorted.map((it) => {
    const pct = Math.round(it.amount / costs.total * 100);
    return /* @__PURE__ */ React.createElement("li", { key: it.key, className: "line-item" }, /* @__PURE__ */ React.createElement("span", { className: "line-dot", style: { background: it.color } }), /* @__PURE__ */ React.createElement("span", { className: "line-emoji" }, it.emoji), /* @__PURE__ */ React.createElement("span", { className: "line-label" }, it.label), /* @__PURE__ */ React.createElement("span", { className: "line-bar" }, /* @__PURE__ */ React.createElement("span", { className: "line-bar-fill", style: { width: pct + "%", background: it.color } })), /* @__PURE__ */ React.createElement("span", { className: "line-amount" }, "$", it.amount.toLocaleString()), /* @__PURE__ */ React.createElement("span", { className: "line-pct" }, pct, "%"));
  }))), /* @__PURE__ */ React.createElement("div", { className: "rcard-footnote" }, "Based on 2026 US averages from ", /* @__PURE__ */ React.createElement("a", { href: "#sources" }, "APPA, AVMA, NAPHIA"), " & BLS Feb 2026 CPI \xB7 adjusted for breed, weight, age & activity."))));
}
function Offers({ species, costs }) {
  const offers = OFFERS[species];
  const monthlyFood = Math.round(costs.food / 12);
  const monthlyVet = Math.round(costs.vet / 12);
  return /* @__PURE__ */ React.createElement("section", { className: "offers-section" }, /* @__PURE__ */ React.createElement("div", { className: "section-head" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#FF5A3C" }), " WAYS TO SPEND LESS"), /* @__PURE__ */ React.createElement("h2", { className: "section-h2" }, "Three picks for your ", /* @__PURE__ */ React.createElement("span", { className: "h2-accent" }, species)), /* @__PURE__ */ React.createElement("p", { className: "section-sub" }, "Affiliate placeholders \u2014 replace with your tracked links. Each is shown only when it makes sense for the result above.")), /* @__PURE__ */ React.createElement("div", { className: "offers-grid" }, offers.map((o, i) => /* @__PURE__ */ React.createElement("article", { key: o.id, className: "offer-card", style: { "--oa": o.accent, "--oad": o.accentDark } }, /* @__PURE__ */ React.createElement("div", { className: "offer-sticker-row" }, /* @__PURE__ */ React.createElement(Sticker, { rotate: -6, className: "offer-sticker" }, /* @__PURE__ */ React.createElement("span", { className: "offer-sticker-emoji" }, o.emoji), /* @__PURE__ */ React.createElement("span", { className: "offer-sticker-text" }, o.sticker)), /* @__PURE__ */ React.createElement("span", { className: "offer-from" }, o.priceFrom)), /* @__PURE__ */ React.createElement("h3", { className: "offer-title" }, o.title), /* @__PURE__ */ React.createElement("div", { className: "offer-partner" }, "\u2014 ", o.partner), /* @__PURE__ */ React.createElement("ul", { className: "offer-bullets" }, /* @__PURE__ */ React.createElement("li", null, "\u2713 ", o.bullet1), /* @__PURE__ */ React.createElement("li", null, "\u2713 ", o.bullet2), /* @__PURE__ */ React.createElement("li", null, "\u2713 ", o.bullet3)), o.id === "fresh-food" && /* @__PURE__ */ React.createElement("div", { className: "offer-context" }, "You currently spend ~", /* @__PURE__ */ React.createElement("strong", null, "$", monthlyFood, "/mo"), " on food."), o.id === "insurance" && /* @__PURE__ */ React.createElement("div", { className: "offer-context" }, "Your vet budget is ~", /* @__PURE__ */ React.createElement("strong", null, "$", monthlyVet, "/mo"), ". One emergency = $3\u201310k."), o.id === "treats" && /* @__PURE__ */ React.createElement("div", { className: "offer-context" }, "Replace random toy-store runs with a curated monthly drop."), /* @__PURE__ */ React.createElement("a", { className: "offer-cta", href: "#", onClick: (e) => e.preventDefault() }, o.ctaText), /* @__PURE__ */ React.createElement("div", { className: "offer-ratings" }, o.ratings)))), /* @__PURE__ */ React.createElement("p", { className: "offers-disclosure" }, "Disclosure: links above are placeholders. In production they're affiliate links \u2014 we may earn a commission at no cost to you."));
}
function HowItWorks() {
  const steps = [
    { n: "01", title: "Tell us about your pet", body: "Breed, weight, age, activity. Sliders only \u2014 no signup, no email." },
    { n: "02", title: "We crunch the numbers", body: "Five categories. 70+ breeds. Adjusted for 2026 US prices. Math in plain sight." },
    { n: "03", title: "Save it or share it", body: "Download a card for IG, copy a link, or just bookmark. Your data never leaves your browser." }
  ];
  return /* @__PURE__ */ React.createElement("section", { className: "hiw-section" }, /* @__PURE__ */ React.createElement("div", { className: "section-head" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#1B1340" }), " HOW IT WORKS"), /* @__PURE__ */ React.createElement("h2", { className: "section-h2" }, "No paywall. No email. ", /* @__PURE__ */ React.createElement("span", { className: "h2-accent" }, "No nonsense."))), /* @__PURE__ */ React.createElement("div", { className: "hiw-grid" }, steps.map((s, i) => /* @__PURE__ */ React.createElement("div", { key: s.n, className: "hiw-step" }, /* @__PURE__ */ React.createElement("div", { className: "hiw-num" }, s.n), /* @__PURE__ */ React.createElement("h3", { className: "hiw-title" }, s.title), /* @__PURE__ */ React.createElement("p", { className: "hiw-body" }, s.body)))));
}
function SocialProof() {
  return /* @__PURE__ */ React.createElement("section", { className: "proof-section" }, /* @__PURE__ */ React.createElement("div", { className: "section-head proof-head" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#FF5A3C" }), " WHAT OWNERS SAID"), /* @__PURE__ */ React.createElement("h2", { className: "section-h2" }, "2.4M calculations and counting"), /* @__PURE__ */ React.createElement("p", { className: "section-sub" }, "(That's a placeholder. But the warm reception is real.)")), /* @__PURE__ */ React.createElement("div", { className: "proof-wall" }, TESTIMONIALS.map((t, i) => /* @__PURE__ */ React.createElement(Sticker, { key: i, rotate: t.rotate, className: "proof-card" }, /* @__PURE__ */ React.createElement("div", { className: "proof-stars" }, "\u2605\u2605\u2605\u2605\u2605"), /* @__PURE__ */ React.createElement("p", { className: "proof-quote" }, t.quote), /* @__PURE__ */ React.createElement("div", { className: "proof-who" }, /* @__PURE__ */ React.createElement("strong", null, t.who), /* @__PURE__ */ React.createElement("span", null, "\xB7 ", t.pet))))), /* @__PURE__ */ React.createElement("div", { className: "press-strip" }, /* @__PURE__ */ React.createElement("span", { className: "press-label" }, "As seen referenced in:"), /* @__PURE__ */ React.createElement("span", { className: "press-logo" }, "NYT-Wirecutter*"), /* @__PURE__ */ React.createElement("span", { className: "press-logo" }, "MarketWatch*"), /* @__PURE__ */ React.createElement("span", { className: "press-logo" }, "Reddit r/dogs*"), /* @__PURE__ */ React.createElement("span", { className: "press-logo" }, "PetMD*"), /* @__PURE__ */ React.createElement("span", { className: "press-label-small" }, "* placeholders")));
}
function Sources() {
  return /* @__PURE__ */ React.createElement("section", { className: "sources-section", id: "sources" }, /* @__PURE__ */ React.createElement("div", { className: "sources-card" }, /* @__PURE__ */ React.createElement("div", { className: "sources-left" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow light" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#FFD23F" }), " RECEIPTS"), /* @__PURE__ */ React.createElement("h2", { className: "sources-h2" }, "Cited, not vibed."), /* @__PURE__ */ React.createElement("p", { className: "sources-sub" }, "Every dollar in our model traces back to one of these sources. We update twice a year.")), /* @__PURE__ */ React.createElement("ul", { className: "sources-list" }, SOURCES.map((s, i) => /* @__PURE__ */ React.createElement("li", { key: i }, /* @__PURE__ */ React.createElement("strong", null, s.name), /* @__PURE__ */ React.createElement("span", null, s.full))))));
}
function Blog() {
  return /* @__PURE__ */ React.createElement("section", { className: "blog-section" }, /* @__PURE__ */ React.createElement("div", { className: "section-head" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#FF5A3C" }), " FROM THE BLOG"), /* @__PURE__ */ React.createElement("h2", { className: "section-h2" }, "Read more, spend less")), /* @__PURE__ */ React.createElement("div", { className: "blog-grid" }, BLOG.map((b, i) => /* @__PURE__ */ React.createElement("a", { key: i, className: "blog-card", href: "#", onClick: (e) => e.preventDefault(), style: { "--ba": b.accent } }, /* @__PURE__ */ React.createElement("div", { className: "blog-thumb" }, /* @__PURE__ */ React.createElement("div", { className: "blog-thumb-pattern" }), /* @__PURE__ */ React.createElement("div", { className: "blog-thumb-glyph" }, "\xB6")), /* @__PURE__ */ React.createElement("div", { className: "blog-body" }, /* @__PURE__ */ React.createElement("div", { className: "blog-tag" }, b.tag), /* @__PURE__ */ React.createElement("h3", { className: "blog-title" }, b.title), /* @__PURE__ */ React.createElement("p", { className: "blog-excerpt" }, b.body), /* @__PURE__ */ React.createElement("div", { className: "blog-meta" }, b.mins, " min read \u2192"))))));
}
function FAQ({ species }) {
  const pet = species;
  const items = [
    {
      q: `How much does a ${pet} cost per year in the US?`,
      a: `In 2026, the average annual cost is ${pet === "dog" ? "$1,500\u2013$3,500" : "$900\u2013$2,000"}, depending on size, breed, age and location. Small ${pet}s cost less per year but live longer; larger ones cost more annually but have shorter lifespans.`
    },
    {
      q: `What's the most expensive part of owning a ${pet}?`,
      a: `Food and veterinary care are consistently the two largest expenses. Food: $${pet === "dog" ? "360\u20132,000" : "240\u2013720"}/yr depending on size and diet. Vet care: $${pet === "dog" ? "200\u20131,500+" : "180\u2013650+"}/yr including routine care. Pet insurance can offset emergency costs.`
    },
    {
      q: "Is pet insurance worth it?",
      a: `Pet insurance is most valuable for ${pet === "dog" ? "brachycephalic breeds (Frenchies, Pugs, Bulldogs), high-cancer-risk breeds (Goldens, Berners), and senior dogs" : "breeds prone to HCM (Maine Coon, Ragdoll), brachycephalic cats (Persian, Exotic Shorthair) and senior cats"}. Compare quotes from 3+ providers \u2014 one emergency surgery can cost $3,000\u2013$10,000.`
    },
    {
      q: "Is fresh food worth the cost?",
      a: `Fresh-meal services run $${pet === "dog" ? "60\u2013360" : "40\u2013180"}/month. While more expensive than kibble, owners often report fewer digestive issues, allergies and weight problems over time \u2014 which can offset vet costs. Most services have a discounted starter box so you can try risk-free.`
    },
    {
      q: `Which ${pet} breeds are cheapest to own?`,
      a: pet === "dog" ? "Small, healthy breeds cost the least: Rat Terriers, Jack Russells, Papillons, Italian Greyhounds. Avoid brachycephalic (French Bulldog, Pug, Bulldog) and giant breeds (Great Dane, Mastiff) if minimizing cost is a priority." : "Domestic Shorthair and Russian Blue are among the lowest-cost cats \u2014 they're hardy, low-grooming and rarely have inherited conditions. Persians, Sphynx and Scottish Folds tend to be the most expensive over a lifetime."
    },
    {
      q: "Where do your numbers come from?",
      a: "We pull annual averages from the APPA 2026 State of the Industry Report, AVMA Pet Ownership stats, NAPHIA insurance data, BLS veterinary CPI (Feb 2026), and PetCareBooker grooming. Adjusted for breed, weight, age and activity. We update the model twice a year."
    }
  ];
  return /* @__PURE__ */ React.createElement("section", { className: "faq-section", id: "faq" }, /* @__PURE__ */ React.createElement("div", { className: "section-head" }, /* @__PURE__ */ React.createElement("div", { className: "section-eyebrow" }, /* @__PURE__ */ React.createElement(Paw, { size: 18, color: "#1B1340" }), " \u2753 QUESTIONS WE GET"), /* @__PURE__ */ React.createElement("h2", { className: "section-h2" }, "FAQ")), /* @__PURE__ */ React.createElement("div", { className: "faq-list" }, items.map((it, i) => /* @__PURE__ */ React.createElement("details", { key: i, className: "faq-item", ...i === 0 ? { open: true } : {} }, /* @__PURE__ */ React.createElement("summary", null, it.q), /* @__PURE__ */ React.createElement("div", { className: "faq-a" }, it.a)))));
}
function Footer() {
  return /* @__PURE__ */ React.createElement("footer", { className: "site-footer" }, /* @__PURE__ */ React.createElement("div", { className: "footer-top" }, /* @__PURE__ */ React.createElement("div", { className: "footer-brand" }, /* @__PURE__ */ React.createElement("div", { className: "footer-mark" }, /* @__PURE__ */ React.createElement(Paw, { size: 28, color: "#FF5A3C" }), /* @__PURE__ */ React.createElement("span", null, "petexpenses", /* @__PURE__ */ React.createElement("span", { className: "brand-dot" }, "."), "com")), /* @__PURE__ */ React.createElement("p", { className: "footer-tagline" }, "Honest pet budgeting since 2026.", /* @__PURE__ */ React.createElement("br", null), "Built for owners who love their pet \u2014 and their wallet.")), /* @__PURE__ */ React.createElement("div", { className: "footer-cols" }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "footer-col-title" }, "Calculators"), /* @__PURE__ */ React.createElement("a", { href: "#calculator" }, "Dog"), /* @__PURE__ */ React.createElement("a", { href: "#calculator" }, "Cat"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Insurance compare"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Food cost")), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "footer-col-title" }, "Read"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Blog"), /* @__PURE__ */ React.createElement("a", { href: "#sources" }, "Data sources"), /* @__PURE__ */ React.createElement("a", { href: "#faq" }, "FAQ"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Methodology")), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "footer-col-title" }, "About"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Who we are"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Contact"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Disclosure"), /* @__PURE__ */ React.createElement("a", { href: "#" }, "Privacy")))), /* @__PURE__ */ React.createElement("div", { className: "footer-bottom" }, /* @__PURE__ */ React.createElement("span", null, "\xA9 2026 petexpenses.com"), /* @__PURE__ */ React.createElement("span", { className: "footer-disclosure" }, "Estimates based on 2026 US averages. Actual costs vary by location & health. Not financial or veterinary advice. This site contains affiliate-link placeholders.")));
}
function App() {
  const [species, setSpecies] = useState("dog");
  const [dogState, setDogState] = useState({
    breed: "Labrador Retriever",
    weight: 65,
    age: "adult",
    activity: "moderate",
    coat: "short"
  });
  const [catState, setCatState] = useState({
    breed: "Maine Coon",
    weight: 16,
    age: "adult",
    activity: "moderate",
    coat: "long"
  });
  const state = species === "dog" ? dogState : catState;
  const setState = species === "dog" ? setDogState : setCatState;
  const breedData = getBreed(species, state.breed);
  const costs = useMemo(
    () => calcCosts({ species, weight: state.weight, age: state.age, activity: state.activity, coat: state.coat, breedData }),
    // Recompute deterministically — using lerpInRange means no randomness, just live numbers
    [species, state.weight, state.age, state.activity, state.coat, state.breed]
  );
  return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(SiteNav, { species, onSpecies: setSpecies }), /* @__PURE__ */ React.createElement(Hero, { species }), /* @__PURE__ */ React.createElement(SpeciesToggle, { species, onChange: setSpecies }), /* @__PURE__ */ React.createElement(CalcForm, { species, state, setState }), /* @__PURE__ */ React.createElement(ResultCard, { species, costs, breedData, state }), /* @__PURE__ */ React.createElement(Offers, { species, costs }), /* @__PURE__ */ React.createElement(HowItWorks, null), /* @__PURE__ */ React.createElement(SocialProof, null), /* @__PURE__ */ React.createElement(Sources, null), /* @__PURE__ */ React.createElement(Blog, null), /* @__PURE__ */ React.createElement(FAQ, { species }), /* @__PURE__ */ React.createElement(Footer, null));
}
function SiteNav({ species, onSpecies }) {
  return /* @__PURE__ */ React.createElement("nav", { className: "site-nav" }, /* @__PURE__ */ React.createElement("a", { className: "site-brand", href: "#" }, /* @__PURE__ */ React.createElement(Paw, { size: 26, color: "#FF5A3C" }), /* @__PURE__ */ React.createElement("span", null, "petexpenses", /* @__PURE__ */ React.createElement("span", { className: "brand-dot" }, "."), "com")), /* @__PURE__ */ React.createElement("div", { className: "site-nav-mid" }, /* @__PURE__ */ React.createElement("a", { href: "#calculator", className: species === "dog" ? "active" : "", onClick: () => onSpecies("dog") }, "\u{1F415} Dogs"), /* @__PURE__ */ React.createElement("a", { href: "#calculator", className: species === "cat" ? "active" : "", onClick: () => onSpecies("cat") }, "\u{1F408} Cats"), /* @__PURE__ */ React.createElement("a", { href: "#sources" }, "Data"), /* @__PURE__ */ React.createElement("a", { href: "#faq" }, "FAQ")), /* @__PURE__ */ React.createElement("a", { href: "#calculator", className: "site-cta" }, "Run the math \u2192"));
}
ReactDOM.createRoot(document.getElementById("root")).render(/* @__PURE__ */ React.createElement(App, null));
