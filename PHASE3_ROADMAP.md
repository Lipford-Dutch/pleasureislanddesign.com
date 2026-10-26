# Bugfix-1 & Phase 3 Roadmap

**Branch:** `bugfix-1`  
**Status:** In Progress  
**Target Date:** TBD

---

## 🐛 BUGFIX-1: Critical Issues

### 1. Contact Form & Newsletter (BLOCKER)
**Issue:** Forms POST to invalid Formspree endpoint → 404 errors → emails never sent  
**Root Cause:** URL format `https://formspree.io/f/<email>` is invalid; Formspree requires form ID hash  
**Solution:** Implement PHP email handler on GoDaddy cPanel  

**Steps:**
- [ ] Create `/forms/contact.php` with mail() handler
- [ ] Validate + sanitize form inputs (no injection)
- [ ] Send to pleasureislanddesign@gmail.com
- [ ] Test locally, then deploy
- [ ] Update JS to POST to `/forms/contact.php` instead

**Effort:** 1–2 hours  
**Risk:** Low (PHP built-in, GoDaddy has mail support)

---

### 2. Reviews Section (ENHANCEMENT)
**Issue:** Currently 3 hardcoded testimonials; not pulling from Google dynamically  
**Decision:** Keep curated reviews (full control, no cost) + add prominent "See all on Google" button  

**Steps:**
- [ ] Update HTML to add "See all reviews" CTA button to Google Business listing
- [ ] Add Google review widget CSS (optional: add star count, review count from GA4 API)
- [ ] Link button to: `https://www.google.com/search?q=Pleasure+Island+Design+Wilmington+NC`
- [ ] Test link on live site

**Effort:** 30 minutes  
**Risk:** Minimal

---

### 3. Calendar & Booking (STRATEGIC)
**Issue:** Current Google Calendar embed is read-only and requires public sharing (often blank)  
**Decision:** Switch to Calendly or Google Appointment Schedules  

**Steps:**
- [ ] Sign up for Calendly Free or Google Appointment Schedules
- [ ] Configure availability (hours, buffer, break times)
- [ ] Set email notification to pleasureislanddesign@gmail.com
- [ ] Get embed URL/button link
- [ ] Replace iframe with Calendly embed or link + CTA button
- [ ] Test end-to-end booking + email confirmation

**Effort:** 1–2 hours  
**Risk:** Moderate (third-party tool, requires account setup)  
**Cost:** Calendly Free (unlimited bookings), Google Appointments (free if using Workspace)

---

### 4. Hero & Mobile Layout (AUDIT + FIXES)
**Issue:** User reports hero section and mobile experience "seem off"  

**Audit Steps:**
- [ ] Take desktop (1920px) and mobile (375px) screenshots
- [ ] Compare against design system (Playfair Display headings, Lato body, spacing grid)
- [ ] Check for:
  - Text overflow, line-height issues
  - Image aspect ratio distortion
  - Button sizing/padding on mobile
  - Spacing consistency (hero stats, credentials strip)
  - Mobile menu animation/usability
- [ ] Document 3–5 concrete issues with before/after mockups
- [ ] Present to Nicole for approval before fixing

**Expected Issues:**
- Hero image may not scale properly on mobile (aspect ratio)
- Stats may stack awkwardly on mobile
- Button sizing may need tweaking

---

### 5. Misspellings (GROOM)
**Status:** Automated spell-check passed (proper nouns: Mayfaire, Seagrove, Murrayville, Pointe all correct)  
**Action:** Please identify specific misspellings you've seen → I'll fix them

---

## 📦 PHASE 3 BACKLOG (Detailed Breakdown)

Phased out like previous work: research → design → implement → test → deploy.

---

### **1. Swag Store (Production Ready)**

**Current State:**  
- `storefront-beta/` has placeholder Printify integration  
- Static shop landing page only  
- Not deployed to production

**Phase 3.1: Shop Strategy & UX** (1 week)
- [ ] Decide: Printify, Shopify, Etsy embed, or custom WooCommerce?
- [ ] Design shop homepage (hero, product grid, filters)
- [ ] Plan product categories (t-shirts, hats, mugs, branded items)
- [ ] Define shipping/tax strategy
- [ ] Create product photography style guide

**Phase 3.2: Integration & Setup** (2 weeks)
- [ ] Connect chosen platform (Printify API, Shopify embed, or WooCommerce)
- [ ] Build product pages (images, descriptions, pricing, variants)
- [ ] Integrate payment gateway (Stripe/PayPal)
- [ ] Add cart functionality
- [ ] Test checkout flow (sandbox → live)

**Phase 3.3: Frontend & Analytics** (1 week)
- [ ] Replace static `/shop` with live product feed
- [ ] Add GA4 e-commerce tracking (product views, add-to-cart, purchase)
- [ ] Integrate with order management (dashboard, email notifications)
- [ ] QA all device sizes

**Phase 3.4: Launch & Monitor** (ongoing)
- [ ] Deploy to production
- [ ] Monitor GA4 funnel (product page → cart → checkout → purchase)
- [ ] Set up email alerts for high-value orders
- [ ] Gather customer feedback

