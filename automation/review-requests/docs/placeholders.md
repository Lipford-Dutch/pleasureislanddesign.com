# PID review-request placeholder dictionary

> **Repo note (2026-11-19):** This document was written for the November 8, 2026 content package, before any code existed. The dry-run tooling in `../pid_reviews/` now implements the renderer, private ledger, eligibility rules, and approval-batch steps described here, and it still sends nothing. Templates are now `v1.1.0-2026-11-19`: same customer-facing copy, plus optional `{{#qr_block}}` and `{{#phone_block}}` sections that are removed unless their verified inputs exist. Wherever this text says "not implemented", read it as "no sending is implemented or authorized".

Template versions covered:

- `pid-review-initial-v1.0.0-2026-11-08`
- `pid-review-reminder-v1.0.0-2026-11-08`

Status: documentation for future rendering only. This package does not implement a renderer, sender, or mail merge. Never leave unsubstituted `{{...}}` tokens in a message that leaves dry-run mode. Never interpolate raw values into HTML, headers, URLs, or queries.

Copy in the templates is approved for review, not approved to send.

## 1. Fields that appear in the customer-facing email

| Placeholder | Required? | Current status | Type / handling | Notes |
|---|---|---|---|---|
| `{{first_name}}` | Optional | Ready as a field | Preferred first name only after human verification. Strip control characters. HTML-escape for HTML. Never guess. | If absent or blank after sanitization, replace the **entire greeting** `Hi {{first_name}},` with `Hello,`. Never render `Hi ,`. |
| `{{google_review_url}}` | Required | **BLOCKED — not verified** | Absolute HTTPS Google-hosted write-review URL or official short link whose redirects have been tested to the correct PID review composer. Allowlist the exact verified URL. Attribute-escape only after validation. No `javascript:` or `data:` schemes, no arbitrary URLs, no tracking query parameters. | **Launch blocker.** The public homepage Google link is only a search URL and must not be substituted. Do not invent a Place ID or sample review URL. Used as the CTA `href` and as the visible selectable URL under the button. |
| `{{business_postal_address}}` | Required | **BLOCKED — owner confirmation outstanding** | Valid physical postal address for the sender, HTML-escaped. Controlled line breaks supplied by the renderer (`<br>` in HTML; real newlines in plain text). | **Launch blocker.** Do not copy a website, schema, or directory address automatically. A displayed public address is not confirmation that mail is received there. |
| `{{qr_image_url}}` | Optional; omitted by default | **Must stay unused** until the review URL is verified | HTTPS PID-owned static image or tested CID attachment generated from the same verified review URL. Validate then attribute-escape. | Present only inside a commented block in the HTML templates. Do not generate a QR from an unverified, search, or sample URL. QR is never the sole path to review. |

## 2. Static values already in the templates (do not placeholder)

These are live text, not merge fields:

| Item | Value |
|---|---|
| Sender mailbox | `pleasureislanddesign@gmail.com` |
| Proposed From display name | `Nicole Rayment \| Pleasure Island Design` |
| Reply-To | `pleasureislanddesign@gmail.com` |
| Signature name | Nicole Rayment (static; no title) |
| Business name | Pleasure Island Design |
| Website (clickable in HTML and present in plain text) | `https://www.pleasureislanddesign.com/` |
| Logo asset | `https://www.pleasureislanddesign.com/img/pid-logo-v2-header.png` |
| Initial subject | An optional review of your PID kitchen cabinet project |
| Initial preheader | Your honest experience can help other homeowners. No obligation. |
| Reminder subject | One optional reminder: your PID project review |
| Reminder preheader | No need to respond; this is our last review reminder. |
| CTA label | Share an honest Google review |
| Opt-out instruction | Reply “unsubscribe.” |
| Commercial identification | Optional customer review solicitation from Pleasure Island Design. |

Do not add unsupported ratings, review counts, awards, or a job title for Nicole. Do not add sales, offers, referral rewards, or suggested review wording. Do not add a phone number: a discrepancy across signature and draft sources is unresolved, so phone stays omitted.

## 3. Runtime / ledger fields that must never appear in the email

These belong in the private authoritative ledger (planned; not implemented in this package). They are required for a safe future send process. Do not print them in templates, public files, URLs, or git.

