# GitHub Pages Setup

## Configuration

GitHub Pages is configured to deploy via **GitHub Actions** (not from a branch directly).

**Settings:** Repository → Settings → Pages → Source: GitHub Actions

## Live Mirror URL

```
https://lipford-dutch.github.io/pleasureislanddesign.com/
```

GitHub Pages is a **mirror** of the public site. Production is GoDaddy cPanel
(see [CI/CD](cicd.md)). The Pages build publishes only the public site files,
the same set `.cpanel.yml` deploys: root HTML/CSS/robots/sitemap/favicons and the
`blog`, `specials`, `shop`, `gallery`, `locations`, `js`, `img`, `fonts`, `forms`
and `opt-images` directories. `docs/`, `automation/`, `blog-automation/`,
`blog/drafts`, `business/`, `tests/`, `.github/` and all `*.php` files are never
published, and the workflow fails if any of them appear in `_site/`.

## Custom Domain (When Ready for Production)

To point a custom domain at GitHub Pages:

1. Add a `CNAME` file to the repo root:
   ```
   www.pleasureislanddesign.com
   ```

2. Update DNS at your domain registrar:
   ```
   Type: CNAME
   Name: www
   Value: lipford-dutch.github.io
   ```

3. For apex domain (`pleasureislanddesign.com`):
   ```
   Type: A
   Name: @
   Values:
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
   ```

4. Enable "Enforce HTTPS" in GitHub Pages settings

5. Wait 24-48 hours for DNS propagation

## Production Hosting

Production already runs on GoDaddy cPanel, deployed from `Lipford-Dutch/pleasureislanddesign.com`
`main` with `.cpanel.yml`. The custom domain is **not** pointed at GitHub Pages.

If production ever moves to another host (Netlify, Vercel, AWS, self-hosted):

1. Update `DEPLOYMENT.md` with new procedures
2. Remove or repurpose `deploy.yml`
3. Add new deployment workflow for chosen host
4. Update DNS records at domain registrar
5. Verify SSL certificate is active
6. Run a full regression test

## Troubleshooting

**Pages not updating after merge?**
- Check Actions tab for deploy workflow status
- Verify GitHub Pages source is set to "GitHub Actions"
- Check for lint failures preventing deployment

**404 on specific paths?**
- Static sites only have `index.html` at root
- All navigation is anchor-based (`#section-id`)
- No server-side routing needed

**Custom domain not working?**
- DNS propagation can take 24-48 hours
- Verify CNAME file exists at repo root
- Check DNS settings at registrar
