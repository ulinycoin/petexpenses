---
version: alpha
name: petexpenses
description: Playful, trustworthy pet cost calculator with sticker-shadow aesthetic, warm coral accent, and bold display typography. Designed for pet owners seeking honest, cited cost data.
colors:
  primary: "#FF5A3C"
  on-primary: "#FFFFFF"
  ink: "#1B1340"
  on-ink: "#FFF7E8"
  ink-soft: "#4A3F6F"
  ink-mute: "#6B6490"
  coral: "#FF5A3C"
  coral-dk: "#E03812"
  coral-soft: "#FFE3DA"
  pink: "#FF8FB1"
  pink-dk: "#E55E89"
  pink-soft: "#FFE2EC"
  sun: "#FFD23F"
  sun-dk: "#C9941E"
  sun-soft: "#FFF1B8"
  mint: "#6EE7B7"
  mint-dk: "#0E9F6E"
  mint-soft: "#C7F4DD"
  lavender: "#A78BFA"
  lav-dk: "#6D49C7"
  lav-soft: "#E6DCFF"
  cream: "#FFF7E8"
  cream-2: "#FBEFD6"
  paper: "#FFFFFF"
  background: "#FFF7E8"
  on-background: "#1B1340"
typography:
  display-hero:
    fontFamily: "Bricolage Grotesque, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "5.6rem"
    fontWeight: "800"
    lineHeight: "0.95"
    letterSpacing: "-0.04em"
  display-h2:
    fontFamily: "Bricolage Grotesque, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "3.4rem"
    fontWeight: "800"
    lineHeight: "1.05"
    letterSpacing: "-0.025em"
  display-h3:
    fontFamily: "Bricolage Grotesque, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "1.6rem"
    fontWeight: "800"
    lineHeight: "1.1"
    letterSpacing: "-0.02em"
  display-card-title:
    fontFamily: "Bricolage Grotesque, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "1.5rem"
    fontWeight: "800"
    lineHeight: "1.1"
    letterSpacing: "-0.02em"
  display-mono-label:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "11px"
    fontWeight: "600"
    letterSpacing: "0.10em"
    textTransform: "uppercase"
  display-badge:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "12px"
    fontWeight: "700"
    letterSpacing: "0.12em"
    textTransform: "uppercase"
  body-main:
    fontFamily: "Geist, system-ui, -apple-system, sans-serif"
    fontSize: "1rem"
    lineHeight: "1.55"
  body-small:
    fontFamily: "Geist, system-ui, -apple-system, sans-serif"
    fontSize: "0.94rem"
    lineHeight: "1.5"
  body-mono:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "0.85rem"
rounded:
  sm: 10px
  md: 14px
  lg: 20px
  xl: 28px
  pill: 999px
spacing:
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 28px
  xxl: 32px
  section: 56px
elevation:
  shadow-sm: "0 1px 0 rgba(27,19,64,0.05), 0 1px 3px rgba(27,19,64,0.06)"
  shadow: "0 2px 0 rgba(27,19,64,0.06), 0 8px 22px -8px rgba(27,19,64,0.18)"
  shadow-lg: "0 4px 0 rgba(27,19,64,0.10), 0 22px 50px -16px rgba(27,19,64,0.30)"
  sticker-shadow: "4px 4px 0 rgba(27,19,64,0.10), 0 12px 30px -10px rgba(27,19,64,0.18)"
  sticker-shadow-strong: "6px 6px 0 #1B1340"
