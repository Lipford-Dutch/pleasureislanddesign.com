"""Configuration loading and launch-blocker checks."""
import json
import os
from pathlib import Path

from .paths import TOOL_DIR, DEFAULT_LEDGER, DEFAULT_OUTPUT

DEFAULTS = {
    "google_review_url": "",
    "google_review_url_verified": False,
    "google_review_url_verified_by": "",
    "google_review_url_verified_on": "",
    "business_postal_address": "",
    "business_postal_address_confirmed_by_owner": False,
    "business_phone": "",
    "business_phone_confirmed_by_owner": False,
    "qr_image_url": "",
    "qr_image_file": "",
    "ledger_path": "",
    "output_dir": "",
    "initial_wait_days": 7,
    "reminder_min_days": 10,
    "reminder_max_days": 14,
    "stale_after_days": 90,
    "approval_max_hours": 72,
}

EXAMPLE_CONFIG = TOOL_DIR / "config.example.json"
LOCAL_CONFIG = TOOL_DIR / "config.local.json"  # gitignored


def load_config(path=None):
    """Load config: explicit path > $PID_REVIEW_CONFIG > config.local.json > config.example.json."""
    explicit = path or os.environ.get("PID_REVIEW_CONFIG")
    if explicit:
        chosen = Path(explicit)
        if not chosen.is_file():
            raise FileNotFoundError(f"Config file not found: {explicit}")
    elif LOCAL_CONFIG.is_file():
        chosen = LOCAL_CONFIG
    elif EXAMPLE_CONFIG.is_file():
        chosen = EXAMPLE_CONFIG
    else:
        chosen = None
    cfg = dict(DEFAULTS)
    if chosen:
        with open(chosen, encoding="utf-8") as fh:
            data = json.load(fh)
        unknown = sorted(k for k in data if k not in DEFAULTS and not k.startswith("_"))
        if unknown:
            raise ValueError(f"Unknown config keys in {chosen}: {', '.join(unknown)}")
        cfg.update({k: v for k, v in data.items() if not k.startswith("_")})
    cfg["_source"] = str(chosen) if chosen else "<defaults>"
    return cfg


def ledger_path(cfg, override=None):
    return Path(override or os.environ.get("PID_REVIEW_LEDGER") or cfg.get("ledger_path") or DEFAULT_LEDGER)


def output_dir(cfg, override=None):
    return Path(override or os.environ.get("PID_REVIEW_OUTPUT") or cfg.get("output_dir") or DEFAULT_OUTPUT)


def config_blockers(cfg):
    """Return launch blockers. Any blocker means real (non-preview) rendering refuses."""
    from .render import validate_review_url, RenderError  # local import avoids a cycle

    blockers = []
    try:
        validate_review_url(cfg.get("google_review_url", ""), cfg)
    except RenderError as exc:
        blockers.append(f"google_review_url: {exc}")
    addr = (cfg.get("business_postal_address") or "").strip()
    if not addr:
        blockers.append("business_postal_address: not set (owner-confirmed postal address required by CAN-SPAM)")
    elif not cfg.get("business_postal_address_confirmed_by_owner"):
        blockers.append("business_postal_address: set but not marked business_postal_address_confirmed_by_owner")
    return blockers
