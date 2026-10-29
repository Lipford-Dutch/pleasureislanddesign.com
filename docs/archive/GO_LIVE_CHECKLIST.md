# Go-Live Checklist: Pleasure Island Design

**Target Date:** May 26, 2026  
**Owner:** Nicole Rayment  
**Emergency Contact:** pleasureislanddesign@gmail.com

---

## 48 Hours Before Launch

- [ ] **Backup Current Site**
  - [ ] Log in to GoDaddy cPanel
  - [ ] Click **Backups** → **Full Backup**
  - [ ] Save backup file locally (keep for 30 days)

- [ ] **Notify Team**
  - [ ] Confirm Nicole is available on launch day (9 AM – 5 PM recommended)
  - [ ] Brief anyone with server/email access on rollback procedure
  - [ ] Share this checklist with team

- [ ] **Final Code Review**
  - [ ] PR #12 merged to `main` ✓ (already done)
  - [ ] All CI checks passing (lint, security, format)
  - [ ] No open issues blocking launch

- [ ] **Content Lock**
  - [ ] No new content will be added between now and launch
  - [ ] All URLs finalized and tested

---

## 24 Hours Before Launch

- [ ] **Email Notifications Set Up**
  - [ ] Contact form sends to pleasureislanddesign@gmail.com ✓
  - [ ] Send test form submission, verify receipt

- [ ] **Analytics Accounts Confirmed**
  - [ ] GA4 account created and ID verified (G-X0PJB95RBE) ✓
  - [ ] GTM account created and ID verified (GTM-W2TMT5K8) ✓
  - [ ] Clarity ID **STILL PENDING** — optional, can be added later

