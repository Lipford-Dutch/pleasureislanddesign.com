<?php
/**
 * Contact Form Handler
 *
 * Security measures actually implemented here:
 * - Origin-restricted CORS (only pleasureislanddesign.com)
 * - Rate limiting (3 submissions per hour per IP, temp-file backed)
 * - Input validation via shared lib (pid_validate_contact)
 * - Output sanitization (htmlspecialchars) before email body
 * - Email header-injection prevention (pid_sanitize_email_header)
 * - Request logging for debugging
 * - User-friendly error responses (no internal detail leaked)
 *
 * NOT implemented (by design / hosting constraints):
 * - CSRF tokens: site is static HTML with no server session; rate limiting
 *   + origin check are the mitigations instead.
 * - Mail authentication (SPF/DKIM): handled at the GoDaddy/DNS level, not here.
 *   See DELIVERABILITY note in BUGFIX_1.md before relying on inbox delivery.
 */

require_once __DIR__ . '/lib/form-helpers.php';

define('LOG_FILE', __DIR__ . '/../.logs/contact-form.log');
define('SUBMISSIONS_FILE', __DIR__ . '/../.data/contact-submissions.jsonl');
define('MAX_SUBMISSIONS_PER_HOUR', 3);
define('RATE_LIMIT_KEY_PREFIX', 'pid_contact_');
define('RECIPIENT_EMAIL', 'pleasureislanddesign@gmail.com');

// Ensure log + data directories exist
foreach ([dirname(LOG_FILE), dirname(SUBMISSIONS_FILE)] as $dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

// Set headers
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

// CORS - restrict to same origin for production
$allowed_origins = ['https://www.pleasureislanddesign.com', 'https://pleasureislanddesign.com'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Pre-flight request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    respond(['error' => 'Method not allowed'], 405);
}

// Parse input
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
    respond(['error' => 'Too many submissions. Please try again later.'], 429);
}

// --- VALIDATION ---
$validation_errors = pid_validate_contact($input);
if (!empty($validation_errors)) {
    respond(['errors' => $validation_errors], 400);
}

// --- SANITIZATION ---
$name = htmlspecialchars($input['name'] ?? '', ENT_QUOTES, 'UTF-8');
$email = filter_var($input['email'] ?? '', FILTER_SANITIZE_EMAIL);
$phone = htmlspecialchars($input['phone'] ?? '', ENT_QUOTES, 'UTF-8');
$service = htmlspecialchars($input['service'] ?? '', ENT_QUOTES, 'UTF-8');
$message = htmlspecialchars($input['message'] ?? '', ENT_QUOTES, 'UTF-8');

// --- PERSIST LEAD FIRST (durable capture, independent of mail delivery) ---
// On shared hosting mail() can return false even for valid submissions; capturing
// the lead to disk first guarantees we never silently drop a consultation request.
$lead_captured = record_contact_submission($name, $email, $phone, $service, $message);

// --- SEND EMAILS (best-effort) ---
$mail_sent = send_contact_emails($name, $email, $phone, $service, $message);

if ($lead_captured || $mail_sent) {
    log_event('CONTACT_FORM_SUBMITTED', [
        'email' => $email,
        'name' => $name,
        'mail_sent' => $mail_sent,
        'lead_captured' => $lead_captured
    ]);
    record_rate_limit($cache_file);
    respond([
        'success' => true,
        'message' => 'Thank you! We\'ll be in touch within 1-2 business days.'
    ], 200);
} else {
    log_event('CONTACT_FORM_FAILED', ['email' => $email, 'error' => 'Mail send and lead capture both failed']);
    respond([
        'error' => 'Unable to send message. Please call (910) 444-1230 or email directly.'
    ], 500);
}

// ===== HELPER FUNCTIONS =====

function respond($data, $code = 200) {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Durably append a consultation request to disk so leads survive mail() failures.
 * Returns true when the line was written.
 */
function record_contact_submission($name, $email, $phone, $service, $message) {
    $entry = [
        'name' => $name,
        'email' => $email,
        'phone' => $phone,
        'service' => $service,
        'message' => $message,
        'submitted_at' => date('Y-m-d H:i:s'),
        'ip' => pid_sanitize_ip($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1'),
    ];
    $line = json_encode($entry, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n";
    return @file_put_contents(SUBMISSIONS_FILE, $line, FILE_APPEND | LOCK_EX) !== false;
}

function send_contact_emails($name, $email, $phone, $service, $message) {
    $to = RECIPIENT_EMAIL;
    $subject = 'New Consultation Request from ' . $name;

    // Build professional email body
    $body = "=== NEW CONSULTATION REQUEST ===\n\n";
    $body .= "Name: {$name}\n";
    $body .= "Email: {$email}\n";
    $body .= "Phone: " . ($phone ?: 'Not provided') . "\n";
    $body .= "Service Interest: " . ($service ?: 'Not specified') . "\n";
    $body .= "\n--- MESSAGE ---\n";
    $body .= "{$message}\n";
    $body .= "\n--- SUBMISSION DETAILS ---\n";
    $body .= "Submitted from: {$_SERVER['HTTP_HOST']}\n";
    $body .= "IP Address: " . pid_sanitize_ip($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1') . "\n";
    $body .= "Date: " . date('Y-m-d H:i:s') . " UTC\n";
    $body .= "User Agent: " . substr($_SERVER['HTTP_USER_AGENT'] ?? 'Unknown', 0, 200) . "\n";

    // Prevent header injection
    $safe_email = pid_sanitize_email_header($email);
    $headers = "From: noreply@pleasureislanddesign.com\r\n";
    $headers .= "Reply-To: {$safe_email}\r\n";
    $headers .= "Return-Path: noreply@pleasureislanddesign.com\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send to business
    $business_sent = mail($to, $subject, $body, $headers);

    // Send confirmation to user
    if ($business_sent) {
        $confirm_subject = 'We Received Your Consultation Request';
        $confirm_body = "Hi {$name},\n\n";
        $confirm_body .= "Thank you for reaching out to Pleasure Island Design! We received your consultation request and will review your message shortly.\n\n";
        $confirm_body .= "We'll get back to you within 1-2 business days via email or phone.\n\n";
        $confirm_body .= "In the meantime, feel free to call us at (910) 444-1230 or visit our website.\n\n";
        $confirm_body .= "Best regards,\n";
        $confirm_body .= "The Pleasure Island Design Team\n";
        $confirm_body .= "https://www.pleasureislanddesign.com\n";

        $user_headers = "From: pleasureislanddesign@gmail.com\r\n";
        $user_headers .= "Return-Path: noreply@pleasureislanddesign.com\r\n";
        $user_headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

        mail($safe_email, $confirm_subject, $confirm_body, $user_headers);
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

    // Reset if older than 1 hour
    if ($now - $timestamp > 3600) {
        @unlink($cache_file);
        return false;
    }

    return $count >= MAX_SUBMISSIONS_PER_HOUR;
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
