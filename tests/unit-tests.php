<?php
/**
 * Unit Tests — exercises the REAL shared form-helpers library.
 *
 * Unlike the previous version, these tests `require` forms/lib/form-helpers.php
 * and call the exact same pid_* functions used in production. If the production
 * validation/sanitization logic changes, these tests change behaviour too.
 *
 * Run: php tests/unit-tests.php
 */

require_once __DIR__ . '/../forms/lib/form-helpers.php';

$passed = 0;
$failed = 0;

echo "========================================\n";
echo "PLEASURE ISLAND DESIGN - UNIT TESTS\n";
echo "(testing real forms/lib/form-helpers.php)\n";
echo "========================================\n\n";

// Sanity: confirm we actually loaded the production lib.
assert_true(function_exists('pid_validate_contact'), 'Production lib is loaded (pid_validate_contact exists)');
assert_true(defined('PID_FORM_HELPERS'), 'PID_FORM_HELPERS constant defined by lib');

echo "\n[SUITE] pid_validate_contact()\n" . str_repeat('-', 50) . "\n";

// Valid input
assert_equal(
    count(pid_validate_contact([
        'name' => 'John Doe', 'email' => 'john@example.com',
        'phone' => '(910) 444-1230', 'service' => 'refinishing',
        'message' => 'I would like to refinish my cabinets, please.'
    ])),
    0, 'Valid input passes with no errors'
);

// Missing fields
$errs = pid_validate_contact(['name' => 'John']);
assert_true(isset($errs['email']), 'Missing email is caught');
assert_true(isset($errs['message']), 'Missing message is caught');

// Invalid email
$errs = pid_validate_contact(['name' => 'John Doe', 'email' => 'not-an-email', 'message' => 'A valid length message.']);
assert_true(isset($errs['email']), 'Invalid email format is caught');

// Name boundaries
assert_true(isset(pid_validate_contact(['name' => 'J', 'email' => 'a@b.co', 'message' => 'Valid length message here.'])['name']), 'Name < 2 chars rejected');
assert_true(isset(pid_validate_contact(['name' => str_repeat('a', 101), 'email' => 'a@b.co', 'message' => 'Valid length message here.'])['name']), 'Name > 100 chars rejected');

// Message boundaries
assert_true(isset(pid_validate_contact(['name' => 'John Doe', 'email' => 'a@b.co', 'message' => 'short'])['message']), 'Message < 10 chars rejected');
assert_true(isset(pid_validate_contact(['name' => 'John Doe', 'email' => 'a@b.co', 'message' => str_repeat('a', 5001)])['message']), 'Message > 5000 chars rejected');

// Phone format
assert_true(isset(pid_validate_contact(['name' => 'John Doe', 'email' => 'a@b.co', 'message' => 'Valid length message here.', 'phone' => 'abc!!!'])['phone']), 'Garbage phone rejected');
assert_equal(count(pid_validate_contact(['name' => 'John Doe', 'email' => 'a@b.co', 'message' => 'Valid length message here.', 'phone' => '+1 (910) 444-1230'])), 0, 'Well-formed phone accepted');

echo "\n[SUITE] pid_validate_email()\n" . str_repeat('-', 50) . "\n";
assert_true(pid_validate_email('user@example.com'), 'Valid email returns true');
foreach (['not-an-email', '@example.com', 'user@', 'user @example.com', ''] as $bad) {
    assert_false(pid_validate_email($bad), "Invalid email '{$bad}' returns false");
}

echo "\n[SUITE] pid_sanitize_email_header() — injection prevention\n" . str_repeat('-', 50) . "\n";
$injected = "test@example.com\nBcc: attacker@example.com";
$clean = pid_sanitize_email_header($injected);
assert_false(strpos($clean, "\n") !== false, 'Newline stripped from email header');
assert_false(strpos($clean, "\r") !== false, 'Carriage return stripped from email header');

echo "\n[SUITE] pid_is_duplicate_email()\n" . str_repeat('-', 50) . "\n";
assert_true(pid_is_duplicate_email('Test@Example.com', ['other@x.com', 'test@example.com']), 'Duplicate detected case-insensitively');
assert_false(pid_is_duplicate_email('new@example.com', ['other@x.com', 'test@example.com']), 'Non-duplicate not flagged');
assert_false(pid_is_duplicate_email('a@b.com', []), 'Empty list never duplicates');

