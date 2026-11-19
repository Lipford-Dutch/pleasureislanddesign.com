# PID review-request tooling (dry run, never sends)

Plans, renders, and packages **optional** Google review requests for Pleasure Island Design
homeowners whose **kitchen cabinet** project is independently confirmed complete **and**
final-invoiced. It follows [`docs/eligibility-and-tracking-SOP.md`](docs/eligibility-and-tracking-SOP.md).

**This tool sends no email.** It has no Gmail, SMTP, or other mail API code. The furthest it
goes is writing `.eml` files for a batch Will has approved, so a person (or a separately
authorized sender, later) can send them from `pleasureislanddesign@gmail.com` as Nicole Rayment.

This folder is **not part of the website**. `.cpanel.yml` and `.github/workflows/deploy.yml`
publish only an allowlist of public files and folders, and `deploy.yml` deletes `_site/automation`
and fails the build if it appears. See [Deployment safety](#deployment-safety).

## Current launch blockers

`check-config` refuses real rendering and batching until these exist in `config.local.json`:

| Needed | From | Why |
|---|---|---|
| `google_review_url` + `google_review_url_verified` / `_by` / `_on` | Will: Google Business Profile → Read reviews → **Get more reviews** link, tested on desktop and mobile | The homepage search link is not a review link. Never invent or guess one. |
| `business_postal_address` + `business_postal_address_confirmed_by_owner` | Will (owner-confirmed) | CAN-SPAM requires a valid physical postal address. |
| Optional: `business_phone` + `business_phone_confirmed_by_owner` | Will | Phone is left out until the number discrepancy is resolved. |
| Optional: `qr_image_url` + `qr_image_file` | Generated locally from the *verified* URL only | The QR block is removed unless both exist and the URL is verified. |

## Layout

```
automation/review-requests/
├── review_requests.py        # CLI entry point (python3, standard library only)
├── pid_reviews/
│   ├── cli.py                # plan (default) | render | send | check-config | ledger-init
│   ├── config.py             # config loading + launch blockers
│   ├── render.py             # placeholder renderer (txt + html), URL validation, greeting fallback
│   ├── ledger.py             # private CSV ledger schema + loader (refuses in-repo ledgers)
│   ├── eligibility.py        # SOP rules: evidence, dedupe, timing, stop conditions, reminder cap
│   ├── batch.py              # approval batch + approval check + .eml outbox (no sending)
│   └── paths.py              # keeps private data and outputs out of the repo
├── templates/                # branded HTML + plain-text initial and reminder emails
├── config.example.json       # every key, blockers empty; copy to config.local.json (gitignored)
├── examples/ledger.example.csv  # FAKE rows only, for trying the CLI
├── tests/                    # unittest suite, fake data only
└── docs/
    ├── eligibility-and-tracking-SOP.md   # the human process (source of the rules)
    ├── placeholders.md                   # placeholder contract
    ├── launch-checklist.md               # go / no-go gates
    ├── how-to-test.md                    # step-by-step testing guide
    ├── content-package-README.md         # notes from the Nov 8 content package
    └── research-and-content-spec.md      # policy research (Google, FTC, CAN-SPAM, Gmail) + copy
```

## Quick start

Run from the repo root (Windows: use `python` instead of `python3`):

```bash
# 1. What is blocking launch?
python3 automation/review-requests/review_requests.py check-config

# 2. Dry-run plan against the FAKE example ledger
python3 automation/review-requests/review_requests.py --ledger automation/review-requests/examples/ledger.example.csv --today 2026-12-01 plan

# 3. Preview the emails (unresolved fields are marked NOT FOR SEND); written to the gitignored out/previews/
python3 automation/review-requests/review_requests.py render --kind initial --preview
python3 automation/review-requests/review_requests.py render --kind reminder --preview

# 4. Tests
python3 -m unittest discover -s automation/review-requests/tests -v
```

## Commands

| Command | What it does | Sends mail? |
|---|---|---|
| `plan` (default) | Reads the private ledger and prints who would get an initial or a reminder today and why every other row is waiting, held, stopped, done, or excluded. `--json` for machine output. | No |
| `render` | Writes `.txt` and `.html` for one ledger row (`--household`, `--project`) or an anonymous sample. Without `--preview` it refuses while any required placeholder is unresolved. | No |
| `send` | Without `--approval`: writes `batches/BATCH-<id>.json` for Will to review and exits with code 3. With `--batch` and a matching, unexpired `--approval`: re-checks the ledger, re-renders, and writes `approved-outbox/BATCH-<id>/*.eml`. | **No, never** |
| `check-config` | Shows which config, ledger, and output paths are in use, plus launch blockers. | No |
| `ledger-init` | Creates an empty private ledger with the right columns (refuses to create one inside the repo). | No |

Global options: `--config`, `--ledger`, `--today YYYY-MM-DD`. Environment overrides:
`PID_REVIEW_CONFIG`, `PID_REVIEW_LEDGER`, `PID_REVIEW_OUTPUT`.

## The private ledger

The ledger is the **source of truth**. Gmail labels are only optional views, and this tool never
creates them. The default location is `~/.pid-private/review-requests/ledger.csv` (on Windows,
`%USERPROFILE%\.pid-private\review-requests\ledger.csv`). The tool refuses any ledger inside the
git repo unless its name ends in `.example.csv`. Columns, defined in `pid_reviews/ledger.py`:

`household_id, project_id, first_name, recipient_email, mailbox_verified, customer_role,
project_scope, completion_verified, completion_evidence_ref, completion_date, final_invoice_issued,
invoice_ref, invoice_date, same_project_confirmed, open_issue, status, initial_sent_at,
reminder_sent_at, reminder_count, stop_reason, service_hold, service_hold_reason,
service_hold_revisit_on, notes`

The operator updates `status`, `initial_sent_at`, `reminder_*`, and `stop_reason` by hand, and only
after a send shows up in Sent mail or a reply, unsubscribe, or bounce arrives. The tool reads the
ledger and never writes to it, apart from `ledger-init`.

## Rules the code enforces

* **Evidence (SOP §6):** the customer must be a homeowner (contractors are excluded, unknown roles
  held) and the scope must be `kitchen_cabinets`. Completion proof is required separately from the
  invoice: an invoice or payment is never completion. Also required: a final invoice, proof that
  both documents cover the same project, no open punch list or cancellation, and one verified
  mailbox. Any gap means HOLD.
* **Status gate:** a row must be marked `verified` by an operator before it can be planned for an initial.
* **Dedupe (SOP §4, §8):** one row per household and project, and one initial per household and project.
  A household already contacted on another project is held, and so is a mailbox shared across
  households. Only one send per household or mailbox per run.
* **Timing (SOP §9):** the initial goes out at least 7 days after the later of completion and
  invoice. A record more than 90 days past completion is held for manual review, and stale outreach
  gets no reminder. There is exactly one reminder, 10–14 days after a confirmed initial. After that
  window, the sequence is done.
* **Stops (SOP §10):** unsubscribe, complaint, or bounce means global suppression across the
  household and mailbox. A reply or a known review stops the sequence. A send stuck in
  `unknown`/`sending` is held until it is reconciled.
* **Service hold:** a neutral pause with a revisit date. It is never an exclusion, so unhappy
  customers are not screened out.
* **Approval (SOP §12):** the batch file is hashed. An approval must name the exact batch ID and
  hash, carry `approved_by`, `approved_at`, and `expires_at` (72 hours at most), and contain the
  exact statement. Any change to the templates, review URL, address, recipients, or eligibility
  invalidates it.
* **Content:** HTML is escaped and the review URL is allowlisted (https, Google review hosts only,
  no search URLs, no tracking parameters). There are no tracking pixels. The greeting falls back to
  `Hello,`. Leftover `{{...}}` tags are an error.

## Deployment safety

* `.cpanel.yml` (GoDaddy cPanel production) copies only named root files plus `blog specials shop
  gallery locations js img fonts forms opt-images`. `automation/` is not on the list.
* `.github/workflows/deploy.yml` (GitHub Pages) copies the same allowlist, runs
  `rm -rf _site/automation`, and fails if `_site/automation*` exists.
* `mkdocs.yml` publishes `docs/` only. These docs live under `automation/review-requests/docs/`,
  so they are not published to the docs site.

## Privacy

No customer names, emails, addresses, phone numbers, invoice numbers, or message content belong in
this folder. The local `.gitignore` blocks `*.csv` (except the fake example), local configs,
`out/`, `batches/`, `approved-outbox/`, `*.eml`, `*.approval.json`, and generated QR images.
