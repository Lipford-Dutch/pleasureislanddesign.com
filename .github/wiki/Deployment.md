# Deployment Guide

How to deploy changes to Pleasure Island Design website.

## Deployment Pipeline

### Automatic Deployment
GitHub Actions automatically deploys changes when PR is merged to main:

1. **PR Created** → Triggers CI checks
2. **All Checks Pass** → PR mergeable
3. **PR Merged** → Deployment workflow runs
4. **Build & Test** → Verify no errors
5. **Publish to GitHub Pages** → Live in ~30 seconds

### Manual Status Check
```bash
# Check GitHub Actions status
gh actions list

# View specific workflow run
gh actions view [run-id]

# View logs for debugging
gh actions view [run-id] --log
```

## Environment URLs

| Environment | URL | Branch | Status |
|---|---|---|---|
| **Production** | https://willyd61.github.io/pleasureislanddesign.com/ | main | Live |
| **Beta/Staging** | phase-beta-release branch | phase-beta-release | Testing |
| **Local Dev** | http://localhost:8000 | Any | Developer |

## Pre-Deployment Checklist

Before pushing changes:

- [ ] **Code Quality**
  - [ ] No console errors
  - [ ] HTML validates
  - [ ] CSS has no errors
  - [ ] JavaScript follows patterns

- [ ] **Testing**
  - [ ] Responsive design works (mobile/tablet/desktop)
  - [ ] All links functional
  - [ ] Forms submit correctly
  - [ ] Images load properly
  - [ ] Analytics firing

- [ ] **SEO**
  - [ ] Canonical tags correct
  - [ ] OG tags correct
  - [ ] Meta descriptions present
  - [ ] Images have alt text
  - [ ] JSON-LD schema valid

- [ ] **Accessibility**
  - [ ] Keyboard navigation works
  - [ ] Color contrast acceptable
  - [ ] Form labels present
  - [ ] ARIA labels where needed

- [ ] **Performance**
  - [ ] Images optimized
  - [ ] CSS minified
  - [ ] JavaScript deferred
  - [ ] Lighthouse score 85+

## Deployment Process

### Step 1: Create Feature Branch
```bash
git checkout phase-beta-release
git pull origin phase-beta-release
git checkout -b feature/your-feature
```

### Step 2: Make Changes & Test Locally
```bash
# Edit files
# Test in browser
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Step 3: Commit Changes
```bash
git add .
git commit -m "feat: description of changes"
# Or multiple commits for logical grouping
git commit -m "fix: specific issue"
git commit -m "docs: update readme"
```

### Step 4: Push to Remote
```bash
git push -u origin feature/your-feature
```

### Step 5: Create Pull Request
```bash
# Via GitHub CLI
gh pr create --title "Brief description" --body "Detailed explanation"

# Or via GitHub web interface
# Visit https://github.com/willyd61/pleasureislanddesign.com
# Click "Compare & pull request"
```

### Step 6: Address Review Comments
```bash
# Make requested changes
git add .
git commit -m "fix: address review feedback"
git push origin feature/your-feature
# Comments automatically update PR
```

### Step 7: Merge PR
```bash
# Merge via CLI
gh pr merge --merge  # Creates merge commit (recommended)
gh pr merge --squash # Squashes commits (clean history)
gh pr merge --rebase # Rebases commits (linear history)

# Or merge via GitHub web interface
```

### Step 8: Verify Deployment
```bash
# Automatic deployment starts immediately after merge
# Check status at: 
# https://github.com/willyd61/pleasureislanddesign.com/deployments

# Or check workflow status
gh actions list
```

## Rollback Procedures

### If Deployment Fails

1. **Check workflow logs:**
```bash
gh actions view [latest-run-id] --log
```

2. **View error details:**
   - Visit GitHub Actions dashboard
   - Click failed workflow
   - Expand error step
   - Read error message

3. **Fix and redeploy:**
   - Fix issue in code
   - Commit and push
   - Previous merge automatically triggers new workflow

### If Wrong Code Was Deployed

1. **Revert commit:**
```bash
git revert [commit-sha]  # Creates inverse commit
git push origin main
```

2. **Or force revert:**
```bash
git reset --hard [previous-good-commit]
git push --force origin main  # Use with caution
```

3. **Create incident issue:**
   - Document what happened
   - How it was caught
   - How it was fixed
   - Prevention for future

## Hotfix Deployments

For critical production issues:

### 1. Create Hotfix Branch
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue
```

