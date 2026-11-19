# PID review-request launch checklist

> **Repo note (2026-11-19):** This document was written for the November 8, 2026 content package, before any code existed. The dry-run tooling in `../pid_reviews/` now implements the renderer, private ledger, eligibility rules, and approval-batch steps described here, and it still sends nothing. Templates are now `v1.1.0-2026-11-19`: same customer-facing copy, plus optional `{{#qr_block}}` and `{{#phone_block}}` sections that are removed unless their verified inputs exist. Wherever this text says "not implemented", read it as "no sending is implemented or authorized".

Date of this checklist: November 8, 2026 (America/New_York).

This is an operator checklist for a future send program. Completing documentation in this package does **not** authorize sending, scheduling, labeling, drafting, or test mail.

Treat this program as a commercial email solicitation unless counsel later documents a different classification. This file is operational guidance, not a legal opinion.

## A. Absolute launch blockers (none of these are cleared)

Do not send, draft to a customer, or schedule anything until every item below is true.

- [ ] Owner has supplied the Google Business Profile write-review URL (Get more reviews / official short link), not a Google search URL, Maps place link, or discovered place ID.
- [ ] A named human has tested that URL on desktop and mobile, confirmed it is Pleasure Island Design using name, website, and location, and confirmed the review composer names the current PID profile (Google sign-in may intervene). Verification date and verifier are recorded. Unresolved phone values are not used as identity proof.
- [ ] `{{google_review_url}}` in both HTML and plain-text templates is replaced only with that allowlisted URL. The homepage search link was not substituted. No discovered Maps feature ID or third-party Birdeye-published place ID was used. Status on November 8, 2026 (America/New_York): public verification found conflicting identifiers; composer identity remains unverified; this box stays unchecked.
- [ ] No QR has been generated from an unverified, search, Maps-place, or conflicting-identifier URL. If a QR will later be used, it was generated locally from the verified URL, scan-tested to the exact CTA destination, and is secondary to the button and visible link. Status: no QR exists in this package, and none should be created until the URL gate clears.
- [ ] Owner has confirmed `{{business_postal_address}}` as a valid physical mailing address. A public website or directory address was not copied automatically.
- [ ] A private verified candidate list exists, with independent completion evidence and final-invoice evidence for each household/project. Payment or an invoice alone was not treated as completion. Status on November 8, 2026 (America/New_York): private Gmail audit inspected 22 invoice PDFs and all identified candidate threads/search pages; eight kitchen projects found; **zero independently verified completions**; the original 15 recipient leads are all HOLD. That set is not a mailing list. No customer evidence or PII is in this package.
- [ ] Each recipient is a homeowner / non-contractor kitchen cabinet customer. Contractors, leads, and guessed matches were not used to fill a quota. Fewer than 15 names is acceptable; a zero-length approved list is the correct current outcome.
- [ ] Historical records more than 90 days after completion have been manually reconfirmed (recipient, completion, prior contact, review history, appropriateness). They have **no default reminder**.
- [ ] Lawful-contact / recipient-expectation review is complete for this commercial message.
- [ ] Sender identity is the authenticated `pleasureislanddesign@gmail.com` mailbox. From display name proposed: `Nicole Rayment | Pleasure Island Design`. Reply-To is the same monitored mailbox. Gmail is not being spoofed through another provider.
- [ ] A private authoritative ledger and global marketing-suppression list exist and are available. Gmail labels, if any are later created, are convenience views only.
- [ ] Reply / unsubscribe monitoring is in place and understood (reply “unsubscribe.” honors a request to stop all PID marketing emails, including review requests). Immediate suppression before any further marketing send.
- [ ] Final content, accessibility, and client rendering QA is complete on the exact MIME that would be sent.
- [ ] An explicit human approval exists for the exact batch (see section E). Template or URL changes, or approval expiry, invalidate that approval.
- [ ] No reminder batch is implied by an initial-batch approval. **No reminder is authorized now.**

## B. Eligibility recap (every recipient)

Confirm all of the following for each person before they can appear on an approval list:

- [ ] Homeowner or other non-contractor customer (not a trade partner acting as contractor).
- [ ] Project scope is kitchen cabinets / kitchen cabinet refinishing.
- [ ] Completion is independently documented (dated walkthrough or sign-off, explicit installation-finished confirmation, or a staff completion record a human has verified).
- [ ] A final invoice was actually issued for that same project.
- [ ] Invoice issued ≠ work complete. Invoice paid ≠ work complete.
- [ ] Evidence is linked to the same household and project.
- [ ] Cancellations, open installs, punch lists, and mismatched invoice scopes were cross-checked.
- [ ] No screening by perceived happiness, likely star rating, neighborhood, or invoice value. All sentiments are equally welcome.
- [ ] Uncertainty of any required fact = hold / quarantine, not a send.

## C. Dedup, suppression, and mailbox preflight

Immediately before approving or sending, for each recipient:

