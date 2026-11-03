<?php
/**
 * Blog Post Publisher — CLI ONLY
 *
 * Scheduled Publishing System
 * - Reads blog-automation/scheduled-posts.json
 * - Publishes drafts from blog-automation/drafts/ into blog/ when publish_date arrives
 * - Auto-updates blog/index.html & sitemap.xml
 * - Logging + backups
 *
 * SECURITY (2026-11 audit):
 *   This script lives OUTSIDE the deployed web root (blog-automation/ is not in
 *   .cpanel.yml) and refuses to run under any web SAPI. It can only be started
 *   from a shell or cron. Optionally, set PID_PUBLISH_TOKEN in the environment
 *   (or in a config file outside public_html, see PID_PUBLISH_CONFIG below) and
 *   pass --token=<value>; when a token is configured it is REQUIRED.
 *
 * Usage (from the repo root):
 *   Preview:  php blog-automation/publish-scheduled.php --dry-run
 *   Publish:  php blog-automation/publish-scheduled.php
 *   Target a different blog dir (e.g. a server cron writing into public_html):
 *             PID_BLOG_DIR=$HOME/public_html/blog php blog-automation/publish-scheduled.php
 *   Note: .cpanel.yml replaces public_html/blog on every deploy, so posts published
 *   straight into public_html are wiped by the next deploy. The safe flow is to
 *   run this in the repo, commit the result, and deploy (see PR notes).
 */

// ---- Hard guard: never runnable over HTTP ----
if (PHP_SAPI !== 'cli' || isset($_SERVER['REQUEST_METHOD'])) {
    if (!headers_sent()) {
        http_response_code(404);
        header('Content-Type: text/plain; charset=utf-8');
    }
    echo 'Not found';
    exit;
}

// ---- Optional shared-secret check (config lives outside the web root) ----
$pid_cli_args = $argv ?? [];
$pid_expected_token = (string) getenv('PID_PUBLISH_TOKEN');
$pid_config_path = getenv('PID_PUBLISH_CONFIG') ?: (getenv('HOME') ? getenv('HOME') . '/.pid-secrets/publisher.php' : '');
if ($pid_expected_token === '' && $pid_config_path && is_readable($pid_config_path)) {
    $pid_cfg = include $pid_config_path; // expected: <?php return ['token' => '...'];
    if (is_array($pid_cfg) && !empty($pid_cfg['token'])) {
        $pid_expected_token = (string) $pid_cfg['token'];
    }
}
if ($pid_expected_token !== '') {
    $pid_given = '';
    foreach ($pid_cli_args as $pid_arg) {
        if (strpos($pid_arg, '--token=') === 0) {
            $pid_given = substr($pid_arg, 8);
        }
    }
    if (!hash_equals($pid_expected_token, $pid_given)) {
        fwrite(STDERR, "[Blog Publisher] Missing or invalid --token. Aborting.\n");
        exit(2);
    }
}

require_once dirname(__DIR__) . '/forms/lib/form-helpers.php';

$pid_blog_dir = getenv('PID_BLOG_DIR') ?: dirname(__DIR__) . '/blog';
define('BLOG_ROOT', rtrim($pid_blog_dir, '/'));
define('CONFIG_FILE', __DIR__ . '/scheduled-posts.json');
define('DRAFTS_DIR', __DIR__ . '/drafts');
define('LOG_FILE', dirname(BLOG_ROOT) . '/.logs/blog-publisher.log');
define('BACKUP_DIR', dirname(BLOG_ROOT) . '/.backups');

