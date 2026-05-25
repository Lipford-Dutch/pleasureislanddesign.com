# Phase 3 — Feature Development Backlog

> Collected during Phase 2 design modernization. Items below are the next
> wave of features to build once Phase 2 is stable and merged.

---

## 🔍 SEO & Organic Traffic

- [ ] **Keyword research** — Identify top cabinet refinishing terms for Wilmington/SE NC
- [ ] **On-page SEO audit** — Title tags, H1-H6 hierarchy, meta descriptions per section
- [ ] **Semantic HTML expansion** — Article schema for blog posts
- [ ] **Location landing pages** — Dedicated pages for: Wilmington, Kure Beach, Carolina Beach, Leland, Wrightsville Beach
- [ ] **Structured data expansion** — Add Service, Review, FAQPage, BreadcrumbList schema
- [ ] **Open Graph images** — Custom branded OG image per page
- [ ] **Image SEO** — Descriptive filenames, alt text audit, EXIF data cleanup
- [ ] **Core Web Vitals** — Achieve green LCP, FID/INP, CLS scores
- [ ] **XML Sitemap** — Auto-generate with all pages and images
- [ ] **Internal linking strategy** — Cross-link services, locations, blog posts

---

## 📊 Analytics & Tracking

- [ ] **GA4 Enhanced Ecommerce** — Track quote form as conversion event
- [ ] **Google Ads conversion tracking** — Set up tag for future ad campaigns
- [ ] **Back-reference link strategy** — Identify opportunities for:
  - Local business directories (Yelp, BBB, Angi, HomeAdvisor)
  - Nextdoor business profile
  - Chamber of Commerce listing
  - Local news/blog features
- [ ] **UTM parameter tracking** — Consistent UTM strategy for all campaigns
- [ ] **Heatmapping** — Integrate Hotjar or Microsoft Clarity (free)
- [ ] **A/B testing** — CTA button text, hero headline, quote form layout
- [ ] **Call tracking** — Track phone call conversions from website

---

## ⭐ Dynamic Reviews Integration

- [ ] **Google Reviews API** — Fetch and display live reviews dynamically
- [ ] **Nextdoor reviews** — Embed or display Neighborhood Favorite recognition
- [ ] **Facebook reviews** — Pull from Facebook page via API
- [ ] **Review aggregator widget** — Display combined rating across platforms
- [ ] **Review response automation** — Template responses for common review types
- [ ] **Review request flow** — Post-job email/SMS asking satisfied clients to leave review

---

## 📝 Blog Section

- [ ] **Blog architecture** — Static site approach (markdown files → HTML) or CMS
- [ ] **Content calendar** — 12-month editorial calendar for SEO posts
- [ ] **Initial blog posts** (suggested topics):
  - "How to Know When Your Cabinets Need Refinishing vs. Replacing"
  - "Cabinet Color Trends 2026 for NC Coastal Homes"
  - "The Complete Guide to Cabinet Hardware"
  - "Before & After: Our Biggest Transformations"
  - "Cabinet Refinishing vs. Painting: What's the Difference?"
  - "How to Care for Refinished Cabinets"
- [ ] **Blog categories** — Tips, Before/After, Trends, How-To, Project Features
- [ ] **RSS feed** — Auto-generate for syndication
- [ ] **Social sharing** — Share buttons on each post
- [ ] **Author bio** — Nicole Rayment bio block on posts

---

## 🛍️ Sales & Specials

- [ ] **Promotions section** — Seasonal flyer display (spring refresh, summer, holiday)
- [ ] **PDF flyer upload** — Simple admin interface for uploading promotion flyers
- [ ] **Promo code tracking** — UTM/coupon codes for promotions
- [ ] **Email campaign integration** — Connect specials to email newsletter
- [ ] **Countdown timers** — For time-limited offers

---

## 🧢 Swag Store (3 Items)

> Small, simple store: shirts, hats, koozies

- [ ] **Platform decision** — Printify + Shopify Lite, or Spring (Teespring), or Printful + custom checkout
- [ ] **Product design** — Branded shirts, hats, koozies using PID logo/colors
- [ ] **Integration** — Embed store or link out to storefront
- [ ] **Product descriptions & photography**
- [ ] **Pricing strategy** — At-cost or small markup for brand awareness

---

## 🎬 Video / Commercial Area

- [ ] **Platform decision** — YouTube (recommended: free, SEO benefits) vs. Vimeo vs. Cloudflare Stream
- [ ] **Video content plan**:
  - Business intro/welcome video
  - Process walkthrough (prep to finish)
  - Before/after transformation time-lapses
  - Client testimonial videos
  - Nicole interview / founder story
- [ ] **YouTube channel setup** — Optimize channel with branding
- [ ] **Video embed section** — YouTube embed in video section on site
- [ ] **Video SEO** — Titles, descriptions, timestamps for YouTube algorithm
- [ ] **Video thumbnail brand consistency** — Custom thumbnail template

---

## 💌 Email Marketing

