# PID review-request package

> **Repo note (2026-11-19):** This document was written for the November 8, 2026 content package, before any code existed. The dry-run tooling in `../pid_reviews/` now implements the renderer, private ledger, eligibility rules, and approval-batch steps described here, and it still sends nothing. Templates are now `v1.1.0-2026-11-19`: same customer-facing copy, plus optional `{{#qr_block}}` and `{{#phone_block}}` sections that are removed unless their verified inputs exist. Wherever this text says "not implemented", read it as "no sending is implemented or authorized".

**Pleasure Island Design LLC (PID)**  
Reusable branded review-request email templates and operator documentation  
Prepared for Will Lipford  
Package date: November 8, 2026 (America/New_York)

These are marketing files and operating documents. They are not application code, not a repository change, and not permission to contact anyone.

Source research for branding, policy, and approved copy: `research-and-content-spec.md` (this folder) (checked November 8, 2026).

## What this package is

A reusable **template and process kit** for asking completed kitchen-cabinet homeowners whether they would like to leave an honest Google review:

- HTML and plain-text templates for one initial note and one optional later reminder
- A placeholder dictionary for future automation
- An eligibility, evidence, dedup, and tracking SOP, including a Gmail label **plan**
- A launch checklist
- A visual preview that is intentionally marked incomplete

Signature is static: **Nicole Rayment**, Pleasure Island Design. Mail is intended to come from **pleasureislanddesign@gmail.com** (proposed From display name: `Nicole Rayment | Pleasure Island Design`). The website `https://www.pleasureislanddesign.com/` is a real, clickable signature link. The review CTA in the production templates remains an unset placeholder, because a direct Google write-review URL has not been identity-verified. The signature includes the live website only; phone is omitted because a discrepancy across signature and draft sources is unresolved.

## What this package is not

- Not a live send implementation
- Not Gmail drafts, labels, scheduled mail, or test messages
- Not source code for a renderer, ledger, or worker, and not a git repository change (a separate repository step was blocked by a coding-service credits / model-setting error)
- Not a mailing list or the last 15 customers (see the Gmail audit result below; no customer evidence or PII is included and none were invented)
- Not authorization to send the initial message or the reminder
- Not a legal opinion

## Implemented vs planned

| Implemented in these files | Not implemented |
|---|---|
| Production HTML templates (`templates/*.html`) with PID branding, live text, fallback greeting rule, CTA placeholder, visible URL line, static Nicole signature, website link, opt-out, and postal placeholder | Any mail merge, Gmail API sender, or scheduling job |
| Matching UTF-8 plain-text parts (`templates/*.txt`) | MIME assembly or actual outbound mail |
| Commented optional QR hook, disabled on purpose | A QR image (none generated; the write-review URL is unverified) |
| Placeholder dictionary and validation rules | A renderer that substitutes and escapes fields |
| Eligibility / tracking SOP and launch checklist | A private ledger application, mailbox watcher, or applied Gmail labels |
| Incomplete visual preview (HTML + PDF) | Customer-populated previews or sample review links that would look usable |
| Label **plan** only | Label creation or application |

## Practical launch blockers

1. **Direct Google write-review URL is not identity-verified — deployment gate preserved.** The public homepage still points at a Google *search* URL (`https://www.google.com/search?q=Pleasure+Island+Design+Wilmington+NC`), which must not be used as the review CTA. A later public check on November 8, 2026 (America/New_York), documented in the private link-verification supplement (kept off-repo on purpose; it lists candidate identifiers that must not be used), resolved a genuine PID Maps listing but found conflicting Maps feature identifiers between that listing and a place ID published on a third-party Birdeye profile. A write-review composer route was not confirmed to name the current PID profile after sign-in. **Do not use any discovered place ID, Maps place link, short link, search URL, or third-party profile link as the CTA. Do not generate a QR from any of those values.** Keep `{{google_review_url}}` unset until an authoritative Google Business Profile “Get more reviews” link is tested on desktop and mobile against PID’s name, website, and location, with verifier and date recorded.
2. **`{{business_postal_address}}` is not owner-confirmed.** A public site or directory address must not be copied into the footer automatically.
3. **Gmail eligibility audit produced HOLDs, not a mailing list.** A private Gmail workstream inspected 22 invoice PDFs and all identified candidate threads and search pages. It found eight kitchen projects and **zero independently verified completions**. The original 15 recipient leads are all on HOLD. Invoice or payment alone is not completion. This package includes no customer names, mailboxes, invoice contents, or other evidence/PII, and none were invented. Uncertainty stays held. Fewer than 15 eligible households would have been acceptable if any had cleared the evidence bar.
4. **Phone is omitted on purpose.** A phone-number discrepancy across signature and draft sources is unresolved. Templates and this preview do not include a phone number and should not gain one until that conflict is resolved.
5. **No reminder is authorized now.** At most one reminder, 10–14 days after a confirmed initial send, and only with a fresh human approval if there has been no reply, opt-out, known review, bounce, or service hold. Historical completions older than 90 days need manual review and have no default reminder.
6. **Ledger, suppression list, authenticated-send check, opt-out monitoring, lawful-contact review, and per-batch approval** are still required before any send. Template changes or expired approvals invalidate approval.

