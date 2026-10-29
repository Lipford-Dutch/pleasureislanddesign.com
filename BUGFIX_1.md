# Bugfix-1 — Forms, Reviews, Blog Scheduler

Single source of truth for the `bugfix-1` branch. Supersedes the earlier
`BUGFIX_IMPLEMENTATION.md`, `DEPLOYMENT_CHECKLIST.md`, and
`GOOGLE_PLACES_API_SETUP.md` (now consolidated here). Phase-3 planning lives in
`PHASE3_ROADMAP.md`.

---

## What changed

| Area | File(s) | Status |
|------|---------|--------|
| Contact form | `forms/contact.php` | Working — POSTs JSON, validates, emails |
| Newsletter | `forms/newsletter.php` | Working — dedup + welcome email |
| Reviews | `forms/get-reviews.php` | Code ready — **needs Google API key + Place ID** |
| Blog scheduling | `blog/publish-scheduled.php`, `blog/scheduled-posts.json` | Working — bulk-write, staggered release |
| Shared logic | `forms/lib/form-helpers.php` | All validation/sanitization (DRY, tested) |
| Tests | `tests/unit-tests.php` | 34 tests, exercise the real shared lib |
| Frontend wiring | `js/pleasure-island-scripts.js` | Posts to `/forms/*.php` |

Architecture note: every validation/sanitization rule lives **once** in
`forms/lib/form-helpers.php`. The handlers and the test suite both call those
`pid_*` functions, so the tests guard the exact code that runs in production
(verified by mutation test).

---

## ⚠️ DELIVERABILITY — read before relying on the contact form

The handlers use PHP `mail()`. On GoDaddy shared hosting this **works**, but
inbox delivery to Gmail is not guaranteed because `mail()` has no SPF/DKIM
signing by itself. Mitigations, in order of effort:

1. **Minimum (do this):** In GoDaddy cPanel, make sure the domain's SPF record
   includes GoDaddy's mail servers and that an email account exists for
   `noreply@pleasureislanddesign.com` (the `From:` address). Without a real
   sending mailbox, Gmail may reject or spam the message.
2. **Better:** Configure cPanel email + DKIM (cPanel → Email Deliverability →
   "Repair"). This signs outgoing mail and dramatically improves inbox rate.
3. **Best (if delivery is critical):** Route mail through an authenticated SMTP
   relay (e.g. a transactional provider). Would require swapping `mail()` for
   SMTP in the two handlers — not done, kept simple per project preference.

**Always run a live test submission and confirm the email lands in the inbox
(not spam) before considering the form "done."**

---

## Deploy

1. **Pre-flight (local):**
   ```bash
   php -l forms/contact.php && php -l forms/newsletter.php \
     && php -l forms/get-reviews.php && php -l blog/publish-scheduled.php
   php tests/unit-tests.php          # expect 34/34
   ```
2. **Push & deploy:** merge `bugfix-1` → `main`, then in GoDaddy cPanel → Git
   Version Control → **Pull** `main`. `.cpanel.yml` copies `forms/` into
   `public_html/` automatically.
3. **Writable runtime dirs** (created automatically on first request, but verify
   they're writable): `.logs/`, `.data/`, `.backups/`. These are gitignored.
4. **Smoke test on production:**
   - Submit the contact form → confirm email arrives (see DELIVERABILITY above).
   - Sign up for the newsletter → confirm welcome email.
   - `curl https://www.pleasureislanddesign.com/forms/get-reviews.php` → returns
     JSON (demo reviews until the API is configured).

---

## Google Places API (reviews) — setup

The reviews endpoint returns demo reviews until two values are supplied. These
must be obtained through the Google Cloud Console in a browser (cannot be
created from the build container):

1. https://console.cloud.google.com → create/select project.
2. **APIs & Services → Library → Places API → Enable.**
3. **Credentials → Create credentials → API key.** Restrict it to "Places API"
   and to the site's HTTP referrers (`https://*.pleasureislanddesign.com/*`).
4. **Place ID:** search the business on Google Maps; copy the Place ID
   (`ChIJ…`). Or use the Place ID Finder tool in Google's Maps docs.
5. **Configure on GoDaddy** (pick one):
   - `.htaccess` in `public_html`:
     ```apache
     SetEnv GOOGLE_PLACES_API_KEY "AIza…"
     SetEnv GOOGLE_PLACE_ID "ChIJ…"
     ```
   - or edit the two `getenv()` lines at the top of `forms/get-reviews.php`.
6. Verify: `curl …/forms/get-reviews.php` now returns live reviews. Responses
   are cached 1 hour to stay inside the free quota (25 calls/day).

**Do not commit the API key to git.**

---

## Blog scheduling (bulk-write, staggered release)

1. Write posts as HTML into `blog/drafts/<slug>.html` (must contain an `<h1>`
   and a `<time datetime="YYYY-MM-DD">`).
2. Add an entry to `blog/scheduled-posts.json` with a `publish_date`.
3. Publishing:
   - Manual: `php blog/publish-scheduled.php`
   - Automated (recommended): cPanel → Cron Jobs, daily:
     `php /home/<acct>/public_html/blog/publish-scheduled.php`
4. On the publish date the post moves from `drafts/` to `blog/`, a backup is
   written to `.backups/`, and the sitemap is updated.

---

## Still open (not in this branch)

- **Hero & mobile design pass** — CSS audit pending (see PHASE3_ROADMAP.md).
- **Calendar → real booking tool** — decided (Calendly / Google Appointments),
  not yet implemented.
- **Misspellings** — automated scan found none; awaiting specific examples.
