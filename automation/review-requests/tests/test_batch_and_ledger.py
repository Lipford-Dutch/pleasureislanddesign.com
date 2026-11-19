import csv
import json
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from email import message_from_bytes
from pathlib import Path

from helpers import cfg, ready_cfg, row
from pid_reviews.batch import APPROVAL_STATEMENT, BatchError, build_batch, build_outbox, verify_approval
from pid_reviews.cli import main
from pid_reviews.ledger import FIELDS, LedgerError, init_ledger, load_ledger
from pid_reviews.paths import PrivatePathError, check_ledger_path, check_output_dir

TODAY = date(2026, 11, 20)
NOW = datetime(2026, 11, 20, 15, 0, tzinfo=timezone.utc)


def approval_for(batch, hours=24, **kw):
    a = {"batch_id": batch["batch_id"], "batch_sha256": batch["batch_sha256"], "approved_by": "unit-test",
         "approved_at": NOW.isoformat(), "expires_at": (NOW + timedelta(hours=hours)).isoformat(),
         "statement": APPROVAL_STATEMENT}
    a.update(kw)
    return a


class Batches(unittest.TestCase):
    def test_batch_refused_while_launch_blockers_remain(self):
        with self.assertRaises(BatchError):
            build_batch([row()], cfg(), today=TODAY, now=NOW)

    def test_batch_contains_only_opaque_ids_and_hashes(self):
        b = build_batch([row(), row(household_id="HH-X", project_id="P-X", customer_role="contractor",
                                    recipient_email="x@example.invalid")], ready_cfg(), today=TODAY, now=NOW)
        self.assertEqual(b["count"], 1)
        self.assertNotIn("t1@example.invalid", json.dumps(b))

    def test_nothing_eligible_refused(self):
        with self.assertRaises(BatchError):
            build_batch([row(stop_reason="unsubscribe")], ready_cfg(), today=TODAY, now=NOW)

    def test_approval_must_match_and_be_unexpired(self):
        c = ready_cfg()
        b = build_batch([row()], c, today=TODAY, now=NOW)
        self.assertTrue(verify_approval(b, approval_for(b), c, now=NOW))
        bad = [approval_for(b, batch_sha256="0" * 64), approval_for(b, statement="ok"),
               approval_for(b, hours=100), approval_for(b, approved_by="")]
        for a in bad:
            with self.assertRaises(BatchError):
                verify_approval(b, a, c, now=NOW)
        with self.assertRaises(BatchError):
            verify_approval(b, approval_for(b), c, now=NOW + timedelta(hours=25))

    def test_approval_invalidated_by_config_or_batch_change(self):
        c = ready_cfg()
        b = build_batch([row()], c, today=TODAY, now=NOW)
        a = approval_for(b)
        with self.assertRaises(BatchError):
            verify_approval(b, a, ready_cfg(business_postal_address="OTHER FAKE ADDRESS"), now=NOW)
        tampered = dict(b, count=5)
        with self.assertRaises(BatchError):
            verify_approval(tampered, a, c, now=NOW)

    def test_outbox_preflight_blocks_newly_suppressed_rows(self):
        c = ready_cfg()
        b = build_batch([row()], c, today=TODAY, now=NOW)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(BatchError):
                build_outbox(b, approval_for(b), [row(stop_reason="unsubscribe")], c, TODAY, tmp, now=NOW)

    def test_outbox_writes_eml_but_sends_nothing(self):
        c = ready_cfg()
        b = build_batch([row(first_name="Sam")], c, today=TODAY, now=NOW)
        with tempfile.TemporaryDirectory() as tmp:
            files = build_outbox(b, approval_for(b), [row(first_name="Sam")], c, TODAY, tmp, now=NOW)
            self.assertEqual(len(files), 1)
            msg = message_from_bytes(files[0].read_bytes())
            self.assertEqual(msg["To"], "t1@example.invalid")
            self.assertIn("pleasureislanddesign@gmail.com", msg["From"])
            self.assertEqual(msg.get_content_type(), "multipart/alternative")
            self.assertTrue((files[0].parent / "OUTBOX-NOT-SENT.json").is_file())


    def test_outbox_embeds_inline_qr_and_qr_change_invalidates_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "qr.png"
            png.write_bytes(b"\x89PNG fake qr")
            c = ready_cfg(qr_image_url="cid:pid-review-qr", qr_image_file=str(png))
            b = build_batch([row()], c, today=TODAY, now=NOW)
            self.assertTrue(b["qr_included"])
            files = build_outbox(b, approval_for(b), [row()], c, TODAY, Path(tmp) / "o", now=NOW)
            msg = message_from_bytes(files[0].read_bytes())
            imgs = [p for p in msg.walk() if p.get_content_type() == "image/png"]
            self.assertEqual(len(imgs), 1)
            self.assertEqual(imgs[0]["Content-ID"], "<pid-review-qr>")
            png.write_bytes(b"\x89PNG different")
            with self.assertRaises(BatchError):
                verify_approval(b, approval_for(b), c, now=NOW)


class LedgerAndPaths(unittest.TestCase):
    def test_ledger_inside_repo_refused_but_example_allowed(self):
        with tempfile.TemporaryDirectory() as repo:
            with self.assertRaises(PrivatePathError):
                check_ledger_path(Path(repo) / "ledger.csv", repo_root=Path(repo))
            check_ledger_path(Path(repo) / "ledger.example.csv", repo_root=Path(repo))

    def test_output_inside_repo_refused(self):
        with tempfile.TemporaryDirectory() as repo:
            with self.assertRaises(PrivatePathError):
                check_output_dir(Path(repo) / "out", repo_root=Path(repo))

    def test_init_and_load_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "private" / "ledger.csv"
            init_ledger(p, repo_root=None)
            self.assertEqual(load_ledger(p), [])
            with self.assertRaises(LedgerError):
                init_ledger(p)

    def test_missing_columns_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "ledger.csv"
            p.write_text("household_id,project_id\nHH,PRJ\n", encoding="utf-8")
            with self.assertRaises(LedgerError):
                load_ledger(p)

    def test_example_ledger_is_fake_only(self):
        p = Path(__file__).resolve().parent.parent / "examples" / "ledger.example.csv"
        with open(p, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(list(rows[0].keys()), FIELDS)
        for r in rows:
            self.assertTrue(r["household_id"].startswith("HH-FAKE-"))
            self.assertTrue(r["recipient_email"].endswith("@example.invalid"))


class Cli(unittest.TestCase):
    def _ledger(self, tmp, rows):
        p = Path(tmp) / "ledger.csv"
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        return p

    def test_default_command_is_dry_run_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main(["--ledger", str(self._ledger(tmp, [row()])), "--today", "2026-11-20"]), 0)

    def test_send_without_approval_only_writes_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "config.json"
            conf.write_text(json.dumps({k: v for k, v in ready_cfg().items()}), encoding="utf-8")
            led = self._ledger(tmp, [row()])
            rc = main(["--config", str(conf), "--ledger", str(led), "--today", "2026-11-20", "send", "--out", tmp])
            self.assertEqual(rc, 3)
            self.assertEqual(len(list((Path(tmp) / "batches").glob("BATCH-*.json"))), 1)
            self.assertFalse((Path(tmp) / "approved-outbox").exists())

    def test_send_refused_with_blocked_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "config.json"
            conf.write_text("{}", encoding="utf-8")
            led = self._ledger(tmp, [row()])
            self.assertEqual(main(["--config", str(conf), "--ledger", str(led), "--today", "2026-11-20", "send", "--out", tmp]), 2)


if __name__ == "__main__":
    unittest.main()
