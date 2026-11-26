"""Eligibility, dedupe, timing, and stop rules from docs/eligibility-and-tracking-SOP.md.

Every uncertainty fails closed (HOLD). Service holds are neutral pauses, never exclusions.
"""
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from .ledger import STATUSES, STOP_REASONS, GLOBAL_STOPS

SEND_INITIAL = "SEND_INITIAL"
SEND_REMINDER = "SEND_REMINDER"
WAIT = "WAIT"        # eligible later; nothing to do today
HOLD = "HOLD"        # needs a human (quarantine / service hold / ambiguity)
EXCLUDE = "EXCLUDE"  # not part of this program (contractor, non-kitchen, bad key)
STOP = "STOP"        # suppressed / replied / reviewed: never contact for reviews again
DONE = "DONE"        # sequence finished (reminder cap reached / window passed)

SEND_ACTIONS = (SEND_INITIAL, SEND_REMINDER)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+'-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


@dataclass
class Decision:
    household_id: str
    project_id: str
    action: str
    reasons: list = field(default_factory=list)
    kind: str = ""          # initial | reminder for send actions
    not_before: str = ""    # YYYY-MM-DD for WAIT
    line: int = 0

    @property
    def key(self):
        return (self.household_id, self.project_id)


def _yes(v):
    return str(v).strip().lower() in ("yes", "y", "true", "1")


def _date(v):
    try:
        return date.fromisoformat(str(v).strip()[:10]) if str(v).strip() else None
    except ValueError:
        return "invalid"


def normalize_email(v):
    # Lowercase only. No Gmail dot/plus folding: it can merge unrelated people (SOP section 8).
    return str(v or "").strip().lower()


def _evidence_problems(r):
    """Return (action, reasons) for evidence failures, or (None, [])."""
    role = r["customer_role"].lower()
    if role == "contractor":
        return EXCLUDE, ["customer_role is contractor (program is homeowners only)"]
    if role != "homeowner":
        return HOLD, ["customer_role unknown; confirm homeowner / non-contractor"]
    scope = r["project_scope"].lower()
    if scope and scope != "kitchen_cabinets":
        return EXCLUDE, [f"project_scope {scope!r} is not a kitchen cabinet project"]
    reasons = []
    if not scope:
        reasons.append("project_scope unknown; confirm kitchen cabinet scope")
    if not (_yes(r["completion_verified"]) and r["completion_evidence_ref"]):
        reasons.append("no independent completion proof (an invoice or payment is NOT completion)")
    cd = _date(r["completion_date"])
    if cd in (None, "invalid"):
        reasons.append("completion_date missing or invalid (unknown date fails closed)")
    if not (_yes(r["final_invoice_issued"]) and r["invoice_ref"]):
        reasons.append("final invoice not documented for this project")
    if _date(r["invoice_date"]) in (None, "invalid"):
        reasons.append("invoice_date missing or invalid")
    if not _yes(r["same_project_confirmed"]):
        reasons.append("completion and invoice proofs not confirmed as the same household/project")
    if _yes(r["open_issue"]):
        reasons.append("open cancellation, unfinished install, or punch list contradicts completion")
    email = r["recipient_email"]
    if not _yes(r["mailbox_verified"]) or not email:
        reasons.append("recipient mailbox not verified for this homeowner")
    elif any(c in email for c in "\r\n,;") or not EMAIL_RE.match(email):
        reasons.append("recipient_email is not a single valid address")
    return (HOLD, reasons) if reasons else (None, [])


