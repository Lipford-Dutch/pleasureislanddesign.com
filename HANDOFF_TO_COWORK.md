# Session Handoff — Finish GoDaddy cPanel Deployment

**Date:** 2026-06-04
**From:** Claude Code (no browser/desktop/SSH access to GoDaddy)
**To:** An agent with browser + desktop + terminal/SSH control (Cowork)
**Goal:** Publish the static site to GoDaddy production. We are ~1 step from done; blocked on a cPanel-side "cannot deploy" gate that needs SSH/UI access to diagnose.

---

## 1. What this project is
- **Site:** Pleasure Island Design — cabinet refinishing, Wilmington NC
- **Production:** GoDaddy **cPanel / shared hosting** at `www.pleasureislanddesign.com`
- **Source of truth:** GitHub `willyd61/pleasureislanddesign.com`, branch `main`
- **Architecture:** Static HTML/CSS/JS. (There is a `storefront-beta/` Node app in the repo — NOT deployed; shared hosting can't run Node. `/shop/` is a static "Coming Soon" page.)

## 2. Current state (all green on GitHub)
- `main` HEAD = **`a09b2378`** ("Add cPanel Git deployment manifest (#15)")
- Recent merges: #12 (audit fixes), #14 (deploy docs + CSS lint fix), #15 (`.cpanel.yml`)
- GitHub Actions CI: **passing** (lint, format, security, links, assets)
- Docs in repo: `GODADDY_DEPLOYMENT.md`, `GO_LIVE_CHECKLIST.md`, `DNS_AND_CUTOVER.md`, `DEPLOYMENT_STATUS.md`

## 3. cPanel facts (from screenshots)
- cPanel user: **`kyjlg8o1knr0`** ; cPanel v134.0.35
- Git repo cloned to: **`/home/kyjlg8o1knr0/repositories/pleasureislanddesign.com`**
- Remote URL: `https://github.com/willyd61/pleasureislanddesign.com.git`
- Checked-out branch: `main`, HEAD `a09b2378` (verified — `.cpanel.yml` present with "New" badge)
- Intended deploy target: **`/home/kyjlg8o1knr0/public_html`**
- Clone from GitHub succeeded with **no auth prompt** → repo is reachable/public.

## 4. THE BLOCKER
Clicking **Pull or Deploy → Deploy HEAD Commit** returns:
> **The system cannot deploy.** Ensure: (1) a valid `.cpanel.yml` exists, (2) no uncommitted changes on the checked-out branch.

This message is generic (shows both requirements regardless of which failed).

### Already ruled out (by Claude)
- `.cpanel.yml` **is** present at HEAD and is **valid YAML** (`deployment.tasks`, 20 tasks). So requirement #1 is satisfied in content.
- **Not** a line-ending problem: `git ls-files --eol` shows 0 index-CRLF files; `git add --renormalize .` stages nothing. No Git LFS, no custom filters.
- Therefore the most probable failing requirement is **#2: cPanel sees the checked-out working tree as having uncommitted changes** — for an environment-specific reason we can't see from outside (cPanel's git version / `core.autocrlf` / the `* text=auto` attribute behaving differently on their box).

## 5. WHAT TO DO (in order)

### Step A — Diagnose definitively (SSH)
```bash
ssh kyjlg8o1knr0@<godaddy-host>        # host from cPanel SSH info / GoDaddy
cd ~/repositories/pleasureislanddesign.com
git status                              # <-- THE key output
git diff --stat                         # what (if anything) is "modified"
git log --oneline -1                    # confirm HEAD = a09b2378
```
- If `git status` is **clean** → the failing requirement is the `.cpanel.yml` validity per cPanel's parser → go to Step C.
- If `git status` shows **modified files** → go to Step B.

### Step B — If working tree is dirty (most likely)
Quickest unblock (discard the spurious local modifications, then deploy):
```bash
cd ~/repositories/pleasureislanddesign.com
git config core.autocrlf false
git checkout -- .          # or:  git reset --hard origin/main
git status                 # should now be clean
```
Then retry **Deploy HEAD Commit** in the cPanel UI.

Durable fix if `* text=auto` is the cause (do on GitHub, then re-pull): edit `.gitattributes`, remove the `* text=auto` line (keep explicit `*.ext text eol=lf` lines), commit to `main`, then in cPanel **Update from Remote** → **Deploy HEAD Commit**.

### Step C — If cPanel rejects the `.cpanel.yml`
- Check the log: `tail -n 100 /usr/local/cpanel/logs/error_log` (or the deploy log under `~/.cpanel/logs/` if present).
- Try a minimal `.cpanel.yml` (cPanel's parser is stricter than generic YAML — remove leading comment block, keep tasks). Current file is at repo root.

### Step D — Guaranteed fallback (bypass cPanel's deploy gate entirely)
The repo is already cloned on the server, so just run the manifest's commands manually over SSH:
```bash
cd ~/repositories/pleasureislanddesign.com
git pull
export DEPLOYPATH=$HOME/public_html
mkdir -p "$DEPLOYPATH"
# BACK UP FIRST: zip current public_html before overwriting
cp -f index.html 404.html styles.css robots.txt sitemap.xml .htaccess .nojekyll "$DEPLOYPATH"/
for d in blog specials shop gallery locations js img fonts forms opt-images; do
  rm -rf "$DEPLOYPATH/$d" && cp -R "$d" "$DEPLOYPATH"/
done
echo "Deployed to $DEPLOYPATH"
```
This produces the exact same result as the `.cpanel.yml` deploy.

## 6. BEFORE deploying — back up current live site
cPanel → Files → **Backup** → Download Full Backup, OR File Manager → zip `public_html`. (User may have already done this — confirm.)

## 7. Verify after deploy
Open Incognito → `https://www.pleasureislanddesign.com`:
- Homepage loads, no 404/500; green padlock (SSL)
- Stats show real numbers (10+, 500+, 5–8, 100%) and animate on scroll
- Two YouTube videos embed in the video section
- Nav works; contact form submits → email arrives at pleasureislanddesign@gmail.com
- Specials page flyer loads
- DevTools Console: no errors (note: `favicon.ico` is missing in repo → one harmless 404; add a favicon later)

## 8. Rollback
- cPanel Git: check out the previous commit → Deploy again, **or**
- Restore the Step 6 backup via File Manager, **or**
- SSH: re-copy from the backup zip.

## 9. Known deferred items (NOT blockers)
- **Microsoft Clarity** analytics still uses `placeholder-clarity-id` in `index.html` (~line 55). Owner will add the real ID from clarity.microsoft.com later.
- **favicon.ico** missing (harmless 404).
- **storefront-beta** Node swag store: future phase, separate hosting (see `PROJECT_BACKLOG.md`).

## 10. Key facts
- GA4: `G-X0PJB95RBE` · GTM: `GTM-W2TMT5K8`
- Contact: (910) 444-1230 · pleasureislanddesign@gmail.com
- Owner: Nicole Rayment · Repo owner GitHub: willyd61
- DNS: already on GoDaddy → **no DNS change needed** (cPanel-to-cPanel code swap).

---
**Bottom line for Cowork:** SSH in, run `git status` in `~/repositories/pleasureislanddesign.com` to learn which requirement is failing, apply Step B (clean tree) or Step C, then Deploy — or just use Step D to copy files directly. Then verify per Section 7.
