# PID review-request eligibility and tracking SOP

> **Repo note (2026-11-19):** This document was written for the November 8, 2026 content package, before any code existed. The dry-run tooling in `../pid_reviews/` now implements the renderer, private ledger, eligibility rules, and approval-batch steps described here, and it still sends nothing. Templates are now `v1.1.0-2026-11-19`: same customer-facing copy, plus optional `{{#qr_block}}` and `{{#phone_block}}` sections that are removed unless their verified inputs exist. Wherever this text says "not implemented", read it as "no sending is implemented or authorized".

**Pleasure Island Design LLC (PID)**  
Operator standard operating procedure  
Effective date of this document: November 8, 2026 (America/New_York)  
Companion files: `README.md`, `placeholders.md`, `launch-checklist.md`, `templates/`

This SOP describes how to find, verify, approve, and track optional review-request emails so PID does not spam customers, misidentify people, or treat unfinished work as complete. It is the human process. It is **not** authorization to send, draft, label, or schedule mail, and it is **not** implemented software.

Private customer records do not belong in this file or anywhere else in this package. Gmail Bot is separately and privately investigating recent kitchen-cabinet completions; no customer names, addresses, or project details were available to this workstream and none are invented here.

## 1. What is implemented vs planned

| Exists in this package now | Planned for a future, separately authorized effort |
|---|---|
| Email HTML and plain-text templates with placeholders | A renderer that safely substitutes placeholders |
| This SOP, the placeholder dictionary, and the launch checklist | A private encrypted ledger application or spreadsheet workbook stored outside shared/public trees |
| A documented Gmail **label plan** | Creating or applying any Gmail labels |
| Rules for eligibility, evidence, dedup, suppressions, approvals, and fail-closed handling | Runtime automation, mailbox watchers, send workers, or scheduled jobs |
| A visually marked incomplete preview | Live or test sends, drafts, or customer-specific mail |

Until a private ledger exists, operators who later run this process manually must still keep an authoritative private register. Convenience flags in Gmail must never become the only record.

## 2. Purpose and risks this process is designed to prevent

The program asks completed kitchen-cabinet homeowners, after a short courtesy wait, whether they would like to leave an honest Google review. Every eligible customer gets the same optional opportunity regardless of sentiment. There are no incentives, no satisfaction funnel, and no sales offers in the message.

This process exists to prevent:

- Messaging someone who is not a completed kitchen-cabinet customer
- Treating a contractor, lead, or household member as the customer of record without evidence
- Treating a deposit, progress invoice, payment, or estimate as proof the job is done
- Duplicate initials or stacked reminders to the same household or project
- Writing again after an unsubscribe, bounce, reply, or known review
- Permanently excluding people who had a service issue (that would screen out negative reviews)
- Sending a search link or the wrong business’s review page
- Approvals that silently survive template, URL, or recipient changes

## 3. Roles and systems

| Role | Responsibility |
|---|---|
| Sender / mailbox owner | Authenticated sends only from `pleasureislanddesign@gmail.com`. Proposed From display name: `Nicole Rayment \| Pleasure Island Design`. The same mailbox is Reply-To and is monitored for replies, unsubscribes, and bounces. |
| Approver (Will or a named delegate) | Approves one exact batch at a time after seeing evidence, exclusions, and the final MIME preview. |
| Operator | Assembles candidates, audits evidence, searches mail history, updates the private ledger, and stops on uncertainty. |
| Gmail Bot workstream | Private, read-only investigation of recent non-contractor kitchen-cabinet completions. November 8, 2026 (America/New_York) result: 22 invoice PDFs and all identified candidate threads/search pages inspected; eight kitchen projects found; zero independently verified completions; the original 15 recipient leads are all HOLD, not a mailing list. No customer evidence or PII from that audit is stored in this package. |
| Counsel (as needed) | Classification questions (commercial vs other), non-US recipients, or unusual consent facts. This SOP is not a legal opinion. |

Systems:

1. **Private authoritative ledger** — source of truth for candidates, evidence references, states, approvals, sends, and suppressions.
2. **Mailbox** — evidence and preflight source, never the ledger.
3. **Gmail labels** — optional later convenience views. They are not source of truth and are not created by this package.

## 4. Authoritative ledger (required before any live program)

Keep the ledger outside git, shared marketing folders, and this package. Minimize retained content. Control access. Preserve the smallest lawful suppression markers if other records are deleted.

Recommended state sequence:

`candidate → quarantined or verified → approved → sending → sent`

Terminal or pause states include `suppressed`, `paused` (service hold or delivery uncertainty), `replied`, `reviewed`, `closed`, and `unknown` (send result not reconciled).

