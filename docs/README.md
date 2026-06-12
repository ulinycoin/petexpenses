# petexpenses.com — Pet Cost Calculator

**Live: [petexpenses.com](https://petexpenses.com/)**

Interactive tool for dogs and cats. Pick a breed or enter weight/age, get an instant annual cost breakdown — food, vet, insurance, grooming, supplies — with personalised savings tips.

Built from 2026 US averages (APPA, AVMA, NAPHIA, BLS). No signup, no paywall.

---

## Tech Stack

| Layer     | What                                                    |
| --------- | ------------------------------------------------------- |
| **UI**    | React 18 (CDN production bundle, no build toolchain)    |
| **Styling** | Custom CSS (~40 KB with custom properties, responsive) |
| **Data**  | Static JS module — 51 dog breeds + 23 cat breeds        |
| **Build** | esbuild for JSX → JS (one-shot, no watcher needed)      |
| **Deploy** | Cloudflare Pages via wrangler                           |

---

## Project Structure

```
dog-cost-tool/
├── index.html          # Entry point — CDN React + analytics
├── app.jsx             # Main app source (JSX)
├── app.js              # Compiled app (esbuild)
├── components.jsx      # Reusable widgets source (JSX)
├── components.js       # Compiled components (esbuild)
├── data.js             # Breeds, cost tables, offers, sources
├── styles.css          # Full stylesheet (~1100 lines)
├── hero-image.png      # Hero section photo
├── og-dog.jpg          # Open Graph image (dog)
├── og-cat.jpg          # Open Graph image (cat)
├── cat-cost.html       # Redirect → /#calculator
├── llms.txt            # LLM index
├── sitemap.xml         # SEO sitemap
├── robots.txt          # SEO robots
├── CPA-SETUP.md        # Affiliate monetisation plan
├── RESEARCH.md         # Niche & market research notes
└── README.md           # This file
```

---

## Quick Start

```bash
# Serve locally (any HTTP server — JSX won't open from file://)
python3 -m http.server 8080

# Open in browser
open http://localhost:8080
```

No npm, no build step required for development. To recompile JSX after editing source files:

```bash
npx esbuild app.jsx components.jsx --bundle --outfile=app.js --outfile=components.js --format=esm
```

---

## Features

- **Dual species** — toggle between dog & cat with separate breed libraries (51 dog, 23 cat)
- **Smart defaults** — breed auto-fills weight, size, coat, and health notes
- **Weight + age sliders** — fine-tune the calculation; costs lerp within breed ranges
- **Activity & coat** — adjusts food, grooming, and supplies costs
- **Donut chart** — visual cost breakdown by category
- **Annual ↔ monthly toggle** — switch views on the fly
- **Personalised offers** — 3 contextual affiliate cards (stubs, ready for real links)
- **Blog teasers** — 3 article cards (stubs, linked when written)
- **Testimonials** — social-proof cards with random rotation
- **Responsive** — mobile through desktop
- **Cited data** — APPA, AVMA, NAPHIA, BLS sources shown inline
- **SEO-ready** — Open Graph tags, meta description, FAQ schema, structured data
- **Analytics** — PostHog (EU hosted, privacy-friendly)

---

## Cost Calculation

The engine in `data.js` defines base cost ranges per size bucket (small / medium / large / giant) and coat type. Multipliers apply for:

| Factor      | What it affects                                 |
| ----------- | ----------------------------------------------- |
| Breed coeff | vet, insurance, food, grooming (up to 1.8×)     |
| Age         | vet (+30% puppy, +60% senior), insurance, supplies |
| Activity    | food (±20%), supplies (+15% high)               |
| Weight      | lerps within the size bucket's cost range        |

---

## Monetisation

See [CPA-SETUP.md](./CPA-SETUP.md). Current offers are placeholders (`Partner #1 / #2 / #3`) — replace with real affiliate links once networks approve.

---

## Deploy

```bash
cd /Users/aleksejs/Desktop/dog-cost-tool
CLOUDFLARE_API_TOKEN=… wrangler pages deploy . --project-name=pet-expenses
```

---

## Data Sources

- **APPA** — 2026 State of the Industry Report
- **AVMA** — Pet Ownership & Demographics 2026
- **NAPHIA** — Pet Health Insurance Report 2026
- **BLS** — Veterinary Services CPI, Feb 2026
- **Industry Surveys** — Pet ownership debt and spending trends

---

## License

Internal project. Not open source.
