"""Approval batches. Nothing here sends email or calls any mail API.

Flow (SOP section 12):
1. `send` without an approval file -> writes batch-<id>.json (opaque IDs, recipient hashes,
   template hashes, review URL, address hash) for Will to review, then exits non-zero.
2. Will writes batch-<id>.approval.json (see docs/how-to-test.md) naming the exact batch hash.
3. `send --batch ... --approval ...` re-checks the ledger (preflight), re-renders, and writes
   an approved outbox of .eml files for a human / future sender. STILL SENDS NOTHING.
Any template, URL, address, recipient, or eligibility change invalidates the approval.
"""
import hashlib
import json
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

from .eligibility import SEND_ACTIONS, evaluate, normalize_email
from .paths import TEMPLATE_DIR
from .render import QR_CID_URL, qr_ready, render

SENDER = "pleasureislanddesign@gmail.com"
FROM_DISPLAY = "Nicole Rayment | Pleasure Island Design"
APPROVAL_STATEMENT = "I approve this exact batch"


class BatchError(Exception):
    pass


def _sha(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def template_hashes():
    return {p.name: _sha(p.read_bytes()) for p in sorted(TEMPLATE_DIR.glob("review-request-*.*"))}


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def batch_digest(batch):
    body = {k: v for k, v in batch.items() if k != "batch_sha256"}
    return _sha(_canonical(body))


def _qr_sha(cfg):
    if not qr_ready(cfg):
        return ""
    return _sha(Path(cfg["qr_image_file"]).read_bytes())


def build_batch(rows, cfg, today, now=None):
    from .config import config_blockers

    blockers = config_blockers(cfg)
    if blockers:
        raise BatchError("cannot prepare a send batch while launch blockers remain:\n  - " + "\n  - ".join(blockers))
    now = now or datetime.now(timezone.utc)
    by_key = {(r["household_id"], r["project_id"]): r for r in rows}
    entries = []
    for d in evaluate(rows, today=today, cfg=cfg):
        if d.action not in SEND_ACTIONS:
            continue
        r = by_key[d.key]
        msg = render(d.kind, r, cfg, preview=False)
        entries.append({
            "request_id": f"REQ-{_sha(f'{d.household_id}|{d.project_id}|{d.kind}')[:12]}",
            "household_id": d.household_id,
            "project_id": d.project_id,
            "kind": d.kind,
            "template_version": msg.template_version,
            "recipient_sha256": _sha(normalize_email(r["recipient_email"])),
            "message_sha256": _sha(msg.text + "\0" + msg.html),
        })
    if not entries:
        raise BatchError("nothing is eligible to send today; see `plan` for reasons")
    batch = {
        "type": "pid-review-request-batch",
        "created_at": now.isoformat(timespec="seconds"),
        "plan_date": today.isoformat(),
        "sender": f"{FROM_DISPLAY} <{SENDER}>",
        "google_review_url": cfg["google_review_url"],
        "postal_address_sha256": _sha(cfg["business_postal_address"].strip()),
        "qr_included": qr_ready(cfg),
        "qr_sha256": _qr_sha(cfg),
        "template_sha256": template_hashes(),
        "count": len(entries),
        "entries": entries,
        "status": "AWAITING_APPROVAL - nothing has been sent",
    }
    batch["batch_id"] = "BATCH-" + batch_digest(batch)[:12]
    batch["batch_sha256"] = batch_digest(batch)
    return batch


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return Path(path)


def _parse_ts(value, label):
    try:
        ts = datetime.fromisoformat(str(value))
    except ValueError:
        raise BatchError(f"approval {label} is not an ISO-8601 timestamp: {value!r}")
    if ts.tzinfo is None:
        raise BatchError(f"approval {label} must include a UTC offset, e.g. 2026-11-20T09:00:00-05:00")
    return ts


def verify_approval(batch, approval, cfg, now=None):
    now = now or datetime.now(timezone.utc)
    if batch_digest(batch) != batch.get("batch_sha256"):
        raise BatchError("batch file was modified after it was generated")
    for key in ("batch_id", "batch_sha256", "approved_by", "approved_at", "expires_at", "statement"):
        if not approval.get(key):
            raise BatchError(f"approval file is missing {key!r}")
    if approval["batch_id"] != batch["batch_id"] or approval["batch_sha256"] != batch["batch_sha256"]:
        raise BatchError("approval does not match this exact batch (id/hash differ)")
    if approval["statement"].strip() != APPROVAL_STATEMENT:
        raise BatchError(f"approval statement must read exactly: {APPROVAL_STATEMENT!r}")
    approved_at = _parse_ts(approval["approved_at"], "approved_at")
    expires_at = _parse_ts(approval["expires_at"], "expires_at")
    if expires_at <= approved_at:
        raise BatchError("approval expires before it was given")
    if expires_at - approved_at > timedelta(hours=int(cfg.get("approval_max_hours", 72))):
        raise BatchError(f"approval window longer than {cfg.get('approval_max_hours', 72)} hours")
    if now >= expires_at:
        raise BatchError("approval has expired; prepare and approve a new batch")
    if approved_at > now + timedelta(minutes=5):
        raise BatchError("approval is dated in the future")
    if template_hashes() != batch["template_sha256"]:
        raise BatchError("templates changed since the batch was approved; approval invalidated")
    if cfg.get("google_review_url") != batch["google_review_url"]:
        raise BatchError("review URL changed since the batch was approved; approval invalidated")
    if _sha((cfg.get("business_postal_address") or "").strip()) != batch["postal_address_sha256"]:
        raise BatchError("postal address changed since the batch was approved; approval invalidated")
    if _qr_sha(cfg) != batch.get("qr_sha256", ""):
        raise BatchError("QR image changed since the batch was approved; approval invalidated")
    return True


def build_outbox(batch, approval, rows, cfg, today, out_dir, now=None):
    """Preflight + write .eml files for an approved batch. Does NOT send anything."""
    verify_approval(batch, approval, cfg, now=now)
    current = build_batch(rows, cfg, today=today, now=now)
    want = {(e["household_id"], e["project_id"], e["kind"], e["recipient_sha256"], e["message_sha256"]) for e in batch["entries"]}
    have = {(e["household_id"], e["project_id"], e["kind"], e["recipient_sha256"], e["message_sha256"]) for e in current["entries"]}
    missing = want - have
    if missing:
        raise BatchError("preflight failed: these approved entries are no longer eligible or changed: "
                         + ", ".join(f"{h}/{p}/{k}" for h, p, k, _, _ in sorted(missing)))
    by_key = {(r["household_id"], r["project_id"]): r for r in rows}
    outdir = Path(out_dir) / batch["batch_id"]
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for e in batch["entries"]:
        r = by_key[(e["household_id"], e["project_id"])]
        msg = render(e["kind"], r, cfg, preview=False)
        em = EmailMessage()
        em["From"] = f'"{FROM_DISPLAY}" <{SENDER}>'
        em["To"] = r["recipient_email"]
        em["Reply-To"] = SENDER
        em["Subject"] = msg.subject
        em["X-PID-Request-Id"] = e["request_id"]
        em["X-PID-Batch-Id"] = batch["batch_id"]
        em["X-PID-Template-Version"] = msg.template_version
        em.set_content(msg.text)
        em.add_alternative(msg.html, subtype="html")
        if f'src="{QR_CID_URL}"' in msg.html:
            em.get_body(("html",)).add_related(Path(cfg["qr_image_file"]).read_bytes(), "image", "png",
                                               cid="<" + QR_CID_URL[4:] + ">", disposition="inline",
                                               filename="pid-google-review-qr.png")
        path = outdir / f"{e['request_id']}.eml"
        path.write_bytes(bytes(em))
        written.append(path)
    write_json(outdir / "OUTBOX-NOT-SENT.json", {
        "batch_id": batch["batch_id"],
        "approved_by": approval["approved_by"],
        "files": [p.name for p in written],
        "note": "Approved outbox only. This tool has no mail integration and sent nothing. "
                "Record each real send in the ledger only after it is visible in Sent mail.",
    })
    return written

