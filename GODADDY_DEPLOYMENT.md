# GoDaddy Production Deployment Runbook

**Pleasure Island Design — Cabinet Refinishing Services**  
**Hosted on:** GoDaddy cPanel / Web Hosting  
**Domain:** www.pleasureislanddesign.com  
**Version:** 1.0.0  
**Last Updated:** May 26, 2026  
**Owner:** Nicole Rayment <pleasureislanddesign@gmail.com>

---

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [First-Time Setup (GoDaddy cPanel Git Integration)](#first-time-setup-godaddy-cpanel-git-integration)
3. [Standard Deployment Process](#standard-deployment-process)
4. [Post-Deployment Verification](#post-deployment-verification)
5. [Rollback Procedure](#rollback-procedure)
6. [Troubleshooting](#troubleshooting)
7. [Architecture & Hosting Details](#architecture--hosting-details)
8. [Maintenance & Monitoring](#maintenance--monitoring)

---

## Pre-Deployment Checklist

Before any deployment to production:

- [ ] **Code Quality**
  - [ ] All code merged to `main` branch
  - [ ] CI/CD pipeline has passed (GitHub Actions: lint, security, formatting)
  - [ ] No unresolved code review comments

- [ ] **Content**
  - [ ] All links are correct (no localhost references)
  - [ ] Images are compressed and optimized
  - [ ] Contact info, phone, email match current details
  - [ ] Analytics IDs (GA4, GTM, Clarity) are configured

- [ ] **SEO & Configuration**
  - [ ] `robots.txt` allows indexing (not set to `Disallow: /`)
  - [ ] `sitemap.xml` is updated and valid
  - [ ] Canonical tags point to `www.pleasureislanddesign.com`
  - [ ] Open Graph (OG) tags are correct
  - [ ] JSON-LD schema references correct domain

- [ ] **Browser & Performance**
  - [ ] Test on Chrome, Firefox, Safari, and mobile browsers
  - [ ] Page load time is acceptable (<3 seconds)
  - [ ] Mobile responsiveness verified
  - [ ] Form submissions work end-to-end

- [ ] **Backup**
  - [ ] Current production has been backed up in GoDaddy
  - [ ] GoDaddy migration repo is synchronized with latest `main`

- [ ] **Stakeholder Sign-Off**
  - [ ] Business owner approves deployment
  - [ ] Rollback plan understood

---

## First-Time Setup (GoDaddy cPanel Git Integration)

This setup is **one-time only**. After this, deployments become a simple `git pull`.

### Step 1: Access cPanel

1. Log in to **GoDaddy account** → **Web Hosting** → **Manage**
2. Click **cPanel** button (usually in the top right)
3. Enter GoDaddy username & password if prompted

### Step 2: Locate Git Version Control

In cPanel:
1. Search for **"Git"** in the search bar, or
2. Under **File Manager** section, click **Git Version Control**

### Step 3: Create Deployment Repository

1. Click **"Create"** to set up a new Git repository
2. **Repository Path:** `/home/[username]/public_html` or `/home/[username]/pleasureislanddesign.com`
   - (Ask your hosting provider which is the correct path for your domain)
3. **Repository URL:** Point it to your GoDaddy-hosted Git repo
   - Format: `https://git.pleasureislanddesign.com/pleasureislanddesign.com.git` (or your actual GoDaddy repo URL)

### Step 4: Configure Remote Origin

If GoDaddy's cPanel interface doesn't auto-configure, SSH into your server and run:

```bash
cd /home/[username]/public_html
git remote set-url origin https://git.pleasureislanddesign.com/pleasureislanddesign.com.git
# (Or use SSH if you've set up keys)
git remote set-url origin git@git.pleasureislanddesign.com:pleasureislanddesign.com.git
```

### Step 5: Pull the Latest Code

In cPanel Git Version Control UI:
1. Click **"Pull"** next to your repository
2. Branch: `main`
3. This downloads the latest code from your repo to the public_html folder

**Result:** Your production site is now live!

---

## Standard Deployment Process

Once first-time setup is complete, deployments are **automated** or **manual**:

### Option A: Automated (Recommended)

**GitHub Actions → GoDaddy Sync Workflow** (if configured):

1. Merge a PR to `main` on GitHub
2. GitHub Actions automatically:
   - Runs CI tests (lint, security, format checks)
   - Pushes to your GoDaddy Git repo
   - cPanel pulls the changes

**Timeline:** ~2–5 minutes after merge.

### Option B: Manual via cPanel Git UI

1. Merge PR to `main` on GitHub
2. Log in to **GoDaddy cPanel** → **Git Version Control**
3. Click **"Pull"** next to the production repository
4. Select branch: `main`
5. Click **"Pull"** button

**Timeline:** Immediate (30 seconds to 1 minute).

### Option C: Manual via SSH (If Enabled)

If you have SSH access (some GoDaddy plans):

```bash
ssh [your-username]@[godaddy-server-ip]
cd /home/[username]/public_html
git pull origin main
```

---

## Post-Deployment Verification

After each deployment, verify the site works:

### 1. Check Site Loads
- [ ] Visit **https://www.pleasureislanddesign.com** in a browser
- [ ] Homepage loads without errors
- [ ] No 404 or 500 errors in the console

### 2. Test Critical Paths
- [ ] Navigation menu works
- [ ] All major links (Home, About, Services, Gallery, Blog, Specials, Contact) load
- [ ] Contact form submits without error
- [ ] Newsletter signup works

### 3. Check Configuration
- [ ] Open browser DevTools → **Network** tab
- [ ] Verify GA4 tracking fires (look for `www.googletagmanager.com` request)
- [ ] Open DevTools → **Console** for any JavaScript errors (should be clean)

### 4. Validate SEO Elements
- [ ] View page source (Ctrl+U / Cmd+U)
- [ ] Confirm canonical tag: `<link rel="canonical" href="https://www.pleasureislanddesign.com">`
- [ ] Confirm OG tags are present and correct
- [ ] Confirm no `noindex` meta tag on public pages

### 5. Performance Check
- [ ] Use **Google PageSpeed Insights** (https://pagespeed.web.dev)
- [ ] Enter `https://www.pleasureislanddesign.com`
- [ ] Core Web Vitals should show as "Good" or "Needs Improvement" (not "Poor")

### 6. Email Notifications
- [ ] Test form submission sends email to `pleasureislanddesign@gmail.com`
- [ ] Verify contact info in email is correct

---

## Rollback Procedure

If something breaks in production, **rollback to the previous version in < 5 minutes.**

### Quick Rollback (Recommended)

**Via cPanel Git UI:**

1. Log in to **GoDaddy cPanel** → **Git Version Control**
2. Click the **History** or **Branches** tab
3. Find the **previous commit** (should be labeled with the previous fix/feature)
4. Click **"Checkout"** or **"Reset to this commit"**
5. Confirm the rollback

**Alternative:** If the UI doesn't have history:

```bash
# Via SSH (if available):
cd /home/[username]/public_html
git log --oneline -5  # See recent commits
git reset --hard [commit-hash-of-last-good-version]
git push origin main --force-with-lease
```

### Full Rollback (cPanel File Manager)

If Git isn't responsive:

1. **GoDaddy cPanel** → **File Manager**
2. Navigate to `/public_html`
3. **Backup** current files (create a `.broken` folder, move broken files there)
4. **Restore** from your GoDaddy account backup (see Backups section below)

### Verify Rollback

After rolling back:
- [ ] Visit https://www.pleasureislanddesign.com
- [ ] Confirm the site loads the old version
- [ ] Check console for no errors
- [ ] Test contact form

### Post-Mortem

After a rollback:

1. **Identify root cause** — what code broke?
2. **Fix locally** — make the fix on your machine, test thoroughly
3. **Re-deploy** — follow Standard Deployment Process above

---

## Troubleshooting

### Issue: "404 Page Not Found" After Deployment

**Cause:** Files didn't pull correctly, or wrong folder is being served.

**Fix:**
1. Verify cPanel shows the correct **public_html** path
2. SSH into server and list contents:
   ```bash
   ls -la /home/[username]/public_html | head -20
   ```
   You should see: `index.html`, `styles.css`, `js/`, `img/`, etc.
3. If missing, manually pull:
   ```bash
   cd /home/[username]/public_html
   git pull origin main --force
   ```

### Issue: "500 Internal Server Error"

**Cause:** Usually a server issue, not a code issue. cPanel/GoDaddy problem.

**Fix:**
1. Check **error logs** in cPanel:
   - **File Manager** → `/public_html/` → right-click → **View Error Logs**
2. If logs mention `.htaccess`, temporarily **rename** it:
   ```bash
   mv .htaccess .htaccess.bak
   ```
   Then test the site. If it works, the `.htaccess` has a syntax error.
3. Contact GoDaddy support if the server itself is down

### Issue: "403 Forbidden"

**Cause:** File permissions are too restrictive.

**Fix:**
1. SSH into server and fix permissions:
   ```bash
   cd /home/[username]/public_html
   find . -type f -exec chmod 644 {} \;  # Files: 644
   find . -type d -exec chmod 755 {} \;  # Directories: 755
   ```
2. Reload the site in browser

### Issue: Forms Don't Submit / Email Not Received

**Cause:** Server-side mail configuration or form endpoint misconfigured.

**Fix:**
1. Check that form points to correct email in `index.html`:
   ```html
   <!-- Should have: pleasureislanddesign@gmail.com -->
   ```
2. Verify GoDaddy email is configured for the domain
3. Check email spam folder (sometimes legitimate form emails are caught)
4. Test via **cPanel → Email** → send a test email from the account

### Issue: Analytics Not Tracking (GA4 / GTM Missing Data)

**Cause:** GA4 ID or GTM ID misconfigured or placeholder not replaced.

**Fix:**
1. View page source (Ctrl+U)
2. Search for `G-X0PJB95RBE` (GA4 ID) — should exist
3. Search for `GTM-W2TMT5K8` (GTM ID) — should exist
4. If either shows `placeholder-*`, the ID wasn't configured. Update:
   ```html
   <!-- In index.html, replace: -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-X0PJB95RBE"></script>
   ```
5. Redeploy after fixing
6. Wait 24 hours for data to appear in GA4 dashboard

### Issue: CSS/JS Not Loading (Old Cached Version)

**Cause:** Browser or CDN cache.

**Fix:**
1. **Hard refresh** in browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Check **DevTools → Network** tab; CSS/JS should show `200` status (not `304`)
3. If still old, clear browser cache entirely or use **Incognito/Private** mode
4. For GoDaddy cPanel, you can set **Cache-Control** headers in `.htaccess` (if needed)

---

## Architecture & Hosting Details

### What's Hosted on GoDaddy

| Component | Type | Location | Notes |
|-----------|------|----------|-------|
| index.html | Static HTML | `/public_html/` | Main homepage |
| styles.css | Static CSS | `/public_html/` | Global styling |
| pleasure-island-scripts.js | Static JS | `/public_html/js/` | Frontend interactions |
| /blog/ | Static pages | `/public_html/blog/` | Blog post directory |
| /specials/ | Static pages | `/public_html/specials/` | Seasonal promotions page |
| /shop/ | Static page | `/public_html/shop/` | Shop landing (Printify coming soon) |
| /img/ | Assets | `/public_html/img/` | Logos, banners, social preview images |
| /gallery/ | Image directory | `/public_html/gallery/` | Cabinet transformation photos |
| robots.txt | Static text | `/public_html/` | Search engine instructions |
| sitemap.xml | Static XML | `/public_html/` | Search engine sitemap |
| .htaccess | Server config | `/public_html/` | Apache rewrite rules (HTTPS, hotlink protection) |

### What's NOT on GoDaddy

- **storefront-beta/** (Node.js server) — stays on GitHub, not deployed to cPanel
- **Database** — static site only, no backend
- **/docs/** (mkdocs) — separate documentation, not public

### Server Tech Stack

- **OS:** Linux (CentOS/AlmaLinux, cPanel-managed)
- **Web Server:** Apache 2.4+
- **PHP:** 7.4+ (available if needed for forms; currently using client-side only)
- **SSL/TLS:** Let's Encrypt (free, auto-renewed by cPanel)
- **DNS:** GoDaddy nameservers

### File Permissions

After any deployment, permissions should be:

```
-rw-r--r-- (644)  for all .html, .css, .js, .xml, .txt files
drwxr-xr-x (755)  for all directories
```

---

## Maintenance & Monitoring

### Daily Monitoring (Automated)

- **Google Analytics:** Check visitor count, bounce rate, top pages
- **Search Console:** Monitor indexing status, top queries
- **Uptime Monitoring:** Set up a free tool like **UptimeRobot** to ping the site every 5 minutes and alert if down

### Weekly Checks

- [ ] Check contact form submissions (email inbox)
- [ ] Monitor GA4 for anomalies (sudden drop in traffic = potential issue)
- [ ] Scan for any error log messages in cPanel

### Monthly Maintenance

- [ ] Update blog with new content
- [ ] Review and refresh testimonials
- [ ] Check all external links (blog, gallery) still point to valid pages
- [ ] Test contact form end-to-end
- [ ] Backup the site:
  - **cPanel → Backup** → Download full backup file

### Quarterly

- [ ] Run **Google PageSpeed Insights** to check performance
- [ ] Review **Google Search Console** for indexing issues
- [ ] Audit forms for spam/abuse patterns
- [ ] Test on new browser versions if major release occurred

### Clarity Analytics Configuration

**Status:** Currently using placeholder ID (`placeholder-clarity-id`). To enable heatmapping and session replay:

1. Visit https://clarity.microsoft.com
2. Sign in with Microsoft account
3. Create a **new project** for `www.pleasureislanddesign.com`
4. Copy the **Project ID**
5. Update `index.html` line 55:
   ```html
   (window,document,"clarity","script","[PASTE-ID-HERE]");
   ```
6. Commit and deploy
7. Wait 24 hours for data to appear

---

## Contact & Support

**Site Owner:** Nicole Rayment  
**Email:** pleasureislanddesign@gmail.com  
**Phone:** (910) 444-1230  

**GoDaddy Support:**
- Phone: 1-480-505-8877
- Live Chat: https://www.godaddy.com/support

**GitHub Issues:** https://github.com/willyd61/pleasureislanddesign.com/issues

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-26 | Claude | Initial GoDaddy cPanel deployment runbook |

---

**Generated:** May 26, 2026  
**Status:** Production-Ready

