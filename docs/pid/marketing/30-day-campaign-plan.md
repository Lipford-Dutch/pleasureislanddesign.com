# 30-Day Launch Campaign & KPI Plan — Pleasure Island Design

A practical 30-day plan to drive **cabinet refinishing leads** across coastal
NC, tying together the assets already built: the website conversion tracking,
the Instagram content calendar, and the blog pipeline.

> Budgets below are expressed as **percentage allocations** plus an example at a
> **$1,500/mo** test budget. Scale the dollar figures to the actual budget — the
> ratios and priorities hold.

---

## 1. Objective & positioning

**Objective:** generate qualified consultation requests for kitchen cabinet
refinishing in Wilmington and the surrounding coastal NC communities.

**Positioning (consistent across every channel):** boutique, factory-quality
cabinet *refinishing* specialist — not a general painter — at a fraction of
replacement cost. Warm, premium, local, craftsmanship-led.

**Primary service area:** Wilmington, Carolina Beach, Kure Beach, Compass Pointe,
Leland, Hampstead, Wrightsville Beach.

---

## 2. Target & message

| Segment | Trigger | Lead message |
|---|---|---|
| Homeowners with dated-but-solid cabinets | "I don't want the cost/mess of new cabinets" | Refinish, don't replace — save 60–80%, keep your layout |
| Coastal / beach-home owners | Salt air, humidity, resale | Durable factory finish built for coastal NC |
| Recently-moved / renovating | Whole-home refresh | Local specialist, neighbor-recommended, personal experience |

---

## 3. Channels & budget allocation

| Channel | % of budget | Example @ $1,500/mo | Role |
|---|---:|---:|---|
| **Google Search (local intent)** | 45% | $675 | Capture high-intent "cabinet refinishing / painting near me" searches |
| **Google Local Services Ads (LSA)** | 20% | $300 | Pay-per-lead, "Google Screened", top of local results |
| **Meta / Instagram (paid boost + retarget)** | 20% | $300 | Amplify the organic calendar; retarget site visitors |
| **Organic IG + blog (content)** | 0% ad spend | — | Owned reach, SEO, social proof (time, not $) |
| **Reserve / testing** | 15% | $225 | Shift to whatever is producing the cheapest leads by week 3 |

### Google Search — starter structure
- **Campaign:** Search, "Maximize conversions" (switch to Target CPA after ~15
  conversions), geo-fenced to the service area + ~10mi radius.
- **Ad groups by intent:**
  - `cabinet refinishing wilmington nc`, `cabinet painting wilmington nc`
  - `kitchen cabinet refinishing`, `cabinet refinishing near me`
  - Beach towns: `cabinet painting carolina beach`, `cabinet refinishing kure beach`
- **Negatives:** `diy`, `spray paint`, `how to`, `jobs`, `wholesale`, `cost to replace`.
- **Assets:** call extension (the `tel:` number), location, sitelinks to
  Gallery / Reviews / Specials, "Free consultation" callout.
- **Landing:** homepage `#contact` (form + phone both tracked). Consider a
  dedicated `/cabinet-refinishing-wilmington` landing page in month 2.

### Local Services Ads
- Complete Google Screened verification (license/insurance) — highest-trust
  placement and pay-per-lead economics suit a boutique operator.

### Meta / Instagram
- Boost the **best 2–3 organic posts/week** from the calendar (before/after
  reels convert best).
- **Retargeting audience:** site visitors (GTM/GA4 audience) + IG engagers →
  "Book your free consultation" with a before/after creative.

---

## 4. Weekly cadence (organic tie-in to the IG calendar)

The parsed calendar (`automation/instagram/content-calendar.json`, ~12 posts,
Aug 11 – Sep 6 window) drives organic. Run `build_queue.py` to get per-post
bundles, review to `approved`, then schedule. Suggested rhythm:

| Week | Organic focus | Paid focus | Blog |
|---|---|---|---|
| 1 | Before/after carousel + process reel | Launch Search + LSA; install/verify tracking | Publish 1 SEO post (see pipeline) |
| 2 | Detail shots + team/BTS (trust) | Add Meta boost on top-performer | — |
| 3 | Durability / "3 years later" proof | Start retargeting; cut worst Search ad group | Publish 1 post |
| 4 | Promo graphic (seasonal special) + timelapse | Shift reserve to cheapest-lead channel | Recap / roundup |

Blog posts are staged via the hardened publisher
(`blog/publish-scheduled.php`) — see the drafts in `blog/drafts/` (finish them
to full styled pages so the quality gate passes).

---

## 5. KPIs & targets

Track against the GA4 **key events** (see `measurement-plan.md`). Targets are
starting benchmarks for a boutique local service at the example budget — refine
after 2–3 weeks of real data.

| KPI | Source | 30-day target (starter) |
|---|---|---|
| **Leads** (`generate_lead` + `phone_call` + `request_consultation`) | GA4 key events | 15–25 |
| Cost per lead (blended) | Ads spend ÷ leads | ≤ $60 |
| Contact-form conversion rate | `generate_lead` ÷ sessions | ≥ 2.5% |
| Phone-tap rate (mobile) | `phone_call` ÷ mobile sessions | ≥ 3% |
| Search CTR | Google Ads | ≥ 6% |
| IG engagement rate | IG insights | ≥ 4% |
| Consultations booked → quoted | CRM / manual | Track ratio for month 2 targets |

**Lead-quality guardrail:** count only in-service-area, in-scope inquiries as
qualified. A cheap lead from outside the area isn't a win — add geographic
negatives if it recurs.

---

## 6. Launch checklist

- [ ] **Deploy the site** so the merged fixes are live (cPanel → Git Version
      Control → Update, then Deploy HEAD Commit). Nothing below matters until
      production reflects `main`.
- [ ] Verify GA4 key events in **DebugView** (form, phone, booking, newsletter).
- [ ] Mark the four key events as conversions in GA4.
- [ ] Set `GOOGLE_PLACES_API_KEY` + `GOOGLE_PLACE_ID` so live reviews render.
- [ ] Complete **LSA / Google Screened** verification.
- [ ] Build Search campaign; add negatives; connect call/location assets.
- [ ] Link GA4 ↔ Google Ads; import key events as conversions (or set the
      `AW-` config from `measurement-plan.md`).
- [ ] Approve week-1 IG posts (`build_queue.py` → set `approved`) and schedule.
- [ ] Confirm the Google Business Profile is current (hours, photos, service area).

---

## 7. What to review at day 30

1. Cheapest **qualified** lead source → shift the 15% reserve there.
2. Best-converting search terms → promote to their own ad groups; expand negatives.
3. Best organic posts → turn into paid creative and future blog topics.
4. Set month-2 targets from real CPL and close-rate instead of these benchmarks.
