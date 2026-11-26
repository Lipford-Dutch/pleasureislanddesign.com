# How to test the review-request tooling

Everything below is safe: **no step sends email**. Use only fake data or internal test
mailboxes. Never use a real customer as a rendering test (SOP §12).

Windows PowerShell: use `python` in place of `python3` and run from the repo root.

## 1. Unit tests (fake data only)

```bash
python3 -m unittest discover -s automation/review-requests/tests -v
```

These cover eligibility evidence, contractor and non-kitchen exclusion, completion versus invoice,
dedupe, the courtesy wait, the reminder window and cap, stop conditions (unsubscribe, complaint,
bounce, reply, known review, unknown send), neutral service holds, placeholder failures, URL
validation, greeting fallback, QR and phone blocks, approval matching and expiry, and the rule that
private paths stay out of the repo.

## 2. Dry-run plan with the fake ledger

```bash
python3 automation/review-requests/review_requests.py \
  --ledger automation/review-requests/examples/ledger.example.csv --today 2026-12-01 plan
```

Expected: `HH-FAKE-001` gets an initial and `HH-FAKE-005` a reminder. `002` waits, `003` is held
(invoice only, no completion proof), `008` is held for service, `007` is stopped (unsubscribed),
`006` is done (reminder cap), and `004`/`009` are excluded (contractor, not kitchen). The plan ends
with **LAUNCH BLOCKED** until the review URL and postal address are configured.

## 3. Visual preview

```bash
python3 automation/review-requests/review_requests.py render --kind initial --preview
python3 automation/review-requests/review_requests.py render --kind reminder --preview
```

Open `automation/review-requests/out/previews/PREVIEW-NOT-FOR-SEND-*.html` in a browser. A red
**PREVIEW ONLY - NOT FOR SEND** banner is expected, and the review link points to
`#unresolved-google-review-url`. The `out/` folder is gitignored.

## 4. Set up a private ledger and config (once Will supplies the inputs)

```bash
python3 automation/review-requests/review_requests.py ledger-init       # creates ~/.pid-private/review-requests/ledger.csv
cp automation/review-requests/config.example.json automation/review-requests/config.local.json
```

In `config.local.json` (gitignored), fill in **only** values Will has confirmed:

* `google_review_url`: the Google Business Profile **Get more reviews** link, after a person has
  tested it on desktop and mobile. Set `google_review_url_verified: true`, plus
  `google_review_url_verified_by` and `google_review_url_verified_on`.
* `business_postal_address` (use `\n` between lines) and `business_postal_address_confirmed_by_owner: true`.
* Optional: `business_phone` + `business_phone_confirmed_by_owner: true`.
* Optional QR: generate a PNG locally from the verified URL (black on white, quiet zone of at least
  4 modules, about 180px) and scan-test it. Host it at a PID-owned https URL, then set `qr_image_url`
  and `qr_image_file` (the local path). Without both, the QR section is removed.

Then run `check-config` and confirm there are no blockers.

## 5. Internal test batch (needs Will's explicit OK for the test recipients)

1. Add rows to the **private** ledger (not the repo) for internal test mailboxes only, such as one
   Will names. Use opaque IDs like `HH-TEST-01` / `PRJ-TEST-01`, fill in the evidence columns,
   and set `status=verified`.
2. `python3 automation/review-requests/review_requests.py send` → writes
   `~/.pid-private/review-requests/out/batches/BATCH-<id>.json` and exits with code 3 (expected).
3. Will reviews the batch and the renders, then creates `BATCH-<id>.approval.json` next to it:

   ```json
   {
     "batch_id": "BATCH-<id from the batch file>",
     "batch_sha256": "<batch_sha256 from the batch file>",
     "approved_by": "Will Lipford",
     "approved_at": "2026-11-20T09:00:00-05:00",
     "expires_at": "2026-11-21T09:00:00-05:00",
     "statement": "I approve this exact batch"
   }
   ```

4. `python3 automation/review-requests/review_requests.py send --batch <batch.json> --approval <approval.json>`
   → re-checks the ledger and writes `.eml` files to `out/approved-outbox/BATCH-<id>/`.
5. Open the `.eml` files in a mail client to inspect them. Any actual send is a separate manual
   step from the PID Gmail account, with Will's approval. After sending, record `initial_sent_at`
   and `status=sent` in the ledger once the message shows up in Sent mail.

## 6. Things that must fail (spot checks)

* `render --kind initial` without `--preview` while blockers remain → `REFUSED`.
* A ledger path inside the repo, for example `--ledger automation/review-requests/ledger.csv`
  → `REFUSED`.
* An approval with a wrong hash, an expired `expires_at`, or a window over 72 hours → `REFUSED`.
* Editing a template after a batch is approved → `REFUSED` (templates changed).
