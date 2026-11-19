"""Command line interface. Dry-run by default; no command sends email."""
import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from . import __version__
from .batch import BatchError, build_batch, build_outbox, write_json
from .config import config_blockers, ledger_path, load_config, output_dir
from .eligibility import SEND_ACTIONS, evaluate
from .ledger import LedgerError, init_ledger, load_ledger
from .paths import PrivatePathError, TOOL_OUT_DIR, check_output_dir
from .render import RenderError, render

NO_SEND = "No email was sent. This tool has no mail integration."
SAMPLE_RECORD = {"household_id": "HH-SAMPLE", "project_id": "PRJ-SAMPLE", "first_name": ""}


def _today(args):
    return date.fromisoformat(args.today) if args.today else date.today()


def cmd_check_config(args, cfg):
    print(f"config: {cfg['_source']}")
    print(f"ledger: {ledger_path(cfg, args.ledger)}")
    print(f"output: {output_dir(cfg, getattr(args, 'out', None))}")
    blockers = config_blockers(cfg)
    if blockers:
        print("LAUNCH BLOCKED:")
        for b in blockers:
            print(f"  - {b}")
        return 2
    print("No config launch blockers. Batches still need Will's per-batch approval.")
    return 0


def cmd_ledger_init(args, cfg):
    path = init_ledger(ledger_path(cfg, args.ledger))
    print(f"Created empty private ledger: {path}")
    return 0


def cmd_plan(args, cfg):
    rows = load_ledger(ledger_path(cfg, args.ledger))
    decisions = evaluate(rows, today=_today(args), cfg=cfg)
    if args.json:
        print(json.dumps([d.__dict__ for d in decisions], indent=2))
    else:
        print(f"DRY RUN plan for {_today(args).isoformat()} ({len(rows)} ledger rows). {NO_SEND}")
        order = ["SEND_INITIAL", "SEND_REMINDER", "WAIT", "HOLD", "STOP", "DONE", "EXCLUDE"]
        for action in order:
            group = [d for d in decisions if d.action == action]
            if not group:
                continue
            print(f"\n{action} ({len(group)})")
            for d in group:
                label = f"{d.household_id or '?'}/{d.project_id or '?'}"
                print(f"  - {label:<28} {'; '.join(d.reasons)}")
    blockers = config_blockers(cfg)
    if blockers and not args.json:
        print("\nLAUNCH BLOCKED (would-send rows above cannot be batched yet):")
        for b in blockers:
            print(f"  - {b}")
    return 0


def cmd_render(args, cfg):
    if args.household or args.project:
        rows = load_ledger(ledger_path(cfg, args.ledger))
        match = [r for r in rows if r["household_id"] == args.household and r["project_id"] == args.project]
        if len(match) != 1:
            print(f"error: expected exactly one ledger row for {args.household}/{args.project}, found {len(match)}", file=sys.stderr)
            return 2
        record = match[0]
    else:
        record = dict(SAMPLE_RECORD)
    msg = render(args.kind, record, cfg, preview=args.preview)
    out = check_output_dir(Path(args.out) if args.out else (TOOL_OUT_DIR / "previews" if args.preview else output_dir(cfg) / "renders"))
    out.mkdir(parents=True, exist_ok=True)
    stem = f"{'PREVIEW-NOT-FOR-SEND-' if msg.preview else ''}{record['household_id']}-{record['project_id']}-{args.kind}"
    (out / f"{stem}.txt").write_text(f"Subject: {msg.subject}\nPreheader: {msg.preheader}\n"
                                     f"template_version: {msg.template_version}\n\n{msg.text}", encoding="utf-8")
    (out / f"{stem}.html").write_text(msg.html, encoding="utf-8")
    print(f"Wrote {out / (stem + '.txt')} and .html")
    if msg.unresolved:
        print(f"PREVIEW ONLY: unresolved {', '.join(msg.unresolved)}")
    print(NO_SEND)
    return 0


def cmd_send(args, cfg):
    rows = load_ledger(ledger_path(cfg, args.ledger))
    today = _today(args)
    out = check_output_dir(Path(args.out) if args.out else output_dir(cfg))
    if not args.approval:
        batch = build_batch(rows, cfg, today=today)
        path = write_json(out / "batches" / f"{batch['batch_id']}.json", batch)
        print(f"Prepared approval batch {batch['batch_id']} with {batch['count']} message(s): {path}")
        print("REFUSING TO GO FURTHER: no approval file. Will must review this batch and create")
        print(f"  {batch['batch_id']}.approval.json (see docs/how-to-test.md), then rerun with")
        print(f"  --batch {path} --approval <approval file>")
        print(NO_SEND)
        return 3
    if not args.batch:
        print("error: --approval requires --batch", file=sys.stderr)
        return 2
    batch = json.loads(Path(args.batch).read_text(encoding="utf-8"))
    approval = json.loads(Path(args.approval).read_text(encoding="utf-8"))
    files = build_outbox(batch, approval, rows, cfg, today=today, out_dir=out / "approved-outbox")
    print(f"Approval verified for {batch['batch_id']}. Wrote {len(files)} .eml file(s) to {files[0].parent}")
    print(NO_SEND + " Record sends in the ledger only once they are visible in Sent mail.")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="review_requests.py", description="PID review-request planner (dry-run, never sends).")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", help="config JSON (default: $PID_REVIEW_CONFIG, config.local.json, config.example.json)")
    p.add_argument("--ledger", help="private ledger CSV (default: $PID_REVIEW_LEDGER or ~/.pid-private/review-requests/ledger.csv)")
    p.add_argument("--today", help="plan date YYYY-MM-DD (default: today, machine local time)")
    sub = p.add_subparsers(dest="command")
    sub.add_parser("check-config", help="show config sources and launch blockers")
    sub.add_parser("ledger-init", help="create an empty private ledger (outside the repo)")
    sp = sub.add_parser("plan", help="DRY RUN (default): who would get what, and why others are excluded")
    sp.add_argument("--json", action="store_true")
    sr = sub.add_parser("render", help="write .txt/.html renders for a ledger row or the anonymous sample")
    sr.add_argument("--kind", choices=["initial", "reminder"], default="initial")
    sr.add_argument("--household")
    sr.add_argument("--project")
    sr.add_argument("--preview", action="store_true", help="allow unresolved blockers, clearly marked NOT FOR SEND")
    sr.add_argument("--out")
    ss = sub.add_parser("send", help="prepare an approval batch; with Will's approval, write an outbox. Never sends.")
    ss.add_argument("--batch")
    ss.add_argument("--approval")
    ss.add_argument("--out")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.command:
        args.command, args.json = "plan", False
    try:
        cfg = load_config(args.config)
        handler = {"check-config": cmd_check_config, "ledger-init": cmd_ledger_init, "plan": cmd_plan,
                   "render": cmd_render, "send": cmd_send}[args.command]
        return handler(args, cfg)
    except (RenderError, BatchError, LedgerError, PrivatePathError, FileNotFoundError, ValueError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        print(NO_SEND, file=sys.stderr)
        return 2
