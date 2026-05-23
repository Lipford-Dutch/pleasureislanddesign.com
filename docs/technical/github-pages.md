# GitHub Pages Setup

## Configuration

GitHub Pages is configured to deploy via **GitHub Actions** (not from a branch directly).

**Settings:** Repository → Settings → Pages → Source: GitHub Actions

## Live Preview URL

```
https://willyd61.github.io/pleasureislanddesign.com/
```

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
   Value: willyd61.github.io
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

## Switching to Production Hosting

When moving from GitHub Pages to a production host (Netlify, Vercel, AWS, self-hosted):

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
