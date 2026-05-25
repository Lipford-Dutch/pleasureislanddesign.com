# Development Guide

Technical documentation for developers working on Pleasure Island Design website.

## Architecture Overview

### Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Static Hosting:** GitHub Pages
- **Build Tools:** Optional (npm-based)
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions

### Why This Stack?
- No server-side overhead needed for static content
- Fast performance (no backend latency)
- Secure (no database to compromise)
- Scalable (GitHub Pages handles traffic)
- Low cost (free hosting)

## Code Organization

### HTML Structure
All pages follow consistent structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta tags, canonical, OG, Twitter -->
  <!-- Analytics (GA4, Clarity, GTM) -->
  <!-- Fonts, CSS -->
  <!-- JSON-LD schema -->
</head>
<body>
  <!-- Google Tag Manager noscript -->
  <!-- Skip to main content link -->
  <!-- Header/Navigation -->
  <main id="main-content">
    <!-- Page content -->
  </main>
  <!-- Footer -->
  <!-- Scripts -->
</body>
</html>
```

### CSS Methodology
- **BEM (Block Element Modifier) naming**
- **Mobile-first responsive design**
- **CSS variables for colors and spacing**
- **Organized by component**

Example:
```css
/* Block */
.hero { }

/* Element */
.hero__title { }

/* Modifier */
.hero--dark { }
```

### JavaScript Patterns
- **IIFE (Immediately Invoked Function Expression) for encapsulation**
- **Event delegation for performance**
- **RequestAnimationFrame for animations**
- **IntersectionObserver for lazy loading**

## Key JavaScript Functions

### Stat Counter Animation
```javascript
function initStatCounters() {
  // Animates counter values when visible
  // Used on homepage for statistics
  // Performance: Uses IntersectionObserver
}
```

### Scroll Reveal
```javascript
function initReveal() {
  // Reveals elements as user scrolls
  // Performance: Lazy-loads visibility
}
```

### Gallery Filter
```javascript
function initGalleryFilter() {
  // Filters gallery items by category
  // Performance: DOM manipulation optimized
}
```

## SEO Implementation

### Meta Tags (CRITICAL - Fixed in Beta Release)
- **Canonical:** Must point to GitHub Pages URL
- **OG Tags:** For social sharing (Facebook, Twitter)
- **Twitter Card:** Specific Twitter preview
- **robots:** index, follow (allow indexing)

### Schema.org Structured Data
- **HomeAndConstructionBusiness:** Main schema
- **LocalBusiness:** Service area information
- **OfferCatalog:** Services listing
- **AggregateRating:** 5-star rating

### Image Alt Text
All images require descriptive alt text:
```html
<img src="transformation.jpg" 
     alt="Before and after kitchen cabinet refinishing, showing transformation from outdated finishes to modern white cabinets with brass hardware">
```

### Internal Linking
- Link to relevant blog posts from homepage
- Use descriptive anchor text (not "click here")
- Create breadcrumb navigation where helpful

## Performance Optimization

### Image Optimization
- Use WebP format where possible with JPG fallback
- Compress images: max quality at smallest file size
- Responsive images with srcset
- Lazy load below-fold images

### JavaScript
- Defer non-critical scripts
- Minimize main bundle size
- Use vanilla JS instead of jQuery (smaller)
- Cache static assets

### CSS
- Minify in production
- Use CSS variables for theming
- Avoid inline styles
- Load fonts async with font-display: swap

### Network
- Enable gzip compression
- Use CDN for static assets (GitHub CDN is free)
- Cache busting with file hashes
- Minimize HTTP requests

## Testing Checklist

### Before Committing
- [ ] Links work (relative and absolute)
- [ ] Images display correctly
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Forms submit correctly
- [ ] Analytics tags firing
- [ ] No console errors
- [ ] SEO meta tags correct
- [ ] Social preview renders properly

### Before Publishing
- [ ] All CI tests pass
- [ ] No broken links
- [ ] No 404 errors
- [ ] Mobile performance acceptable
- [ ] Lighthouse score 85+
- [ ] No security warnings
- [ ] Canonical tags correct

## Common Issues & Solutions

### Placeholder Statistics Showing "0+"
**Problem:** Stat counter animation not firing  
**Solution:**
- Check IntersectionObserver threshold
- Verify data-target attribute exists
- Check browser console for JS errors
- Consider rendering as static HTML

### Images Not Loading
**Problem:** Path issues with GitHub Pages  
**Solution:**
- Use relative paths: `img/filename.jpg`
- Not absolute paths: `/pleasureislanddesign.com/img/...`
- Check filename case sensitivity
- Verify file exists with `git ls-files`

### Canonical/OG Tags Wrong
**Problem:** Points to www.pleasureislanddesign.com  
**Solution:**
```html
<!-- WRONG -->
<link rel="canonical" href="https://www.pleasureislanddesign.com">

<!-- RIGHT -->
<link rel="canonical" href="https://willyd61.github.io/pleasureislanddesign.com">
```

### Analytics Not Tracking
**Problem:** Clarity ID is "placeholder-clarity-id"  
**Solution:**
1. Go to https://clarity.microsoft.com
2. Get real project ID
3. Replace in HTML: `(window,document,"clarity","script","YOUR_ID")`

## Build Commands

### Available NPM Scripts
```bash
npm run test:links      # Validate all links
npm run test:seo        # Check SEO quality
npm run build          # Build production assets
npm run serve          # Start local server
npm run generate-pdf   # Create audit PDF
```

## Git Workflow

### Branch Strategy
- `main` - Production ready, stable
- `phase-beta-release` - Current development
- `feature/*` - Individual features
- `hotfix/*` - Critical production fixes

### Commit Message Format
```
[type]: [subject]

[body]

[footer]

Types: feat, fix, docs, style, refactor, perf, test, chore
Example: feat: add blog comment system
```

### Pull Request Process
1. Create feature branch from `phase-beta-release`
2. Make changes with clear commits
3. Push and create PR
4. Wait for CI checks (must pass)
5. Request code review
6. Merge when approved

## Deployment

See [Deployment Guide](./Deployment.md) for publishing process.

---

*Last Updated: May 25, 2026*