components:
  site-nav:
    backgroundColor: "rgba(255,247,232,0.85)"
    backdropFilter: "saturate(180%) blur(12px)"
    padding: "16px 32px"
    borderBottom: "1px solid rgba(27,19,64,0.07)"
  site-cta:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
    fontWeight: "600"
  site-cta-hover:
    backgroundColor: "{colors.coral}"
    transform: "translateY(-1px)"
  site-nav-link:
    padding: "8px 14px"
    rounded: "{rounded.pill}"
    fontSize: "0.92rem"
    fontWeight: "500"
    color: "{colors.ink-soft}"
  site-nav-link-active:
    backgroundColor: "{colors.ink}"
    color: "{colors.cream}"
  hero-photo-frame:
    borderRadius: "240px 240px 60px 60px / 220px 220px 80px 80px"
    border: "3px solid {colors.ink}"
    boxShadow: "6px 6px 0 {colors.ink}"
    transform: "rotate(-3deg)"
    background: "radial-gradient(ellipse at 50% 30%, rgba(255,210,63,0.6), transparent 70%), repeating-linear-gradient(45deg, rgba(27,19,64,0.06) 0 2px, transparent 2px 14px), {colors.coral-soft}"
  hero-photo-frame-cat:
    background: "radial-gradient(ellipse at 50% 30%, rgba(255,210,63,0.6), transparent 70%), repeating-linear-gradient(45deg, rgba(27,19,64,0.06) 0 2px, transparent 2px 14px), {colors.pink-soft}"
  deco-sticker-paid:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    rounded: "18px"
    padding: "14px 18px"
  deco-sticker-savings:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "12px 18px"
  deco-sticker-rating:
    backgroundColor: "{colors.paper}"
    rounded: "14px"
    padding: "14px 18px"
  species-toggle:
    backgroundColor: "{colors.ink}"
    padding: "6px"
    rounded: "{rounded.pill}"
  species-toggle-btn:
    padding: "12px 24px"
    rounded: "{rounded.pill}"
    fontWeight: "600"
    fontSize: "1rem"
    color: "rgba(255,247,232,0.65)"
  species-toggle-btn-active:
    backgroundColor: "{colors.coral}"
    color: "{colors.cream}"
  species-toggle-btn-cat-active:
    backgroundColor: "{colors.pink}"
    color: "{colors.ink}"
  calc-card:
    backgroundColor: "{colors.paper}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    boxShadow: "6px 6px 0 {colors.ink}, 0 24px 50px -20px rgba(27,19,64,0.28)"
    padding: "44px 48px"
  calc-title-sticker:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    fontFamily: "Bricolage Grotesque"
    fontWeight: "800"
    fontSize: "1.4rem"
    padding: "12px 20px"
  breed-input:
    padding: "14px 16px"
    backgroundColor: "{colors.cream}"
    border: "2px solid {colors.ink}"
    rounded: "{rounded.md}"
    fontSize: "1.05rem"
  breed-input-focus:
    boxShadow: "4px 4px 0 {colors.coral}"
  breed-list:
    backgroundColor: "{colors.paper}"
    border: "2px solid {colors.ink}"
    rounded: "{rounded.md}"
    boxShadow: "4px 4px 0 {colors.ink}"
    padding: "6px"
  breed-list-item-hover:
    backgroundColor: "{colors.coral-soft}"
  slider:
    backgroundColor: "{colors.cream}"
    border: "2px solid {colors.ink}"
    rounded: "{rounded.md}"
    padding: "18px 22px"
  slider-value:
    fontFamily: "Bricolage Grotesque"
    fontWeight: "800"
    fontSize: "1.8rem"
    letterSpacing: "-0.02em"
  segmented-control:
    backgroundColor: "{colors.cream}"
    border: "2px solid {colors.ink}"
    rounded: "{rounded.pill}"
    padding: "4px"
  segmented-btn:
    padding: "11px 14px"
    rounded: "{rounded.pill}"
    fontWeight: "600"
    fontSize: "0.92rem"
    color: "{colors.ink-soft}"
  segmented-btn-active:
    boxShadow: "2px 2px 0 {colors.ink}"
    color: "{colors.ink}"
  rcard-total:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    padding: "32px"
    boxShadow: "6px 6px 0 {colors.coral}"
  rcard-total-amount:
    fontFamily: "Bricolage Grotesque"
    fontWeight: "800"
    fontSize: "6.4rem"
    letterSpacing: "-0.04em"
    color: "{colors.sun}"
  rcard-breakdown:
    backgroundColor: "{colors.paper}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    padding: "32px"
    boxShadow: "6px 6px 0 {colors.ink}"
  rcard-cta:
    backgroundColor: "rgba(110,231,183,0.12)"
    border: "1.5px solid rgba(110,231,183,0.4)"
    rounded: "{rounded.lg}"
    padding: "14px 18px"
  rcard-cta-btn:
    backgroundColor: "{colors.mint-dk}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "9px 18px"
    fontWeight: "700"
  rcard-cta-btn-hover:
    backgroundColor: "{colors.mint}"
    transform: "translateY(-1px)"
  share-btn:
    backgroundColor: "rgba(255,247,232,0.1)"
    border: "1.5px solid rgba(255,247,232,0.25)"
    rounded: "{rounded.pill}"
    padding: "11px 16px"
    color: "{colors.cream}"
    fontWeight: "600"
  share-btn-primary:
    backgroundColor: "{colors.sun}"
    borderColor: "{colors.sun}"
    color: "{colors.ink}"
  offer-card:
    backgroundColor: "{colors.paper}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    padding: "24px"
    boxShadow: "4px 4px 0 {colors.ink}"
  offer-card-hover:
    transform: "translateY(-4px)"
    boxShadow: "6px 8px 0 {colors.ink}"
  offer-sticker:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.ink}"
    border: "2.5px solid {colors.ink}"
    boxShadow: "2px 2px 0 {colors.ink}"
    padding: "6px 12px"
    rounded: "6px"
    fontFamily: "JetBrains Mono"
    fontSize: "11px"
    fontWeight: "800"
    letterSpacing: "0.1em"
  offer-cta:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    rounded: "{rounded.pill}"
    padding: "14px 20px"
    fontWeight: "700"
  offer-cta-hover:
    backgroundColor: "{colors.coral-dk}"
    transform: "translateY(-1px)"
  hiw-step:
    backgroundColor: "{colors.paper}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    padding: "28px 26px"
    boxShadow: "4px 4px 0 {colors.ink}"
  hiw-num:
    fontFamily: "Bricolage Grotesque"
    fontWeight: "800"
    fontSize: "3.6rem"
    letterSpacing: "-0.04em"
    color: "{colors.coral}"
  hiw-num-step2:
    color: "{colors.lav-dk}"
  hiw-num-step3:
    color: "{colors.mint-dk}"
  blog-card:
    backgroundColor: "{colors.paper}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    boxShadow: "4px 4px 0 {colors.ink}"
  blog-card-hover:
    transform: "translateY(-4px)"
    boxShadow: "6px 8px 0 {colors.ink}"
  blog-thumb:
    aspectRatio: "16/9"
    borderBottom: "2.5px solid {colors.ink}"
  blog-thumb-glyph:
    fontFamily: "Bricolage Grotesque"
    fontWeight: "800"
    fontSize: "7rem"
    transform: "rotate(-8deg)"
  faq-item:
    backgroundColor: "{colors.paper}"
    border: "2px solid {colors.ink}"
    rounded: "{rounded.lg}"
  faq-item-open:
    boxShadow: "4px 4px 0 {colors.coral}"
  faq-summary-arrow:
    color: "{colors.coral}"
    fontSize: "1.6rem"
  proof-card:
    padding: "18px"
    rounded: "12px"
    backgroundColor: "{colors.paper}"
  proof-card-alt1:
    backgroundColor: "{colors.cream-2}"
  proof-card-alt2:
    backgroundColor: "{colors.mint-soft}"
  proof-card-alt3:
    backgroundColor: "{colors.pink-soft}"
  proof-card-alt4:
    backgroundColor: "{colors.sun-soft}"
  site-footer:
    backgroundColor: "{colors.ink}"
    color: "{colors.cream}"
    padding: "56px 24px 32px"
  sources-card:
    backgroundColor: "{colors.ink}"
    color: "{colors.cream}"
    border: "2.5px solid {colors.ink}"
    rounded: "{rounded.xl}"
    padding: "44px 48px"
    boxShadow: "6px 6px 0 {colors.sun}"
  sources-list-strong:
    color: "{colors.sun}"
