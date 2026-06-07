# Pleasure Island Design

> Premium Cabinet Refinishing & Repair Services in Southeast North Carolina

[![CI](https://github.com/willyd61/pleasureislanddesign.com/actions/workflows/ci.yml/badge.svg)](https://github.com/willyd61/pleasureislanddesign.com/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 🎯 About

Pleasure Island Design specializes in **high-quality cabinet refinishing and repair services**, transforming kitchens with affordable luxury and minimal disruption. We deliver expert craftsmanship with a seamless process that enhances homes across Southeast North Carolina.

- **Service Area:** Wilmington, Kure Beach, Carolina Beach, and surrounding areas
- **Specialties:** Cabinet refinishing, refacing, repair, hardware installation, custom modifications
- **Timeline:** Most projects completed in 5-8 days
- **Award-winning:** Voted Neighborhood Favorite in 2021 & 2023 by Nextdoor

---

## 🖼️ Digital Archive & Knowledge Base (NEW — AI-Powered Initiative)

**This repository is now the complete digital home for Pleasure Island Design LLC** — public website + professional, searchable business archive and institutional knowledge base.

We are actively migrating and AI-enhancing business documents (marketing plans, strategy, operations, hiring, brand assets) from Google Drive using a turn-key multi-AI pipeline (Grok + Claude + GPT Codex + Gemini + Copilot). 

**See the full system**: [business/README.md](business/README.md) on the `feature/ai-digital-home-archive` branch (or soon main).

This unlocks:
- Single source of truth for decision making
- Rich, authentic content for website blog, whitepapers, and marketing
- Version history and provenance for all business knowledge
- Foundation for future internal AI tools (RAG over your own docs)

**Current Status**: Foundation structure seeded. Pilot ingestion in progress. Contributions welcome via the documented workflow.

---

## 🚀 Getting Started

### Prerequisites
- Node.js 20+ ([Download](https://nodejs.org))
- npm 10+ (included with Node.js)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/willyd61/pleasureislanddesign.com.git
cd pleasureislanddesign.com

# Install dependencies
npm install --legacy-peer-deps

# Run linters locally (recommended before committing)
npm run lint
```

### Local Development

```bash
# Check code quality
npm run lint              # Run all linters
npm run lint:html        # HTML validation only
npm run lint:css         # CSS linting only
npm run lint:js         # JavaScript linting only

# Fix formatting issues automatically
npm run format
npm run format:check     # Check without fixing
```

---

## 📂 Project Structure

```
.
├── index.html              # Main website file
├── styles.css              # Stylesheet
├── js/
│   └── pleasure-island-scripts.js  # JavaScript functionality
├── img/                    # Logo, awards, hero images
├── gallery/                # Before/after project photos
├── business/               # NEW: AI-augmented business archive & knowledge base (see business/README.md)
├── .github/
│   └── workflows/
│       └── ci.yml         # Automated testing on PRs
├── package.json           # Dependencies & npm scripts
└── docs/                   # MkDocs technical reference & whitepapers
    └── CONTRIBUTING.md    # Developer guidelines
```

---

## 🔄 Workflow & Contributing

We follow a structured development workflow to maintain code quality and reliability.

### For Team Members

1. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test locally:
   ```bash
   npm run lint    # All checks must pass
   npm run format  # Fix formatting
   ```

3. **Commit with clear messages:**
   ```bash
   git commit -m "Brief description of changes"
   ```

4. **Push and create a Pull Request:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

5. **Address review feedback** — CI checks must pass before merging

For complete guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)

---

## ✅ Quality Assurance

All code is automatically validated using:

| Check | Tool | Purpose |
|-------|------|---------|
| **HTML** | HTMLHint | Validates syntax, alt tags, structure |
| **CSS** | Stylelint | Checks consistency, prevents errors |
| **JavaScript** | ESLint | Enforces style, catches syntax errors |
| **Assets** | Custom | Detects broken image references |
| **Links** | Custom | Verifies anchor links are valid |
| **Security** | Custom | Scans for hardcoded secrets |

✚ **All PR checks must pass** before code can be merged.

---

## 📌 Content & Assets

### Images
- **Optimize before committing** — use tools like TinyPNG or ImageOptim
- **Use relative paths** — `gallery/image.jpg` not `/gallery/image.jpg`
- **Require alt text** — all images must have descriptive alt attributes
- **Format:** JPG for photos, PNG for graphics, WebP for modern browsers

### Gallery
- Before/after project photos stored in `gallery/{project-name}-{year}/`
- Naming convention: `before-1.jpg`, `after-1.jpg` etc.
- File names should not contain spaces

### Business Documents
- Follow the AI-assisted workflow in [business/README.md](business/README.md)
- Always include provenance and structured metadata

---

## 🌍 Deployment

This static website is hosted on a web server.

**To deploy changes:**
1. Merge your PR to `main` branch
2. Changes automatically sync to production via your hosting provider
3. No build step required (static HTML/CSS/JS)

---

## 📞 Contact & Support

**Business Inquiries:**
- Phone: [(910) 444-1230](tel:+9104441230)
- Email: [pleasureislanddesign@gmail.com](mailto:pleasureislanddesign@gmail.com)
- Address: 3720 Carolina Beach Road, Suite F, Wilmington, NC 28412

**Follow Us:**
- [Facebook](https://www.facebook.com/pidnrayment/)
- [Instagram](https://www.instagram.com/pleasureislanddesign/)
- [LinkedIn](https://www.linkedin.com/in/pleasureislanddesign/)
- [Nextdoor](https://nextdoor.com/pages/nicole-rayment-carolina-beach-nc/)

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ You can use, modify, and distribute this code
- ✅ Commercial use is permitted
- ✅ You must include a copy of the license
- ✅ You must state significant changes made to the code
- ❌ The software is provided "as is" with no warranty

---

## 🎓 Development Standards

### Code Style
- **HTML:** Use semantic tags, require alt attributes for images
- **CSS:** Keep it simple, avoid deep nesting, use meaningful class names
- **JavaScript:** Use `const`/`let` (never `var`), strict equality (`===`), descriptive names

### Commit Messages
```
Descriptive title under 50 characters

Optional detailed explanation of why this change was made.
Wrap at ~72 characters.
```

### PR Titles
```
action: brief description (e.g., "fix: broken mobile menu", "feat: dark mode toggle")
```

### Docs Commits
Use `docs(business): ` or `feat(archive): ` for archive work.

---

## 🔮 Roadmap

**Phase 2 (Upcoming):**
- Enhanced feature development
- Performance optimization
- Accessibility improvements

**Phase 3 (Future):**
- Modern design system (Claude Design)
- User interaction tracking
- Content management system

**Parallel Enabler: AI Digital Archive** (see business/README.md)
- Complete migration of Google Drive remnants
- Populate knowledge-base/ with insights
- Integrate summaries into website content & whitepapers

---

## 💡 Tips for Success

1. **Always pull before you push:**
   ```bash
   git pull origin main
   ```

2. **Test locally before committing:**
   ```bash
   npm run lint
   ```

3. **Write clear commit messages** so the team understands what changed and why

4. **Ask questions** — reach out if something is unclear

5. **Keep it simple** — small, focused commits are easier to review

## 📚 Resources

- [MDN Web Docs](https://developer.mozilla.org/) — HTML/CSS/JavaScript reference
- [ESLint Rules](https://eslint.org/docs/rules/) — JavaScript style guide
- [Git Documentation](https://git-scm.com/doc) — Version control help
- [Semantic HTML](https://developer.mozilla.org/en-US/docs/Glossary/Semantic_HTML) — Best practices

## ❓ FAQ

**Q: How do I report a bug?**
A: Create an issue on GitHub with clear steps to reproduce and expected vs. actual behavior.

**Q: Can I modify the design?**
A: Yes, but discuss major changes with the team first. Submit a PR for review.

**Q: What if I break something?**
A: Don't worry — we have version control. Create a new PR with the fix and reference the original issue.

**Q: How often do we deploy?**
A: Changes merge to `main` when PR checks pass. Deployment happens automatically via your hosting provider.

**Q: How do I contribute to the business archive?**
A: Follow the turn-key workflow in [business/README.md](business/README.md). Use AI assistance heavily.

**Last Updated:** June 2026 (AI Digital Home Initiative added)  
**Version:** 1.1.0  
**Maintained by:** Pleasure Island Design LLC + multi-AI collaboration

For questions or suggestions, open an issue on GitHub or contact us directly.
