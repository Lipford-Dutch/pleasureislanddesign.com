# Contributing to Pleasure Island Design

## Development Setup

### Prerequisites
- Node.js 20+ 
- npm 10+

### Installation

```bash
# Install dependencies
npm install
```

## Running Linters Locally

Before pushing code, run the linters to catch issues early:

```bash
# Run all linters
npm run lint

# Run specific linters
npm run lint:html      # HTML validation
npm run lint:css       # CSS linting
npm run lint:js        # JavaScript linting

# Check code formatting
npm run format:check

# Auto-fix formatting issues
npm run format
```

## Code Quality Standards

### HTML
- Valid HTML5 syntax
- All images require `alt` attributes
- Semantic HTML structure
- No inline styles (use CSS classes)

### CSS
- Use consistent indentation (2 spaces)
- Follow BEM naming convention for complex styles
- No unused styles
- Max nesting depth of 4 levels
- Short hex color notation where applicable

### JavaScript
- Use `const` by default, `let` when needed, never `var`
- Use strict equality (`===` instead of `==`)
- No console logs in production code
- Descriptive variable/function names

## Continuous Integration

All pull requests automatically run:
1. **HTML Linting** — Validates HTML5 syntax and best practices
2. **CSS Linting** — Checks CSS for errors and style consistency
3. **JavaScript Linting** — Validates JS syntax and applies style rules
4. **Asset Validation** — Checks for broken image references
5. **Link Validation** — Verifies all internal anchor links are valid
6. **Security Checks** — Scans for common vulnerabilities

All checks must pass before a PR can be merged.

## Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run linters locally: `npm run lint`
4. Fix any issues: `npm run format` (auto-fixes some)
5. Commit with clear messages
6. Push and create a pull request
7. CI checks run automatically
8. Address any feedback or failing checks
9. Once approved, PR can be merged

## Common Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org

**"Missing image" error in CI**
- Check that image paths in HTML are relative and point to existing files
- Use forward slashes `/` not backslashes

**"Broken anchor link" error**
- Ensure all `href="#..."` links match an `id="..."` in the HTML
- Example: `<a href="#about">` needs `<section id="about">`

## Questions?

For questions about the development process, contact the team.
