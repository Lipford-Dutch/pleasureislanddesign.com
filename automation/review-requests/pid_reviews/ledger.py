"""Private CSV ledger: the single source of truth for review requests (SOP section 4).

The real ledger lives OUTSIDE the git repo (default ~/.pid-private/review-requests/ledger.csv,
override with $PID_REVIEW_LEDGER or config "ledger_path"). Gmail labels are only views.
"""
import csv
from pathlib import Path

from .paths import check_ledger_path

FIELDS = [
    "household_id",            # opaque, e.g. HH-0001 (never derived from name/address/email)
    "project_id",              # opaque, e.g. PRJ-0001
    "first_name",              # optional, human-verified preferred first name
    "recipient_email",         # one verified mailbox for this household (private)
    "mailbox_verified",        # yes/no: mailbox belongs to this homeowner customer
    "customer_role",           # homeowner | contractor | unknown
    "project_scope",           # kitchen_cabinets | other | (blank = unknown)
    "completion_verified",     # yes/no: INDEPENDENT completion proof (not invoice/payment)
    "completion_evidence_ref", # private pointer to sign-off / install-complete confirmation
    "completion_date",         # YYYY-MM-DD documented completion date
    "final_invoice_issued",    # yes/no: final invoice exists for this same project
    "invoice_ref",             # private pointer to the final invoice
    "invoice_date",            # YYYY-MM-DD final invoice issue date
    "same_project_confirmed",  # yes/no: completion + invoice proofs are the same household/project
    "open_issue",              # yes/no: open cancellation, unfinished install, or punch list
    "status",                  # candidate|quarantined|verified|approved|sending|sent|suppressed|paused|replied|reviewed|closed|unknown
    "initial_sent_at",         # YYYY-MM-DD of CONFIRMED initial send (reconciled with Sent mail)
    "reminder_sent_at",        # YYYY-MM-DD of CONFIRMED reminder send
    "reminder_count",          # 0 or 1 (max 1)
    "stop_reason",             # unsubscribe|complaint|bounce|reply|known_review|(blank)
    "service_hold",            # yes/no: neutral, temporary hold (never a sentiment exclusion)
    "service_hold_reason",
    "service_hold_revisit_on", # YYYY-MM-DD, reassess at least weekly
    "notes",                   # operator notes (no message bodies)
]

STATUSES = {"candidate", "quarantined", "verified", "approved", "sending", "sent",
            "suppressed", "paused", "replied", "reviewed", "closed", "unknown"}
STOP_REASONS = {"", "unsubscribe", "complaint", "bounce", "reply", "known_review"}
GLOBAL_STOPS = {"unsubscribe", "complaint", "bounce"}


class LedgerError(Exception):
    pass


def load_ledger(path, repo_root=None):
    path = check_ledger_path(path, repo_root=repo_root)
    if not Path(path).is_file():
        raise LedgerError(f"Ledger not found: {path}. Create one with: review_requests.py ledger-init")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [f for f in FIELDS if f not in (reader.fieldnames or [])]
        if missing:
            raise LedgerError(f"Ledger {path} is missing columns: {', '.join(missing)}")
        rows = []
        for i, row in enumerate(reader, start=2):
            clean = {k: (row.get(k) or "").strip() for k in FIELDS}
            clean["_line"] = i
            rows.append(clean)
    return rows


def init_ledger(path, repo_root=None):
    path = check_ledger_path(path, repo_root=repo_root)
    path = Path(path)
    if path.exists():
        raise LedgerError(f"Ledger already exists, not overwriting: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=FIELDS).writeheader()
    return path
