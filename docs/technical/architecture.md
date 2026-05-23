# Site Architecture

## Overview

pleasureislanddesign.com is a **static HTML/CSS/JavaScript website** with no server-side processing, no build step, and no framework dependencies. This keeps it:

- Fast to load
- Easy to maintain
- Simple to deploy (any static host)
- Zero server security surface area

## File Structure

```
pleasureislanddesign.com/
├── index.html              # Single-page application
├── styles.css              # Design system + all styles
├── js/
│   └── pleasure-island-scripts.js  # All JavaScript
├── img/                    # Core brand assets
│   ├── pid-logo-small.jpg
│   ├── hero-bg.jpg
│   ├── 2021-nextdoor-award.jpg
│   └── 2023-nextdoor-award.jpg
├── gallery/                # Project photos
│   ├── brunswick-forest-2023/
│   ├── compass-pointe-2023/
│   ├── seagrove-2023/
│   ├── motts-landing-2023/
│   ├── kure-beach-2023/
│   ├── carolina-beach-2023/
│   └── paradise-towers-2023/
├── opt-images/             # Marketing/branded assets
├── docs/                   # MkDocs documentation source
├── .github/workflows/      # CI/CD pipelines
└── mkdocs.yml             # Docs configuration
```

## Design System

CSS custom properties (design tokens) are defined in `:root` and used throughout `styles.css`. This enables:

- Consistent colors, spacing, typography
- Easy global updates (change one variable, updates everywhere)
- Future dark mode support

See [Design System](design-system.md) for full token reference.

## Performance Strategy

- Images compressed to <300KB each
- JavaScript deferred loading
- No external JavaScript frameworks
- Google Fonts loaded with `display=swap`
- Lazy loading for gallery images

## Future Architecture Considerations

For Phase 3+ scaling needs, consider:
- **Eleventy or Astro** — Static site generator for blog/CMS
- **Netlify or Vercel** — Better CI/CD + serverless functions for forms
- **Cloudinary** — Image optimization CDN
- **Headless CMS** — Contentful or Sanity for content management