- [ ] **DNS & Domain Check**
  - [ ] Domain registrar: GoDaddy ✓
  - [ ] Domain: www.pleasureislanddesign.com ✓
  - [ ] Nameservers point to GoDaddy ✓
  - [ ] SSL certificate active (Let's Encrypt via cPanel) ✓

- [ ] **Browser Testing Completed**
  - [ ] Chrome (Windows & Mac) ✓
  - [ ] Firefox (Windows & Mac) ✓
  - [ ] Safari (Mac & iOS) ✓
  - [ ] Edge (Windows) ✓
  - [ ] Mobile: iPhone Safari, Android Chrome ✓

---

## 2 Hours Before Launch (Final Verification)

### CI/CD Pipeline Status
- [ ] Latest commit on GitHub `main`: `4d50ebe` (CSS lint fix)
- [ ] All GitHub Actions checks: **PASSING** (lint, security, formatting)
- [ ] No pending CI runs

### Code Readiness
- [ ] No uncommitted changes on local machine
- [ ] `main` branch is clean and up to date
- [ ] GoDaddy Git repo is synchronized (if using cPanel Git)

### Content Verification
- [ ] No `localhost` references anywhere in code
- [ ] All images load (check DevTools Network tab)
- [ ] Contact form target email is correct
- [ ] Navigation links all work
- [ ] Blog, gallery, specials sections accessible

### Analytics Verification
- [ ] GA4 tracking code present in index.html ✓
- [ ] GTM tracking code present in index.html ✓
- [ ] Clarity ID either configured or noted as "to be done later" ✓

### SEO Check
- [ ] robots.txt allows indexing (not `Disallow: /`)
- [ ] sitemap.xml is valid and updated
- [ ] Canonical tag points to www.pleasureislanddesign.com
- [ ] No `noindex` meta tag on public pages
- [ ] JSON-LD schema is correct

---

## Launch Day (Execution)

### T-Minus 30 Minutes

1. **Final Backup**
   ```bash
   # GoDaddy cPanel → Backups → Full Backup
   # (Just to be extra safe)
   ```

2. **Confirm Uptime Monitoring**
   - [ ] UptimeRobot (or similar) is watching www.pleasureislanddesign.com
   - [ ] Alert email is configured

3. **Prepare Rollback Commands**
   - [ ] Have `GODADDY_DEPLOYMENT.md` open (rollback section)
   - [ ] Know your GoDaddy cPanel username
   - [ ] Know the last good commit hash (saved somewhere safe)

### T = 0 (Go-Live)

#### Step 1: Deploy Code
Choose one:

**Option A: Via cPanel Git (Recommended)**
1. Log in to GoDaddy cPanel
2. Go to **Git Version Control**
3. Click **"Pull"** next to production repository
4. Select branch: `main`
5. Click **Pull** → Wait for completion (30 sec – 1 min)

**Option B: Manual via SSH** (if available)
```bash
ssh [username]@[godaddy-server-ip]
cd /home/[username]/public_html
git pull origin main
```

**Option C: Automated via GitHub Actions** (if configured)
- Merge to main triggers auto-deploy
- Monitor GitHub Actions for completion

**Timeline:** 1–5 minutes

#### Step 2: Verify Site Loads (Immediately)
1. Open https://www.pleasureislanddesign.com in browser (new Incognito/Private window)
2. Confirm:
   - [ ] Page loads without 404 or 500 error
   - [ ] Homepage displays correctly
   - [ ] Navigation menu works
   - [ ] No console errors (DevTools → Console tab)

#### Step 3: Test Critical Functions (Next 5 Minutes)
1. **Forms:** Fill out contact form, submit, verify email received
2. **Links:** Click Home, About, Services, Gallery, Blog, Specials, Contact
3. **Mobile:** Open site on phone browser, confirm responsive layout
4. **Analytics:** Check DevTools → Network → confirm GA4/GTM tracking

#### Step 4: Monitor (Next 30 Minutes)
- [ ] Watch real-time GA4 dashboard for initial visits
- [ ] Monitor email inbox for any contact form submissions
- [ ] Scan browser console for JavaScript errors (on different pages)
- [ ] Check CloudFlare/cPanel logs for any 5xx errors

---

## ✅ Launch Success Criteria

You can declare launch **successful** when:

- [ ] Homepage loads without errors
- [ ] All navigation works
- [ ] Contact form sends to your inbox
- [ ] GA4 shows real-time user activity
- [ ] No critical errors in DevTools console
- [ ] Site is responsive on mobile
- [ ] Uptime monitor shows site as "UP"

---

## 🚨 If Something Goes Wrong

### Red Flags (Immediate Rollback)
- **500 error** on homepage
- **404 error** for CSS or JavaScript files
- **Forms don't submit** (multiple test failures)
- **Contact form sends email to wrong address**
- **Uptime monitor shows "DOWN"**

### Rollback Steps (< 5 Minutes)

1. **Log in to GoDaddy cPanel**
2. **Git Version Control** → Click the commit before the deploy
3. **Click "Reset to this commit"** or **"Checkout"**
4. **Confirm rollback**
5. **Verify site loads the old version**

**Then:**
- Identify what broke
- Fix it locally on your machine
- Test thoroughly before re-deploying

---

## ✅ Post-Launch (First 24 Hours)

- [ ] Check email inbox every 2 hours for contact form submissions
- [ ] Monitor GA4 for anomalies (sudden traffic spikes or drops)
- [ ] Monitor server logs in cPanel for errors
- [ ] Test contact form once more (send test email)
- [ ] Confirm SSL certificate is active (green lock in browser)

### End of Day 1
- [ ] Take a final screenshot of the live site
- [ ] Document any issues encountered
- [ ] Brief team on launch success/issues
- [ ] Set reminder for Clarity ID configuration (if deferred)

---

## 📋 Post-Launch (Week 1)

- [ ] Monitor GA4 for full week of data (identify patterns)
- [ ] Check Google Search Console for indexing progress
- [ ] Verify all blog posts and gallery images load
- [ ] Test specials flyer download
- [ ] Monitor uptime monitor for any downtime alerts

---

## 🎯 Success Metrics (Week 1+)

Track these over the first week to measure launch success:

| Metric | Target | Check After |
|--------|--------|-------------|
| **Page Load Time** | < 3 sec | 24 hours |
| **Uptime** | 99.9%+ | 7 days |
| **Contact Form Submissions** | ≥ 1 per day | 7 days |
| **GA4 Sessions** | ≥ 50 | 7 days |
| **Mobile Traffic** | ≥ 40% of total | 7 days |
| **Bounce Rate** | < 60% | 7 days |
| **Avg Session Duration** | > 1 min | 7 days |

---

## 📞 Emergency Contacts

**If something breaks after launch:**

1. **Immediate (First Response)**
   - Check `GODADDY_DEPLOYMENT.md` → Troubleshooting section
   - Attempt rollback if unsure

2. **GoDaddy Support**
   - Phone: 1-480-505-8877
   - Hours: 24/7
   - Have your account email & domain ready

3. **Developer (Claude / Follow-Up)**
   - GitHub: https://github.com/willyd61/pleasureislanddesign.com/issues
   - Describe the issue, include error messages from cPanel logs

---

**Good luck! You've got this.** 🚀

Generated: May 26, 2026