Each candidate row should be able to store, at minimum, the runtime fields listed in `placeholders.md` section 3: opaque `household_id` and `project_id`, verified recipient mailbox, completion date, final invoice reference, evidence references, current state, suppression reason, template version, approval identifiers, send identifiers, and timestamps. Operator-facing dates use America/New_York; stored timestamps may be ISO UTC if conversion is consistent.

Rules:

- One initial request per household/project.
- At most one reminder per household/project, and only after a confirmed initial send.
- Pilot default: do not automatically start a fresh initial for an already-contacted household under a different project without a new human approval.
- Do not collapse unrelated people because they share a surname, a street, or a similar Gmail local-part.
- Do not infer a missing email or silently substitute another household member.
- Unique reservation of `household_id` + `project_id` + request type (initial/reminder) before any send attempt, even in a manual process: write the intent first, then send, then record the result.
- Provider acceptance is not proof of delivery. A crash or timeout after clicking send is `unknown` until the Sent mailbox is reconciled. If reconciliation is impossible, stop. Do not retry blindly.

## 5. Gmail label plan (plan only — do not apply now)

If labels are later authorized, use a single prefix so they stay easy to filter. Proposed set:

| Label | Meaning (view only) |
|---|---|
| `PID/Reviews/Candidate` | Seen during discovery; eligibility not finished |
| `PID/Reviews/Verified` | Eligibility evidence accepted |
| `PID/Reviews/Needs-review` | Ambiguity or conflicting evidence |
| `PID/Reviews/Paused` | Temporary service or delivery hold |
| `PID/Reviews/Approved` | Currently inside an unexpired exact-batch approval |
| `PID/Reviews/Initial-sent` | Ledger records a confirmed initial send |
| `PID/Reviews/Reminder-sent` | Ledger records a confirmed reminder send |
| `PID/Reviews/Replied` | Any reply after a request; reminders stopped |
| `PID/Reviews/Reviewed` | Known review of any rating, or customer says they already reviewed |
| `PID/Reviews/Suppressed` | Opt-out, complaint, hard bounce, or other permanent marketing stop |
| `PID/Reviews/Closed` | No further review-program action |

Creating, renaming, or applying these labels requires separate authorization. An `Approved` label by itself does not authorize a send. Removing a sent label does not authorize a resend. If a label and the ledger disagree, the ledger wins and the case is quarantined until a human reconciles it.

## 6. Eligibility criteria

A person may be a candidate only when **all** of the following are true. Return fewer than 15 if fewer qualify. Do not fill a quota with contractors, leads, incomplete jobs, or guessed matches.

1. **Homeowner / non-contractor.** The customer is not being contacted as a trade contractor or similar B2B partner for this project. If the role is unclear, hold.
2. **Kitchen cabinet scope.** The completed work is a kitchen cabinet project (PID cabinet refinishing / related kitchen cabinetry work documented as such). Adjacent furniture-only or unrelated interior work does not qualify for this template, which names a kitchen cabinet project.
3. **Independently documented completion.** Proof can be a dated walkthrough or sign-off, an explicit installation-finished confirmation, or a staff completion record that a human verifies. An estimate, deposit request, or invoice does not prove completion.
4. **Final invoice issued** for that same project. “Issued” means a real final invoice exists, not that someone intended to bill later.
5. **Payment is not a proxy for completion.** A paid invoice can still belong to unfinished, canceled, or disputed work. A paid deposit is not completion.
6. **Same household and project.** Completion proof and invoice proof resolve to the same job and the same customer household.
7. **No open cancellation or unfinished install.** Cross-check cancellations, punch lists, and invoice scopes that do not match the work described.
8. **Neutral as to sentiment.** Do not include or exclude anyone because they seemed happy or unhappy, might leave fewer than five stars, live in a particular neighborhood, or had a large or small invoice.
9. **Contactable at one verified mailbox** that already has a prior customer relationship and a lawful basis for this commercial message. Project correspondence is not automatically marketing consent.
10. **Not already handled** by a prior request, suppression, known review, or unresolved hold for that household/project.

Uncertainty on any point = `quarantined` / hold. Fail closed.

### 6.1 Evidence audit

For each candidate, the operator records private references (not copies in this package) to:

| Evidence | Acceptable examples | Not sufficient alone |
|---|---|---|
| Completion | Dated sign-off, written “install complete” confirmation, verified internal completion note tied to the project | Invoice, payment receipt, scheduling email, photos without a completion statement, thread recency |
| Final invoice issued | The issued final invoice for that project | Estimate, deposit invoice, progress invoice that is not final, “we should bill them” notes |
| Identity and role | Project file and mailbox showing the homeowner customer | Last name match, neighborhood guess, a contractor copied on updates |
| Mailbox | Address used in the customer relationship, confirmed as current enough to contact | An address inferred from a directory or from another household member |

Link each piece of evidence to `household_id` and `project_id`. If two documents might describe different jobs, hold.

### 6.2 Historical last-15 list and stale records

