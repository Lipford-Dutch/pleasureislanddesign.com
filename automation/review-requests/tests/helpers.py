"""Shared FAKE fixtures. Nothing here is a real customer, URL, address, or phone."""
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from pid_reviews.config import DEFAULTS  # noqa: E402
from pid_reviews.ledger import FIELDS  # noqa: E402

FAKE_REVIEW_URL = "https://g.page/r/FAKE-TEST-ONLY-NOT-A-REAL-LISTING/review"
FAKE_ADDRESS = "FAKE TEST ADDRESS LINE 1\nFAKE CITY, ZZ 00000"


def cfg(**overrides):
    c = dict(DEFAULTS)
    c.update(overrides)
    return c


def ready_cfg(**overrides):
    c = cfg(google_review_url=FAKE_REVIEW_URL, google_review_url_verified=True,
            google_review_url_verified_by="unit-test", google_review_url_verified_on="2026-11-19",
            business_postal_address=FAKE_ADDRESS, business_postal_address_confirmed_by_owner=True)
    c.update(overrides)
    return c


def row(**kw):
    r = dict.fromkeys(FIELDS, "")
    r.update(household_id="HH-T1", project_id="PRJ-T1", recipient_email="t1@example.invalid",
             mailbox_verified="yes", customer_role="homeowner", project_scope="kitchen_cabinets",
             completion_verified="yes", completion_evidence_ref="FAKE-EV", completion_date="2026-11-01",
             final_invoice_issued="yes", invoice_ref="FAKE-INV", invoice_date="2026-11-02",
             same_project_confirmed="yes", open_issue="no", status="verified", reminder_count="0",
             service_hold="no")
    r.update(kw)
    return r