**Timeline:** 4–6 weeks (depends on platform choice)  
**Cost:** Free (Printify, Etsy) to $30–100/mo (Shopify, WooCommerce + hosting)

---

### **2. Expanded Gallery with Lightbox**

**Current State:**  
- 20+ before-and-after images in `/gallery/`  
- Displayed in grid; click leads to standalone image page (clunky)

**Phase 3.5: Gallery UX & Design** (1 week)
- [ ] Audit existing gallery images (quality, organization)
- [ ] Plan gallery layout: grid vs. masonry, thumbnails vs. full
- [ ] Design lightbox UI (close, prev/next, fullscreen, metadata)
- [ ] Plan metadata: project name, location, date, services

**Phase 3.6: Lightbox Implementation** (1 week)
- [ ] Integrate Lightbox2 or Swipebox (simple, no jQuery)
- [ ] Or build custom lightbox using native JS (better control)
- [ ] Add before-and-after slider if desired
- [ ] Implement lazy loading for gallery images
- [ ] Add keyboard navigation (arrow keys, ESC)

**Phase 3.7: Gallery Expansion & Photography** (2–4 weeks)
- [ ] Target 50–100 before-and-after pairs (currently ~20)
- [ ] Plan photo shoots: different kitchen types, styles, scales
- [ ] Organize by service type (refinishing, refacing, hardware, repair)
- [ ] Tag by location (Wilmington, Kure Beach, etc.)
- [ ] Add filters/search by service, location, style

**Phase 3.8: Content & Metadata** (1 week)
- [ ] Write short project descriptions (client testimonial snippet, turnaround time)
- [ ] Add structured data (JSON-LD ImageObject) for SEO
- [ ] Create gallery index page with filters
- [ ] Link to blog posts for similar services

**Timeline:** 4–8 weeks (content-heavy; photo shoots take time)  
**Cost:** Free (if using existing photos) to $500–1500 (professional photography)

---

### **3. SEO Implementation (Backlog)**

**Current State:**  
- Basic on-page SEO (title, description, keywords, schema)  
- GA4 installed (tracking live)  
- No technical SEO audit done  
- Minimal internal linking strategy

**Phase 3.9: Technical SEO** (1 week)
- [ ] Run Lighthouse audit (performance, accessibility, SEO)
- [ ] Fix crawlability issues (robots.txt, sitemap.xml, canonical tags)
- [ ] Implement breadcrumbs (JSON-LD schema)
- [ ] Optimize Core Web Vitals (LCP, FID, CLS)
- [ ] Set up Google Search Console + Bing Webmaster Tools
- [ ] Fix redirect chains, 404 errors

**Phase 3.10: Content SEO** (2 weeks)
- [ ] Keyword research: "cabinet refinishing wilmington nc", "kitchen cabinet painting", etc.
- [ ] Expand blog: target 20+ articles (currently 3)
  - Topic clusters: refinishing, repair, care, trends, FAQs
  - Internal linking strategy
- [ ] Optimize title tags & meta descriptions (CTR)
- [ ] Add FAQ schema (rich snippets in search)

**Phase 3.11: Link & Authority Building** (ongoing)
- [ ] Local SEO: Google Business Profile, local citations
- [ ] Request reviews on Google, Nextdoor, Yelp, Facebook
- [ ] Reach out to local business directories
- [ ] Guest post opportunities (home design blogs)

**Timeline:** 4–8 weeks (ongoing)  
**Cost:** Free (in-house) or $500–2000 (SEO consultant for 1-month audit)

---

### **4. Knowledge Base / Wiki (Support)**

**Current State:**  
- 3 blog posts (care guide, refinishing guide, color trends)  
- FAQ section on homepage  
- No dedicated support/knowledge base

**Phase 3.12: Content Strategy** (1 week)
- [ ] Plan content structure: how-to, FAQs, troubleshooting, maintenance
- [ ] Write 15–20 articles: cabinet care, paint types, product compatibility, pet-friendly options, etc.
- [ ] Plan search: keyword-driven navigation, filters

**Phase 3.13: Platform Choice** (2 days)
Options:
- Static wiki (GitHub Pages + Markdown + Jekyll) — fast, free, no maintenance
- Notion wiki embed — collaborative, free tier available
- Custom PHP wiki (cPanel-friendly) — control, but maintenance burden
- **Recommendation:** Notion wiki (easiest for Nicole to maintain) or static Markdown on repo

**Phase 3.14: Build & Launch** (1–2 weeks)
- [ ] Create wiki structure & navigation
- [ ] Write/port all articles
- [ ] Add search functionality (if not built-in)
- [ ] Promote from homepage, contact flow, blog
- [ ] QA internal links, formatting

**Timeline:** 3–4 weeks  
**Cost:** Free (GitHub Pages, Notion) to $50/mo (custom hosting)

---

### **5. AI Website Bot (Support Chatbot)**

**Current State:**  
- No chatbot or live chat  
- Contact form only way to reach business  

