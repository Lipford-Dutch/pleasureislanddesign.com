import unittest
from datetime import date

from helpers import cfg, row
from pid_reviews.eligibility import (DONE, EXCLUDE, HOLD, SEND_INITIAL, SEND_REMINDER, STOP, WAIT, evaluate)

TODAY = date(2026, 11, 20)


def one(r, today=TODAY, **c):
    return evaluate([r], today=today, cfg=cfg(**c))[0]


class EligibilityRules(unittest.TestCase):
    def test_fully_evidenced_verified_row_gets_initial(self):
        d = one(row())
        self.assertEqual(d.action, SEND_INITIAL)
        self.assertEqual(d.kind, "initial")

    def test_invoice_without_completion_proof_is_held(self):
        d = one(row(completion_verified="no", completion_evidence_ref=""))
        self.assertEqual(d.action, HOLD)
        self.assertIn("NOT completion", d.reasons[0])

    def test_completion_flag_without_evidence_ref_is_held(self):
        self.assertEqual(one(row(completion_evidence_ref="")).action, HOLD)

    def test_missing_final_invoice_is_held(self):
        self.assertEqual(one(row(final_invoice_issued="no")).action, HOLD)

    def test_unknown_completion_date_fails_closed(self):
        self.assertEqual(one(row(completion_date="")).action, HOLD)
        self.assertEqual(one(row(completion_date="soon")).action, HOLD)

    def test_contractor_excluded_unknown_role_held(self):
        self.assertEqual(one(row(customer_role="contractor")).action, EXCLUDE)
        self.assertEqual(one(row(customer_role="")).action, HOLD)

    def test_non_kitchen_excluded_unknown_scope_held(self):
        self.assertEqual(one(row(project_scope="bathroom_vanity")).action, EXCLUDE)
        self.assertEqual(one(row(project_scope="")).action, HOLD)

    def test_proofs_for_different_jobs_held(self):
        self.assertEqual(one(row(same_project_confirmed="no")).action, HOLD)

    def test_open_punch_list_held(self):
        self.assertEqual(one(row(open_issue="yes")).action, HOLD)

    def test_unverified_or_bad_mailbox_held(self):
        self.assertEqual(one(row(mailbox_verified="no")).action, HOLD)
        self.assertEqual(one(row(recipient_email="a@example.invalid, b@example.invalid")).action, HOLD)
        self.assertEqual(one(row(recipient_email="a@example.invalid\r\nBcc: x@example.invalid")).action, HOLD)

    def test_candidate_status_needs_operator_verification(self):
        self.assertEqual(one(row(status="candidate")).action, HOLD)

    def test_quarantined_held(self):
        self.assertEqual(one(row(status="quarantined")).action, HOLD)

    def test_courtesy_wait_uses_later_of_completion_and_invoice(self):
        d = one(row(completion_date="2026-11-15", invoice_date="2026-11-18"))
        self.assertEqual(d.action, WAIT)
        self.assertEqual(d.not_before, "2026-11-25")

    def test_stale_historical_record_needs_manual_review(self):
        d = one(row(completion_date="2026-07-01", invoice_date="2026-07-02"))
        self.assertEqual(d.action, HOLD)
        self.assertIn("stale", d.reasons[0])


class StopConditions(unittest.TestCase):
    def test_unsubscribe_complaint_bounce_stop(self):
        for reason in ("unsubscribe", "complaint", "bounce"):
            self.assertEqual(one(row(stop_reason=reason)).action, STOP, reason)

    def test_global_suppression_applies_to_other_projects_and_households_sharing_mailbox(self):
        rows = [row(household_id="HH-A", project_id="P1", stop_reason="unsubscribe", status="suppressed"),
                row(household_id="HH-A", project_id="P2"),
                row(household_id="HH-B", project_id="P3", recipient_email="T1@EXAMPLE.INVALID")]
        actions = [d.action for d in evaluate(rows, today=TODAY, cfg=cfg())]
        self.assertEqual(actions, [STOP, STOP, STOP])

    def test_reply_stops(self):
        self.assertEqual(one(row(stop_reason="reply", status="sent", initial_sent_at="2026-11-08")).action, STOP)

    def test_known_review_stops(self):
        self.assertEqual(one(row(stop_reason="known_review")).action, STOP)

    def test_unknown_send_outcome_held(self):
        self.assertEqual(one(row(status="unknown")).action, HOLD)
        self.assertEqual(one(row(status="sending")).action, HOLD)

    def test_unknown_stop_reason_held(self):
        self.assertEqual(one(row(stop_reason="angry")).action, HOLD)


