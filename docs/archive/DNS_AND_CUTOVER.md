# DNS & Cutover Plan

**Pleasure Island Design → GoDaddy Production**

---

## Current Setup

- **Current Host:** GoDaddy (assumed already live from earlier deployment)
- **Current Domain:** www.pleasureislanddesign.com
- **Current Nameservers:** GoDaddy NS (ns01.godaddy.com, ns02.godaddy.com, etc.)
- **DNS Registrar:** GoDaddy
- **SSL:** Let's Encrypt (via cPanel, auto-renewed)

---

## DNS Cutover Plan

Since **both old and new code are on GoDaddy cPanel**, the DNS doesn't need to change. This is a **code-only cutover**, not a host migration.

### Before Cutover

1. **Verify Current DNS Resolves Correctly**
   ```bash
   nslookup www.pleasureislanddesign.com
   # Should return GoDaddy IP
   ```

2. **Confirm cPanel Git is Synchronized**
   - GoDaddy cPanel Git repo points to your GitHub `main` branch
   - Run a `git pull` to get the latest code

3. **Verify SSL Certificate**
   - Log in to GoDaddy cPanel → **SSL/TLS** → Verify Let's Encrypt cert is active
   - Cert should auto-renew 30 days before expiry

### Cutover (Code Deployment Only)

**Step 1: Deploy Code** (as outlined in GO_LIVE_CHECKLIST.md)
```bash
# Via cPanel Git UI:
cPanel → Git Version Control → Pull main
```

**Step 2: Verify Deployment**
- [ ] Visit https://www.pleasureislanddesign.com
- [ ] Confirm latest code is live
- [ ] Test contact form, navigation, all critical paths

**Step 3: Monitor Traffic**
- Monitor GA4, email submissions, uptime monitor for next 24 hours

### After Cutover (No Changes Required)

- **DNS:** No change — already points to GoDaddy
- **Email:** No change — already hosted on GoDaddy
- **SSL:** No change — Let's Encrypt auto-renews
- **Backups:** Continue as configured in cPanel

---

## If You Later Migrate Away from GoDaddy (Future)

If you ever move to a different host (e.g., Netlify, Vercel, AWS), you **will** need to:

1. **Update DNS Nameservers** at GoDaddy Registrar
2. **Point domain to new host's nameservers**
3. **Wait 24–48 hours for DNS propagation**

But that's for a future date. For now, **no DNS changes are needed** — it's a cPanel-to-cPanel code swap.

---

## DNS Health Check

Before you go live, verify DNS is healthy:

```bash
# Check nameservers
dig www.pleasureislanddesign.com NS

# Check A record (IPv4)
dig www.pleasureislanddesign.com A

# Check all records
dig www.pleasureislanddesign.com ANY

# Troubleshoot propagation (optional)
nslookup www.pleasureislanddesign.com 8.8.8.8  # Google DNS
nslookup www.pleasureislanddesign.com 1.1.1.1  # Cloudflare DNS
```

All should return the **GoDaddy IP** (you can find it in cPanel → **IP Functions**).

---

## GoDaddy cPanel Quick Reference

| Service | Where in cPanel | Notes |
|---------|-----------------|-------|
| **Git Version Control** | File Manager section | Deploy code from GitHub |
| **SSL/TLS** | Home → SSL/TLS Status | Verify Let's Encrypt is active |
| **Email Accounts** | Email section | Manage email users for domain |
| **DNS Zone Editor** | Domains section | Manage DNS records (if needed) |
| **Backups** | Tools → Backups | Create/restore full site backups |
| **Error Logs** | File Manager → Error Logs | Debug 500 errors |
| **File Manager** | File Manager | Browse `/public_html` directory |

---

## SSL Certificate Details

**Current Setup:**
- Provider: Let's Encrypt (Free)
- Auto-Renewal: Enabled (via cPanel)
- Renewal Timing: 30 days before expiry
- Domain(s): www.pleasureislanddesign.com, pleasureislanddesign.com

**Check Certificate Status:**
1. GoDaddy cPanel → **SSL/TLS**
2. Look for a green checkmark next to your domain
3. Expiry date should be ~1 year from now

**If Certificate Expires:**
- Let's Encrypt auto-renews; no action needed
- If auto-renewal fails, cPanel will send email warning
- Manual renewal: cPanel → SSL/TLS → **AutoSSL** → Run

---

## Summary

✅ **No DNS changes required for this go-live**

The cutover is purely a **code deployment** to the same server. DNS already points to GoDaddy cPanel, and that's where the new code will run.

Simply:
1. Pull the latest code via cPanel Git
2. Verify it loads
3. Test critical functions
4. Monitor for 24 hours

Done!

---

Generated: May 26, 2026

