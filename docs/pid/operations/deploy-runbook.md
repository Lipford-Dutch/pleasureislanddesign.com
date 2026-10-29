# Deploy Runbook — Pushing `main` Live to Production

**Authoritative step-by-step for getting merged changes onto the live site.**

> ⚠️ Deployment is **not automatic.** Merging a PR to `main` updates GitHub only.
> The live GoDaddy/cPanel site does **not** change until you run the deploy
> below. (If the site looks out of date after merging, this is why.)

---

## How deployment actually works

The repo ships a cPanel **Git Version Control** manifest (`.cpanel.yml`). cPanel
keeps a private clone of the repo at `~/repositories/…`; when you **Deploy HEAD
Commit**, it runs the manifest, which copies the public files into
`~/public_html`. Two manual steps are involved: **pull** (Update from Remote),
then **deploy** (Deploy HEAD Commit).

```
GitHub main ──(Update from Remote)──▶ cPanel private clone ──(Deploy HEAD Commit)──▶ public_html (live)
```

Only public files are published. `.git`, `docs/`, `automation/`,
`storefront-beta/`, and build scripts are intentionally kept out of the web root.

---

## Deploy (normal path) — ~2 minutes

1. Confirm `main` is green: the PR's CI checks passed before merge.
2. Log in to **cPanel** (GoDaddy → hosting → cPanel).
3. Open **Files → Git™ Version Control**.
4. Find the `pleasureislanddesign.com` repository → **Manage**.
5. **Pull Latest** tab → **Update from Remote** (fast-forwards the private clone
   to the latest `main`).
6. **Pull and Deploy** tab → **Deploy HEAD Commit**. Wait for the success log
   (`Deploy complete -> …/public_html`).
7. **Verify** (see checklist below).

> If **Update from Remote** fails with "would overwrite local changes," someone
> edited files directly in the private clone. Don't force blindly — check
> `~/repositories/…` over SSH/File Manager first; those edits are otherwise lost.

---

## Post-deploy verification (do every time)

Load `https://www.pleasureislanddesign.com` in a **private/incognito** window
(avoids your browser cache) and confirm:

- [ ] Header shows the current logo and **"The Swag Shop"** appears in the nav
      (quick proof the new build is live).
- [ ] **Contact form:** submit a real test (name, valid email, a message of **10+
      characters**). Expect the success message, not "Something went wrong."
      A too-short message should now show a specific hint, not a generic error.
- [ ] **Newsletter:** submit a test email → success message.
- [ ] Reviews section renders (curated cards until the Google API key is set).
- [ ] Spot-check one blog post and `/shop/` load without 404s.
- [ ] Hard-refresh (Ctrl/Cmd+Shift+R) if CSS/JS looks stale — see caching note.

### First deploy after the form fixes — also confirm
- [ ] After a successful contact submit, a `contact-submissions.jsonl` file
      appears at `~/public_html/.data/` (leads are captured even if email is
      flaky). It must **not** be publicly reachable:
      `https://www.pleasureislanddesign.com/.data/contact-submissions.jsonl`
      should return **404/403** (the `.htaccess` guard). If it downloads, the
      `.htaccess` didn't deploy — re-deploy and re-check.

---

## Rollback

Because the deploy is a copy from `main`, rolling back = pointing `main` at a
good commit, then re-deploying.

1. **Find the last good commit:**
   ```bash
   git log --oneline -10
   ```
2. **Revert the bad change** (safe; keeps history):
   ```bash
   git revert <bad-commit-sha>
   git push origin main
   ```
   (For a range, `git revert <old>..<new>`.)
3. **Re-deploy** via cPanel (Update from Remote → Deploy HEAD Commit).
4. Verify with the checklist.

There is no separate "previous build" to restore — production is always whatever
the last deploy copied. Keeping `main` correct and re-deploying is the rollback.

---

## Caching note

`.htaccess`/CDN may cache CSS/JS. If a change doesn't show after deploy:
- Hard-refresh (Ctrl/Cmd+Shift+R) or check in incognito first.
- If it persists for visitors, bump a version query string on the asset
  (e.g. `styles.css?v=2025-07`) in `index.html` and re-deploy.

---

## One-time configuration (not part of each deploy)

Set in **cPanel → Environment / MultiPHP INI or `.env`** as your host supports:

| Variable | Purpose | Effect if unset |
|---|---|---|
| `GOOGLE_PLACES_API_KEY` | Live Google reviews | Curated review cards show (no error) |
| `GOOGLE_PLACE_ID` | Live Google reviews | Same as above |

Google Ads conversion IDs are set in the site code/GTM, not here — see
`docs/pid/marketing/measurement-plan.md`.

---

## Quick reference

| Task | Where |
|---|---|
| Deploy | cPanel → Git Version Control → Update from Remote → Deploy HEAD Commit |
| Rollback | `git revert` on `main` + push, then re-deploy |
| Verify | Incognito load + form/newsletter test + `.data/` 404 check |
| PHP logs | `~/public_html/.logs/` (contact, newsletter, reviews, blog-publisher) |
