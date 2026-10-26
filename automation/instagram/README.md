# Instagram Content Pipeline

Scaffolding that turns the Pleasure Island Design 30-day Instagram planning
workbook into a reviewable, status-tracked posting queue.

It is deliberately **integration-agnostic**: it prepares and tracks content but
does **not** post to Instagram. Posting to Instagram requires either the Meta
Graph API (Instagram Professional account + Facebook Page + a reviewed Meta app)
or a third-party scheduler (Buffer, Later, Metricool). Wiring one of those in is
the last step — see [Connecting a poster](#connecting-a-real-poster).

```
  source .xlsx
      │  parse_calendar.py
      ▼
  content-calendar.json          (structured, one record per row, all sheets)
      │  build_queue.py
      ▼
  queue.json  +  bundles/*.md    (status-tracked queue + copy-paste bundles)
      │  (human review / scheduler / Graph API)
      ▼
  posted to Instagram
```

## Files

| File | Purpose | Tracked in git |
|------|---------|----------------|
| `parse_calendar.py` | `.xlsx` → `content-calendar.json`. Stdlib only, no pip installs. | ✅ |
| `build_queue.py` | `content-calendar.json` → `queue.json` + `bundles/*.md`. | ✅ |
| `content-calendar.schema.json` | JSON Schema for the parsed calendar. | ✅ |
| `content-calendar.sample.json` | Small labeled sample so the pipeline runs before the real parse. | ✅ |
| `content-calendar.json` | Authoritative calendar from the real workbook. | ignored by default |
| `queue.json` | Master queue; each item has a `status`. | ignored by default |
| `bundles/*.md` | Per-post ready-to-post briefs. | ignored by default |

`content-calendar.json`, `queue.json`, and `bundles/` are git-ignored so a local
parse of a private workbook isn't committed by accident. Commit them deliberately
once you want the calendar and review status versioned.

## Usage

```bash
# 1. Parse the workbook into structured JSON
python3 automation/instagram/parse_calendar.py path/to/Instagram_Calendar.xlsx

# 2. Build the review queue + per-post bundles
python3 automation/instagram/build_queue.py

# (no workbook yet? the pipeline falls back to the labeled sample)
python3 automation/instagram/build_queue.py automation/instagram/content-calendar.sample.json
```

## Review workflow

Each post in `queue.json` carries a `status`:

| Status | Meaning |
|--------|---------|
| `draft` | Imported from the calendar, not yet reviewed. |
| `approved` | Caption + visual signed off, ready to schedule. |
| `scheduled` | Handed to a scheduler / queued with a post time. |
| `posted` | Live on Instagram. |

Edit the `status` field in `queue.json` as you review. Re-running
`build_queue.py` **preserves existing statuses** (matched by post `id`), so
regenerating after a calendar change never resets your review progress.

## Connecting a real poster

**The poster is implemented: `post_queue.py`.** It reads `queue.json`, takes
items with `status: "approved"` (or `"scheduled"` whose date has arrived),
publishes them via the Meta Graph API, and flips them to `"posted"`.

```bash
python3 automation/instagram/post_queue.py --dry-run   # preview, no credentials needed
python3 automation/instagram/post_queue.py --limit 1   # post at most one item
# cron: one post per weekday morning
# 5 9 * * 1-5 cd /path/to/site && python3 automation/instagram/post_queue.py --limit 1
```

### One-time Meta setup (required before it can post)
1. Convert the Instagram account to **Professional** and link it to a Facebook
   Page (Instagram app → Settings → Account type).
2. Create a Meta app at developers.facebook.com → add **Instagram Graph API**
   → grant `instagram_content_publish` (+ `pages_show_list`).
3. Generate a **long-lived access token** (Graph API Explorer → extend token),
   and find the numeric **IG user id** (`GET /me/accounts` → page →
   `?fields=instagram_business_account`).
4. Export credentials where the cron/user runs (never commit them):
   ```bash
   export IG_USER_ID=1784xxxxxxxxxxx
   export META_ACCESS_TOKEN=EAAG...
   ```
5. During review, add an `image_url` to each queue item — a **public** URL
   (the live site's `gallery/` images work). Items without one are skipped.

Alternative: a third-party scheduler (Buffer / Later / Metricool) fed from the
`bundles/*.md` files — lowest-effort, no Meta app review.

## Notes

- The parser is resilient to column reordering: `build_queue.py` looks up columns
  case- and spacing-insensitively (`Post Type` == `posttype`).
- Every worksheet is preserved under `sheets` in the parsed JSON, so story-idea
  and reference tabs aren't lost even though only the calendar sheet feeds the queue.
