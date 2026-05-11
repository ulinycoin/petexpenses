// ───────────────────────────────────────────────────────────────
// PetExpenses — main React app
// ───────────────────────────────────────────────────────────────
const { DOG_BREEDS, CAT_BREEDS, DOG_COSTS, CAT_COSTS, AGE_MULT, ACTIVITY_MULT, OFFERS, SOURCES, BLOG, TESTIMONIALS } = window.PET_DATA;

// ── helpers ───────────────────────────────────────────────────
function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function midOf(arr) { return Math.round((arr[0] + arr[1]) / 2); }
function lerpInRange(range, t) {
  // t in [0,1] maps across the min..max of the cost range
  return Math.round(range[0] + (range[1] - range[0]) * t);
}

// Map a weight (lb) to size bucket
function sizeFromWeight(species, weight) {
  if (species === 'dog') {
    if (weight < 20) return 'small';
    if (weight < 50) return 'medium';
    if (weight < 80) return 'large';
    return 'giant';
  } else {
    if (weight < 8)  return 'small';
    if (weight < 14) return 'medium';
    return 'large';
  }
}

// Position within range (0..1) based on weight inside its bucket
function intraT(species, weight) {
  if (species === 'dog') {
    if (weight < 20) return clamp((weight - 4) / (20 - 4), 0, 1);
    if (weight < 50) return clamp((weight - 20) / (50 - 20), 0, 1);
    if (weight < 80) return clamp((weight - 50) / (80 - 50), 0, 1);
    return clamp((weight - 80) / (160 - 80), 0, 1);
  } else {
    if (weight < 8)  return clamp((weight - 4) / (8 - 4), 0, 1);
    if (weight < 14) return clamp((weight - 8) / (14 - 8), 0, 1);
    return clamp((weight - 14) / (25 - 14), 0, 1);
  }
}

// ── core calc ────────────────────────────────────────────────
function calcCosts({ species, weight, age, activity, coat, breedData }) {
  const size = sizeFromWeight(species, weight);
  const t = intraT(species, weight);
  const tbl = species === 'dog' ? DOG_COSTS : CAT_COSTS;
  const bm = breedData || { vetMult: 1, insMult: 1, foodMult: 1, groomMult: 1 };

  let food      = lerpInRange(tbl.food[size], t);
  let vet       = lerpInRange(tbl.vet[size], t);
  let insurance = lerpInRange(tbl.insurance[size], t);
  const groomT  = tbl.grooming[coat] || tbl.grooming.short;
  let grooming  = lerpInRange(groomT[size], t);
  let supplies  = lerpInRange(tbl.supplies[size], t);

  food      = Math.round(food      * (bm.foodMult  ?? 1));
  vet       = Math.round(vet       * (bm.vetMult   ?? 1));
  insurance = Math.round(insurance * (bm.insMult   ?? 1));
  grooming  = Math.round(grooming  * (bm.groomMult ?? 1));

  const am = AGE_MULT[age] || {};
  if (am.vet) vet = Math.round(vet * am.vet);
  if (am.insurance) insurance = Math.round(insurance * am.insurance);
  if (am.supplies) supplies = Math.round(supplies * am.supplies);

  const acm = ACTIVITY_MULT[activity] || {};
  if (acm.food) food = Math.round(food * acm.food);
  if (acm.supplies) supplies = Math.round(supplies * acm.supplies);

  return {
    food, vet, insurance, grooming, supplies,
    total: food + vet + insurance + grooming + supplies,
    size,
  };
}

// ── breed lookup ─────────────────────────────────────────────
function getBreed(species, name) {
  if (!name) return null;
  const map = species === 'dog' ? DOG_BREEDS : CAT_BREEDS;
  const key = Object.keys(map).find((k) => k.toLowerCase() === name.toLowerCase());
  if (!key) return null;
  const [size, coat, vetMult, insMult, foodMult, groomMult, note] = map[key];
  return { name: key, size, coat, vetMult, insMult, foodMult, groomMult, note };
}

// ── default weight from breed size bucket ────────────────────
function defaultWeightFromSize(species, size) {
  if (species === 'dog') return ({ small: 12, medium: 35, large: 65, giant: 110 })[size];
  return ({ small: 6, medium: 11, large: 18 })[size];
}

