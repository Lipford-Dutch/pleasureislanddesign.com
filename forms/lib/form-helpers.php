<?php
/**
 * Shared Form Helpers (pure, side-effect-free)
 *
 * These functions contain ALL validation/sanitization logic used by the
 * form handlers. They perform no I/O, set no headers, and never exit — so
 * the unit tests can call the exact same code that runs in production.
 *
 * Used by:
 *   - forms/contact.php
 *   - forms/newsletter.php
 *   - blog/publish-scheduled.php
 *   - tests/unit-tests.php
 */

if (!defined('PID_FORM_HELPERS')) {
    define('PID_FORM_HELPERS', '1.0');

    /**
     * Validate a contact-form payload. Returns a map of field => error message.
     * An empty array means the input is valid.
     */
    function pid_validate_contact(array $input): array {
        $errors = [];
        $name = trim($input['name'] ?? '');
        $email = trim($input['email'] ?? '');
        $message = trim($input['message'] ?? '');

        if (strlen($name) < 2 || strlen($name) > 100) {
            $errors['name'] = 'Name must be 2-100 characters';
        }
        if (strlen($email) < 5 || strlen($email) > 255) {
            $errors['email'] = 'Invalid email address';
        } elseif (!pid_validate_email($email)) {
            $errors['email'] = 'Invalid email format';
        }
        if (strlen($message) < 10 || strlen($message) > 5000) {
            $errors['message'] = 'Message must be 10-5000 characters';
        }

        $phone = trim($input['phone'] ?? '');
        if ($phone !== '' && !preg_match('/^[\d\s\-\+\(\)\.]+$/', $phone)) {
            $errors['phone'] = 'Invalid phone number format';
        }

        return $errors;
    }

    /** True when the string is a syntactically valid email address. */
    function pid_validate_email(string $email): bool {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }

    /**
     * Strip header-injection vectors (newlines, etc.) from an email address.
     * Returns the sanitized address safe to place in a mail header.
     */
    function pid_sanitize_email_header(string $email): string {
        $clean = filter_var($email, FILTER_SANITIZE_EMAIL);
        // FILTER_SANITIZE_EMAIL already removes \r and \n, but be explicit.
        return str_replace(["\r", "\n", "%0a", "%0d"], '', $clean);
    }

    /** Case-insensitive duplicate check against a list of existing emails. */
    function pid_is_duplicate_email(string $email, array $existing): bool {
        $needle = strtolower(trim($email));
        foreach ($existing as $candidate) {
            if (strtolower(trim((string)$candidate)) === $needle) {
                return true;
            }
        }
        return false;
    }

    /** Return a valid IP or the loopback fallback. Never returns junk. */
    function pid_sanitize_ip(string $ip): string {
        return filter_var($ip, FILTER_VALIDATE_IP) ? $ip : '127.0.0.1';
    }

    /** Reduce a slug to [a-z0-9-] so it can never escape the blog directory. */
    function pid_sanitize_slug(string $slug): string {
        return preg_replace('/[^a-z0-9\-]/i', '', $slug);
    }

    /**
     * Lightweight structural check for a blog post body:
     * must contain an <h1> and have balanced angle brackets.
     */
    function pid_validate_post_html(string $content): bool {
        if (!preg_match('/<h1[^>]*>/', $content)) {
            return false;
        }
        if (substr_count($content, '<') !== substr_count($content, '>')) {
            return false;
        }
        return true;
    }

    /**
     * True when a draft is a fully-built page rather than a bare stub — i.e. it
     * carries the site chrome (a stylesheet link) and real body copy. Prevents
     * the scheduler from silently publishing an unstyled placeholder.
     */
    function pid_is_publishable_post(string $content): bool {
        if (!pid_validate_post_html($content)) {
            return false;
        }
        // Must link the site stylesheet (relative or absolute) — stubs don't.
        if (!preg_match('/<link[^>]+rel=["\']stylesheet["\']/i', $content)
            && !preg_match('/styles\.css/i', $content)) {
            return false;
        }
        // Must have a meaningful amount of visible copy.
        $text = trim(preg_replace('/\s+/', ' ', strip_tags($content)));
        return strlen($text) >= 400;
    }

    /**
     * Render a single blog index card (pure — no I/O). $meta keys:
     *   slug, title, excerpt, category, image, date_human
     * All values are HTML-escaped here, so callers pass raw strings.
     */
    function pid_render_blog_card(array $meta): string {
        $slug     = pid_sanitize_slug($meta['slug'] ?? '');
        $title    = htmlspecialchars(trim($meta['title'] ?? 'Untitled'), ENT_QUOTES, 'UTF-8');
        $excerpt  = htmlspecialchars(trim($meta['excerpt'] ?? ''), ENT_QUOTES, 'UTF-8');
        $category = htmlspecialchars(trim($meta['category'] ?? 'Blog'), ENT_QUOTES, 'UTF-8');
        $image    = htmlspecialchars(trim($meta['image'] ?? '../gallery/motts-landing-2023/after-1.jpg'), ENT_QUOTES, 'UTF-8');
        $date     = htmlspecialchars(trim($meta['date_human'] ?? ''), ENT_QUOTES, 'UTF-8');

        return "        <!-- Auto-published: {$slug} -->\n"
            . "        <article class=\"blog-card\">\n"
            . "          <div class=\"blog-card-img\">\n"
            . "            <img src=\"{$image}\" alt=\"{$title} — Pleasure Island Design\" loading=\"lazy\" width=\"800\" height=\"500\">\n"
            . "            <span class=\"blog-card-category\">{$category}</span>\n"
            . "          </div>\n"
            . "          <div class=\"blog-card-body\">\n"
            . "            <p class=\"blog-card-date\">{$date}</p>\n"
            . "            <h2 class=\"blog-card-title\">{$title}</h2>\n"
            . "            <p class=\"blog-card-excerpt\">{$excerpt}</p>\n"
            . "            <a href=\"{$slug}.html\" class=\"blog-card-link\" aria-label=\"Read: {$title}\">Read More →</a>\n"
            . "          </div>\n"
            . "        </article>\n";
    }
}