- [ ] **Platform selection** — Mailchimp, Klaviyo, or ConvertKit
- [ ] **Welcome sequence** — 3-email sequence for new subscribers
- [ ] **Newsletter template** — Branded monthly newsletter
- [ ] **Segments** — Leads, customers, referral partners
- [ ] **Automated flows** — Quote follow-up, post-project thank you, review request

---

## 🔧 Technical / Infrastructure

- [ ] **Production hosting decision** — Self-hosted vs. Netlify vs. Vercel vs. AWS S3+CloudFront
- [ ] **Custom domain on GitHub Pages** — CNAME record for production preview
- [ ] **CDN setup** — For image delivery optimization
- [ ] **Web Application Firewall** — Basic WAF if self-hosted
- [ ] **SSL certificate** — Auto-renewing via hosting provider or Let's Encrypt
- [ ] **Backup strategy** — Automated repo + asset backups
- [ ] **Staging environment** — Separate staging URL for testing before production
- [ ] **Monitoring & alerts** — Uptime monitoring (UptimeRobot or similar, free tier)
- [ ] **Google Search Console** — Set up and verify, submit sitemap
- [ ] **Image CDN** — Consider Cloudinary for image optimization pipeline

---

## ♿ Accessibility

- [ ] **WCAG 2.1 AA audit** — Full accessibility review
- [ ] **Color contrast** — Verify all text meets 4.5:1 ratio
- [ ] **Keyboard navigation** — All interactive elements keyboard accessible
- [ ] **Screen reader testing** — Test with NVDA/JAWS/VoiceOver
- [ ] **ARIA labels** — Audit and complete ARIA label coverage
- [ ] **Focus indicators** — Visible focus styles for all interactive elements
- [ ] **Alt text audit** — All images need descriptive alt text
- [ ] **Form accessibility** — Labels, error messages, success states

---

## 🎨 Design Enhancements

- [ ] **Dark mode** — Complete dark mode implementation
- [ ] **Print styles** — Printable quote/service sheet
- [ ] **Animation polish** — Refine scroll animations, micro-interactions
- [ ] **Loading states** — Skeleton screens for dynamic content
- [x] **Error pages** — Custom 404 page *(done Phase 3)*

---

## 🏗️ Landing Pages & Trade Sections

> Moved from Phase 4 — high ROI for designer/builder audience

- [ ] **Interior Designer Landing Page** — Dedicated `/designers` page with trade program details, reference list, downloadable spec sheet
- [ ] **Contractor/Builder Landing Page** — Dedicated `/builders` page explaining partnership workflow and turnaround SLA
- [ ] **Featured Project Case Study** — Deep-dive section: one project shown as before → process photos → after, with client quote. Builds narrative trust.
- [ ] **Location landing pages** — Remaining pages: Kure Beach, Carolina Beach, Leland, Wrightsville Beach *(Wilmington done Phase 3)*

---

## 📸 Content & Media

- [ ] **Instagram Feed Grid** — Live @pleasureislanddesign feed embedded in gallery or footer section
- [ ] **Video Testimonials** — Support embedding short client video clips alongside text reviews
- [ ] **Project 360° Tours** — Interactive room tours for select showcase projects
- [ ] **Before/After Photo Submission Portal** — Let past clients submit their own project photos (with approval workflow)
- [ ] **Progressive Image Loading** — Replace heavy gallery images with WebP + srcset for Core Web Vitals

---

## 🛠️ UX Enhancements

- [ ] **Sticky Header CTA on Desktop** — Show "Request Consultation" button in header after scrolling past hero
- [ ] **Seasonal Promotions System** — CMS-driven banner for Sales/Specials (spring refresh, holiday booking)
- [ ] **Material Sample Request** — "Request a finish sample" form for designers and builders evaluating finishes
- [ ] **Virtual Consultation Option** — Zoom/video call booking option alongside in-person for out-of-area designers

---

## 📋 Notes

- **Priority order suggested:** SEO → Reviews → Blog → Video → Swag Store → Landing Pages
- **Quick wins:** Google Reviews integration, heatmapping, back-reference links
- **Biggest ROI:** Location landing pages + blog posts for organic traffic
- **Platform recommendation for video:** YouTube (free, SEO boost, no hosting costs)
- **Swag store recommendation:** Printify + custom checkout or Printful (no inventory needed)

---

## Phase 3 Progress

> Items completed in Phase 3:

- [x] Blog section: listing page + 3 SEO posts
- [x] Specials page (`/specials/`)
- [x] Shop page (`/shop/`)
- [x] Custom 404 page
- [x] Location landing page: Wilmington NC (`/locations/wilmington.html`)
- [x] Video section placeholder on homepage
- [x] Blog teaser section on homepage
- [x] Service area map section on homepage
- [x] Skip-to-content accessibility link
- [x] Microsoft Clarity heatmapping
- [x] Sitemap.xml expanded with all new pages
- [x] Nav updated with Blog + Specials links
- [x] Phase 4 backlog merged into Phase 3

_Last updated: Phase 3 Feature Development_
_Next review: Pre-release testing_