// Ensure directories exist
foreach ([dirname(LOG_FILE), BACKUP_DIR] as $dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

$start_time = microtime(true);
$DRY_RUN = in_array('--dry-run', $pid_cli_args, true);
$stats = ['published' => 0, 'would_publish' => 0, 'skipped' => 0, 'errors' => 0];

if ($DRY_RUN) {
    echo "[Blog Publisher] DRY RUN — no files will be moved or written.\n";
}
echo "[Blog Publisher] Starting...\n";
log_event('PUBLISHER_START');

// Load config
if (!file_exists(CONFIG_FILE)) {
    echo "[ERROR] Config not found: " . CONFIG_FILE . "\n";
    log_event('CONFIG_NOT_FOUND', ['file' => CONFIG_FILE]);
    exit(1);
}

$config = json_decode(file_get_contents(CONFIG_FILE), true);
if (!$config || !isset($config['posts'])) {
    echo "[ERROR] Invalid config format\n";
    log_event('INVALID_CONFIG');
    exit(1);
}

$today = gmdate('Y-m-d');
$published_posts = [];
$errors = [];

// Process posts
foreach ($config['posts'] as $post) {
    $slug = $post['slug'] ?? '';
    $title = $post['title'] ?? 'Untitled';
    $publish_date = $post['publish_date'] ?? '';

    // Validate post entry
    if (!$slug) {
        echo "[SKIP] No slug for post: $title\n";
        $stats['skipped']++;
        continue;
    }

    // Check if date has arrived
    if ($publish_date && $publish_date > $today) {
        echo "[SCHEDULED] {$title} (publishes on {$publish_date})\n";
        $stats['skipped']++;
        continue;
    }

    $draft_file = DRAFTS_DIR . '/' . pid_sanitize_slug($slug) . '.html';
    $live_file = BLOG_ROOT . '/' . pid_sanitize_slug($slug) . '.html';

    // Check if already published
    if (file_exists($live_file)) {
        echo "[EXISTS] {$title} already published\n";
        $stats['skipped']++;
        continue;
    }

    // Check draft exists
    if (!file_exists($draft_file)) {
        echo "[ERROR] Draft not found: $draft_file\n";
        $errors[] = "Draft missing for '{$title}'";
        $stats['errors']++;
        log_event('DRAFT_NOT_FOUND', ['slug' => $slug, 'file' => $draft_file]);
        continue;
    }

    // Quality gate: must be a real, styled page — not a bare stub.
    $content = file_get_contents($draft_file);
    if (!pid_is_publishable_post($content)) {
        echo "[ERROR] Draft not publish-ready (stub or missing site chrome): {$draft_file}\n";
        $errors[] = "Draft not publish-ready: '{$title}'";
        $stats['errors']++;
        log_event('DRAFT_NOT_PUBLISHABLE', ['slug' => $slug]);
        continue;
    }

    if ($DRY_RUN) {
        echo "[DRY-RUN] Would publish: {$title}\n";
        $stats['would_publish']++;
        continue;
    }

    // Backup before publishing
    $backup_file = BACKUP_DIR . '/' . pid_sanitize_slug($slug) . '_' . date('YmdHis') . '.html.bak';
    copy($draft_file, $backup_file);

    // Move to live
    if (rename($draft_file, $live_file)) {
        echo "[✓] Published: {$title}\n";
        $published_posts[] = [
            'slug' => $slug,
            'title' => $title,
            'publish_date' => $publish_date ?: $today,
            'backup' => $backup_file
        ];
        $stats['published']++;
        log_event('POST_PUBLISHED', ['slug' => $slug, 'title' => $title]);
    } else {
        echo "[ERROR] Failed to publish: {$title}\n";
        $errors[] = "Failed to move draft for '{$title}'";
        $stats['errors']++;
        log_event('PUBLISH_FAILED', ['slug' => $slug]);
    }
}

// Update blog assets if anything published
if ($stats['published'] > 0 && !$DRY_RUN) {
    echo "\n[UPDATE] Regenerating blog index...\n";
    if (regenerate_blog_index()) {
        echo "[✓] Blog index updated\n";
        log_event('INDEX_UPDATED');
    } else {
        echo "[WARN] Failed to update index\n";
    }

    echo "[UPDATE] Regenerating sitemap...\n";
    if (regenerate_sitemap()) {
        echo "[✓] Sitemap updated\n";
        log_event('SITEMAP_UPDATED');
    } else {
        echo "[WARN] Failed to update sitemap\n";
    }
}

// Final report
$duration = round(microtime(true) - $start_time, 2);
echo "\n=== SUMMARY ===\n";
if ($DRY_RUN) {
    echo "Would publish: {$stats['would_publish']}\n";
}
echo "Published: {$stats['published']}\n";
echo "Skipped: {$stats['skipped']}\n";
echo "Errors: {$stats['errors']}\n";
echo "Duration: {$duration}s\n";

if (!empty($errors)) {
    echo "\n[WARNINGS]\n";
    foreach ($errors as $error) {
        echo "  - {$error}\n";
    }
}

log_event('PUBLISHER_END', $stats);
exit($stats['errors'] > 0 ? 1 : 0);

// ===== HELPER FUNCTIONS =====

/**
 * Inject a styled card for every newly-published post into the designed blog
 * index, between the BLOG_POSTS_START / BLOG_POSTS_END markers. This is
 * deliberately non-destructive: it never rewrites the whole page (which would
 * wipe the hand-built layout, SEO tags, and existing cards) and it is
 * idempotent — a post already carded is skipped.
 */
function regenerate_blog_index() {
    $index_file = BLOG_ROOT . '/index.html';
    if (!file_exists($index_file)) {
        log_event('INDEX_MISSING', ['file' => $index_file]);
        return false;
    }

    $html = file_get_contents($index_file);
    if ($html === false) {
        return false;
    }

    // Fail safe: without the markers we do NOT touch the page.
    $end_marker = '<!-- BLOG_POSTS_END -->';
    $start_pos = strpos($html, '<!-- BLOG_POSTS_START');
    $end_pos = strpos($html, $end_marker);
    if ($start_pos === false || $end_pos === false || $end_pos < $start_pos) {
        log_event('INDEX_MARKERS_NOT_FOUND');
        return false;
    }
    $existing_region = substr($html, $start_pos, $end_pos - $start_pos);

    // Metadata comes from the schedule config (authoritative for title/category).
    $meta_by_slug = [];
    $config = json_decode(@file_get_contents(CONFIG_FILE), true);
    if ($config && isset($config['posts'])) {
        foreach ($config['posts'] as $p) {
            $s = pid_sanitize_slug($p['slug'] ?? '');
            if ($s !== '') {
                $meta_by_slug[$s] = $p;
            }
        }
    }

    // We have no per-post hero images, so map by category to a representative one.
    $category_images = [
        'care'        => '../gallery/motts-landing-2023/after-1.jpg',
        'maintenance' => '../gallery/motts-landing-2023/after-1.jpg',
        'design'      => '../gallery/seagrove-2023/after-1.jpg',
        'trends'      => '../gallery/compass-pointe-2023/compess_pointe_after.jpg',
        'services'    => '../gallery/motts-landing-2023/after-1.jpg',
    ];
    $default_image = '../gallery/motts-landing-2023/after-1.jpg';

    $files = @scandir(BLOG_ROOT);
    if ($files === false) {
        return false;
    }
    sort($files);

    $new_cards = '';
    $added = 0;
    foreach ($files as $file) {
        if ($file === 'index.html' || !preg_match('/^([a-z0-9\-]+)\.html$/', $file, $m)) {
            continue;
        }
        $slug = $m[1];
        // Already carded (existing region or just-injected)? skip — idempotent.
        if (strpos($existing_region, "href=\"{$slug}.html\"") !== false
            || strpos($new_cards, "href=\"{$slug}.html\"") !== false) {
            continue;
        }

        $meta = $meta_by_slug[$slug] ?? [];
        $category = $meta['category'] ?? 'Blog';
        $image = $category_images[strtolower($category)] ?? $default_image;

        $date_human = '';
        if (!empty($meta['publish_date'])) {
            $ts = strtotime($meta['publish_date']);
            $date_human = $ts ? date('F j, Y', $ts) : $meta['publish_date'];
        }

        $title = $meta['title'] ?? '';
        if ($title === '') {
            $content = @file_get_contents(BLOG_ROOT . '/' . $file);
            if ($content && preg_match('/<h1[^>]*>([^<]+)<\/h1>/', $content, $tm)) {
                $title = trim($tm[1]);
            } else {
                $title = ucwords(str_replace('-', ' ', $slug));
            }
        }

        $new_cards .= "\n" . pid_render_blog_card([
            'slug' => $slug,
            'title' => $title,
            'excerpt' => $meta['description'] ?? '',
            'category' => $category,
            'image' => $image,
            'date_human' => $date_human,
        ]);
        $added++;
    }

    if ($added === 0) {
        return true; // page already current
    }

    $injection = rtrim($new_cards, "\n") . "\n\n        ";
    $updated = str_replace($end_marker, $injection . $end_marker, $html);
    if (file_put_contents($index_file, $updated) === false) {
        return false;
    }

    log_event('INDEX_CARDS_INJECTED', ['added' => $added]);
    return true;
}

function regenerate_sitemap() {
    $sitemap_file = dirname(BLOG_ROOT) . '/sitemap.xml';

    if (!file_exists($sitemap_file)) {
        return false;
    }

    $sitemap = @simplexml_load_file($sitemap_file);
    if ($sitemap === false) {
        return false;
    }

    $base_url = 'https://www.pleasureislanddesign.com/blog/';
    $blog_dir = BLOG_ROOT;

    // Get existing blog URLs
    $existing = [];
    foreach ($sitemap->url as $url) {
        $loc = (string)$url->loc;
        if (strpos($loc, '/blog/') !== false) {
            $existing[$loc] = true;
        }
    }

    // Add new posts
    $added = 0;
    $files = @scandir($blog_dir);
    if ($files === false) {
        return false;
    }

    foreach ($files as $file) {
        if (!preg_match('/^[a-z0-9\-]+\.html$/', $file)) {
            continue;
        }

        $loc = $base_url . $file;
        if (!isset($existing[$loc])) {
            $url = $sitemap->addChild('url');
            $url->addChild('loc', $loc);
            $url->addChild('lastmod', date('Y-m-d'));
            $url->addChild('changefreq', 'monthly');
            $url->addChild('priority', '0.7');
            $added++;
        }
    }

    if ($added > 0) {
        $sitemap->asXML($sitemap_file);
    }

    return true;
}

function log_event($event, $data = []) {
    $timestamp = date('Y-m-d H:i:s');
    $entry = "{$timestamp} | {$event} | " . json_encode($data) . "\n";
    @error_log($entry, 3, LOG_FILE);
}
?>
