# CI/CD Pipeline

## Workflows Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | All PRs + push to main | Lint HTML/CSS/JS, validate assets and links |
| `deploy.yml` | Push to main | Publish the public site files (only) to the GitHub Pages mirror |
| `docs.yml` | Push to main + PRs to main | Build MkDocs (strict) and upload it as an artifact |
| `cpanel-deploy.yml` | Push to main (site files) + manual | Auto-deploy `main` to production (GoDaddy cPanel) via UAPI, then smoke-test |
| cPanel `.cpanel.yml` | cPanel Git deploy of `main` | Back up `public_html`, then deploy the public site to production (GoDaddy) |

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

Before copying, `.cpanel.yml` archives the current web root to
`$HOME/backups/public_html-YYYYMMDD-HHMMSS.tgz` (outside `public_html`, mode 700)
and keeps only the newest 5 archives.

### Auto-deploy workflow (`cpanel-deploy.yml`)

Runs on push to `main` (changes only under `docs/`, `*.md` or `mkdocs.yml` are
ignored) and on manual dispatch. One deploy at a time (`concurrency: cpanel-deploy`).

**How it works** (all calls are cPanel UAPI over `https://$CPANEL_HOST:2083/execute/...`
with header `Authorization: cpanel $CPANEL_USER:$CPANEL_API_TOKEN`):
1. `VersionControl/update` with `branch=main` — cPanel pulls `main` into
   `~/repositories/pleasureislanddesign.com`
2. `VersionControlDeployment/create` — runs `.cpanel.yml` (backup, then copy)
3. Polls `VersionControlDeployment/retrieve` until that deploy succeeds or fails (3 min timeout)
4. Smoke test: `www` returns 200, the bare domain 301-redirects to `www`,
   `/blog/publish-scheduled.php` and `/blog/scheduled-posts.json` return 404

If `CPANEL_API_TOKEN` (or the user/host secrets) is not set, the job skips with a
notice instead of failing.

**Required repo secrets** (`Settings → Secrets and variables → Actions`):

| Secret | Value |
|--------|-------|
| `CPANEL_API_TOKEN` | cPanel API token named `grokbot-deploy` |
| `CPANEL_USER` | cPanel username |
| `CPANEL_HOST` | cPanel server hostname (no `https://`, no port) |

**Revoking the token:**
1. cPanel → Security → Manage API Tokens → select `grokbot-deploy` → Revoke
2. GitHub → repo Settings → Secrets and variables → Actions → delete `CPANEL_API_TOKEN`
   (or `gh secret delete CPANEL_API_TOKEN --repo Lipford-Dutch/pleasureislanddesign.com`)

After revoking, pushes to `main` will fail at step 1 until the secret is deleted
(then they skip) or replaced with a new token.

**Manual fallback:**
- cPanel → Files → Git™ Version Control → Manage the repo → Pull or Deploy tab →
  Update from Remote, then Deploy HEAD Commit; or
- cPanel → Advanced → Terminal:
  ```bash
  uapi VersionControl update repository_root=$HOME/repositories/pleasureislanddesign.com branch=main
  uapi VersionControlDeployment create repository_root=$HOME/repositories/pleasureislanddesign.com
  ```

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

Secrets in use: `CPANEL_API_TOKEN`, `CPANEL_USER`, `CPANEL_HOST` (see Production Deploy above).

- Add secrets at: `Settings → Secrets and variables → Actions`
- Reference in workflows as: `${{ secrets.YOUR_SECRET_NAME }}`
- Never hardcode API keys or passwords in code
