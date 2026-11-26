# PID review-request content and safe-distribution specification
Research checked November 8, 2026 (EST). Design input for PID-DEV, not authorization to send, schedule, apply labels, or publish. No customer records or repository accessed; Gmail verification is a separate read-only workstream.

## 1. Launch gates and verified identity
- Sender requested by Will: **pleasureislanddesign@gmail.com**; display name proposed **Nicole Rayment | Pleasure Island Design**. Reply-To same monitored mailbox. Confirm authenticated sending-account identity in implementation; never spoof Gmail through another provider.
- First-party public identity: **Pleasure Island Design**, kitchen cabinet refinishing, Wilmington/coastal NC; Nicole Rayment is named on the homepage [P1]. Avoid unsupported ratings, testimonial counts, award claims or Nicole job titles in this email.
- **Direct Google review URL: NOT VERIFIED — deployment/send blocker.** The homepage Google link is only `https://www.google.com/search?q=Pleasure+Island+Design+Wilmington+NC`, NOT a write-review deep link. No place ID was verified or invented. Neither homepage nor search URL may substitute for the required review URL.
- Owner should supply Business Profile → Read reviews → Get more reviews link/QR [G2]. Human must test destination on desktop/mobile, confirm exact PID identity using name, business website, phone/location and confirm it opens the review composer (Google sign-in may intervene). Record verification date and verifier. Do not route to a similarly named business or silently replace a broken link.
- First-party public contact: `(910) 444-1230`, website `https://www.pleasureislanddesign.com/`, email above [P1]. Optional phone omitted from default copy to keep focus.
- Site displays a street address, but this does **not** establish a currently valid mailing address. **`{{business_postal_address}}` remains REQUIRED and owner-confirmed; launch blocker.** Do not automatically copy a public address into the compliance footer.

## 2. Policy and legal boundaries (requirements vs defaults)
| Classification | Rule / implementation consequence |
|---|---|
| Google policy requirement [G1,G2] | Ask only people with genuine experience. No incentives of any kind for Google reviews, edits or removals. No selectively soliciting positive reviews, discouraging negative reviews, satisfaction-screening funnel, required wording, star targets, staff-name requests, on-premises pressure or quotas. Same review opportunity for every objectively eligible customer regardless of sentiment. |
| FTC rule [F1] | No fabricated/AI-written customer experiences, nonexistent reviewers, false testimonials, sentiment-conditioned rewards, undisclosed prohibited insider practices, intimidation or groundless threats to suppress reviews. FTC's incentive restriction is not identical to Google's: the FTC rule specifically bans sentiment-conditioned compensation; Google bans incentives for any review. PID adopts **no incentives**. |
| CAN-SPAM classification [F2] | A prior customer relationship does NOT automatically make a review request transactional. Primary purpose is contextual; the narrow transactional categories do not automatically cover reputation-building requests. Have counsel resolve classification where necessary. Default: treat this program as commercial solicitation and satisfy full safeguards. Do not mix coupons, Thanksgiving specials, sales, referral rewards or upsells into review requests. |
| Commercial-email statutory requirements [F3] | Accurate sender/routing and nondeceptive subject; clear solicitation identification unless affirmative-consent exception applies; valid physical postal address; conspicuous functional opt-out (reply email can qualify), working for at least 30 days; honor opt-out within 10 business days. Do not sell/transfer opted-out addresses except as legally permitted for compliance. Do not assume project correspondence equals affirmative marketing consent. |
| Gmail requirements [G3] | All senders to personal Gmail: SPF **or** DKIM, valid forward/reverse DNS, TLS, RFC 5322 formatting, spam rate under 0.3%, no Gmail From impersonation. Gmail handles infrastructure for native authenticated Gmail sending; validate actual test headers rather than configuring DNS for gmail.com. Never send `@gmail.com` From through an unauthenticated third party. |
| Gmail bulk-only requirements [G3] | Over 5,000/day to personal Gmail: SPF **and** DKIM, DMARC/alignment, one-click unsubscribe plus visible body unsubscribe for marketing/subscribed mail. These are not universally mandatory just because a 15-recipient batch is automated. Reply opt-out is **not** RFC 8058 one-click. If scale changes, block launch until capabilities reviewed. |
| Conservative PID defaults (not statutory deadlines) | Immediate opt-out suppression before another send; explicit batch approval; maximum one reminder; no tracking pixels or click redirects; no purchased/scraped addresses; confirm lawful contact basis and recipient expectation. Google recommends opt-in/only wanted mail [G3]; do not interpret federal CAN-SPAM as permission to send unwanted mail. Non-US recipients require separate jurisdiction review, not US-only assumptions. |

