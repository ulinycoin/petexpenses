# petexpenses.com Memory & Context

## DEPLOYMENT GUARDRAILS (READ BEFORE ANY COMMIT)

**CRITICAL — SEO SAFETY RULES:**
1. **Git push to main = immediate production deploy.** There is NO staging. CF Pages auto-deploys on push.
2. **Never delete or redirect breed pages** without explicit owner approval. The June 2026 breed page purge killed 80% of GSC impressions.
3. **After ANY change to breed pages, verify sitemap:**
   ```bash
   grep -c '<url>' sitemap.xml  # Must be 90+ (all pages)
   ```
4. **After ANY change to breed pages, verify titles:**
   ```bash
   grep -L 'Purchase Price' breeds/*.html | wc -l  # Must be 0
   ```
5. **After ANY change to breeds/ or blog/, verify _redirects** doesn't accidentally redirect active pages.
6. **Never regenerate breed pages from `generate_breeds.py`** without first checking the generator has the correct title format (no "Annual Guide" hardcode).
7. **IndexNow ping after every deploy:** `curl -s "https://www.bing.com/indexnow?url=https://petexpenses.com/sitemap.xml&key=763CFC8CA4F13B4D2C8A131618CB3670"`

**TITLE FORMAT (current — do NOT revert):**
`[Breed] Cost in 2026: Purchase Price + $X–$Y/Year Ownership`

**META DESCRIPTION FORMAT (current — do NOT revert):**
`What a [Breed] really costs in 2026 — puppy/kitten price, annual food & vet bills ($X–$Y/yr), insurance, and hidden expenses. Free calculator with real data.`

## Active Priorities & Campaign State
- **Pinterest Integration:** Sandbox setup completed (June 2026). First commercial Pin (ID: `1109855901953667024`, Topic: "Is Pet Insurance Worth It?") successfully published on "Pet Insurance & Vet Bills" board.
- **Monetisation:** CPA placeholder links (`Partner #1 / #2 / #3`) ready to be replaced with real affiliate programs (Raw Paws, Petcube, MeoWant).

## App Credentials & Secret Tokens
- **Pinterest API (Sandbox):** credentials in `.env` (`PINTEREST_APP_ID`, `PINTEREST_APP_SECRET`, `PINTEREST_ACCESS_TOKEN`). Never commit or paste secrets into docs.
  - **Boards:**
    - `Dog Cost Calculator & Expenses` (ID: `1109855970611401481`)
    - `Cat Cost Calculator & Budgets` (ID: `1109855970611401482`)
    - `Dog Breeds Cost Comparison` (ID: `1109855970611401483`)
    - `Pet Insurance & Vet Bills` (ID: `1109855970611401484`)
    - `Smart Pet Budgeting Tips` (ID: `1109855970611401485`)

## Technology Stack & Infrastructure
- **UI:** Vanilla JS (no React despite prior config — React CDN not loaded).
- **Hosting & DNS:** Cloudflare Pages (auto-deploy on git push to main — NO manual wrangler deploy needed).
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
