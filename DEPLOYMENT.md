# Deployment Guide

## Overview

This is a static website (HTML/CSS/JavaScript) with no build process. Deployment is simple: push changes to `main` branch and they automatically sync to production.

## Deployment Workflow

### 1. Local Development
```bash
# Create a feature branch
git checkout -b feature/my-feature

# Make changes and test
npm run lint
npm run format

# Commit with clear message
git commit -m "description of changes"
```

### 2. Pull Request
```bash
# Push your branch
git push -u origin feature/my-feature

# Create PR on GitHub
# Wait for CI checks to pass (automatic)
# Request review
```

### 3. Code Review
- Team reviews your code
- Address feedback if needed
- Once approved, merge to `main`

### 4. Automatic Deployment
When merged to `main`:
1. ✅ CI/CD pipeline runs all checks
2. ✅ Files sync to production server
3. ✅ Changes live immediately (no cache busting needed)

## Pre-Deployment Checklist

Before merging a PR, verify:

- [ ] All CI checks pass (GitHub Actions)
- [ ] HTML/CSS/JS linting passes (`npm run lint`)
- [ ] Code has been reviewed and approved
- [ ] Images are optimized (under 500KB each unless necessary)
- [ ] No broken links in gallery or content
- [ ] Form endpoints are correct (Formspree)
- [ ] Analytics tokens are correct (Google Analytics, GTM)
- [ ] External links work and use HTTPS
- [ ] Metadata (OG tags, title, description) updated if content changed

## Rollback Procedure

If something breaks after deployment:

1. **Identify the problematic commit:**
   ```bash
   git log --oneline -10
   ```

2. **Revert the commit:**
   ```bash
   git revert <commit-sha>
   git push origin main
   ```

3. **Investigation:**
   - Fix the issue in a new PR
   - Test thoroughly before re-deploying

## Performance Considerations

### Image Optimization
- Compress images before committing
- Use JPG for photos, PNG for graphics
- Typical sizes: 100-300KB per image
- Gallery images: 200-500KB (resize if larger)

### Caching
- Static assets are served with appropriate cache headers
- CSS/JS changes may require cache busting (appending query string)
- HTML is typically not cached by CDN

### Monitoring
- Check [Google Analytics](https://analytics.google.com) for traffic
- Monitor [Google Search Console](https://search.google.com/search-console) for indexing
- Set up alerts for 404 errors and performance issues

## Content Updates

### Adding Gallery Images
1. Place images in `gallery/{project-name}-{year}/`
2. Update `index.html` with correct paths
3. Use descriptive alt text
4. Optimize image size (compress before commit)
5. Test links locally
6. Create PR for review

### Updating Text Content
1. Edit `index.html`
2. Update meta tags if needed (title, description, OG tags)
3. Test locally with linters
4. Create PR for review

### Fixing Typos/Bugs
1. Fix in a feature branch
2. Create PR (even for small changes)
3. Let CI validate
4. Merge after review

## Emergency Procedures

### Website is down
- Check hosting provider status page
- Verify DNS settings
- Review CI/CD logs for failed deployments
- Contact hosting support if needed

### Form not submitting
- Verify Formspree endpoint is correct
- Check browser console for errors
- Test locally with linting

### Images not loading
- Verify paths are relative (no leading `/`)
- Check file exists in repository
- Clear browser cache and test

### Style/Layout broken
- Check CSS syntax with `npm run lint:css`
- Review recent CSS changes
- Test in multiple browsers

## Maintenance Tasks

### Weekly
- Monitor CI logs for warnings
- Check Google Analytics for issues

### Monthly
- Run `npm audit` and update dependencies if needed
- Review and respond to GitHub issues
- Check external links still work

### Quarterly
- Update CHANGELOG.md with summary
- Create a release tag
- Review security practices
- Update contact information if changed

## Contact & Support

For deployment issues or questions:
- **Email:** pleasureislanddesign@gmail.com
- **Phone:** (910) 444-1230
- **GitHub:** https://github.com/willyd61/pleasureislanddesign.com

---

**Last Updated:** December 2024