This is operational guidance, not a legal opinion. CAN-SPAM applies to individual commercial messages too, not just mass campaigns. Keep service/warranty replies separate from marketing suppressions.

## 3. Branding and accessible email design
Evidence: the private PID brand guide, `SOURCE-repo-brand-guidelines.md`, `SOURCE-repo-design-system.md` read; live stylesheet [P2] resolves documented drift.
- Logo public asset: **https://www.pleasureislanddesign.com/img/pid-logo-v2-header.png**. Referenced in live HTML and successfully fetched as PNG; use current production asset, not conceptual logos. Review visually against light/dark background before launch; no redesign required.
- Live colors: navy `#1E3A5F`, dark navy `#0F1E30`, sage `#7DA69E`, gold `#C4973B`, cream `#F9F6F1`, charcoal `#1C1C1E`, muted `#5A5A6E`, white `#FFFFFF` [P2]. Live sage-light `#9DBFB8`, sage-dark `#5B8078` differ from old docs. Email: cream outer background, white content, charcoal body, navy CTA with white text; sage/gold decorative accents only. Do not use low-contrast white-on-sage/gold text.
- Live fonts: heading `Playfair Display, Georgia, Times New Roman, serif`; body `Lato, Helvetica Neue, Arial, sans-serif` [P2]. Email uses safe fallback Georgia/Arial without reliance on webfont download; brand fonts optional progressive enhancement.
- MIME multipart/alternative: complete UTF-8 plain text plus HTML. One-column 100%-width outer presentation table and centered 600px maximum-width inner table; Outlook fixed-width conditional wrapper; inline essential CSS. `lang="en"`, logical reading order, presentation roles only on layout tables.
- Logo ~280px wide, fluid max-width:100%, preserved aspect ratio; meaningful alt **Pleasure Island Design**. Live text heading/body/signature, never image-only email. Body 16px, line-height ~1.5; footer >=14px. Text contrast >=4.5:1; verify dark mode, 200% zoom, images off and 320px mobile width. Underline text links; visible focus where supported.
- One prominent real-link CTA **Share an honest Google review**, minimum 44px tap height and mobile full width; bulletproof table-based button, not image button. Beneath it expose same direct URL as selectable text, wrapping long URLs safely. No required attachment, JavaScript, form, animation or PDF.
- Optional SECONDARY QR only after URL verification: locally generated PNG, black/white high contrast, quiet zone >=4 modules, ~160–200px rendered, no logo overlay; scan-test exact decoded URL equals CTA URL. Alt **Scan to open Pleasure Island Design’s Google review page**. Caption “Prefer your phone? Scan this code.” QR must never be the sole route; same-phone readers need CTA. No remote QR API, unique recipient payloads or tracking query parameters.
- No tracking pixel, read receipt, open-based follow-up logic, click rewriting or PII in URLs. Ordinary hosted logo/QR fetches can produce server logs: minimize retention; do not claim zero network logging. Prefer no QR in compact initial version. Visible preheader rather than concealed keyword/padding tricks, consistent with Gmail's warning about hidden content [G3].

## 4. Approved-for-review copy (not approved to send)
From/Reply-To: pleasureislanddesign@gmail.com. To: verified individual customer only; never CC/BCC the cohort.

### Initial
**Subject:** An optional review of your PID kitchen cabinet project

**Preheader:** Your honest experience can help other homeowners. No obligation.