- [ ] Authoritative ledger checked for a prior initial or reminder on this household/project.
- [ ] Mailbox history searched across relevant threads and aliases for prior review requests, replies, unsubscribes, bounces, known reviews, and open service cases.
- [ ] Global marketing opt-out list checked. An opt-out, spam complaint, or hard bounce suppresses immediately and cannot be overridden by batch approval without verified later consent where lawful.
- [ ] Any reply after a request stops automatic reminders. Out-of-office pauses rather than triggering repeats.
- [ ] Known review of any rating, or a customer saying they already reviewed, suppresses the request or reminder. Ambiguous public-name matches pause for a human. Never demand a screenshot.
- [ ] Genuine unresolved service / punch-list cases are on a temporary service hold, reviewed at least weekly, and are not a permanent “likely unhappy” exclusion. Support, refunds, or case closure are never conditioned on a review.
- [ ] Soft bounce, rate-limit, or delivery uncertainty: pause and reconcile; no automatic reminder or alternate-address retry.
- [ ] Unknown prior-send outcome: reconcile the Sent mailbox before any retry; if still unknown, fail closed. Do not blind-resend.
- [ ] One To: address only. Never CC/BCC the cohort.

## D. Template and accessibility QA (exact files in `templates/`)

- [ ] HTML and matching plain-text parts are used together (`multipart/alternative`, UTF-8).
- [ ] Template version strings still match the approved versions. Any edit creates a new version and voids prior approvals.
- [ ] Logo loads from `https://www.pleasureislanddesign.com/img/pid-logo-v2-header.png` and remains understandable with images off (live text remains).
- [ ] Navy `#1E3A5F` CTA with white text; cream outer `#F9F6F1`; body text `#1C1C1E`; Georgia headings / Arial body fallbacks.
- [ ] One-column layout, 600px maximum inner width, readable at 320px width and at 200% zoom.
- [ ] CTA is at least 44px tall, full width on small screens, and not an image button.
- [ ] The same review URL is visible as selectable underlined text under the button and wraps safely.
- [ ] Signature includes Nicole Rayment, Pleasure Island Design, the live website link, and `pleasureislanddesign@gmail.com`. No phone number is present (an unresolved discrepancy across signature and draft sources; keep phone omitted until resolved).
- [ ] Footer identifies an optional review solicitation, shows the owner-confirmed postal address, and includes the reply-unsubscribe instruction.
- [ ] No tracking pixel, click redirector, unique recipient URL parameters, JavaScript, form, animation, or required attachment.
- [ ] Contrast checked (body and footer at least 4.5:1). Links are underlined. Focus style is present where supported.
- [ ] Test rendering in Gmail (web and mobile) and Outlook, images on and off, and a dark-mode pass (logo is a light-background mark).
- [ ] No incentives, review funnel, star targets, suggested wording, sales, coupons, or positive-only prompts.

## E. Approval of one exact batch

An approval is permission for listed messages only, not a standing routine.

The approval record (private) must include:

- [ ] `batch_id`, approver, `approved_at`, and `approval_expires_at`
- [ ] Template versions / hashes for HTML and plain text
- [ ] Exact `google_review_url` and QR status (omitted or verified)
- [ ] Sender mailbox and From display name
- [ ] Recipient count and the opaque household/project identifiers
- [ ] Eligibility evidence references and exclusion reasons for people considered but not included
- [ ] Final MIME preview of the exact initial or reminder being approved
- [ ] Confirmation that preflight (section C) was run against current mailbox and ledger state

Invalidation triggers: template change, URL or QR change, postal-address change, expiry, new opt-out or conflicting evidence, or any unresolved blocker above.

Separate, later approval is required for any reminder batch. Default reminder window: 10–14 days after **confirmed** initial send. None authorized now.

## F. Timing defaults (configurable only with human review)

- [ ] New initial: 7–14 days after the later of independently verified completion and final invoice issuance.
- [ ] At most one reminder: 10–14 days after confirmed initial send, only if there is no reply, opt-out, known review, bounce, service hold, or unknown send outcome.
- [ ] No second reminder. Silence means stop.
- [ ] Historical outreach more than 90 days after completion: manual review only; no default reminder.
- [ ] No automated scheduling is authorized by this package.

## G. After a future approved send (planned process; not implemented here)

- [ ] Record provider message/thread IDs and the actual result in the private ledger. Provider acceptance is not proof of delivery.
- [ ] Crash, timeout, or uncertain result → state `unknown` → reconcile Sent mail before any retry; otherwise stop.
- [ ] Honor unsubscribe and other suppressions immediately, before any further marketing send (statutory outer limit is 10 business days; PID default is immediate).
- [ ] Keep service and warranty replies separate from marketing suppressions.
- [ ] Do not create a review quota or report that pressures staff to obtain positive reviews.

## H. Explicitly out of scope for this package

Do not treat any of the following as done just because these files exist:

- Live send implementation, Gmail drafts, scheduled mail, or test messages
- Creation or application of Gmail labels
- A software ledger, worker locks, or repository source code
- A populated last-15 customer list or any HOLD-lead identities (the Gmail audit produced holds, not mailables)
- A phone number in the customer-facing templates
- Counsel’s formal legal opinion
