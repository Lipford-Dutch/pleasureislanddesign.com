<?php
/**
 * Newsletter Signup Handler (Production-Ready)
 *
 * Security & Best Practices:
 * - Rate limiting (5 signups per hour per IP)
 * - Duplicate prevention (email deduplication)
 * - Input validation & sanitization
 * - Secure email headers
 * - Request logging
 * - Error handling
 */

require_once __DIR__ . '/lib/form-helpers.php';

define('LOG_FILE', __DIR__ . '/../.logs/newsletter.log');
define('SUBSCRIBERS_FILE', __DIR__ . '/../.data/newsletter-subscribers.jsonl');
define('MAX_SIGNUPS_PER_HOUR', 5);
define('RATE_LIMIT_KEY_PREFIX', 'pid_newsletter_');
define('RECIPIENT_EMAIL', 'pleasureislanddesign@gmail.com');

// Ensure directories exist
foreach ([dirname(LOG_FILE), dirname(SUBSCRIBERS_FILE)] as $dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

// Set headers
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// CORS
$allowed_origins = ['https://www.pleasureislanddesign.com', 'https://pleasureislanddesign.com'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Pre-flight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    respond(['error' => 'Method not allowed'], 405);
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    respond(['error' => 'Invalid JSON'], 400);
}

// --- RATE LIMITING ---
$ip = pid_sanitize_ip($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1');
$rate_limit_key = RATE_LIMIT_KEY_PREFIX . $ip;
$cache_file = sys_get_temp_dir() . '/' . md5($rate_limit_key) . '.tmp';

if (check_rate_limit($cache_file)) {
    log_event('RATE_LIMIT_EXCEEDED', ['ip' => $ip]);
    respond(['error' => 'Too many signup attempts. Please try again later.'], 429);
}

// --- VALIDATION ---
$email = trim($input['email'] ?? '');

if (strlen($email) < 5 || strlen($email) > 255) {
    respond(['error' => 'Invalid email address'], 400);
}

if (!pid_validate_email($email)) {
    respond(['error' => 'Please enter a valid email address'], 400);
}

$email = pid_sanitize_email_header($email);

// --- DUPLICATE CHECK ---
if (is_duplicate_subscriber($email)) {
    log_event('DUPLICATE_SIGNUP', ['email' => $email]);
    respond([
        'success' => true,
        'message' => 'You\'re already subscribed! Thanks for your interest.'
    ], 200);
}

// --- RECORD SUBSCRIBER FIRST (durable capture, independent of mail delivery) ---
// The point of a signup is capturing the address; the notification email is secondary.
// On shared hosting mail() can return false for valid input, so success must not
// depend on it — otherwise we'd reject and lose a legitimate subscriber.
$recorded = record_subscriber($email);

// --- SEND EMAILS (best-effort) ---
$mail_sent = send_newsletter_emails($email);

if ($recorded || $mail_sent) {
    log_event('NEWSLETTER_SIGNUP', ['email' => $email, 'mail_sent' => $mail_sent, 'recorded' => $recorded]);
    record_rate_limit($cache_file);
    respond([
        'success' => true,
        'message' => 'You\'re subscribed! Welcome to the community.'
    ], 200);
} else {
    log_event('NEWSLETTER_SIGNUP_FAILED', ['email' => $email]);
    respond([
        'error' => 'Subscription failed. Please try again or email us directly.'
    ], 500);
}

// ===== HELPER FUNCTIONS =====

function respond($data, $code = 200) {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function is_duplicate_subscriber($email) {
    if (!file_exists(SUBSCRIBERS_FILE)) {
        return false;
    }

    $file = fopen(SUBSCRIBERS_FILE, 'r');
    while (($line = fgets($file)) !== false) {
        $data = json_decode($line, true);
        if ($data && pid_is_duplicate_email($email, [$data['email'] ?? ''])) {
            fclose($file);
            return true;
        }
    }
    fclose($file);
    return false;
}

function record_subscriber($email) {
    $entry = [
        'email' => $email,
        'subscribed_at' => date('Y-m-d H:i:s'),
        'ip' => pid_sanitize_ip($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1'),
        'user_agent' => substr($_SERVER['HTTP_USER_AGENT'] ?? 'Unknown', 0, 200)
    ];
    $line = json_encode($entry) . "\n";
    return @file_put_contents(SUBSCRIBERS_FILE, $line, FILE_APPEND | LOCK_EX) !== false;
}

function send_newsletter_emails($email) {
    // Email to business (notification)
    $to = RECIPIENT_EMAIL;
    $subject = 'New Newsletter Subscriber';
    $body = "New newsletter signup:\n\n";
    $body .= "Email: {$email}\n";
    $body .= "Timestamp: " . date('Y-m-d H:i:s') . " UTC\n";
    $body .= "IP: " . pid_sanitize_ip($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1') . "\n";

    $headers = "From: noreply@pleasureislanddesign.com\r\n";
    $headers .= "Return-Path: noreply@pleasureislanddesign.com\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    $business_sent = mail($to, $subject, $body, $headers);

    // Welcome email to subscriber
    if ($business_sent) {
        $welcome_subject = 'Welcome to Pleasure Island Design!';
        $welcome_body = "Hi there,\n\n";
        $welcome_body .= "Thank you for subscribing to our newsletter! You'll now receive updates about:\n\n";
        $welcome_body .= "• Cabinet refinishing tips & techniques\n";
        $welcome_body .= "• Design trends & style inspiration\n";
        $welcome_body .= "• Maintenance guides & care tips\n";
        $welcome_body .= "• Special promotions & exclusive offers\n\n";
        $welcome_body .= "We send newsletters 1-2 times per month, so you'll stay informed without being overwhelmed.\n\n";
        $welcome_body .= "Questions? Just reply to this email or visit our website.\n\n";
        $welcome_body .= "Best regards,\n";
        $welcome_body .= "Pleasure Island Design\n";
        $welcome_body .= "https://www.pleasureislanddesign.com\n";
        $welcome_body .= "(910) 444-1230\n";

        $user_headers = "From: pleasureislanddesign@gmail.com\r\n";
        $user_headers .= "Return-Path: noreply@pleasureislanddesign.com\r\n";
        $user_headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

        mail($email, $welcome_subject, $welcome_body, $user_headers);
    }

    return $business_sent;
}

function check_rate_limit($cache_file) {
    if (!file_exists($cache_file)) {
        return false;
    }

    $data = json_decode(file_get_contents($cache_file), true);
    $count = $data['count'] ?? 0;
    $timestamp = $data['timestamp'] ?? 0;
    $now = time();

    if ($now - $timestamp > 3600) {
        @unlink($cache_file);
        return false;
    }

    return $count >= MAX_SIGNUPS_PER_HOUR;
}

function record_rate_limit($cache_file) {
    $data = file_exists($cache_file) ? json_decode(file_get_contents($cache_file), true) : [];
    $data['count'] = ($data['count'] ?? 0) + 1;
    $data['timestamp'] = $data['timestamp'] ?? time();
    file_put_contents($cache_file, json_encode($data));
}

function log_event($event, $data = []) {
    $timestamp = date('Y-m-d H:i:s');
    $entry = "{$timestamp} | {$event} | " . json_encode($data) . "\n";
    @error_log($entry, 3, LOG_FILE);
}
?>