---

## Overview

Petexpenses.com is a free pet cost calculator built for pet owners who want
honest, data-backed estimates. The design language is playfully trustworthy —
bold sticker shadows, warm coral accents, and friendly organic shapes create
a "financial tool that doesn't feel cold" experience.

The brand voice is direct and transparent: no upselling pressure, no signup
walls, just cited data from APPA, AVMA, and NAPHIA.

## Colors

- **Ink (#1B1340):** Deep navy-brown for all primary text, dark backgrounds
  (footer, total card, species toggle, CTA buttons). Provides authoritative
  contrast against the warm cream page background.
- **Coral (#FF5A3C):** Primary interaction accent — active toggle, brand dot,
  hero accent text, calculator focus, FAQ open arrow. Warm, energetic, but
  not aggressive.
- **Pink (#FF8FB1):** Cat-mode accent — replaces coral when the calculator
  switches to cat mode. Active cat toggle, cat hero frame.
- **Sun (#FFD23F):** Highlight accent — total cost amount, savings stickers,
  footer section titles, sources card shadow. Draws immediate attention.
- **Mint (#6EE7B7):** Positive signal — savings decorations, insurance CTA,
  hiw step 3 number. Signals "good news / savings."
- **Lavender (#A78BFA):** Tertiary accent — hiw step 2 number. Used sparingly.
- **Cream (#FFF7E8):** Page background. Warm, soft, non-clinical feel.
  Combined with the sticker-shadow aesthetic, the cream base makes the
  ink-bordered cards feel tactile like paper.
- **Paper (#FFFFFF):** Card/surface background. Clean white for content areas
  inside the cream page.

### Usage rules

- Do not use coral and pink simultaneously for the same purpose — coral is
  dog mode, pink is cat mode.
- Ink on cream is the default text-background pair. Always maintain this
  unless inside a dark container (footer, rcard-total).
- The sun color is reserved for the most important numeric value (total cost).
- Mint signals "you save money" or "positive action."

## Typography

Three-font system with broad fallback stacks:

| Role | Font | Usage |
|------|------|-------|
| **Display** | Bricolage Grotesque (800 weight) | Hero H1, section H2, card titles, large amounts, big numbers |
| **Body** | Geist | All paragraph text, labels, navigation |
| **Mono** | JetBrains Mono | Data labels, USD amounts, badges, metadata, uppercase captions |

Key sizing rules:

- **Hero H1:** `clamp(2.6rem, 6.3vw, 5.6rem)` — aggressively large, tight
  line-height (0.95), tight letter-spacing (-0.04em)
- **Section H2:** `clamp(2.1rem, 4vw, 3.4rem)` with `font-variation-settings: "wdth" 95`
- **Body:** `1rem` (16px) default, `.94rem` for secondary text
- **Mono labels:** `11px` uppercase with .10em letter-spacing
- **Badges / eyebrow:** `12px` uppercase mono

## Layout & Spacing

- **Content max-width:** 1160px (most sections), 1200px (hero), 1100px (proof)
- **Page background:** cream (#FFF7E8) with ink (#1B1340) text
- **Section padding:** 0 24px horizontal, 56px vertical top, 64px bottom
- **Card padding:** 24–48px depending on component size
- **Grid patterns:**
  - Hero: 2-column (1.05fr 1fr) → stacks at 900px
  - Calculator: 2-column form → stacks at 700px
  - Results: 2-column (1fr 1.2fr) → stacks at 900px
  - Affiliate offers: 3-column → stacks at 900px
  - Breed grid: 4-column → 2-column at 700px → 1-column at 420px
  - Blog grid: 4-column → 1-column at 900px
  - How it works: 3-column → 1-column at 800px
  - Proof wall: 4-column → 2-column at 960px → 1-column at 540px
  - Footer: 2-column top → stacks at 800px; footer col 3 → 2 at 540px

## Elevation & Depth

The signature visual device is the **sticker shadow** — a thick, flat
offset shadow that makes elements look like physical stickers on paper.

- **Default sticker:** `6px 6px 0 {colors.ink}` — used on hero photo frame,
  calculator card, total + breakdown cards, offer cards, blog cards, how-it-works
  steps, sources card
- **Light sticker:** `4px 4px 0 {colors.ink}` — offer cards, blog cards, how-it-works
  steps (default state)
- **Accent sticker shadow:** `6px 6px 0 {colors.coral}` — total card
- **Accent sticker shadow (sources):** `6px 6px 0 {colors.sun}` — sources card
- **Sticker hover:** translateY(-4px) with deeper shadow — offer cards, blog cards
- **Navigation:** backdrop blur glassmorphism (saturate(180%) blur(12px)) on
  sticky nav with subtle bottom border

## Shapes

- **Cards:** `28px` xl radius (calc-card, rcard, offer-card, blog-card, hiw-step, sources-card)
- **Buttons/pills:** `999px` pill radius (nav links, toggles, CTAs, badges)
- **Inputs:** `14px` radius (breed search, slider container)
- **Hero photo frame:** organic asymmetric — `240px 240px 60px 60px / 220px 220px 80px 80px`
- **Decorative dots:** small repeating radial dot pattern on footer and sources card
- **Breed list:** `8px` radius on hover items, `6px` padding on container

## Components

### Navigation (`site-nav`)
- Sticky with glassmorphism backdrop, ink bottom border
- Left: site brand (display font + coral dot)
- Center: nav links (mono labels, pill rounded, ink active state)
- Right: CTA button (ink bg → coral on hover)

### Hero
- Warm radial gradient overlay on cream bg
- Left column: pretitle badge → hero H1 with coral/pink accent word → subtitle
  with trust badges → badge row (⊕ Free forever, ⚡ Instant result, etc.)
- Right column: framed photo container — organic border radius, sticker-shadow,
  -3deg rotation, decorative pattern lines. Inside: pet illustration.
  Decorations: paid sticker, savings sticker, rating card.
- Cat mode: pink-soft frame instead of coral-soft

### Calculator (`calc-card`)
- White card with ink border + strong sticker shadow
- Title sticker: "Pet Cost Calculator" on ink bg
- Two-column form:
  - Breed search (text input → dropdown list)
  - Weight slider (custom styled range)
  - Age slider
  - Activity level (segmented pill control)
- Species toggle above calculator (dog/cat pill)

### Results (2-card layout)
- **Total card** (ink bg + coral shadow): breed label → large sun-colored
  amount → meta grid (year/month/week amounts) → share buttons →
  insurance CTA row (mint tint)
- **Breakdown card** (paper + ink shadow): doughnut chart (SVG) → line list
  (Food, Vet, Insurance, Supplies, Grooming, Misc) with colored dots,
  bars, amounts, percentages

### Affiliate Offers (`offer-card`)
- 3-column grid of affiliate cards with sticker style
- Colored sticker badge, partner name, bullet list, context note (amber bg),
  CTA button (ink → coral-dk on hover)
- Each card has custom `--oa` / `--oad` CSS vars for accent color

### How It Works (`hiw-step`)
- 3-column sticker cards with numbered steps
- Numbers use display font in coral / lavender / mint-dk
- Flexbox layout: number → title → description

### Testimonials (`proof-card`)
- 4-column alternating background colors (cream-2, mint-soft, pink-soft, sun-soft)
- Stars → quote → attribution
- Press strip below with logo names

### Blog Cards (`blog-card`)
- 4-column sticker cards with colored thumb strip
- Thumb: icon glyph on colored bg with diagonal line pattern
- Body: tag → title → excerpt → meta (read time / date)
- Hover: lift + deeper shadow

### FAQ (`faq-item`)
- Accordion with ink border, rounded-lg
- Open state: coral shadow
- Summary: display font, thin weight; custom +/– toggle in coral

### Footer (`site-footer`)
- Full-ink background with dot pattern overlay
- 2-column top: brand mark + tagline → 3-column link groups
- Bottom: copyright, disclosure text (small mono, low opacity)

## Do's and Don'ts

### Do's
- Use sticker shadows (6px 6px 0 ink) on all bordered cards — this is the
  signature visual device
- Keep warm tone: cream bg, coral accent, ink typography
- Use clamp() for responsive font sizes
- Always provide dog-mode (coral) and cat-mode (pink) visual variants
- Use JetBrains Mono for data, amounts, labels, badges
- Stack grids to single column on mobile breakpoints
- Apply rotate(-2deg) or rotate(-3deg) sparingly for playful character
- Use the dot pattern overlay on ink backgrounds (footer, sources)

### Don'ts
- Don't use cold colors (blues, grays) as accents — the palette is intentionally
  warm (coral, pink, sun, mint)
- Don't remove the sticker shadow — it is the brand's most distinctive element
- Don't use emoji in the interface (🐕, 🐈, ⚡, ★, etc.) — they should be
  replaced with inline SVG icons if visual polish is needed
- Don't add images to breed pages — they are intentionally text-only for SEO
  (but a hero illustration can be added to the main page)
- Don't change the cream page background — it's the foundation of the warm feel
- Don't make primary CTA transparent — always use ink or coral fill
- Don't add border-radius smaller than 10px on interactive elements
- Don't use `overflow-x: hidden` as a lazy fix for layout issues
