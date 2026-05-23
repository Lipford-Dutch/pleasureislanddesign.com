# CI/CD Pipeline

## Workflows Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | All PRs + push to main | Lint HTML/CSS/JS, validate assets and links |
| `deploy.yml` | Push to main | Deploy website to GitHub Pages |
| `docs.yml` | Push to main / PR merge | Build MkDocs, update release notes |

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

Runs after CI passes on push to main. Deploys the static site to GitHub Pages.

**Steps:**
1. Run lint (quality gate)
2. Configure GitHub Pages
3. Upload site files as artifact
4. Deploy to GitHub Pages

**Live URL:** https://willyd61.github.io/pleasureislanddesign.com/

## Docs Workflow (`docs.yml`)

Runs on push to main and closed (merged) PRs. Builds the MkDocs site and auto-updates release notes.

**Steps:**
1. Copy CHANGELOG.md → docs/release-notes.md
2. Build MkDocs site (strict mode — fails on warnings)
3. Commit updated release notes back to main

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
