#!/usr/bin/env python3
"""
post_queue.py — Publish approved queue items to Instagram via the Meta Graph API.

The final stage of the pipeline:
    parse_calendar.py -> build_queue.py -> [human approves] -> post_queue.py

What it does
    1. Reads queue.json and selects items with status "approved" (or
       "scheduled" whose date is today or earlier).
    2. For each, creates a media container (image URL + caption+hashtags) and
       publishes it to the connected Instagram Professional account.
    3. Flips the item's status to "posted" and records the media id.

Requirements (see README.md "Connecting a real poster")
    - Instagram Professional account linked to a Facebook Page
    - A Meta app with instagram_content_publish permission
    - Environment variables:
        IG_USER_ID          numeric Instagram user id
        META_ACCESS_TOKEN   long-lived page/system-user token  (never commit!)
    - Each queue item needs an "image_url" field pointing at a PUBLIC image
      (e.g. https://www.pleasureislanddesign.com/gallery/...). Items without
      one are skipped with a warning — add image_url to queue.json during review.

Usage
    python3 automation/instagram/post_queue.py --dry-run   # show what would post
    python3 automation/instagram/post_queue.py             # post approved items
    python3 automation/instagram/post_queue.py --limit 1   # at most N posts this run

Cron (one post per weekday at 9:05am)
    5 9 * * 1-5 cd /path/to/site && python3 automation/instagram/post_queue.py --limit 1

Stdlib only — no pip installs.
"""
import sys
import os
import json
import time
import datetime
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, 'queue.json')
GRAPH = 'https://graph.facebook.com/v21.0'


def _api(path, params, method='POST'):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f'{GRAPH}/{path}', data=data, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def publish(ig_user, token, image_url, caption):
    """Two-step publish: create container, then publish it. Returns media id."""
    container = _api(f'{ig_user}/media', {
        'image_url': image_url,
        'caption': caption,
        'access_token': token,
    })
    creation_id = container['id']
    # Media containers can take a moment to be ready.
    time.sleep(3)
    result = _api(f'{ig_user}/media_publish', {
        'creation_id': creation_id,
        'access_token': token,
    })
    return result['id']


def due(item, today):
    if item.get('status') == 'approved':
        return True
    if item.get('status') == 'scheduled':
        d = (item.get('date') or '')[:10]
        return bool(d) and d <= today
    return False


def main(argv):
    dry = '--dry-run' in argv
    limit = None
    if '--limit' in argv:
        limit = int(argv[argv.index('--limit') + 1])

    if not os.path.exists(QUEUE):
        print('[ERROR] queue.json not found — run build_queue.py first.')
        return 1
    with open(QUEUE, encoding='utf-8') as fh:
        queue = json.load(fh)

    ig_user = os.environ.get('IG_USER_ID', '')
    token = os.environ.get('META_ACCESS_TOKEN', '')
    if not dry and (not ig_user or not token):
        print('[ERROR] IG_USER_ID and META_ACCESS_TOKEN must be set (see README).')
        print('        Run with --dry-run to preview without credentials.')
        return 1

    today = datetime.date.today().isoformat()
    candidates = [it for it in queue['items'] if due(it, today)]
    if limit is not None:
        candidates = candidates[:limit]
    if not candidates:
        print('[OK] Nothing due to post (no approved/scheduled items).')
        return 0

    posted = 0
    for item in candidates:
        caption = (item.get('caption') or '').strip()
        tags = (item.get('hashtags') or '').strip()
        full_caption = f'{caption}\n\n{tags}'.strip()
        image_url = (item.get('image_url') or '').strip()

        label = f"{item['id']} ({item.get('post_type', 'Post')})"
        if not image_url:
            print(f'[SKIP] {label}: no image_url set — add one in queue.json.')
            continue
        if dry:
            print(f'[DRY-RUN] Would post {label}')
            print(f'          image:   {image_url}')
            print(f'          caption: {full_caption[:100]}...')
            continue

        try:
            media_id = publish(ig_user, token, image_url, full_caption)
        except Exception as exc:  # surface Graph errors, keep queue consistent
            print(f'[ERROR] {label}: {exc}')
            continue

        item['status'] = 'posted'
        item['posted_media_id'] = media_id
        item['posted_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        posted += 1
        print(f'[✓] Posted {label} -> media {media_id}')

    if not dry and posted:
        with open(QUEUE, 'w', encoding='utf-8') as fh:
            json.dump(queue, fh, indent=2, ensure_ascii=False)
        print(f'[OK] {posted} item(s) posted; queue.json updated.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
