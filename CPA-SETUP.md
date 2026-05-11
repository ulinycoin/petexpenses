# 🐕 Dog Cost Calculator — Monetization Plan

## CPA / Affiliate Links Used

| Network | Offer | Payout | URL In Tool |
|---------|-------|--------|-------------|
| ShareASale | Ollie (fresh dog food) | **$60 flat / first order** | [YOUR_SHAREASALE_LINK] |
| ShareASale | BarkBox (subscription) | **$18-45 / subscription** | [YOUR_SHAREASALE_LINK] |
| Commission Junction | Pet Insurance (compare) | **$1-5 CPL** | [YOUR_CJ_LINK] |

## Your Earnings Per 100 Visitors (estimated)

```
100 visitors → ~25% calculate → ~25 calc completions
  ├── 5 click Ollie ($60)  → 1-2 conversions = $60-120
  ├── 3 click BarkBox ($35) → 1 conversion       = $35
  └── 8 click Insurance    → 2 leads @ $3 avg    = $6
                                            ———————
                      EPMV estimate:       $101-161
                                            per 1000 visitors
```

**Conservative estimate: ~$50-80 RPM** after accounting for the "only some click, only some convert" reality.

## CPA Network Setup

### 1. ShareASale (Ollie + BarkBox)

- Sign up: https://www.shareasale.com/
- Merchant IDs: Ollie = 133580, BarkBox = 159934
- Your affiliate ID: replace with yours
- Minimum payout: $50 (check or direct deposit)
- Cookie duration: 30-60 days (both offers)

### 2. Commission Junction (Pet Insurance)

- Sign up: https://www.cj.com/
- Replace `[YOUR_CJ_CID]` with your publisher CID
- Offers: Embrace, Lemonade, Pets Best, Healthy Paws.

### 3. Alternative: MyLead (one dashboard)

MyLead has pet insurance offers under "For Animals" category.
- Pros: single dashboard, €100 min payout
- Cons: lower payouts than direct CJ/ShareASale
- If EPC < $0.50 after 500 clicks, switch to direct networks.

## Traffic Strategy (Phase 1 — No PBN)

### Organic SEO (Free)

| Target Keyword | Volume | Difficulty | Tool Match |
|----------------|--------|------------|------------|
| "how much does a dog cost per year" | 5.4K/mo | Medium | ✅ Direct |
| "dog annual cost calculator" | 900/mo | Low | ✅ Direct |
| "cost of owning a dog by breed" | 2.1K/mo | Medium | ✅ Direct |
| "how much does pet insurance cost" | 13K/mo | High | ✅ Recommendation |
| "Ollie dog food price" | 800/mo | Low | ✅ Recommendation |
| "dog grooming cost by breed" | 1.5K/mo | Medium | ✅ Calc input |

**Page structure for SEO:**
- Title + H1: "Dog Cost Calculator — How Much Does a Dog Really Cost?"
- H2 sections for each cost category (food, vet, insurance, grooming)
- FAQ schema at bottom
- Internal links to Ollie/BarkBox/Insurance pages

### Social traffic

- **Reddit**: r/dogs, r/puppy101, r/DogCare — post in "how much does a dog cost" threads (non-spammy tool link)
- **Pinterest**: infographic of annual costs by breed → link to tool
- **TikTok/Reels**: "I calculated my dog's lifetime cost…" — viral format

## Scaling

### Phase 1 (Now — EPC validation)
- One tool (this one)
- Get 1,000 unique visitors
- Track: visits → calc completions → clicks → conversions

### Phase 2 (If EPC > $0.50)
- Add: cat version (same formula, different data)
- Add: "Puppy Cost Calculator" (targeting new owners)
- Build 2-3 more pet micro-tools
- Consider PBN if CPA revenue supports it

### Phase 3 (If EPC > $1.00)
- Scale with PBN + DeepSeek bulk content
- But NOT before validated EPC — no grey tactics until we know it works.

## Tracking Setup

Simplest: **UTM parameters on all affiliate links**
```
?utm_source=dogcost&utm_medium=tool&utm_campaign=ollie_organic
?utm_source=dogcost&utm_medium=tool&utm_campaign=barkbox_organic
?utm_source=dogcost&utm_medium=tool&utm_campaign=insurance_organic
```

Or use Google Analytics 4 with these events:
- `calculate` — user ran calculator
- `click_ollie`, `click_barkbox`, `click_insurance`
- Track via GA4's `gtag('event', ...)` in JS.

## To-Do Before Launch

- [ ] Register domain (dogcostcalculator.com or similar)
- [ ] Host on Cloudflare Pages / Vercel / Netlify (free)
- [ ] Replace ShareASale IDs with your real IDs
- [ ] Replace CJ link with your real CJ link
- [ ] Add GA4 tracking code
- [ ] Add robots.txt + sitemap.xml
- [ ] Test all links manually
- [ ] Add Open Graph images
