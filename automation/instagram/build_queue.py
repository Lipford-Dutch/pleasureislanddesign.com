#!/usr/bin/env python3
"""
build_queue.py — Turn a parsed content-calendar.json into a reviewable posting
queue plus one ready-to-post bundle per post.

This is the scaffolding layer of the Instagram pipeline. It does NOT post to
Instagram (that requires a Meta Graph API / third-party scheduler integration —
see README.md). It prepares and tracks content so a human, a scheduler, or a
future posting integration can pick each item up.

Pipeline stages:
    xlsx --parse_calendar.py--> content-calendar.json --build_queue.py--> queue.json + bundles/

Usage:
    python3 automation/instagram/build_queue.py [calendar.json]

If no calendar path is given it prefers content-calendar.json, then falls back
to content-calendar.sample.json so the pipeline is always runnable.

Outputs (all under automation/instagram/, git-ignored except this script):
    queue.json          — master list: one entry per post with a "status"
                          (draft | approved | scheduled | posted) preserved
                          across re-runs so review progress is never lost.
    bundles/NN-slug.md  — human-readable, copy-paste-ready caption + hashtags +
                          visual brief for each post.
"""
import sys
import os
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
VALID_STATUS = ('draft', 'approved', 'scheduled', 'posted')


def _pick(rec, *names, default=''):
    """Case/spacing-insensitive column lookup."""
    norm = {re.sub(r'\s+', '', k).lower(): v for k, v in rec.items()}
    for name in names:
        key = re.sub(r'\s+', '', name).lower()
        if key in norm and str(norm[key]).strip():
            return str(norm[key]).strip()
    return default


def _slug(text, index):
    base = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    base = '-'.join(base.split('-')[:6]) or 'post'
    return f"{index:02d}-{base}"


def _load_calendar(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def _load_existing_queue(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        return {item['id']: item for item in data.get('items', [])}
    except (ValueError, KeyError):
        return {}


def build(calendar_path):
    calendar = _load_calendar(calendar_path)
    posts = calendar.get('posts', [])
    queue_path = os.path.join(HERE, 'queue.json')
    bundles_dir = os.path.join(HERE, 'bundles')
    os.makedirs(bundles_dir, exist_ok=True)

    existing = _load_existing_queue(queue_path)
    items = []

    for i, rec in enumerate(posts, start=1):
        day = _pick(rec, 'Day')
        date = _pick(rec, 'Date')
        post_type = _pick(rec, 'Post Type', 'PostType', default='Post')
        visual = _pick(rec, 'Visual Instructions', 'Visual', 'Visual Instruction')
        caption = _pick(rec, 'Caption')
        hashtags = _pick(rec, 'Hashtag Bundle', 'Hashtags', 'Hashtag')
        notes = _pick(rec, 'Notes', 'Note')

        pid = _slug(caption or post_type, i)
        # Preserve human review status across re-runs.
        status = existing.get(pid, {}).get('status', 'draft')
        if status not in VALID_STATUS:
            status = 'draft'

        item = {
            'id': pid,
            'sequence': i,
            'date': date,
            'day': day,
            'post_type': post_type,
            'visual': visual,
            'caption': caption,
            'hashtags': hashtags,
            'notes': notes,
            'status': status,
        }
        items.append(item)

        bundle = (
            f"# {i:02d}. {post_type}"
            + (f" — {day}" if day else "")
            + (f" ({date})" if date else "")
            + "\n\n"
            f"**Status:** {status}\n\n"
            f"## Caption\n\n{caption or '_(none)_'}\n\n"
            f"## Hashtags\n\n{hashtags or '_(none)_'}\n\n"
            f"## Visual brief\n\n{visual or '_(none)_'}\n\n"
            f"## Notes\n\n{notes or '_(none)_'}\n"
        )
        with open(os.path.join(bundles_dir, f"{pid}.md"), 'w', encoding='utf-8') as fh:
            fh.write(bundle)

    queue = {
        'source_calendar': os.path.basename(calendar_path),
        'count': len(items),
        'status_legend': list(VALID_STATUS),
        'items': items,
    }
    with open(queue_path, 'w', encoding='utf-8') as fh:
        json.dump(queue, fh, indent=2, ensure_ascii=False)

    return queue, queue_path, bundles_dir


def main(argv):
    if len(argv) > 1:
        calendar_path = argv[1]
    else:
        primary = os.path.join(HERE, 'content-calendar.json')
        sample = os.path.join(HERE, 'content-calendar.sample.json')
        calendar_path = primary if os.path.exists(primary) else sample

    if not os.path.exists(calendar_path):
        print(f"[ERROR] No calendar found at {calendar_path}. "
              f"Run parse_calendar.py first.")
        return 1

    queue, queue_path, bundles_dir = build(calendar_path)
    posted = sum(1 for it in queue['items'] if it['status'] == 'posted')
    print(f"[OK] Source: {queue['source_calendar']}")
    print(f"[OK] Queue: {queue['count']} post(s) ({posted} marked posted) -> {queue_path}")
    print(f"[OK] Bundles written to {bundles_dir}/")
    if queue['source_calendar'].startswith('content-calendar.sample'):
        print("[NOTE] Using the SAMPLE calendar. Generate the real one with "
              "parse_calendar.py against the source .xlsx.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
