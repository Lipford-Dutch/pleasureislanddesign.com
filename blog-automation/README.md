# Blog automation (not web-served)

This folder holds unpublished drafts, the publishing schedule and the publisher
script. It is **not** listed in `.cpanel.yml`, so it is never copied into
`public_html`. `.htaccess` also 404s `/blog/drafts/`, `/blog/publish-scheduled.php`,
`/blog/scheduled-posts.json` and `/blog-automation/` in case old copies exist on
the server.

`publish-scheduled.php` only runs from the command line (it answers 404 under any
web server). If `PID_PUBLISH_TOKEN` is set in the environment, or
`~/.pid-secrets/publisher.php` returns `['token' => '...']`, the script also
requires `--token=<same value>`.

## Current state (Nov 2026)

The five posts scheduled for 2026-07-01 → 2026-09-01 never published. Each draft
is a ~400-byte stub (title + one sentence), and the publisher's quality gate
(`pid_is_publishable_post`) correctly refuses to publish stubs. A dry run shows
`Would publish: 0, Errors: 5`.

## Publishing safely (recommended: in git, not on the server)

1. Write the full post into `drafts/<slug>.html`, using an existing post in
   `blog/` as the template (full header/footer, `<h1>`, `<time datetime>`).
   Remove the `noindex` meta when it is final.
2. Set `publish_date` in `scheduled-posts.json` (today or earlier to publish now).
3. From the repo root: `php blog-automation/publish-scheduled.php --dry-run`
4. If the preview is right: `php blog-automation/publish-scheduled.php`
   This moves the draft into `blog/`, adds its card to `blog/index.html` and
   updates `sitemap.xml`.
5. Commit, open a PR, review, merge, deploy as usual.

Why not cron straight into `public_html`? `.cpanel.yml` does
`rm -rf public_html/blog && cp -R blog`, so anything a server cron publishes is
wiped by the next deploy unless it is also committed.

## Optional server cron (only if you accept the caveat above)

cPanel → Cron Jobs, daily at 6:00 AM, pointing at the private repo clone:

    0 6 * * * cd $HOME/repositories/pleasureislanddesign.com && PID_BLOG_DIR=$HOME/public_html/blog /usr/local/bin/php blog-automation/publish-scheduled.php >> $HOME/logs/blog-publisher.log 2>&1

Run it once by hand with `--dry-run` first. Adjust the repository path to
whatever cPanel → Git Version Control shows.
