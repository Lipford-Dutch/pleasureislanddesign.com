# Google Ads — First 30 Minutes (Do This In Order)

A click-by-click session to turn spend into booked consultations. Pairs with
the full `google-ads-campaign-pack.md`. Do the phases **in order** — Phase 1 is
the difference between Google optimizing for leads vs. flying blind.

> **You have two linked Ads accounts** (seen in GA4 access management:
> `106-108-2603` and `158-692-4305`). Decide which one is the "live" account for
> these campaigns and do everything below in that one. If unsure which has
> billing set up, check **Ads → Billing** in each. Ignore/pause the other so
> spend and reporting aren't split.

---

## Phase 0 — Deploy first (5 min)
Ads pointing at stale pages waste money.
1. cPanel → Git Version Control → **Update from Remote** → **Deploy HEAD Commit**.
2. In an **incognito** window, confirm: new logo in the header, USA 250 + Summer
   specials on `/specials/`, and the contact form submits with a 10+ char message.

## Phase 1 — The conversion unlock (10 min) — BEFORE spending a dollar
Your GA4 key events (`form_submission`, `click_to_call`, `cta_click`,
`email_click`) now receive data from the site. Wire them into Ads:
1. On the **live** site, submit the contact form once and tap the phone link
   (seeds the events so they're importable).
2. **GA4** (analytics.google.com) → Admin → **Events** → confirm
   `form_submission`, `click_to_call`, `cta_click`, `email_click` are toggled
   **Mark as key event**. (They already exist — they were just never receiving
   data. This is the fix for the "No stream data detected" you saw.)
3. GA4 → Admin → **Product links → Google Ads** → link your live Ads account.
4. **Google Ads** → Tools → **Conversions** → **New conversion** → **Import** →
   **Google Analytics 4 (Web)** → import `form_submission` + `click_to_call`
   (set **Primary**), and `cta_click` (set **Secondary**).
5. Give it ~a day to register the first conversions, then set campaigns to
   **Maximize Conversions** bidding.

## Phase 2 — Pause the losers (5 min)
Open the two existing campaigns in the live account.
- If a campaign is **Smart** or **Performance Max**, or **Conversions = none** →
  **pause it**. A mis-tracked campaign's history isn't worth keeping.
- Full audit checklist: `google-ads-campaign-pack.md` §1.

## Phase 3 — Import the new campaigns (10 min)
1. Install **[Google Ads Editor](https://ads.google.com/home/tools/ads-editor/)**
   (free desktop app) and sign into the live account.
2. **Account → Import → From file** → import
   `automation/google-ads/keywords.csv`, then `negative-keywords.csv`.
3. Set on **each** campaign before posting:
   - **Locations:** "Presence: people **in or regularly in**" your towns
     (NOT "interested in" — that's the #1 budget leak).
   - **Networks:** **Search only** (turn **Display OFF**).
   - **Budget:** Campaign 1 = **$47/day**, Campaign 2 = **$20/day** (~$2k/mo).
   - **Bidding:** Maximize Conversions (switch on after Phase 1 conversions land).
4. Paste the RSA ad copy from the pack §4. Add the **call asset** (910) 444-1230
   and sitelinks (Gallery, Reviews, Specials, The Swag Shop).
5. **Post**.

---

## Which special is working? (built-in)
Every lead now carries a **`promo`** parameter (`usa250`, `summer`, `military`,
`referral`, `none`) — set from the last special CTA the visitor clicked.
- **GA4:** Reports → Engagement → Events → `form_submission` → break down by
  `promo` (register `promo` as a custom dimension first: Admin → Custom
  definitions → Create → event parameter `promo`).
- Read it as: "of the leads that came in, which special had they engaged?"
  Shift ad emphasis and budget toward the special with the best lead share.

## The two mistakes that quietly drain budget
1. **Location = "interested in"** instead of "in or regularly in" → out-of-state
   clicks. Fix in each campaign's Location settings.
2. **Display network left on** for a Search campaign → cheap junk impressions.
   Turn it off.

## Week-1 checkpoints
- Day 2: confirm conversions are importing (Ads → Conversions shows recent count).
- Day 4: Search terms report → add negatives, pause any 0-conversion ad group
  over $150 spend.
- Day 7: compare cost/lead to the ~$55 target; shift budget to the cheaper campaign.