// ── line item meta (color, emoji, label) ─────────────────────
const LINE_META = {
  food:      { emoji: '🍖', label: 'Food',      color: '#FF5A3C' },
  vet:       { emoji: '🩺', label: 'Vet care',  color: '#A78BFA' },
  insurance: { emoji: '🛡️', label: 'Insurance', color: '#0E9F6E' },
  grooming:  { emoji: '✂️', label: 'Grooming',  color: '#FFD23F' },
  supplies:  { emoji: '🎾', label: 'Supplies',  color: '#1B1340' },
};

// ── catty version of food emoji ──────────────────────────────
function lineMetaFor(species) {
  return { ...LINE_META, food: { ...LINE_META.food, emoji: species === 'cat' ? '🐟' : '🍖' } };
}

// ─────────────────────────────────────────────────────────────
// HERO
// ─────────────────────────────────────────────────────────────
function Hero({ species }) {
  const isDog = species === 'dog';
  return (
    <section className="hero">
      <HalftoneBg color="rgba(27,19,64,0.06)" size={18} />
      <div className="hero-grid">
        <div className="hero-left">
          <div className="hero-pretitle">
            <Paw size={20} color="#FF5A3C" />
            <span>petexpenses.com · updated may 2026</span>
          </div>
          <h1 className="hero-h1">
            How much does<br/>
            your <span className={isDog ? 'h1-accent-orange' : 'h1-accent-pink'}>
              {isDog ? 'dog' : 'cat'}
            </span> <span className="h1-stamp">really</span><br/>
            cost a year?
          </h1>
          <p className="hero-sub">
            Free, honest, no email grab. We crunch <strong>2026 US averages</strong> from APPA, AVMA &amp; NAPHIA — by breed, age, weight &amp; activity. You get the number, the breakdown, and three ways to spend less.
          </p>
          <div className="hero-badges">
            <span className="hbadge">✦ Free forever</span>
            <span className="hbadge">⚡ Instant result</span>
            <span className="hbadge">🔒 No sign-up</span>
            <span className="hbadge">📊 Cited data</span>
          </div>
        </div>

        <div className="hero-right">
          {/* Big rounded photo placeholder */}
          <div className={`hero-photo ${isDog ? 'hero-photo-dog' : 'hero-photo-cat'}`}>
            <img src="hero-image.jpg" alt={`${isDog ? 'Dog' : 'Cat'} cost calculator`} className="hero-photo-img" fetchpriority="high" width="643" height="804" />
          </div>

          {/* Decorative stickers */}
          <Sticker rotate={-8} className="deco-sticker deco-paid">
            <div className="deco-paid-amount">$4,272</div>
            <div className="deco-paid-cap">avg US owner / year</div>
            <div className="deco-paid-src">source: NYPost · Healthy Paws 2026</div>
          </Sticker>

          <Sticker rotate={6} className="deco-sticker deco-savings">
            <Paw size={16} color="#1B1340" />
            <span>save up to <strong>$840/yr</strong></span>
          </Sticker>

          <Sticker rotate={-4} className="deco-sticker deco-rating">
            <span className="deco-stars">★★★★★</span>
            <span>"finally a calculator that<br/>doesn't want my email"</span>
          </Sticker>
        </div>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// SPECIES TOGGLE
// ─────────────────────────────────────────────────────────────
function SpeciesToggle({ species, onChange }) {
  return (
    <div className="species-toggle-wrap">
      <div className="species-toggle">
        <button
          className={`st-btn st-dog ${species === 'dog' ? 'active' : ''}`}
          onClick={() => onChange('dog')}
        >
          <span className="st-emoji">🐕</span>
          <span className="st-label">Dog calculator</span>
        </button>
        <button
          className={`st-btn st-cat ${species === 'cat' ? 'active' : ''}`}
          onClick={() => onChange('cat')}
        >
          <span className="st-emoji">🐈</span>
          <span className="st-label">Cat calculator</span>
        </button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// CALCULATOR FORM
// ─────────────────────────────────────────────────────────────
function CalcForm({ species, state, setState }) {
  const breeds = species === 'dog' ? DOG_BREEDS : CAT_BREEDS;
  const breedData = getBreed(species, state.breed);
  const accent = species === 'dog' ? '#FF5A3C' : '#FF8FB1';

  const weightMin = species === 'dog' ? 4 : 4;
  const weightMax = species === 'dog' ? 160 : 25;
  const weightStep = species === 'dog' ? 1 : 0.5;
  const weightTicks = species === 'dog'
    ? ['4 lb', 'small', 'medium', 'large', 'giant', '160+']
    : ['4 lb', 'small', 'medium', 'large', '25+'];

  // When breed picked, snap size+coat to breed defaults, default weight
  function onBreedPick(name) {
    const bd = getBreed(species, name);
    if (bd) {
      setState({
        ...state,
        breed: bd.name,
        coat: bd.coat,
        weight: defaultWeightFromSize(species, bd.size),
      });
    } else {
      setState({ ...state, breed: name });
    }
  }

  return (
    <section className="calc-wrap" id="calculator">
      <div className="calc-card">
        <HalftoneBg color="rgba(27,19,64,0.04)" size={16} />
        <div className="calc-card-inner">
          <div className="calc-header">
            <Sticker rotate={-3} className="calc-title-sticker">
              <span>About your {species}</span>
              <Paw size={20} color="#FFF7E8" />
            </Sticker>
            <p className="calc-sub">Slide it around. Numbers update live as you go.</p>
          </div>

          <div className="calc-grid">
            {/* BREED */}
            <div className="calc-field full">
              <label className="calc-label">
                Breed
                <span className="calc-label-hint">type to auto-fill size &amp; coat</span>
              </label>
              <BreedSearch
                breeds={breeds}
                value={state.breed}
                onChange={onBreedPick}
                placeholder={species === 'dog' ? 'e.g. Labrador, French Bulldog…' : 'e.g. Maine Coon, Ragdoll…'}
                accent={accent}
              />
              {breedData && (
                <div className="breed-note" style={{ borderLeftColor: accent }}>
                  <Paw size={14} color={accent} /> <strong>{breedData.name}</strong> · {breedData.note}
                </div>
              )}
            </div>

            {/* WEIGHT */}
            <div className="calc-field full">
              <BigSlider
                label={`Weight (lb)`}
                value={state.weight}
                onChange={(v) => setState({ ...state, weight: v })}
                min={weightMin} max={weightMax} step={weightStep}
                format={(v) => `${v} lb`}
                ticks={weightTicks}
                accent={accent}
              />
            </div>

            {/* AGE */}
            <div className="calc-field">
              <label className="calc-label">Life stage</label>
              <PillSegment
                value={state.age}
                onChange={(v) => setState({ ...state, age: v })}
                accent={accent}
                options={[
                  { value: 'puppy',  label: species === 'dog' ? 'Puppy' : 'Kitten' },
                  { value: 'adult',  label: 'Adult' },
                  { value: 'senior', label: 'Senior' },
                ]}
              />
            </div>

            {/* ACTIVITY */}
            <div className="calc-field">
              <label className="calc-label">Activity</label>
              <PillSegment
                value={state.activity}
                onChange={(v) => setState({ ...state, activity: v })}
                accent={accent}
                options={[
                  { value: 'low',      label: 'Chill' },
                  { value: 'moderate', label: 'Normal' },
                  { value: 'high',     label: 'Bouncy' },
                ]}
              />
            </div>

            {/* COAT */}
            <div className="calc-field full">
              <label className="calc-label">Coat</label>
              <PillSegment
                value={state.coat}
                onChange={(v) => setState({ ...state, coat: v })}
                accent={accent}
                options={species === 'dog' ? [
                  { value: 'short', label: 'Short / Smooth' },
                  { value: 'long',  label: 'Long / Double' },
                  { value: 'wire',  label: 'Curly / Wire' },
                ] : [
                  { value: 'short', label: 'Shorthair' },
                  { value: 'long',  label: 'Longhair' },
                ]}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// RESULT CARD (the shareable hero of the page)
// ─────────────────────────────────────────────────────────────
function ResultCard({ species, costs, breedData, state }) {
  const accent = species === 'dog' ? '#FF5A3C' : '#FF8FB1';
  const meta = lineMetaFor(species);
  const items = ['food', 'vet', 'insurance', 'grooming', 'supplies'].map((k) => ({
    key: k,
    label: meta[k].label,
    emoji: meta[k].emoji,
    color: meta[k].color,
    amount: costs[k],
  }));
  const monthly = Math.round(costs.total / 12);
  const lifetime = Math.round(costs.total * (species === 'dog' ? 12 : 14));

  const nationalAvg = species === 'dog' ? 2800 : 1450;
  const vsAvg = costs.total - nationalAvg;
  const vsAvgPct = Math.round((vsAvg / nationalAvg) * 100);

  // Top categories (sorted desc) for the breakdown
  const sorted = [...items].sort((a, b) => b.amount - a.amount);

  return (
    <section className="result-section" id="result">
      <div className="result-stage">

        {/* ─── BIG NUMBER CARD ─── */}
        <div className="rcard rcard-total" style={{ '--accent': accent }}>
          <HalftoneBg color="rgba(255,255,255,0.18)" size={14} />
          <div className="rcard-total-inner">
            <div className="rcard-total-top">
              <div className="rcard-stamp">YOUR {species.toUpperCase()} COSTS</div>
              {breedData && <div className="rcard-breed">{breedData.name}</div>}
            </div>
            <div className="rcard-total-num">
              <AnimatedDollar value={costs.total} className="rcard-total-amount" />
              <span className="rcard-total-unit">/ year</span>
            </div>
            <div className="rcard-total-meta">
              <div className="rcard-mini">
                <div className="rcard-mini-label">/ month</div>
                <div className="rcard-mini-val"><AnimatedDollar value={monthly} /></div>
              </div>
              <div className="rcard-mini">
                <div className="rcard-mini-label">lifetime ({species === 'dog' ? '~12' : '~14'} yrs)</div>
                <div className="rcard-mini-val"><AnimatedDollar value={lifetime} /></div>
              </div>
              <div className="rcard-mini">
                <div className="rcard-mini-label">vs US average</div>
                <div className="rcard-mini-val rcard-mini-vs">
                  {vsAvg >= 0 ? '+' : ''}{vsAvgPct}%
                </div>
              </div>
            </div>

            <div className="rcard-share-row">
              <button className="share-btn share-btn-primary">
                <span>📸</span> Save as image
              </button>
              <button className="share-btn">
                <span>🔗</span> Copy link
              </button>
              <button className="share-btn">
                <span>𝕏</span> Share on X
              </button>
            </div>
            <div className="rcard-share-note">
              Shareable card · personal data stays in your browser
            </div>
          </div>
        </div>

        {/* ─── BREAKDOWN CARD ─── */}
        <div className="rcard rcard-breakdown">
          <div className="rcard-breakdown-head">
            <div>
              <div className="rcard-stamp dark">WHERE IT GOES</div>
              <div className="rcard-breakdown-title">The breakdown</div>
            </div>
            <Sticker rotate={4} className="breakdown-sticker">
              <Paw size={14} color="#FFF7E8" />
              <span>2026 data</span>
            </Sticker>
          </div>

          <div className="rcard-breakdown-body">
            <div className="donut-wrap">
              <Donut items={items} total={costs.total} />
              <div className="donut-center">
                <div className="donut-center-label">total / year</div>
                <div className="donut-center-num">
                  <AnimatedDollar value={costs.total} />
                </div>
              </div>
            </div>

            <ul className="rcard-line-list">
              {sorted.map((it) => {
                const pct = Math.round((it.amount / costs.total) * 100);
                return (
                  <li key={it.key} className="line-item">
                    <span className="line-dot" style={{ background: it.color }} />
                    <span className="line-emoji">{it.emoji}</span>
                    <span className="line-label">{it.label}</span>
                    <span className="line-bar">
                      <span className="line-bar-fill" style={{ width: pct + '%', background: it.color }} />
                    </span>
                    <span className="line-amount">${it.amount.toLocaleString()}</span>
                    <span className="line-pct">{pct}%</span>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="rcard-footnote">
            Based on 2026 US averages from <a href="#sources">APPA, AVMA, NAPHIA</a> &amp; BLS Feb 2026 CPI · adjusted for breed, weight, age &amp; activity.
          </div>
        </div>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// OFFERS (stubs)
// ─────────────────────────────────────────────────────────────
function Offers({ species, costs }) {
  const offers = OFFERS[species];
  const monthlyFood = Math.round(costs.food / 12);
  const monthlyVet  = Math.round(costs.vet / 12);
  return (
    <section className="offers-section">
      <div className="section-head">
        <div className="section-eyebrow">
          <Paw size={18} color="#FF5A3C" /> WAYS TO SPEND LESS
        </div>
        <h2 className="section-h2">Three picks for your <span className="h2-accent">{species}</span></h2>
        <p className="section-sub">Affiliate placeholders — replace with your tracked links. Each is shown only when it makes sense for the result above.</p>
      </div>

      <div className="offers-grid">
        {offers.map((o, i) => (
          <article key={o.id} className="offer-card" style={{ '--oa': o.accent, '--oad': o.accentDark }}>
            <div className="offer-sticker-row">
              <Sticker rotate={-6} className="offer-sticker">
                <span className="offer-sticker-emoji">{o.emoji}</span>
                <span className="offer-sticker-text">{o.sticker}</span>
              </Sticker>
              <span className="offer-from">{o.priceFrom}</span>
            </div>
            <h3 className="offer-title">{o.title}</h3>
            <div className="offer-partner">— {o.partner}</div>
            <ul className="offer-bullets">
              <li>✓ {o.bullet1}</li>
              <li>✓ {o.bullet2}</li>
              <li>✓ {o.bullet3}</li>
            </ul>
            {o.id === 'fresh-food' && (
              <div className="offer-context">
                You currently spend ~<strong>${monthlyFood}/mo</strong> on food.
              </div>
            )}
            {o.id === 'insurance' && (
              <div className="offer-context">
                Your vet budget is ~<strong>${monthlyVet}/mo</strong>. One emergency = $3–10k.
              </div>
            )}
            {o.id === 'treats' && (
              <div className="offer-context">
                Replace random toy-store runs with a curated monthly drop.
              </div>
            )}
            <a className="offer-cta" href="#" onClick={(e) => e.preventDefault()}>
              {o.ctaText}
            </a>
            <div className="offer-ratings">{o.ratings}</div>
          </article>
        ))}
      </div>

      <p className="offers-disclosure">
        Disclosure: links above are placeholders. In production they're affiliate links — we may earn a commission at no cost to you.
      </p>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// HOW IT WORKS
// ─────────────────────────────────────────────────────────────
function HowItWorks() {
  const steps = [
    { n: '01', title: 'Tell us about your pet', body: 'Breed, weight, age, activity. Sliders only — no signup, no email.' },
    { n: '02', title: 'We crunch the numbers', body: 'Five categories. 70+ breeds. Adjusted for 2026 US prices. Math in plain sight.' },
    { n: '03', title: 'Save it or share it', body: 'Download a card for IG, copy a link, or just bookmark. Your data never leaves your browser.' },
  ];
  return (
    <section className="hiw-section">
      <div className="section-head">
        <div className="section-eyebrow"><Paw size={18} color="#1B1340" /> HOW IT WORKS</div>
        <h2 className="section-h2">No paywall. No email. <span className="h2-accent">No nonsense.</span></h2>
      </div>
      <div className="hiw-grid">
        {steps.map((s, i) => (
          <div key={s.n} className="hiw-step">
            <div className="hiw-num">{s.n}</div>
            <h3 className="hiw-title">{s.title}</h3>
            <p className="hiw-body">{s.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// SOCIAL PROOF — testimonial sticker wall
// ─────────────────────────────────────────────────────────────
function SocialProof() {
  return (
    <section className="proof-section">
      <div className="section-head proof-head">
        <div className="section-eyebrow"><Paw size={18} color="#FF5A3C" /> WHAT OWNERS SAID</div>
        <h2 className="section-h2">2.4M calculations and counting</h2>
        <p className="section-sub">(That's a placeholder. But the warm reception is real.)</p>
      </div>

      <div className="proof-wall">
        {TESTIMONIALS.map((t, i) => (
          <Sticker key={i} rotate={t.rotate} className="proof-card">
            <div className="proof-stars">★★★★★</div>
            <p className="proof-quote">{t.quote}</p>
            <div className="proof-who">
              <strong>{t.who}</strong>
              <span>· {t.pet}</span>
            </div>
          </Sticker>
        ))}
      </div>

      <div className="press-strip">
        <span className="press-label">As seen referenced in:</span>
        <span className="press-logo">NYT-Wirecutter*</span>
        <span className="press-logo">MarketWatch*</span>
        <span className="press-logo">Reddit r/dogs*</span>
        <span className="press-logo">PetMD*</span>
        <span className="press-label-small">* placeholders</span>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// SOURCES
// ─────────────────────────────────────────────────────────────
function Sources() {
  return (
    <section className="sources-section" id="sources">
      <div className="sources-card">
        <div className="sources-left">
          <div className="section-eyebrow light"><Paw size={18} color="#FFD23F" /> RECEIPTS</div>
          <h2 className="sources-h2">Cited, not vibed.</h2>
          <p className="sources-sub">Every dollar in our model traces back to one of these sources. We update twice a year.</p>
        </div>
        <ul className="sources-list">
          {SOURCES.map((s, i) => (
            <li key={i}>
              <strong>{s.name}</strong>
              <span>{s.full}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// BLOG TEASERS
// ─────────────────────────────────────────────────────────────
function Blog() {
  return (
    <section className="blog-section">
      <div className="section-head">
        <div className="section-eyebrow"><Paw size={18} color="#FF5A3C" /> FROM THE BLOG</div>
        <h2 className="section-h2">Read more, spend less</h2>
      </div>
      <div className="blog-grid">
        {BLOG.map((b, i) => (
          <a key={i} className="blog-card" href="#" onClick={(e) => e.preventDefault()} style={{ '--ba': b.accent }}>
            <div className="blog-thumb">
              <div className="blog-thumb-pattern" />
              <div className="blog-thumb-glyph">¶</div>
            </div>
            <div className="blog-body">
              <div className="blog-tag">{b.tag}</div>
              <h3 className="blog-title">{b.title}</h3>
              <p className="blog-excerpt">{b.body}</p>
              <div className="blog-meta">{b.mins} min read →</div>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// FAQ
// ─────────────────────────────────────────────────────────────
function FAQ({ species }) {
  const pet = species;
  const items = [
    {
      q: `How much does a ${pet} cost per year in the US?`,
      a: `In 2026, the average annual cost is ${pet === 'dog' ? '$1,500–$3,500' : '$900–$2,000'}, depending on size, breed, age and location. Small ${pet}s cost less per year but live longer; larger ones cost more annually but have shorter lifespans.`,
    },
    {
      q: `What's the most expensive part of owning a ${pet}?`,
      a: `Food and veterinary care are consistently the two largest expenses. Food: $${pet === 'dog' ? '360–2,000' : '240–720'}/yr depending on size and diet. Vet care: $${pet === 'dog' ? '200–1,500+' : '180–650+'}/yr including routine care. Pet insurance can offset emergency costs.`,
    },
    {
      q: 'Is pet insurance worth it?',
      a: `Pet insurance is most valuable for ${pet === 'dog' ? 'brachycephalic breeds (Frenchies, Pugs, Bulldogs), high-cancer-risk breeds (Goldens, Berners), and senior dogs' : 'breeds prone to HCM (Maine Coon, Ragdoll), brachycephalic cats (Persian, Exotic Shorthair) and senior cats'}. Compare quotes from 3+ providers — one emergency surgery can cost $3,000–$10,000.`,
    },
    {
      q: 'Is fresh food worth the cost?',
      a: `Fresh-meal services run $${pet === 'dog' ? '60–360' : '40–180'}/month. While more expensive than kibble, owners often report fewer digestive issues, allergies and weight problems over time — which can offset vet costs. Most services have a discounted starter box so you can try risk-free.`,
    },
    {
      q: `Which ${pet} breeds are cheapest to own?`,
      a: pet === 'dog'
        ? 'Small, healthy breeds cost the least: Rat Terriers, Jack Russells, Papillons, Italian Greyhounds. Avoid brachycephalic (French Bulldog, Pug, Bulldog) and giant breeds (Great Dane, Mastiff) if minimizing cost is a priority.'
        : 'Domestic Shorthair and Russian Blue are among the lowest-cost cats — they\'re hardy, low-grooming and rarely have inherited conditions. Persians, Sphynx and Scottish Folds tend to be the most expensive over a lifetime.',
    },
    {
      q: 'Where do your numbers come from?',
      a: 'We pull annual averages from the APPA 2026 State of the Industry Report, AVMA Pet Ownership stats, NAPHIA insurance data, BLS veterinary CPI (Feb 2026), and PetCareBooker grooming. Adjusted for breed, weight, age and activity. We update the model twice a year.',
    },
  ];
  return (
    <section className="faq-section" id="faq">
      <div className="section-head">
        <div className="section-eyebrow"><Paw size={18} color="#1B1340" /> ❓ QUESTIONS WE GET</div>
        <h2 className="section-h2">FAQ</h2>
      </div>
      <div className="faq-list">
        {items.map((it, i) => (
          <details key={i} className="faq-item" {...(i === 0 ? { open: true } : {})}>
            <summary>{it.q}</summary>
            <div className="faq-a">{it.a}</div>
          </details>
        ))}
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────
// FOOTER
// ─────────────────────────────────────────────────────────────
function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-top">
        <div className="footer-brand">
          <div className="footer-mark">
            <Paw size={28} color="#FF5A3C" />
            <span>petexpenses<span className="brand-dot">.</span>com</span>
          </div>
          <p className="footer-tagline">Honest pet budgeting since 2026.<br/>Built for owners who love their pet — and their wallet.</p>
        </div>
        <div className="footer-cols">
          <div>
            <div className="footer-col-title">Calculators</div>
            <a href="#calculator">Dog</a>
            <a href="#calculator">Cat</a>
            <a href="#">Insurance compare</a>
            <a href="#">Food cost</a>
          </div>
          <div>
            <div className="footer-col-title">Read</div>
            <a href="#">Blog</a>
            <a href="#sources">Data sources</a>
            <a href="#faq">FAQ</a>
            <a href="#">Methodology</a>
          </div>
          <div>
            <div className="footer-col-title">About</div>
            <a href="#">Who we are</a>
            <a href="#">Contact</a>
            <a href="#">Disclosure</a>
            <a href="#">Privacy</a>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <span>© 2026 petexpenses.com</span>
        <span className="footer-disclosure">
          Estimates based on 2026 US averages. Actual costs vary by location &amp; health. Not financial or veterinary advice.
          This site contains affiliate-link placeholders.
        </span>
      </div>
    </footer>
  );
}

// ─────────────────────────────────────────────────────────────
// MAIN APP
// ─────────────────────────────────────────────────────────────
function App() {
  const [species, setSpecies] = useState('dog');
  const [dogState, setDogState] = useState({
    breed: 'Labrador Retriever',
    weight: 65, age: 'adult', activity: 'moderate', coat: 'short',
  });
  const [catState, setCatState] = useState({
    breed: 'Maine Coon',
    weight: 16, age: 'adult', activity: 'moderate', coat: 'long',
  });

  const state    = species === 'dog' ? dogState : catState;
  const setState = species === 'dog' ? setDogState : setCatState;
  const breedData = getBreed(species, state.breed);
  const costs = useMemo(
    () => calcCosts({ species, weight: state.weight, age: state.age, activity: state.activity, coat: state.coat, breedData }),
    // Recompute deterministically — using lerpInRange means no randomness, just live numbers
    [species, state.weight, state.age, state.activity, state.coat, state.breed]
  );

  return (
    <>
      <SiteNav species={species} onSpecies={setSpecies} />
      <Hero species={species} />
      <SpeciesToggle species={species} onChange={setSpecies} />
      <CalcForm species={species} state={state} setState={setState} />
      <ResultCard species={species} costs={costs} breedData={breedData} state={state} />
      <Offers species={species} costs={costs} />
      <HowItWorks />
      <SocialProof />
      <Sources />
      <Blog />
      <FAQ species={species} />
      <Footer />
    </>
  );
}

// ─────────────────────────────────────────────────────────────
// TOP NAV
// ─────────────────────────────────────────────────────────────
function SiteNav({ species, onSpecies }) {
  return (
    <nav className="site-nav">
      <a className="site-brand" href="#">
        <Paw size={26} color="#FF5A3C" />
        <span>petexpenses<span className="brand-dot">.</span>com</span>
      </a>
      <div className="site-nav-mid">
        <a href="#calculator" className={species === 'dog' ? 'active' : ''} onClick={() => onSpecies('dog')}>🐕 Dogs</a>
        <a href="#calculator" className={species === 'cat' ? 'active' : ''} onClick={() => onSpecies('cat')}>🐈 Cats</a>
        <a href="#sources">Data</a>
        <a href="#faq">FAQ</a>
      </div>
      <a href="#calculator" className="site-cta">Run the math →</a>
    </nav>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