## File inventory

| Path | Purpose |
|---|---|
| `README.md` | This file |
| `eligibility-and-tracking-SOP.md` | How to find, evidence-audit, deduplicate, hold, approve, and track without spamming or misidentifying people |
| `placeholders.md` | Merge-field dictionary, greeting rule, URL/QR rules, runtime fields that must stay private |
| `launch-checklist.md` | Pre-send gates and QA |
| `templates/review-request-initial.html` | Production initial HTML template (600px, placeholders intact) |
| `templates/review-request-initial.txt` | Production initial plain text |
| `templates/review-request-reminder.html` | Production reminder HTML template |
| `templates/review-request-reminder.txt` | Production reminder plain text |
| `preview/content-preview.html` | Printable visual preview, marked incomplete |
| `preview/content-preview.pdf` | Concise PDF of that preview |
| `preview/assets/pid-logo-v2-header.png` | Local copy of the live public logo, used only so the preview can render offline |

Production templates reference the live logo at `https://www.pleasureislanddesign.com/img/pid-logo-v2-header.png`.

## Branding applied

- Business: Pleasure Island Design (kitchen cabinet refinishing; Wilmington / coastal NC)
- Homepage: `https://www.pleasureislanddesign.com/`
- Logo: live `pid-logo-v2-header.png`, placed on a navy header band because that production asset is a light-on-dark mark
- Navy `#1E3A5F`, cream `#F9F6F1`, charcoal text `#1C1C1E`, gold `#C4973B` and sage `#7DA69E` as decorative accents only
- Headings Georgia (brand Playfair Display as progressive enhancement only; email does not depend on webfonts); body Arial
- No unsupported ratings, review counts, awards, or Nicole job titles
- No phone number in the signature or footer

## Copy and compliance posture

The templates use the approved-for-review wording from the research specification: warm, optional, and neutral. All sentiments are equally welcome. There are no incentives, review funnels, star prompts, suggested review text, or sales offers.

The body reads as a note from Nicole, not a heavy solicitation. The footer identifies the message as an optional customer review solicitation, reserves space for the owner-confirmed postal address, and tells people they can stop all PID marketing emails, including review requests, by replying “unsubscribe.”

New initials default to 7–14 days after the later of independently verified completion and final invoice issuance.

## Preview vs production

Open the files in `templates/` when preparing a future send. They still contain `{{google_review_url}}` and `{{business_postal_address}}` on purpose.

Open `preview/content-preview.html` or `preview/content-preview.pdf` only to judge layout and tone. That preview:

- Uses the generic greeting `Hello,` (no invented customer names)
- Replaces the review URL with a visible “unverified — launch blocker” marker, not a clickable stand-in
- Replaces the postal address with an owner-confirmation marker
- Does **not** include a QR code
- Is watermarked as an incomplete preview that must not be sent

## How a future operator would use the templates

1. Clear every blocker on `launch-checklist.md` using the process in `eligibility-and-tracking-SOP.md`.
2. Keep customer data in the private ledger only.
3. Substitute placeholders according to `placeholders.md` (greeting fallback, HTML escaping, URL allowlist).
4. Send as UTF-8 `multipart/alternative` from the authenticated Gmail account, one recipient in `To:` at a time, after an explicit unexpired batch approval.
5. Do not enable the commented QR block unless the review URL is verified and a locally generated QR decodes to that exact URL.

Until then, do not send, draft to customers, apply labels, or schedule anything from these files.
