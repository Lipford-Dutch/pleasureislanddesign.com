# Measurement Plan — Pleasure Island Design

How the website tracks conversions, and exactly what to configure in GA4 and
Google Ads to make the data actionable. Written for the current stack: static
site + `js/pleasure-island-scripts.js`, with **GA4** and **Google Tag Manager**
already installed.

- GA4 property: `G-X0PJB95RBE` (gtag, loaded in `index.html`)
- GTM container: `GTM-W2TMT5K8`
- Conversion logic: `trackConversion()` in `js/pleasure-island-scripts.js`

---

## 1. What we measure

The site fires a semantic GA4 event for every meaningful action. The four that
represent real business value are the **key events** (GA4's term for
conversions); the rest are engagement signals.

> **Event names match the key events already configured in this property**
> (`form_submission`, `click_to_call`, `email_click`, `cta_click`,
> `gallery_click`, `scroll_depth`). Earlier drafts used GA4's generic
> `generate_lead`/`phone_call` names; the site was reconciled to the existing
> key events so they receive data after deploy (they previously showed
> "No stream data detected" because nothing fired them).

| Event name | Fires when | Key event? | Notes |
|---|---|:---:|---|
| `form_submission` | Contact form submits successfully | ✅ | The primary lead. Carries `promo` = which special drove it. |
| `click_to_call` | Any `tel:` link tapped | ✅ | Most valuable signal for a local service business. |
| `cta_click` | Any `[data-track]` CTA clicked | ✅ | Carries `event_label` (the CTA) + `promo`. |
| `email_click` | Any `mailto:` link clicked | ✅ | Engagement/contact intent. |
| `gallery_click` | A gallery image is opened | — | Content engagement. |
| `newsletter_signup` | Newsletter subscribe succeeds | — | Top-of-funnel; secondary. |
| `scroll_depth` | 25/50/75/100% depth reached | — | Content engagement. |

Each lead-related event carries `method`, `event_category`, and **`promo`** (the
last special the visitor engaged with — `usa250`, `summer`, `military`,
`referral`, or `none`) so you can see **which special produces leads** in GA4.

---

## 2. GA4 setup (one-time, in the GA4 UI)

1. **Admin → Events → Mark as key event** for: `form_submission`,
   `click_to_call`, `cta_click`, `email_click`. (These already exist in the
   property — just confirm they're toggled on. They'll start receiving data
   after the site is deployed.)
2. **Admin → Custom definitions →** register `method` and `event_category` as
   custom dimensions so they're usable in reports.
3. Build a **Conversions overview** exploration segmented by `method` to see
   which path (form vs phone vs booking) produces leads.

### QA with DebugView
- Install the **Google Analytics Debugger** extension (or append `?debug_mode=1`).
- Open **Admin → DebugView**, then exercise each action on the live site and
  confirm the event + parameters appear. This is the fastest way to verify
  before relying on the numbers.

---

## 3. Google Ads conversion tracking (activate when running ads)

The code is wired but **dormant** until an Ads conversion ID + labels are set —
no Ads calls fire before then, so there's nothing to remove if ads aren't
running yet.

### Steps
1. In **Google Ads → Goals → Conversions**, create one conversion action per
   event you want to bid on (start with `form_submission`, `click_to_call`,
   `cta_click`). Choose **"Import from a website / use the tag"** with
   the Google tag, not a separate snippet.
2. Each conversion action gives you a **conversion ID** (`AW-XXXXXXXXX`, shared
   across the account) and a **conversion label** (per action).
3. Provide them to the site in **one** of two ways:

   **Option A — inline config (simplest).** Add before
   `js/pleasure-island-scripts.js` loads in `index.html`:
   ```html
   <script>
     window.PID_ANALYTICS = { googleAds: {
       conversionId: 'AW-XXXXXXXXX',
       labels: {
         form_submission: 'AbC-D_efG-h12',
         click_to_call:   'IjK-L_mnO-p34',
         cta_click:       'QrS-T_uvW-x56',
         newsletter_signup: ''   // leave '' to skip
       },
       leadValue: 0   // optional $ value per conversion
     }};
   </script>
   ```
   **Option B — edit the `ADS` defaults** at the top of
   `js/pleasure-island-scripts.js` (same fields).

4. Also register `AW-XXXXXXXXX` with the Google tag so the account is linked
   (Ads → Data manager, or a GTM Google Ads Conversion tag). Once set,
   `trackConversion()` fires `gtag('event', 'conversion', { send_to, value, currency })`
   alongside the GA4 event automatically.

### Recommended: import GA4 key events instead of duplicating tags
The cleanest setup is to **link GA4 to Google Ads** (GA4 Admin → Product links →
Google Ads) and **import** the GA4 key events as Ads conversions. Then you don't
need the `AW-` labels at all — GA4 is the single source of truth. Use the inline
`AW-` path only if you specifically want gtag-side conversions (e.g. for
enhanced conversions configured separately).

---

## 4. Call tracking note

`click_to_call` fires on `tel:` **clicks**, which is the right signal on mobile.
It does not confirm a call connected or its duration. If phone leads become the
primary channel, add a call-tracking provider (e.g. Google Ads call reporting,
or a CallRail number) for connected-call and duration data.

---

## 5. Change log

- **2026-07** — Introduced `trackConversion()`; standardized on GA4-recommended
  event names, later reconciled to the property's existing key events
  (`form_submission`, `click_to_call`, `cta_click`, `email_click`,
  `gallery_click`, `scroll_depth`) and added per-promo attribution. Previously
  the form fired a generic `form_submit` event and phone/email clicks were
  untracked.
