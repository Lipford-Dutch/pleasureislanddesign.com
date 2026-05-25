# Security Policy

## Reporting a Vulnerability

**Please do not report security vulnerabilities publicly.** Instead, email security concerns to:

📧 **pleasureislanddesign@gmail.com**

Include the following information:
- Type of vulnerability
- Location of the vulnerability
- Steps to reproduce (if possible)
- Potential impact
- Suggested fix (if you have one)

We take all security reports seriously and will respond promptly.

## Security Best Practices

### For Contributors
- Never commit sensitive information (API keys, passwords, tokens)
- Use environment variables for configuration
- Follow the principle of least privilege
- Keep dependencies up to date

### Code Review Process
All PRs undergo:
- ✅ Automated security scanning
- ✅ Manual code review
- ✅ Linting checks (catches common issues)
- ✅ Test coverage validation

### Dependency Management
- Regular dependency updates via npm audit
- Pinned versions in package-lock.json for reproducible installs
- GitHub security alerts enabled

## Known Issues

None at this time. Please report any discovered vulnerabilities to the email above.

## Security Advisories

GitHub will post security advisories for any critical vulnerabilities found in this project.

Subscribe to notifications by:
1. Go to https://github.com/willyd61/pleasureislanddesign.com
2. Click "Watch" > "Custom"
3. Enable "Security alerts"
