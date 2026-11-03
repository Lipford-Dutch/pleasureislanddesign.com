# CI/CD Pipeline

## Workflows Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | All PRs + push to main | Lint HTML/CSS/JS, validate assets and links |
| `deploy.yml` | Push to main | Publish the public site files (only) to the GitHub Pages mirror |
| `docs.yml` | Push to main + PRs to main | Build MkDocs (strict) and upload it as an artifact |
| cPanel `.cpanel.yml` | cPanel Git deploy of `main` | Deploy the public site to production (GoDaddy) |

## CI Workflow (`ci.yml`)

Runs on every PR and push to main. All checks must pass before code can be merged.

**Steps:**
1. Lint HTML with HTMLHint
2. Lint CSS with Stylelint
3. Lint JavaScript with ESLint
4. Validate image references
5. Validate anchor links
6. Security scan
7. Prettier format check

**Local equivalent:**
```bash
npm run lint
npm run format:check
```

## Deploy Workflow (`deploy.yml`)

Runs on push to main. Publishes a mirror of the public site to GitHub Pages
(Pages source: GitHub Actions). Production is GoDaddy cPanel, not Pages.

**Steps:**
1. Run lint (quality gate)
2. Assemble only the public site files into `_site/` (same set as `.cpanel.yml`;
   drafts, automation, `docs/` and `*.php` are excluded, with a guardrail that fails the job if they appear)
3. Configure GitHub Pages
4. Upload `_site/` as the Pages artifact
5. Deploy to GitHub Pages

**Mirror URL:** https://lipford-dutch.github.io/pleasureislanddesign.com/

## Production Deploy (GoDaddy cPanel)

The production site is deployed from this repo's `main` branch by cPanel Git
Version Control. `.cpanel.yml` removes and re-copies the public directories and
root files into the web root, so stale files (for example old blog drafts) are
cleared on each deploy. `blog-automation/` is intentionally not deployed.

## Docs Workflow (`docs.yml`)

Runs on push to main and on PRs to main. Builds the MkDocs site; it never commits
to `main`, so it works with branch protection.

**Steps:**
1. Copy CHANGELOG.md → docs/release-notes.md (build workspace only, not committed)
2. Build MkDocs site (strict mode — fails on warnings)
3. Upload the built site as the `docs-site` artifact (kept 14 days)

## Adding a New Workflow

1. Create `.github/workflows/your-workflow.yml`
2. Test locally with `act` (optional)
3. Push to a feature branch
4. PR will trigger existing CI
5. Once merged, new workflow activates

## Secrets & Environment Variables

Currently no secrets are required. For future integrations:

- Add secrets at: `Settings → Secrets and variables → Actions`
- Reference in workflows as: `${{ secrets.YOUR_SECRET_NAME }}`
- Never hardcode API keys or passwords in code