### 2. Make Minimal Fix
- Fix ONLY the critical issue
- No other changes
- Keep commit small and focused

### 3. Deploy Immediately
```bash
git add .
git commit -m "hotfix: description"
git push -u origin hotfix/critical-issue
gh pr create --title "Hotfix: description"
# Merge ASAP after brief review
```

### 4. Document Incident
Create issue with:
- What went wrong
- Impact assessment
- Root cause
- Fix implemented
- Prevention measures

## Configuration Management

### Startup Management (pid-startup.html)
Dynamic configuration is managed via `pid-startup.html`:

```bash
# Update configuration
# Edit pid-startup.html with latest settings
# Push changes
# CI/CD automatically syncs to repo

# Configuration includes:
# - Feature flags
# - Analytics IDs
# - API endpoints
# - Version information
```

### Environment Variables
Stored in GitHub Secrets (not in code):
```bash
# View secrets
gh secret list

# Add secret
gh secret set MY_SECRET --body "value"

# Use in workflow
env:
  MY_VAR: ${{ secrets.MY_SECRET }}
```

## Monitoring Deployments

### Real-Time Status
```bash
# Watch deployment in progress
watch -n 5 'gh actions view $(gh actions list | head -1 | awk "{print \\$1}") --log'
```

### Post-Deployment Checks
1. **Visit website:** https://willyd61.github.io/pleasureislanddesign.com/
2. **Check key pages:**
   - [ ] Homepage loads
   - [ ] Blog posts accessible
   - [ ] Forms work
   - [ ] Links functional

3. **Verify analytics:**
   - [ ] Google Analytics receiving data
   - [ ] Clarity tracking active
   - [ ] GTM firing events

4. **Test critical flows:**
   - [ ] Request consultation button works
   - [ ] Newsletter signup functional
   - [ ] Video embeds play
   - [ ] Images load

## Performance Monitoring

### Lighthouse Scores
```bash
npm run test:lighthouse
```

Target scores:
- Performance: 85+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 95+

### Real User Monitoring
- Google Analytics: User behavior, conversions
- Clarity: Heatmaps, session replays
- Custom events: Consultation requests, form fills

## Version History

| Date | Version | Changes | Deployed |
|---|---|---|---|
| 2026-05-25 | 1.0.0 | Initial audit & wiki | Yes |
| Pending | 1.1.0 | Logo redesign, enhanced branding | No |
| Pending | 1.2.0 | Social media assets | No |
| Pending | 2.0.0 | Dynamic startup page | No |

## Troubleshooting Deployments

### Workflow Failures

**Problem:** Deployment workflow fails
```bash
# Check logs
gh actions view [run-id] --log

# Common causes:
# 1. Syntax errors in HTML/CSS/JS
# 2. Broken links or missing images
# 3. Secrets not configured
# 4. Permission issues
```

**Problem:** Changes not live after 30 minutes
```bash
# GitHub Pages cache can take time
# Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
# Or wait up to 5 minutes for CDN propagation
```

**Problem:** Old version still showing
```bash
# Clear browser cache
# Check GitHub Pages settings in repo
# Verify correct branch is deployed (Settings > Pages)
```

## Best Practices

### Always Test First
- Never push directly to main
- Use feature branches
- Test locally before pushing
- Request code review

### Keep Commits Clean
- Logical grouping of changes
- Clear, descriptive messages
- Small commits are easier to review and rollback

### Document Changes
- Update relevant wiki pages
- Add inline code comments for complex logic
- Create issues for discovered problems

### Monitor After Deploy
- Check website loads
- Test critical user flows
- Review analytics for issues
- Watch for error spikes

---

*Last Updated: May 25, 2026*
