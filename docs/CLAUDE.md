# petexpenses.com Memory & Context

## Active Priorities & Campaign State
- **Pinterest Integration:** Sandbox setup completed (June 2026). First commercial Pin (ID: `1109855901953667024`, Topic: "Is Pet Insurance Worth It?") successfully published on "Pet Insurance & Vet Bills" board.
- **Monetisation:** CPA placeholder links (`Partner #1 / #2 / #3`) ready to be replaced with real affiliate programs (Raw Paws, Petcube, MeoWant).

## App Credentials & Secret Tokens
- **Pinterest API (Sandbox):**
  - **App ID:** `1579094`
  - **App Secret:** `828a3672b9fe5db37ebd394204cd490a46b56b85`
  - **Access Token:** Saved in `.env` (`PINTEREST_ACCESS_TOKEN`)
  - **Boards:**
    - `Dog Cost Calculator & Expenses` (ID: `1109855970611401481`)
    - `Cat Cost Calculator & Budgets` (ID: `1109855970611401482`)
    - `Dog Breeds Cost Comparison` (ID: `1109855970611401483`)
    - `Pet Insurance & Vet Bills` (ID: `1109855970611401484`)
    - `Smart Pet Budgeting Tips` (ID: `1109855970611401485`)

## Technology Stack & Infrastructure
- **UI:** Vanilla JS (no React despite prior config — React CDN not loaded).
- **Hosting & DNS:** Cloudflare Pages (deploy via `wrangler pages deploy . --project-name=pet-expenses`).
- **Analytics:** PostHog (self-hosted EU).
- **Core Files:**
  - [index.html](file:///Users/aleksejs/Desktop/dog-cost-tool/index.html) — Main calculator entrypoint (inline CSS + JS).
  - [assets/data/generate_breeds.py](file:///Users/aleksejs/Desktop/dog-cost-tool/assets/data/generate_breeds.py) — Cost matrix generator.
  - [scripts/utils/](file:///Users/aleksejs/Desktop/dog-cost-tool/scripts/utils/) — Pinterest/FB/Awin automation scripts.
  - [docs/](file:///Users/aleksejs/Desktop/dog-cost-tool/docs/) — Project docs (CLAUDE.md, DESIGN.md, etc).

## Project Structure
```
dog-cost-tool/
├── index.html              # Main page (inline CSS+JS+data)
├── about.html, contact.html, privacy.html, terms.html, sources.html, compare.html, widget.html
├── _headers, _redirects, robots.txt, sitemap.xml, llms.txt, ai-summary.json
├── wrangler.toml
├── assets/
│   ├── images/             # hero-image.jpg, og-dog.jpg, og-cat.jpg
│   │   └── blog/           # Blog post images
│   ├── icons/              # favicon.* files
│   └── data/               # CSV, generate_breeds.py
├── blog/                   # Blog articles (HTML)
├── breeds/                 # Breed cost pages (HTML)
├── scripts/                # FB autoposting scripts
│   └── utils/              # Pinterest, Awin, CSV utilities
├── docs/                   # CLAUDE.md, DESIGN.md, CPA-SETUP.md, RESEARCH.md, README.md
├── embed/                  # Embeddable widget
├── functions/              # Cloudflare Functions
└── .github/                # CI/CD
```

## Core Commands
- **Local Dev Server:** `python3 -m http.server 8080` (from project root)
- **Compile JSX:** `npx esbuild app.jsx components.jsx --bundle --outfile=app.js --outfile=components.js --format=esm`
- **Deploy to Cloudflare:** `wrangler pages deploy . --project-name=pet-expenses`
- **Test Pinterest API:** `python3 scratch/pinterest_test.py`
