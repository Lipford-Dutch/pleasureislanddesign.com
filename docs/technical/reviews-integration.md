# Live Google Reviews — Cost Reality & Decision

**Short version: at this site's volume the Places API is effectively $0/month
— but it does require a credit card on the Google Cloud project, which is a
legitimate reason to skip it. Skipping costs nothing: the curated reviews
already display.**

## The numbers

- Google's Places API pricing (since March 2025) includes a **monthly free
  call allowance per SKU** (thousands of calls/month for the Place Details
  tier that returns reviews) before any billing starts.
- Our endpoint (`forms/get-reviews.php`) caches responses for **1 hour**, so
  the theoretical maximum is ~**720 calls/month** — far below the free tier.
- However, Google requires a **billing account (card on file)** to issue any
  API key, and an unprotected key that leaks *can* be abused into real
  charges.

## If you ever enable it, do these three things
1. Restrict the API key to the **Places API only** + HTTP referrer
   `www.pleasureislanddesign.com/*`.
2. Set a **budget alert at $5** on the Cloud project (Billing → Budgets).
3. Set daily quota caps (Places API → Quotas → e.g. 100 requests/day).

## Current state (nothing to do)

With no key configured, the site shows the **hand-curated 5-star testimonials
plus the Nextdoor recommendations section** — real quotes, zero API risk,
zero cost. The dynamic integration stays dormant in the code; it activates
only if `GOOGLE_PLACES_API_KEY` + `GOOGLE_PLACE_ID` are ever set.

**Free alternative if freshness matters:** every month or two, copy any new
5-star Google review text into the curated cards in `index.html` (and/or the
demo set in `forms/get-reviews.php`). Manual, but 10 minutes and genuinely $0.