Hi {{first_name}},

Thank you for choosing Pleasure Island Design for your kitchen cabinet project. If you’d like, would you share an honest review of your experience on Google? Your feedback can help other homeowners decide whether we’re the right fit.

**[Share an honest Google review]({{google_review_url}})**

This is completely optional, and all feedback is welcome. Google requires a Google Account to post a review.

If you need help with your project, you can reply to me here—whether or not you leave a review.

Thank you,
Nicole Rayment
Pleasure Island Design
pleasureislanddesign@gmail.com

Optional customer review solicitation from Pleasure Island Design.
{{business_postal_address}}
To stop all PID marketing emails, including review requests, reply “unsubscribe.”

Plain-text version uses the identical prose, with `Share an honest Google review: {{google_review_url}}` in place of the button. HTML also shows this literal URL below the button. No “recently,” “last week,” invented project details, stars, or suggested review text. Greeting fallback: “Hello,” if name is absent.

### One optional gentle reminder
**Subject:** One optional reminder: your PID project review

**Preheader:** No need to respond; this is our last review reminder.

Hi {{first_name}},

One gentle reminder: if you’d like to share your experience with Pleasure Island Design on Google, the link is below. Honest feedback of any kind is welcome.

**[Share an honest Google review]({{google_review_url}})**

If you’ve already reviewed us, thank you—there’s nothing more to do. This is our last review reminder. If you need help with your project, just reply here.

Thank you,
Nicole Rayment
Pleasure Island Design
pleasureislanddesign@gmail.com

Optional customer review solicitation from Pleasure Island Design.
{{business_postal_address}}
To stop all PID marketing emails, including review requests, reply “unsubscribe.”

Use same plain-text/link/footer rules. Never send reminder when a known review exists; courtesy “already reviewed” language only addresses unavoidable identity uncertainty, not permission to ignore records. General replies end automatic reminders pending human handling.

## 5. Placeholder and validation contract
Never allow arbitrary HTML or unrendered `{{...}}` to leave dry-run mode.
| Field | Required? | Type / handling |
|---|---|---|
| `first_name` | Optional | Verified preferred first name, HTML-escape for HTML and strip control characters; absent → whole greeting “Hello,”. No guessed names. |
| `google_review_url` | Required, blocked now | Absolute HTTPS, vetted Google-hosted review URL/official short link with redirects validated to the correct PID review destination. Allowlist verified exact URL; no arbitrary URL or javascript/data scheme. Attribute-escape only after URL validation; QR encodes original validated URL, not HTML entities. |
| `business_postal_address` | Required, owner confirmation outstanding | Valid sender postal address, HTML-escaped; explicit line breaks controlled by renderer. Never infer from customer data or assume website address receives mail. |
| `logo_url` | Required configuration if logo used | Exact HTTPS public PNG asset above; immutable approved configuration, URL-validate then attribute-escape. Logo failure must not conceal sender or CTA. |
| `qr_image_url` | Optional | HTTPS PID-owned static asset or tested CID support; generated from same verified review URL. Validate/escape as URL; no third-party customer-data sharing. |
| `recipient_email` | Required private runtime | Valid single mailbox, prior customer evidence, no CR/LF; no header injection. Never inserted into source fixtures/public URLs. |
| `household_id`, `project_id`, `request_id`, `batch_id` | Required private runtime | Opaque internal identifiers, not displayed; no address-derived plaintext identifiers in repo. |
| `completion_date`, `invoice_id`, `evidence_refs` | Required private runtime | Validated completion timestamp, issued final invoice reference, independent completion/invoice proofs. Not rendered by default. Invoice issued != work complete; invoice paid alone != completion either. |
| `template_version`, `approval_id`, `approved_at`, `sent_message_id`, `sent_at`, `suppression_reason` | Required when applicable | Typed audit metadata; trusted clock, consistent zone conversion. Operator reports use America/New_York (EST/EDT); storage can use ISO UTC. |