When assembling a “most recent completed kitchen cabinet homeowners” list:

- Sort by **documented completion date**, descending.
- Do not sort by last email date or payment date.
- Use `project_id` as the stable tie-breaker.
- Unknown completion date is ambiguous; hold rather than guess.
- Operational stale threshold for this pilot: more than **90 days** since completion. Stale records need manual reconfirmation of the current recipient, completion, prior contact, review history, and whether outreach is still appropriate. **Do not imply the work was recent.** Default: **no reminder** on stale historical outreach.
- If fewer than 15 records survive, ship the shorter list. There is no quota.

Gmail audit status, November 8, 2026 (America/New_York): a private workstream inspected 22 invoice PDFs and all identified candidate threads and search pages. It found eight kitchen projects and independently verified **zero** completions. The original 15 recipient leads are all on HOLD. They are not a mailing list and must not be mailed from. No customer evidence or PII from that audit appears in this package. Do not invent stand-in names or project details to exercise the process. Fail closed: invoice issuance, payment, or a kitchen-scoped thread is not completion.

## 7. How to find candidates (manual discovery)

Discovery is read-only. Do not send, draft, star, or label during discovery unless a later authorization says otherwise.

Suggested operator sequence against PID’s own business mailbox and project files:

1. Start from project or accounting records of kitchen cabinet jobs, not from whoever emailed most recently.
2. For each job, collect completion evidence and the final invoice. Discard or quarantine anything missing either one.
3. Confirm the customer is a homeowner / non-contractor and that the mailbox belongs to that customer.
4. Search the mailbox for that household and project — not only one thread — for completion language, invoice issuance, cancellations, punch lists, prior review requests, unsubscribes, and service issues.
5. Search more broadly for previous review-request subjects or wording (`An optional review of your PID kitchen cabinet project` and `One optional reminder: your PID project review` once those have been used) so a missing ledger row does not cause a duplicate.
6. Assign opaque household and project identifiers in the private ledger.
7. Mark anyone who fails a required criterion as excluded, with a dated reason. Exclusions are part of the audit trail.

Do not purchase, scrape, or append outside addresses. Do not contact anyone to “confirm they are the right person” as part of building this list unless a separate, ordinary service conversation already exists.

## 8. Deduplication

Before a record can move from `candidate` to `verified`:

- Match on stable `household_id` and `project_id`, not on display name alone.
- Normalize the verified mailbox for comparison (case, trivial dots only with care — Gmail-style normalization can over-merge unrelated accounts; when unsure, hold).
- If the same household had multiple kitchen cabinet projects, the pilot default is no automatic new initial without human approval if any project already received a request.
- If two mailboxes appear to be the same person, a human decides; do not silently keep both or drop one.
- If the only match is a shared surname or a similarly named business, treat it as not a match.

## 9. Timing

Recommended defaults, changeable only with human review. This package does not schedule anything.

| Message | When | Other limits |
|---|---|---|
| Initial | 7–14 days after the **later** of independently verified completion and final invoice issuance | Not before both facts exist. Not while quarantined, suppressed, or on hold. |
| Reminder | 10–14 days after a **confirmed** initial send | Exactly one. Fresh human approval of that reminder batch. None authorized now. |
| After silence | Stop | No second reminder. No open-tracking logic (this program does not use open tracking). |
| Historical >90 days | Manual review only | No default reminder. Do not use language that implies recent work. |

No automated scheduling is authorized by this specification.

## 10. Event handling

| Event | Required action |
|---|---|
| Explicit opt-out, “unsubscribe,” spam complaint, or hard bounce | Immediate global marketing suppression, including future review requests. Service and warranty replies may continue. No batch approval overrides this without verified later consent where lawful. Honor at once; do not wait for the statutory 10-business-day outer limit. |
| Any reply after a request | Stop automatic reminders. A human reads the reply. An out-of-office pauses; it does not trigger another send. Do not treat silence as consent. |
| Known prior review (any rating) or “I already reviewed” | Suppress request or reminder. The customer’s word is enough. Never demand proof. An ambiguous public-name match pauses for a human and is not assumed to be the same person. Courtesy “already reviewed” language in the reminder template does not permit ignoring a known review. |
| Prior request for the same household/project | Consult the ledger **and** mailbox history. No second initial. |
| Unknown send outcome | Reconcile Sent mail. If still unknown, fail closed. No blind retry and no automatic reminder. |
| Unresolved service case, repair, or punch list | Temporary `paused` service hold — not a permanent negative-sentiment exclusion. Keep the person in the candidate register with a dated reason and owner. Reassess at least weekly. After objective case closure, they receive the same optional review opportunity regardless of satisfaction. Do not condition support, a refund, or case closure on posting or removing a review. Audit long pauses so unhappy clients are not systematically screened out. |
| Soft bounce, rate limit, or delivery uncertainty | Pause, investigate, reconcile. No automatic reminder and no retry to an alternate address. |
| Identity, authorization, completion, invoice, or lawful-contact ambiguity | Quarantine. Human resolution with evidence. |

