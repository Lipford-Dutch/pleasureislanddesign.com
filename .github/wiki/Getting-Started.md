# Getting Started

Guide to setting up your development environment for Pleasure Island Design website.

## Prerequisites

- Git
- Node.js 16+ (for build tools)
- Python 3.8+
- A text editor or IDE (VS Code recommended)

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/willyd61/pleasureislanddesign.com.git
cd pleasureislanddesign.com
```

### 2. Create Development Branch

```bash
git checkout phase-beta-release
# or create your feature branch from this one
git checkout -b feature/your-feature
```

### 3. Install Dependencies

```bash
# For static site (minimal requirements)
pip install reportlab  # For PDF generation
npm install            # If using build tools
```

### 4. Run Local Server

#### Option A: Python Simple Server
```bash
python3 -m http.server 8000
# Visit http://localhost:8000
```

#### Option B: Node HTTP Server
```bash
npx http-server
# Visit http://localhost:8080
```

#### Option C: Live Server (VS Code)
Install "Live Server" extension and right-click on index.html → "Open with Live Server"

## Project Structure

```
pleasureislanddesign.com/
├── index.html              # Homepage
├── blog/                   # Blog posts
│   ├── index.html
│   ├── cabinet-refinishing-guide.html
│   ├── coastal-color-trends-2026.html
│   └── cabinet-care-guide.html
├── locations/              # Service area pages
│   └── wilmington.html
├── specials/               # Promotions page
├── shop/                   # Merchandise store
├── img/                    # Images and assets
├── css/                    # Stylesheets
├── js/                     # JavaScript
├── .github/                # GitHub workflows & templates
│   ├── wiki/               # Documentation
│   └── workflows/          # CI/CD pipelines
├── docs/                   # Additional documentation
└── sitemap.xml, robots.txt # SEO files
```

## Key Files to Know

- **index.html** - Main homepage with all key sections
- **styles.css** - Global stylesheet
- **pleasure-island-scripts.js** - Main JavaScript file
- **robots.txt** - Search engine directives
- **sitemap.xml** - URL index for search engines
- **pid-startup.html** - Dynamic startup management page

## Building & Testing

### Run Tests
```bash
# Link validation
npm run test:links

# HTML validation
npm run test:html

# SEO checks
npm run test:seo
```

### Generate PDF Reports
```bash
python3 generate_audit_pdf.py
```

### Build Assets
```bash
npm run build
```

## Common Tasks

### Update Content
1. Edit the HTML file (e.g., index.html, blog/cabinet-care-guide.html)
2. Save changes
3. Refresh browser to see updates
4. Commit and push when ready

### Add Blog Post
1. Create new file in `blog/` directory: `blog/your-slug.html`
2. Use existing blog post as template
3. Update `blog/index.html` to link to new post
4. Add URL to `sitemap.xml`
5. Commit and push

### Update Special Offers
1. Edit `specials/index.html`
2. Update promotion dates and details
3. Upload promotional PDFs to `assets/flyers/`
4. Commit and push

### Deploy Changes
```bash
git add .
git commit -m "Description of changes"
git push origin phase-beta-release
# Create PR to main for review
```

## Troubleshooting

### Images not loading?
- Check image path is correct (use relative paths like `img/filename.jpg`)
- Verify file exists in `img/` directory
- Check file permissions

### Links broken?
- Verify file exists at target path
- Check file extensions (.html)
- Test links with `npm run test:links`

### CSS not updating?
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check CSS file is linked in HTML head
- Verify selector matches HTML element

### Analytics not tracking?
- Verify Google Tag Manager ID is correct (GTM-W2TMT5K8)
- Check Clarity ID is configured (not "placeholder-clarity-id")
- Allow time for data to propagate (up to 24 hours)

## Git Workflow

```bash
# Pull latest changes
git pull origin phase-beta-release

# Create feature branch
git checkout -b feature/my-feature

# Make changes, test locally

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description"

# Push to remote
git push -u origin feature/my-feature

# Create Pull Request on GitHub
# Wait for review and CI checks to pass
# Merge when approved
```

## Need Help?

- Check [Brand Guidelines](./Brand-Guidelines.md) for design consistency
- See [Development](./Development.md) for technical details
- Review [Deployment](./Deployment.md) for publishing changes
- Contact: pleasureislanddesign@gmail.com

---

*Last Updated: May 25, 2026*