Subject/preheader static; if future dynamic headers are added reject newline/control characters. No raw interpolation into HTML, headers, URLs or SQL. Fixtures use empty/opaque synthetic placeholders only, never real customers.

## 6. Neutral eligibility, timing and handling
**Recommended defaults, configurable only with human review:** initial 7–14 days after independently verified completion and final invoice issuance (later event controls). One reminder no sooner than 10–14 days after confirmed initial send. No second reminder; no response = stop. No automated scheduling is authorized by this specification.

For the historical last-15 list, sort by documented completion date descending, not thread recency or payment date; stable tie-breaker project ID. Define stale as >90 days since completion for this pilot (operational default, not law). Unknown completion date is ambiguous. Stale records need manual reconfirmation of correct current recipient, completion, prior contact/review history and appropriateness; default no reminder for stale outreach. Never imply recent work. Return fewer than 15 if fewer qualify; do not fill quota with contractors, leads or guessed matches.

Require homeowner/non-contractor kitchen cabinet scope + independently evidenced completed work + actual final invoice issued. Completion proof can be dated walkthrough/sign-off, explicit installation finished confirmation, or staff completion record verified by human; an estimate/deposit/invoice does not prove it. Link evidence to same project/household. Cross-check cancellations, open installs/punch lists and mismatched invoice scopes. No assessment of happiness, likelihood of five stars, neighborhood prestige or invoice value.

| Event | Action |
|---|---|
| Explicit opt-out, spam complaint, hard bounce | Immediate suppression; opt-out applies across PID marketing/review campaigns, not necessary service messages. No approval can override without verified subsequent customer consent where lawful. |
| Any reply after request | Stop automatic reminders; human handles actual intent; an out-of-office pauses rather than triggers repeat sends. Do not classify silence/open tracking as consent. |
| Known prior review (any rating) / “already reviewed” | Suppress request/reminder; customer assertion enough to stop. Ambiguous public name match → pause for human review, not assumed identity. Never demand proof/screenshots. |
| Prior request for same household/project | Consult authoritative ledger AND mailbox history; no duplicate initial. Unknown send outcome → reconcile, never blind retry. |
| Unresolved service case, repair/punch list | Neutral temporary service-workflow pause, not permanent negative-sentiment exclusion. Keep in candidate register with dated reason/owner, review weekly; allow identical review opportunity after objective case closure regardless of satisfaction. Do not condition support, refund or case closure on review/removal. Audit prolonged pauses so unhappy clients are not systematically screened out. |
| Soft bounce, rate limit, delivery uncertainty | Pause; investigate/reconcile; no automatic reminder or alternate-address retry. Hard bounce suppress address. |
| Identity, recipient authorization, completion, invoice or lawful-contact ambiguity | Quarantine; human resolution required with evidence. No inferred email or automatic household member substitution. |