**Phase 3.15: Bot Strategy** (1 week)
**Options:**
- **OpenAI Assistant + Langchain** (most capable) — $20–100/mo depending on volume
- **Chatbase** (trained on your docs) — free tier, $20/mo paid, drag-drop embed
- **Intercom** (full customer support suite) — $50/mo+
- **HubSpot Chatbot** (free tier) — basic but solid

**Recommendation:** Chatbase (cheapest, fastest to deploy)

**Phase 3.16: Training & Setup** (1 week)
- [ ] Choose platform
- [ ] Feed it your FAQ, blog, service pages (PDF/URL scrape)
- [ ] Write initial bot personality (friendly, professional, redirect to Nicole for complex Q)
- [ ] Set up hand-off to contact form or email
- [ ] Test 50+ Q&A scenarios

**Phase 3.17: Deployment & Monitoring** (ongoing)
- [ ] Embed widget on homepage (bottom-right corner)
- [ ] Monitor conversation logs; improve FAQ based on questions
- [ ] Track response satisfaction (thumbs up/down)
- [ ] Monthly review of "escalation to human" conversations

**Timeline:** 2–3 weeks  
**Cost:** Free–$100/mo (depends on platform & volume)

---

### **6. Blog Automation / Content Publishing**

**Current State:**  
- 3 hand-written blog posts in `/blog/`  
- No publishing schedule or CMS  
- Requires manual HTML edit to add posts

**Phase 3.18: Content Calendar & Strategy** (1 week)
- [ ] Plan blog schedule (1–2 posts/month, topics for 6 months)
- [ ] Assign categories (Care, Design, Trends, Behind the Scenes, FAQs)
- [ ] Plan SEO keywords per post
- [ ] Nicole writes posts in Google Docs (easier than HTML)

**Phase 3.19: Publishing Workflow** (1 week)
**Options:**
- **Option A (Simple):** Markdown repo + GitHub Actions to auto-generate HTML → deploy
  - Easiest for Nicole (write in Markdown), version control, free, CI/CD
- **Option B (CMS):** WordPress.com embed or Contentful API → fetch posts dynamically
  - Better for collaboration, scheduling, but adds complexity
- **Option C (Manual):** Keep current HTML workflow, optimize for ease

**Recommendation:** Option A (Markdown + GitHub Actions) — best balance

**Phase 3.20: Automation & Publishing** (2 weeks)
- [ ] Create blog post Markdown template (frontmatter: date, title, image, excerpt, tags)
- [ ] Build GitHub Actions workflow to:
  - Convert Markdown → HTML
  - Update blog index
  - Regenerate sitemap
  - Deploy to GoDaddy
- [ ] Set up auto-social-media posting (Buffer, Later, or IFTTT)
- [ ] Monitoring: GA4 blog traffic, engagement metrics

**Timeline:** 3–4 weeks  
**Cost:** Free (GitHub, Buffer free tier) to $20/mo (Contentful, Buffer Pro)

---

## 🎯 Phase 3 Timeline (Proposed)

| Component | Weeks | Start | End | Dependencies |
|-----------|-------|-------|-----|--------------|
| **1. Swag Store** | 4–6 | W1 | W4–6 | Platform choice by W1 |
| **2. Gallery Expansion** | 4–8 | W1 | W4–8 | Photo shoots in parallel |
| **3. SEO Implementation** | 4–8 | W2 | W5–9 | Can start anytime |
| **4. Knowledge Base** | 3–4 | W3 | W6–7 | Content writing in parallel |
| **5. AI Bot** | 2–3 | W4 | W6–7 | Depends on wiki content |
| **6. Blog Automation** | 3–4 | W5 | W8–9 | Platform choice by W5 |

**Critical Path:** Swag Store (widest range) + Gallery (photo shoots slow) = 8 weeks  
**Recommended Sprint:** Start with Swag Store decision + SEO audit (both can run in parallel); defer Blog automation until posting schedule is clear.

---

## 📊 Success Metrics

| Metric | Target | Check |
|--------|--------|-------|
| **Swag Store** | $500+/mo in swag sales | Monthly revenue report |
| **Gallery** | 50+ before-and-after pairs, 40%+ mobile traffic | GA4 traffic by section, time-on-page |
| **SEO** | Top 10 search results for "cabinet refinishing wilmington nc" | Google Search Console, rank tracker |
| **KB/Wiki** | 300+ monthly visitors from organic search | GA4 /wiki traffic |
| **Bot** | 50%+ of homepage visitors engage with bot; 30%+ escalate to contact | Chatbot analytics, contact form volume |
| **Blog** | 2 posts/month, 200+/month blog traffic | Editorial calendar, GA4 blog traffic |

---

## 📝 Decision Matrix (NEXT MEETING)

Before proceeding, confirm:

1. **Swag Store:** Printify (dropship), Shopify (full), or Etsy (hybrid)?
2. **Booking:** Calendly or Google Appointments? (cost/preference)
3. **Blog:** GitHub Actions + Markdown, WordPress embed, or status quo?
4. **Timeline:** Full parallel (8 weeks) or phased (start with 1–2 initiatives)?
5. **Budget:** Max monthly spend on tools/services?

---

Generated: June 18, 2026  
Next Review: After bugfix-1 closed