echo "\n[SUITE] pid_sanitize_ip()\n" . str_repeat('-', 50) . "\n";
assert_equal(pid_sanitize_ip('203.0.113.7'), '203.0.113.7', 'Valid IPv4 preserved');
assert_equal(pid_sanitize_ip('not-an-ip'), '127.0.0.1', 'Junk IP falls back to loopback');
assert_equal(pid_sanitize_ip('::1'), '::1', 'Valid IPv6 preserved');

echo "\n[SUITE] pid_sanitize_slug()\n" . str_repeat('-', 50) . "\n";
$cases = [
    'valid-slug' => 'valid-slug',
    'Invalid Slug!' => 'InvalidSlug',
    'slug-with-123' => 'slug-with-123',
    'slug<script>' => 'slugscript',
    '../../etc/passwd' => 'etcpasswd',
];
foreach ($cases as $in => $expected) {
    assert_equal(pid_sanitize_slug($in), $expected, "Slug '{$in}' sanitized correctly");
}

echo "\n[SUITE] pid_validate_post_html()\n" . str_repeat('-', 50) . "\n";
assert_true(pid_validate_post_html('<article><h1>Test Post</h1><p>Content</p></article>'), 'Well-formed post passes');
assert_false(pid_validate_post_html('<article><p>No heading here</p></article>'), 'Post without <h1> rejected');
assert_false(pid_validate_post_html('<article<h1>Broken bracket</h1>'), 'Unbalanced angle brackets rejected');

echo "\n[SUITE] pid_is_publishable_post()\n" . str_repeat('-', 50) . "\n";
$styled_body = str_repeat('Real cabinet refinishing copy that a reader would actually see. ', 8);
$styled_post = '<!DOCTYPE html><html><head><link rel="stylesheet" href="../styles.css"></head>'
    . '<body><article><h1>Real Post</h1><p>' . $styled_body . '</p></article></body></html>';
assert_true(pid_is_publishable_post($styled_post), 'Styled post with chrome + copy is publishable');
assert_false(pid_is_publishable_post('<html><body><article><h1>Stub</h1><p>Too short.</p></article></body></html>'), 'Bare stub (no stylesheet, thin copy) rejected');
$no_css = '<html><body><article><h1>No CSS</h1><p>' . $styled_body . '</p></article></body></html>';
assert_false(pid_is_publishable_post($no_css), 'Post without a stylesheet link rejected');
$thin = '<html><head><link rel="stylesheet" href="../styles.css"></head><body><article><h1>Thin</h1><p>Short body.</p></article></body></html>';
assert_false(pid_is_publishable_post($thin), 'Styled but too-thin post rejected');

echo "\n[SUITE] pid_render_blog_card()\n" . str_repeat('-', 50) . "\n";
$card = pid_render_blog_card([
    'slug' => 'my-post',
    'title' => 'My Post',
    'excerpt' => 'A short excerpt.',
    'category' => 'Design',
    'image' => '../gallery/x.jpg',
    'date_human' => 'July 1, 2026',
]);
assert_true(strpos($card, 'href="my-post.html"') !== false, 'Card links to the post slug');
assert_true(strpos($card, 'class="blog-card"') !== false, 'Card uses the blog-card component');
assert_true(strpos($card, 'July 1, 2026') !== false, 'Card shows the human date');
$xss = pid_render_blog_card(['slug' => 'x', 'title' => '<script>alert(1)</script>', 'excerpt' => 'e']);
assert_true(strpos($xss, '<script>alert(1)</script>') === false, 'Card escapes HTML in the title');
$badslug = pid_render_blog_card(['slug' => '../../etc/passwd', 'title' => 'T']);
assert_true(strpos($badslug, 'href="etcpasswd.html"') !== false, 'Card sanitizes the slug in the href');

// ===== RESULTS =====
echo "\n" . str_repeat('=', 50) . "\n";
echo "TEST RESULTS\n" . str_repeat('=', 50) . "\n";
echo "Passed: {$passed}\nFailed: {$failed}\nTotal: " . ($passed + $failed) . "\n\n";
echo $failed === 0 ? "✓ All tests passed!\n" : "✗ Some tests failed.\n";
exit($failed === 0 ? 0 : 1);

// ===== ASSERTIONS =====

function assert_equal($actual, $expected, $message) {
    global $passed, $failed;
    if ($actual === $expected) {
        echo "✓ {$message}\n"; $passed++;
    } else {
        echo "✗ {$message}\n  Expected: " . var_export($expected, true) . "\n  Actual:   " . var_export($actual, true) . "\n";
        $failed++;
    }
}

function assert_true($condition, $message) { assert_equal($condition === true, true, $message); }
function assert_false($condition, $message) { assert_equal($condition === false, true, $message); }
