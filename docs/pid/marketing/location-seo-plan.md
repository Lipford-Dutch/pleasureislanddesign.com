# Local SEO Expansion Plan — Location Pages

Goal: rank for "cabinet refinishing / painting [town]" across the coastal-NC
service area (Carolina Beach, Kure Beach, Leland, Wilmington, Wrightsville
Beach, Burgaw), and capture that local intent with dedicated, high-quality
location pages — using a **phased** rollout so each page earns its place.

---

## 1. The key decision: subdomains vs. subdirectories

You asked about `carolina-beach.pleasureislanddesign.com`, `kure.…`, etc.
**My strong recommendation is subdirectories, not subdomains** —
`pleasureislanddesign.com/locations/carolina-beach/`. Here's the honest
industry-standard reasoning:

| | Subdirectory `/locations/kure-beach/` | Subdomain `kure.pleasureislanddesign.com` |
|---|---|---|
| **SEO authority** | Inherits the main domain's authority directly | Google treats it as a **separate site**; authority is diluted/split |
| **Setup** | Just a file/folder — deploys with the current cPanel flow | New DNS record + vhost + SSL **per town** (6×) |
| **Maintenance** | One codebase, one deploy | 6 mini-sites to keep in sync |
| **Analytics** | One GA4 property, clean | Cross-domain tracking headaches |
| **Best for** | **Local service-area landing pages (this exact case)** | Genuinely separate products/brands/apps |

Google's own guidance and the consensus of local-SEO practitioners (Moz, Ahrefs,
Google Search Central) is that for **service-area landing pages**, subdirectories
consolidate ranking signals better and are far less work. Subdomains made sense
in an older era and for truly distinct sites — not for six neighborhood pages of
one cabinet business.

**The site already uses this pattern** — `/locations/wilmington.html` exists and
works. We extend it.

> If you still want the `town.pleasureislanddesign.com` vanity URLs for
> marketing/print, the best of both worlds is: build the real pages as
> subdirectories, then set each subdomain as a **301 redirect** to its
> subdirectory. You get the memorable URL on a business card without splitting
> SEO authority. I've noted this as an optional Phase 4.

**⛔ The risk to avoid regardless of structure:** near-duplicate "doorway pages"
(same text, town name swapped) are a Google penalty. Every location page must
have genuinely unique, useful local content (see §3). This is why we phase it —
quality per page beats six thin pages shipped at once.

---

## 2. Phased rollout

### Phase 1 — Foundation (template + 2 flagship towns)
- Refactor the existing Wilmington page into a reusable **location template**
  (`/locations/<town>/index.html`) with clean URL structure.
- Build **Carolina Beach** and **Kure Beach** first (home turf — "Pleasure
  Island"). These are the strongest local-relevance wins.
- Add each to `sitemap.xml`, interlink from the footer + a new "Service Areas"
  section on the homepage.
- Ship `LocalBusiness` schema per page with the town's `areaServed` + geo.

### Phase 2 — Expand coverage (3 towns)
- Add **Leland**, **Wrightsville Beach**, **Burgaw**.
- Each with unique local content: neighborhoods served, a local project from the
  gallery, town-specific FAQ, driving-distance/"we come to you" copy.

### Phase 3 — Authority & conversion
- 1 locally-focused blog post per town (e.g., "Cabinet refinishing in
  salt-air homes: Kure Beach guide") interlinked to its location page.
- Town-specific review pull-quotes on each page (Nextdoor/Google, where the
  reviewer is from that area).
- Google Business Profile: ensure service areas + posts align with the pages.

### Phase 4 (optional) — Vanity subdomains
- If desired, register `town.pleasureislanddesign.com` and 301-redirect each to
  its `/locations/<town>/` page. Pure marketing convenience; zero SEO downside
  because the canonical content lives in the subdirectory.

---

## 3. What every location page must have (quality bar)

To be an asset, not a doorway page, each needs **unique**:
1. **H1 + title/meta** with "Cabinet Refinishing [Town], NC" (not keyword-stuffed).
2. **200+ words of genuinely local copy** — neighborhoods, coastal considerations
   (humidity/salt air), local landmarks, "serving [town] since 2014".
3. **A real local project** from the gallery (with the town in the caption/alt).
4. **Town-specific FAQ** (2–4 Q&As) — also powers FAQ schema.
5. **`LocalBusiness`/`Service` JSON-LD** with the town's `areaServed` + geo coords.
6. **Local proof** — a review from someone in/near that town where possible.
7. **Clear CTA** to the native contact form + click-to-call (already tracked).
8. **Canonical** self-reference + internal links to/from the homepage and siblings.

---

## 4. Coordinates (for schema, per town)

| Town | Lat | Lng |
|---|---|---|
| Wilmington | 34.2257 | -77.9447 |
| Carolina Beach | 34.0352 | -77.8936 |
| Kure Beach | 33.9963 | -77.9075 |
| Leland | 34.2563 | -78.0447 |
| Wrightsville Beach | 34.2085 | -77.7964 |
| Burgaw | 34.5527 | -77.9289 |

---

## 5. Recommendation & next step

**Proceed with subdirectories, Phase 1 first.** When you give the go-ahead I'll:
1. Build the location template from the Wilmington page.
2. Ship Carolina Beach + Kure Beach with full unique content + schema.
3. Add a "Service Areas" section to the homepage and wire internal links + sitemap.

That's a self-contained PR you can review before we expand to the rest. We hold
on subdomains unless you specifically want the vanity URLs in Phase 4.