## 11. Mailbox preflight (immediately before each send)

Even after approval, immediately before each individual send (and again before a reminder), requery:

- The ledger and the global suppression list
- Recent mailbox activity across relevant threads and aliases
- Replies, unsubscribes, earlier review requests, bounces, known reviews, and service cases
- That the batch approval is still unexpired and still matches the template version, review URL, postal address, sender, and recipient set

Fail closed when permissions are missing, sync looks stale, the ledger is unavailable, or evidence conflicts. An approval never bypasses a current suppression.

Single-recipient `To:` only. Never CC or BCC the rest of a cohort.

## 12. Approval rules

Current request status: **preparation only**. No customer sends are authorized. No reminder is authorized.

When an approver later reviews a batch, the approval is bounded to those exact messages. It must list recipients (by opaque IDs plus the private mailbox in the private record), evidence and exclusion reasons, sender, final MIME preview, template version/hash, exact review URL and QR status, count, and expiry.

Invalidation triggers:

- Any edit to the HTML or plain-text templates (new `template_version` required)
- Any change to the review URL, QR, postal address, sender, or recipient list
- Expiry of `approval_expires_at`
- Newly discovered opt-out, reply, bounce, review, service hold, or identity doubt

A reminder batch always needs its own later approval. There is no standing permission to “follow up automatically.”

Test sends, if ever used, also need explicit approval of recipient and content. Prefer internal mailboxes. Do not use real customers as a rendering test.

## 13. Policy boundaries operators must not cross

- Ask only people with genuine experience of the completed project.
- No incentives of any kind for a Google review, an edit, or a removal (PID adopts Google’s stricter “no incentives” rule).
- No selective prompting of happy customers and no discouraging of negative reviews.
- No required wording, star targets, staff-name requests, or on-site pressure.
- No coupons, holiday specials, referral rewards, or upsells inside a review request.
- No fabricated or AI-written customer experiences.
- No tracking pixels, read receipts, open-based follow-ups, or click-rewriting.
- Identify the message as an optional customer review solicitation in the footer, include a valid owner-confirmed postal address, and honor reply-based opt-out.
- Native authenticated Gmail sending only for this From address.

Cited reference points (retrieved with the research specification dated November 8, 2026): Google contribution policy and Business Profile review-link guidance; Gmail sender guidelines; FTC Consumer Reviews and Testimonials Rule (16 CFR Part 465); CAN-SPAM primary-purpose rule (16 CFR 316.3) and 15 USC 7704. See `research-and-content-spec.md` (this folder).

## 14. Operator checklists

### 14.1 Candidate intake

- [ ] Kitchen cabinet project documented
- [ ] Homeowner / non-contractor role documented
- [ ] Independent completion evidence linked to this project
- [ ] Final invoice issued, linked to this project
- [ ] Payment not used as a stand-in for completion
- [ ] No cancellation or open punch list that contradicts completion
- [ ] Verified single recipient mailbox
- [ ] Opaque `household_id` and `project_id` assigned in the private ledger
- [ ] Dedup against household, project, and mailbox
- [ ] Uncertainty held, not forced through

### 14.2 Pre-approval packet (private)

- [ ] Sorted by completion date if this is a historical batch
- [ ] Stale (>90 day) rows flagged for manual review; no default reminder
- [ ] Exclusions listed with reasons
- [ ] Ledger and mailbox searched for prior requests
- [ ] Suppressions, replies, known reviews, and service holds applied
- [ ] Template versions recorded
- [ ] Review URL and postal address verification attached — or the packet is marked blocked and not submitted for send approval
- [ ] Final HTML and plain-text preview attached

### 14.3 Reminder decision (none authorized now)

- [ ] Initial send is confirmed in the ledger **and** visible in Sent mail
- [ ] 10–14 days have passed since that confirmed send
- [ ] No reply, opt-out, complaint, bounce, known review, or service hold
- [ ] Record is not a stale historical outreach using the no-default-reminder rule
- [ ] Fresh reminder-batch approval obtained
- [ ] Preflight repeated immediately before send

### 14.4 After any future send

- [ ] Ledger updated with result and provider IDs, or marked `unknown`
- [ ] `unknown` reconciled against Sent mail before any other action
- [ ] Monitoring continues for replies and unsubscribes
- [ ] No second reminder queued “just in case”

## 15. Privacy

Do not place customer names, emails, phone numbers, street addresses, invoice images, message contents, tokens, or populated environment files in git, this package, previews, or shared marketing documents. This SOP uses only opaque identifier shapes such as `HH-UNASSIGNED`. If a report must include personal information, store it in the private ledger with restricted access.
