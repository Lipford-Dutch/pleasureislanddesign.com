"""Path helpers that keep private data out of the git repository."""
import os
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = TOOL_DIR / "templates"
TOOL_OUT_DIR = TOOL_DIR / "out"  # gitignored scratch area for previews

PRIVATE_HOME = Path(os.path.expanduser("~")) / ".pid-private" / "review-requests"
DEFAULT_LEDGER = PRIVATE_HOME / "ledger.csv"
DEFAULT_OUTPUT = PRIVATE_HOME / "out"


class PrivatePathError(Exception):
    """Raised when private data would be read from or written inside the repo."""


def find_repo_root(start=None):
    p = Path(start or TOOL_DIR).resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def _is_within(child, parent):
    try:
        Path(child).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def check_ledger_path(path, repo_root=None):
    """A real ledger must live outside the repo. Fake *.example.csv files are allowed."""
    path = Path(path)
    root = repo_root if repo_root is not None else find_repo_root()
    if root and _is_within(path, root) and not path.name.endswith(".example.csv"):
        raise PrivatePathError(
            f"Refusing to use a ledger inside the git repo ({path}). Keep the real ledger "
            f"outside the repo (default {DEFAULT_LEDGER}) or set PID_REVIEW_LEDGER."
        )
    return path


def check_output_dir(path, repo_root=None):
    """Outputs may hold rendered personal data: outside the repo, or the gitignored out/ folder."""
    path = Path(path)
    root = repo_root if repo_root is not None else find_repo_root()
    if root and _is_within(path, root) and not _is_within(path, TOOL_OUT_DIR):
        raise PrivatePathError(
            f"Refusing to write outputs inside the git repo ({path}). Use a folder outside "
            f"the repo (default {DEFAULT_OUTPUT}) or the gitignored {TOOL_OUT_DIR}."
        )
    return path
