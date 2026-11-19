#!/usr/bin/env python3
"""Entry point: python automation/review-requests/review_requests.py [command] ...

Dry-run planner for PID review requests. It never sends email. See README.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pid_reviews.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