def evaluate(rows, today=None, cfg=None):
    """Return one Decision per ledger row."""
    cfg = cfg or {}
    today = today or date.today()
    wait_days = int(cfg.get("initial_wait_days", 7))
    rem_min = int(cfg.get("reminder_min_days", 10))
    rem_max = int(cfg.get("reminder_max_days", 14))
    stale = int(cfg.get("stale_after_days", 90))

    by_key = defaultdict(list)
    households_by_email = defaultdict(set)
    contacted_households = defaultdict(set)   # household -> projects with an initial attempt
    suppressed_emails, suppressed_households = set(), set()
    for r in rows:
        by_key[(r["household_id"], r["project_id"])].append(r)
        if r["recipient_email"]:
            households_by_email[normalize_email(r["recipient_email"])].add(r["household_id"])
        if r["initial_sent_at"] or r["status"] in ("approved", "sending", "sent", "unknown"):
            contacted_households[r["household_id"]].add(r["project_id"])
        if r["stop_reason"].lower() in GLOBAL_STOPS or r["status"] == "suppressed":
            suppressed_households.add(r["household_id"])
            if r["recipient_email"]:
                suppressed_emails.add(normalize_email(r["recipient_email"]))

    decisions = []
    for r in rows:
        hh, pj = r["household_id"], r["project_id"]
        d = Decision(hh, pj, HOLD, line=r.get("_line", 0))
        decisions.append(d)
        email = normalize_email(r["recipient_email"])
        status = r["status"].lower()
        stop = r["stop_reason"].lower()

        if not hh or not pj:
            d.action, d.reasons = EXCLUDE, ["missing household_id or project_id"]
            continue
        if len(by_key[(hh, pj)]) > 1:
            d.reasons = ["duplicate ledger rows for this household+project; reconcile to one row"]
            continue
        if stop not in STOP_REASONS:
            d.reasons = [f"unknown stop_reason {stop!r}"]
            continue
        if status not in STATUSES:
            d.reasons = [f"unknown status {status!r}"]
            continue
        # Stop conditions: always win over everything else, including approvals.
        if hh in suppressed_households or (email and email in suppressed_emails):
            d.action = STOP
            d.reasons = [f"global marketing suppression ({stop or 'suppressed on a related row'}); never email again for reviews"]
            continue
        if stop == "reply" or status == "replied":
            d.action, d.reasons = STOP, ["customer replied; automatic follow-up stopped, a human reads the reply"]
            continue
        if stop == "known_review" or status == "reviewed":
            d.action, d.reasons = STOP, ["known review (any rating) or customer said they already reviewed"]
            continue
        if status == "closed":
            d.action, d.reasons = DONE, ["closed in ledger"]
            continue
        if status in ("unknown", "sending"):
            d.reasons = ["send outcome not reconciled; check Sent mail before anything else (no blind retry)"]
            continue
        if _yes(r["service_hold"]) or status == "paused":
            revisit = _date(r["service_hold_revisit_on"])
            why = r["service_hold_reason"] or "service/delivery hold"
            msg = f"service hold (neutral pause, not an exclusion): {why}"
            if revisit in (None, "invalid"):
                msg += "; set service_hold_revisit_on (reassess at least weekly)"
            elif revisit <= today:
                msg += f"; revisit due since {revisit.isoformat()}"
            else:
                msg += f"; revisit on {revisit.isoformat()}"
            d.reasons = [msg]
            continue
        if status == "quarantined":
            d.reasons = ["quarantined in ledger; human must resolve the ambiguity"]
            continue

        action, reasons = _evidence_problems(r)
        if action:
            d.action, d.reasons = action, reasons
            continue
        completion = _date(r["completion_date"])
        invoice = _date(r["invoice_date"])
        if email and len(households_by_email[email]) > 1:
            d.reasons = ["same mailbox appears under more than one household; a human decides"]
            continue

        try:
            reminders = int(r["reminder_count"] or 0)
        except ValueError:
            d.reasons = ["reminder_count is not a number"]
            continue
        initial_sent = _date(r["initial_sent_at"])
        if initial_sent == "invalid":
            d.reasons = ["initial_sent_at is not a valid date"]
            continue

        if initial_sent is None:
            # ---- initial request -------------------------------------------------
            if reminders or r["reminder_sent_at"]:
                d.reasons = ["reminder recorded without a confirmed initial send; reconcile"]
                continue
            if status != "verified" and status != "approved":
                d.reasons = [f"status is {status!r}; an operator must mark the row 'verified' after the evidence audit"]
                continue
            others = contacted_households[hh] - {pj}
            if others:
                d.reasons = ["household already contacted under another project; a new initial needs fresh human approval"]
                continue
            earliest = max(completion, invoice) + timedelta(days=wait_days)
            if (today - completion).days > stale:
                d.reasons = [f"stale historical record (> {stale} days since completion): manual reconfirmation; no default reminder"]
                continue
            if today < earliest:
                d.action, d.not_before = WAIT, earliest.isoformat()
                d.reasons = [f"courtesy wait: earliest initial is {earliest.isoformat()} ({wait_days} days after the later of completion and invoice)"]
                continue
            d.action, d.kind = SEND_INITIAL, "initial"
            d.reasons = ["all eligibility evidence present; one initial request per household+project"]
            continue

        # ---- reminder ---------------------------------------------------------
        if status != "sent":
            d.reasons = [f"initial_sent_at is set but status is {status!r}; reconcile"]
            continue
        if reminders >= 1 or r["reminder_sent_at"]:
            d.action, d.reasons = DONE, ["reminder cap reached (max 1); sequence finished"]
            if reminders > 1:
                d.action, d.reasons = HOLD, ["reminder_count > 1 violates the cap; audit this record"]
            continue
        if (initial_sent - completion).days > stale:
            d.action, d.reasons = DONE, ["historical (stale) outreach: no default reminder"]
            continue
        age = (today - initial_sent).days
        if age < rem_min:
            nb = initial_sent + timedelta(days=rem_min)
            d.action, d.not_before = WAIT, nb.isoformat()
            d.reasons = [f"reminder not before {nb.isoformat()} ({rem_min} days after confirmed initial)"]
            continue
        if age > rem_max:
            d.action, d.reasons = DONE, [f"reminder window ({rem_min}-{rem_max} days) passed; no reminder"]
            continue
        d.action, d.kind = SEND_REMINDER, "reminder"
        d.reasons = ["single reminder: confirmed initial, no reply/opt-out/review/bounce/hold"]

    # Batch-level dedupe: never two sends to one household or one mailbox in a run.
    rows_by_key = {(r["household_id"], r["project_id"]): r for r in rows}
    seen_hh, seen_mail = defaultdict(list), defaultdict(list)
    for d in decisions:
        if d.action in SEND_ACTIONS:
            seen_hh[d.household_id].append(d)
            seen_mail[normalize_email(rows_by_key[d.key]["recipient_email"])].append(d)
    for group in list(seen_hh.values()) + list(seen_mail.values()):
        if len(group) > 1:
            for d in group:
                d.action, d.kind = HOLD, ""
                d.reasons = ["more than one request for the same household/mailbox in this run; a human picks one"]
    return decisions