class ServiceHold(unittest.TestCase):
    def test_service_hold_is_neutral_pause_with_revisit(self):
        d = one(row(service_hold="yes", service_hold_reason="touch-up", service_hold_revisit_on="2026-11-27"))
        self.assertEqual(d.action, HOLD)
        self.assertIn("neutral", d.reasons[0])
        self.assertIn("revisit on 2026-11-27", d.reasons[0])

    def test_overdue_revisit_is_flagged(self):
        d = one(row(service_hold="yes", service_hold_revisit_on="2026-11-10"))
        self.assertIn("revisit due", d.reasons[0])

    def test_hold_released_returns_to_normal_eligibility(self):
        self.assertEqual(one(row(service_hold="no")).action, SEND_INITIAL)


class DedupeAndReminders(unittest.TestCase):
    def test_duplicate_rows_for_same_household_project_held(self):
        ds = evaluate([row(), row()], today=TODAY, cfg=cfg())
        self.assertEqual([d.action for d in ds], [HOLD, HOLD])

    def test_household_already_contacted_on_other_project_held(self):
        rows = [row(project_id="P1", status="sent", initial_sent_at="2026-10-01", reminder_count="1",
                    reminder_sent_at="2026-10-12"),
                row(project_id="P2")]
        ds = evaluate(rows, today=TODAY, cfg=cfg())
        self.assertEqual(ds[1].action, HOLD)
        self.assertIn("another project", ds[1].reasons[0])

    def test_two_eligible_projects_one_household_held_in_same_run(self):
        ds = evaluate([row(project_id="P1"), row(project_id="P2")], today=TODAY, cfg=cfg())
        self.assertEqual([d.action for d in ds], [HOLD, HOLD])

    def test_same_mailbox_under_two_households_held(self):
        ds = evaluate([row(household_id="HH-A"), row(household_id="HH-B")], today=TODAY, cfg=cfg())
        self.assertEqual([d.action for d in ds], [HOLD, HOLD])

    def test_initial_never_repeated(self):
        d = one(row(status="sent", initial_sent_at="2026-11-18"))
        self.assertNotEqual(d.action, SEND_INITIAL)

    def test_reminder_window(self):
        sent = row(status="sent", initial_sent_at="2026-11-05")
        self.assertEqual(one(sent, today=date(2026, 11, 14)).action, WAIT)
        self.assertEqual(one(sent, today=date(2026, 11, 15)).action, SEND_REMINDER)
        self.assertEqual(one(sent, today=date(2026, 11, 19)).action, SEND_REMINDER)
        self.assertEqual(one(sent, today=date(2026, 11, 20)).action, DONE)

    def test_reminder_cap_is_one(self):
        d = one(row(status="sent", initial_sent_at="2026-11-05", reminder_count="1",
                    reminder_sent_at="2026-11-16"), today=date(2026, 11, 17))
        self.assertEqual(d.action, DONE)
        self.assertIn("max 1", d.reasons[0])

    def test_reminder_count_over_cap_flagged(self):
        d = one(row(status="sent", initial_sent_at="2026-11-05", reminder_count="2"), today=date(2026, 11, 17))
        self.assertEqual(d.action, HOLD)

    def test_no_default_reminder_for_stale_historical_outreach(self):
        d = one(row(completion_date="2026-06-01", invoice_date="2026-06-02", status="sent",
                    initial_sent_at="2026-11-08"), today=date(2026, 11, 19))
        self.assertEqual(d.action, DONE)

    def test_reminder_without_initial_is_held(self):
        self.assertEqual(one(row(reminder_count="1")).action, HOLD)


if __name__ == "__main__":
    unittest.main()