## 7. Implementation controls for PID-DEV
1. Dry-run default, no send credentials required for rendering/tests. Discovery read-only. Preview report includes eligibility evidence, exclusions and template/URL verification status; private PII report stored outside repo. Label plan only; no labels applied now.
2. Private authoritative transactional ledger and suppressions store; Gmail labels are convenience views, never truth. Proposed labels: `PID/Reviews/Candidate`, `Verified`, `Needs-review`, `Paused`, `Approved`, `Initial-sent`, `Reminder-sent`, `Replied`, `Reviewed`, `Suppressed`, `Closed`. Application/creation requires separate authorization; approval label alone cannot authorize sending.
3. Stable household/project keys + normalized verified contact mapping. One initial per household/project and at most one reminder; pilot default no fresh automated initial for already-contacted household under a different project without human approval. Do not over-normalize unrelated Gmail identities or silently collapse people on surname alone.
4. Atomic unique constraints/reservations and worker lock prevent concurrent duplicate sends. Lifecycle `candidate → quarantined/verified → approved → sending → sent` with terminal/pause states. Persist intent before API call; record provider message/thread IDs and actual result. Provider acceptance isn't proof of delivery. Crash after acceptance/timeout → `unknown`, reconcile Sent mailbox before any retry; if unable, stop. Do not promise exactly-once across an external API.
5. Explicit human approval for EACH exact batch and reminder batch: recipients, evidence, exclusion reasons, sender, final MIME preview, template hash/version, exact review URL/QR, expiry of approval and count. Approval is bounded to those messages, not a routine or general sending permission. Changes invalidate approval. Current request authorizes preparation, not customer sends.
6. Immediately before EACH send requery recent mailbox activity across relevant threads/aliases for replies, unsubscribes, previous review requests, bounces, known reviews and service cases; recheck ledger/global suppression and batch approval. Missing permissions, stale sync, unavailable ledger or conflicting evidence = fail closed. Approval never bypasses current suppressions.
7. Single-recipient To, no cohort disclosure. Rate-limited small pilot under account/provider limits after approval; no quota target for reviews. Native authenticated Gmail only for this sender. Test rendering/MIME in Gmail mobile/web and Outlook, links, reply opt-out monitoring, bounce handling, TLS/authentication headers, no tracking and accessibility before launch. Actual test sends also need explicit recipient/content approval.
8. Audit records: evidence IDs (private), eligibility decision/reason, operator, before/after state, template hash, approved exact batch, preflight time, send result/message ID, suppression events. Minimize retained content; access-controlled encrypted storage, retention policy and deletion procedure preserving minimal lawful suppression markers. No customer names, addresses, emails, invoice scans, exports, tokens or populated `.env` in git; sanitized logs and no PII in CI artifacts.
9. Documentation/code handoff should include policy README, eligibility SOP, evidence schema, ledger/state-machine design, template rendering module and text/HTML templates, approval manifest schema, dry-run CLI, suppression/bounce/reply runbook, review-link/QR verification checklist, retention/access policy, deployment checklist and tests. Tests cover missing proof, contractor/lead exclusions, stale records, opt-outs during approval, sent-label removal, duplicate workers, unknown send reconciliation, malicious placeholders and equal opportunity irrespective of sentiment. No enabling live-send routine in this change.

## 8. Sources retrieved this turn
- [G1] Google Maps prohibited/restricted content: https://support.google.com/contributionpolicy/answer/7400114?hl=en
- [G2] Google Business Profile review request/link/QR guidance: https://support.google.com/business/answer/3474122?hl=en
- [G3] Gmail sender guidelines: https://support.google.com/mail/answer/81126?hl=en
- [F1] FTC Consumer Reviews and Testimonials Rule, 16 CFR Part 465 (current text): https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465
- [F2] FTC CAN-SPAM primary-purpose regulation, 16 CFR 316.3: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-316/section-316.3
- [F3] CAN-SPAM statutory text, 15 USC 7704, reproduced by Cornell LII: https://www.law.cornell.edu/uscode/text/15/7704
- [P1] First-party PID homepage, retrieved via WebFetch and public HTML download: https://www.pleasureislanddesign.com/ (apex redirects to www).
- [P2] First-party live design tokens: https://www.pleasureislanddesign.com/styles.css
- [P3] Live logo, fetched via public curl: https://www.pleasureislanddesign.com/img/pid-logo-v2-header.png

Retrieval caveat: FTC consumer-facing guidance URLs for CAN-SPAM and review-rule FAQs returned 404 in WebFetch; public CAN-SPAM curl fallback returned 403. They are NOT cited as retrieved guidance; the current FTC regulations and statute above ground the legal discussion instead. No claim that failed URLs do not exist. Public searches surfaced inconsistent older third-party PID location details, which were not accepted as business-profile verification.

## 9. Outstanding blockers
Verified owner-supplied Google review deep link and correct profile test; owner-confirmed valid postal address; private verified customer/evidence list from Gmail workstream; lawful-contact/expectation check and historical manual reconfirmations; authenticated sender check, tested opt-out monitoring and private ledger; final content/design/QA and explicit per-batch send approval. No Gmail labels, drafts, messages, schedules, repository changes or external contacts were made for this research.
