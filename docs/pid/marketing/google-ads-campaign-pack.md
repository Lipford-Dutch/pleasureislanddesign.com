# Google Ads Campaign Pack — PID Summer 2026

Everything needed to audit the two existing campaigns and rebuild them for
lead volume, sized for a **~$2,000/mo** budget. Written to be executed in the
Google Ads UI (or bulk-imported via Google Ads Editor using the CSVs in
`automation/google-ads/`).

> **Why this is a document and not a done deed:** this repo's tooling can't
> reach a logged-in browser session on your machine — Claude Code cloud
> sessions run in an isolated container with no access to your local Chrome.
> Everything below is therefore staged for a 30–45 minute working session in
> your Ads console, with the exact click-paths written out. The site-side tag
> work IS done in code and activates the moment you paste the two IDs (§5).

---

## 1. Audit the two existing campaigns first (15 min)

Work through this in **Campaigns → [each campaign]**:

| Check | Where | Red flag → action |
|---|---|---|
| Campaign type | Overview | "Smart" or "Performance Max" with no asset groups → rebuild as Search |
| Location targeting | Settings → Locations | "People interested in" instead of "People in or regularly in" → switch (stops out-of-area clicks) |
| Location scope | Settings → Locations | Whole-state NC or 50mi+ radius → tighten to the service area list (§2) |
| Search partners / Display expansion | Settings → Networks | Both ON is a silent budget leak for local service → turn OFF Display, keep partners optional |
| Bid strategy | Settings → Bidding | "Maximize clicks" → switch to Maximize Conversions once §5 tracking is live |
| Conversions counted | Tools → Conversions | If it lists only "page views" or nothing → this is the core problem; fix via §5 |
| Search terms | Insights → Search terms | DIY/jobs/how-to terms burning spend → add negatives (§3) |
| Ad strength | Ads | "Poor/Average" RSAs → replace with §4 copy |
| Sitelinks/calls | Assets | No call asset → add (910) 444-1230; no sitelinks → add Gallery/Reviews/Specials |

**Decision rule:** if either existing campaign is a Smart campaign or has no
conversion tracking, don't remodel it — pause it and build fresh from §2.
History on a mis-configured campaign isn't worth preserving.

## 2. Target structure (2 campaigns, $2,000/mo)

### Campaign 1 — "PID | Search | Cabinet Refinishing" — $1,400/mo (70%)
- Type: Search · Networks: Google Search only
- Locations (People in or regularly in): Wilmington, Carolina Beach, Kure
  Beach, Wrightsville Beach, Leland, Hampstead, Compass Pointe NC + 15 mi
  around 28412
- Bidding: Maximize Conversions (add tCPA ≈ $55 after ~15 conversions)
- Ad schedule: Mon–Sat 6am–9pm (calls land in business hours)

| Ad group | Theme | Example keywords (phrase/exact — full list in CSV) |
|---|---|---|
| Refinishing — Core | "cabinet refinishing wilmington nc", "cabinet refinishers near me" | 8 kw |
| Painting — Core | "cabinet painting wilmington nc", "kitchen cabinet painters near me" | 8 kw |
| Beach towns | "cabinet painting carolina beach", "cabinet refinishing kure beach" | 6 kw |
| Cost/comparison | "cost to refinish kitchen cabinets", "refinish vs replace cabinets" | 6 kw |

### Campaign 2 — "PID | Search | USA 250 Promo + Brand" — $600/mo (30%)
- Ad group **Brand**: "pleasure island design" (protect the name; cheap clicks)
- Ad group **Promo**: "cabinet refinishing deals", "kitchen cabinet specials
  wilmington" → lands on `/specials/` with the USA 250 banner
- Same geo/bidding as Campaign 1.

## 3. Negative keyword list (apply to both campaigns)

`diy, how to, jobs, hiring, salary, wholesale, supplies, home depot, lowes,
rustoleum, kit, rental, apartment, laminate flooring, countertop, free,
youtube, course, training, spray paint can, furniture flipping`

(Also in `automation/google-ads/negative-keywords.csv`.)

## 4. Responsive Search Ads (3 per ad group; 2 examples)

**Refinishing — Core**
- H: Cabinet Refinishing Wilmington · Factory-Quality Sprayed Finish · Save
  60–80% vs New Cabinets · Kitchens Done in 5–8 Days · Free In-Home
  Consultation · Local, Neighbor-Recommended · 5-Star Rated Craftsmanship ·
  $250 Off Projects $2,500+ · Doors Sprayed In Our Studio · Serving Coastal NC
- D: Boutique cabinet refinishing studio serving Wilmington & Pleasure
  Island. Factory-smooth sprayed finishes that last. / Don't replace —
  refinish. Transform your kitchen in about a week for a fraction of the
  cost. / USA 250th Birthday Special: $250 off projects $2,500+ through Dec
  31, 2026. / Free consultation — call (910) 444-1230.
- Final URL: `https://www.pleasureislanddesign.com/#contact`

**Promo (USA 250)**
- H: $250 Off Cabinet Refinishing · USA 250th Birthday Special · Celebrate
  1776–2026 & Save · Offer Runs Through Dec 2026 · Min. Project $2,500 ·
  Factory-Quality Finishes · Book Your Free Consultation
- D: America turns 250 — your kitchen gets the glow-up. $250 off any
  refinishing project of $2,500+. / Local coastal-NC craftsmanship,
  neighbor-recommended on Nextdoor. Book through Dec 31, 2026.
- Final URL: `https://www.pleasureislanddesign.com/specials/`

Assets for both campaigns: call asset (910) 444-1230 · sitelinks Gallery,
Reviews, Specials, The Swag Shop · callouts "Free Consultation", "5–8 Day
Turnaround", "Licensed & Insured", "$250 Off $2,500+" · location asset (link
Google Business Profile).

## 5. Conversion tracking — the 20-minute unlock (do this FIRST)

The site already fires GA4 key events (`generate_lead`, `phone_call`,
`request_consultation`, `newsletter_signup`) — see `measurement-plan.md`.
The fastest, cleanest path (no code changes needed):

1. **Link GA4 ↔ Google Ads:** GA4 Admin → Product links → Google Ads → link
   the Ads account.
2. **GA4:** Admin → Events → mark the four events above as **key events**
   (fire each once on the live site first so they appear).
3. **Google Ads:** Tools → Conversions → **New** → Import → Google Analytics
   4 → select `generate_lead`, `phone_call`, `request_consultation`. Set
   `generate_lead` + `phone_call` as **Primary** (used for bidding);
   `request_consultation` secondary to start.
4. Wait for first conversions, then move both campaigns to Maximize
   Conversions.

*Optional gtag route:* the site also supports direct `AW-` conversions — add
IDs per `measurement-plan.md` §3. Skip unless you later need enhanced
conversions; the GA4 import above is sufficient and simpler.

## 6. Weekly rhythm (15 min/wk)

1. Search terms report → add negatives, promote winners to exact.
2. Pause any ad group with spend > $150 and 0 conversions after 2 weeks.
3. Check per-lead cost vs the $55 target; shift budget toward the cheaper
   campaign at month end.

## 7. KPI targets (month 1 at $2,000)

| Metric | Target |
|---|---|
| Clicks | 550–800 |
| CTR | ≥ 6% |
| Leads (form + call + booking) | 25–36 |
| Cost / lead | ≤ $60, trending to $45 |
| Booked consultations | ≥ 10 |