| Field | Required when | Handling |
|---|---|---|
| `recipient_email` | Every intended send | One valid mailbox; no CR/LF; no header injection. Prior-customer evidence required. Never CC/BCC a cohort. Never stored in this package. |
| `household_id` | Every candidate | Opaque internal identifier. Not derived as plaintext from an email or street address in shared files. |
| `project_id` | Every candidate | Opaque internal identifier for the kitchen cabinet project. |
| `request_id` | Every request attempt | Opaque identifier for one outreach attempt (initial or reminder). |
| `batch_id` | Every approved batch | Opaque identifier for the exact human-approved set of messages. |
| `completion_date` | Eligibility | Independently documented completion timestamp. Unknown date is ambiguous and fails closed. Operator reports use America/New_York; storage may use ISO UTC. |
| `invoice_id` | Eligibility | Issued **final** invoice reference. Invoice issued is not completion. Payment alone is not completion. |
| `evidence_refs` | Eligibility | Pointers to independent completion proof and invoice proof for the **same** household/project. Store privately. |
| `template_version` | Approval and send | Exact string from the template header. Changing a template invalidates existing approvals. |
| `approval_id` | Before any send | Bounded to one exact batch. |
| `approved_at` | Before any send | Trusted clock. |
| `approval_expires_at` | Before any send | Expiry invalidates the approval. |
| `sent_message_id` | After provider acceptance | Provider message/thread IDs. Acceptance is not proof of delivery. |
| `sent_at` | After a recorded send | Trusted clock; convert to America/New_York for operator reports. |
| `suppression_reason` | When suppressed | Typed reason (opt-out, bounce, known review, reply, service hold, ambiguity, etc.). |
| `logo_url` | If a future renderer injects the logo instead of using the baked-in asset | Must remain the approved HTTPS production PNG above. |

## 4. Greeting rule

| `first_name` after sanitization | Rendered greeting |
|---|---|
| Present (example shape only: a verified given name) | `Hi {first_name},` |
| Missing, blank, or untrusted | `Hello,` |

Do not invent names for previews. The visual preview in this package uses the generic fallback `Hello,`.

## 5. Review URL and QR rules

1. Owner supplies the Google Business Profile “Get more reviews” write-review link or official QR destination, or further verification resolves identity without guessing.
2. A human tests it on desktop and mobile, confirms it is Pleasure Island Design using name, website, and location (not an unresolved phone value), and confirms it opens the review composer (Google sign-in may appear). Record the exact URL, verification date, and verifier in the private ledger.
3. Until that happens, production templates keep `{{google_review_url}}` as an unsubstituted required placeholder, and the preview must show an incomplete marker instead of a clickable stand-in. Never invent a URL to “complete” a template.
4. Homepage search URL `https://www.google.com/search?q=Pleasure+Island+Design+Wilmington+NC` is **not** a valid value.
5. A November 8, 2026 public verification supplement found a genuine PID Maps listing but conflicting Maps feature identifiers versus a place ID published on a third-party Birdeye profile. Composer identity after sign-in was not verified. **Do not insert any discovered place ID, write-review URL, Maps place link, short link, or third-party profile link into `{{google_review_url}}`.** See the private link-verification supplement (kept off-repo on purpose; it lists candidate identifiers that must not be used) for the research trail; do not copy candidate IDs from it into deployable configuration.
6. If a QR is added later: generate it locally from the *verified* URL only; black on white; quiet zone of at least four modules; about 160–200px; no logo overlay; scan-test that the decoded URL equals the CTA URL; alt text `Scan to open Pleasure Island Design’s Google review page`; caption `Prefer your phone? Scan this code.` Same-device readers still need the button and visible URL. **No QR may be generated from an unverified or conflicting identifier.**

## 6. Dry-run fixture shape (synthetic only)

Use empty or opaque values. Do not populate real customers.

```
first_name:                <empty → greeting becomes Hello,>
google_review_url:         <UNRESOLVED launch blocker>
business_postal_address:   <UNRESOLVED launch blocker>
qr_image_url:              <omit>
recipient_email:           <private runtime only>
household_id:              HH-UNASSIGNED
project_id:                PRJ-UNASSIGNED
request_id:                REQ-UNASSIGNED
batch_id:                  BATCH-UNASSIGNED
template_version:          pid-review-initial-v1.0.0-2026-11-08
```

## 7. MIME assembly note (planned, not implemented)

A future sender should send `multipart/alternative` UTF-8 mail: the matching `.txt` part plus the matching `.html` part. Plain text uses `Share an honest Google review:` followed by the URL on its own line. HTML uses the navy button plus the same URL as live underlined text underneath. No tracking pixel part. Native authenticated Gmail sending only for `pleasureislanddesign@gmail.com`; do not spoof this From address through another provider.
