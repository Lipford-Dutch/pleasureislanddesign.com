"""Template renderer for the PID review-request emails.

Rules (docs/placeholders.md):
* {{google_review_url}} and {{business_postal_address}} are REQUIRED. Real rendering
  refuses until both are verified in config. Preview rendering shows a loud
  "UNRESOLVED" marker instead and is never usable for sending.
* Greeting falls back to "Hello," when first_name is blank or untrusted.
* {{#qr_block}} is kept only when the review URL is verified AND a locally generated
  QR image file exists AND qr_image_url is an https URL.
* {{#phone_block}} is kept only when an owner-confirmed business_phone is configured.
* Any {{...}} left after rendering is an error.
"""
import html
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from .paths import TEMPLATE_DIR

KINDS = ("initial", "reminder")
PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")
SECTION_RE = re.compile(r"\{\{#([a-z_]+)\}\}(.*?)\{\{/\1\}\}", re.S)
ANY_TAG_RE = re.compile(r"\{\{.*?\}\}", re.S)
# Developer comments are stripped; Outlook conditional comments (<!--[if ...]>) are kept.
DEV_COMMENT_RE = re.compile(r"[ \t]*<!--(?!\[if)(?!\s*\[endif).*?-->[ \t]*\n?", re.S)
GREETING_RE = re.compile(r"Hi \{\{\s*first_name\s*\}\},")
NAME_OK_RE = re.compile(r"^[^\W\d_]+(?:[ '\u2019.-][^\W\d_]+)*\.?$", re.U)

REQUIRED = ("google_review_url", "business_postal_address")
QR_CID_URL = "cid:pid-review-qr"  # inline attachment; the outbox embeds qr_image_file
GPAGE_REVIEW_RE = re.compile(r"^/r/[A-Za-z0-9_-]{6,64}/review/?$")
REVIEW_HOSTS = {"g.page", "search.google.com", "www.google.com", "google.com", "maps.app.goo.gl"}
UNRESOLVED = "[[UNRESOLVED {name} - PREVIEW ONLY, NOT FOR SEND]]"


class RenderError(Exception):
    pass


@dataclass
class RenderedMessage:
    kind: str
    template_version: str
    subject: str
    preheader: str
    text: str
    html: str
    preview: bool
    unresolved: list = field(default_factory=list)


def validate_review_url(url, cfg):
    """Validate the CTA URL. It must be the owner-verified Google write-review link."""
    url = (url or "").strip()
    if not url:
        raise RenderError("not set (needs the verified Google Business Profile 'Get more reviews' link)")
    if not cfg.get("google_review_url_verified"):
        raise RenderError("set but not marked google_review_url_verified (test on desktop + mobile first)")
    if not (cfg.get("google_review_url_verified_by") and cfg.get("google_review_url_verified_on")):
        raise RenderError("google_review_url_verified_by and google_review_url_verified_on must be recorded")
    if any(ch in url for ch in "\r\n\t \"'<>`"):
        raise RenderError("contains whitespace or characters that are not allowed in a URL")
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise RenderError("must be an https:// URL")
    if parts.username or parts.password or parts.port:
        raise RenderError("must not contain credentials or a port")
    host = (parts.hostname or "").lower()
    if host not in REVIEW_HOSTS:
        raise RenderError(f"host {host!r} is not a Google review host ({', '.join(sorted(REVIEW_HOSTS))})")
    if host == "g.page" and not GPAGE_REVIEW_RE.match(parts.path):
        raise RenderError("g.page links must be Google's official review short link: https://g.page/r/<id>/review")
    if host in ("www.google.com", "google.com") and parts.path.rstrip("/") in ("/search", "", "/maps"):
        raise RenderError("a Google search/maps URL is not a write-review link")
    if re.search(r"(^|&)(utm_[a-z]+|gclid|fbclid|mc_eid)=", parts.query or ""):
        raise RenderError("tracking query parameters are not allowed")
    return url


def qr_ready(cfg):
    try:
        validate_review_url(cfg.get("google_review_url"), cfg)
    except RenderError:
        return False
    qr_url = (cfg.get("qr_image_url") or "").strip()
    qr_file = (cfg.get("qr_image_file") or "").strip()
    url_ok = qr_url.startswith("https://") or qr_url == QR_CID_URL
    return bool(url_ok and qr_file and Path(qr_file).is_file())


def phone_ready(cfg):
    return bool((cfg.get("business_phone") or "").strip() and cfg.get("business_phone_confirmed_by_owner"))


def sanitize_first_name(value):
    """Return a safe display name or "" (which triggers the "Hello," greeting)."""
    if not value:
        return ""
    value = "".join(ch for ch in str(value) if unicodedata.category(ch)[0] != "C")
    value = " ".join(value.split())
    if not value or len(value) > 40 or not NAME_OK_RE.match(value):
        return ""
    return value


def _read_template(kind, fmt):
    if kind not in KINDS:
        raise RenderError(f"unknown template kind {kind!r}; use one of {KINDS}")
    path = TEMPLATE_DIR / f"review-request-{kind}.{fmt}"
    return path.read_text(encoding="utf-8")


def _parse_text_header(raw):
    header, _, body = raw.partition("\n\n")
    meta = {}
    for line in header.splitlines():
        key, sep, val = line.partition(":")
        if sep:
            meta[key.strip().lower()] = val.strip()
    return meta, body


def _apply_sections(tpl, enabled):
    def repl(m):
        return m.group(2) if enabled.get(m.group(1)) else ""
    return SECTION_RE.sub(repl, tpl)


def _values(record, cfg, preview, for_html):
    esc = (lambda s: html.escape(s, quote=True)) if for_html else (lambda s: s)
    vals, unresolved = {}, []
    try:
        vals["google_review_url"] = esc(validate_review_url(cfg.get("google_review_url"), cfg))
    except RenderError as exc:
        if not preview:
            raise RenderError(f"required placeholder google_review_url is unresolved: {exc}")
        unresolved.append("google_review_url")
        vals["google_review_url"] = esc(UNRESOLVED.format(name="google_review_url"))
    addr = (cfg.get("business_postal_address") or "").strip()
    if not addr or not cfg.get("business_postal_address_confirmed_by_owner"):
        if not preview:
            raise RenderError("required placeholder business_postal_address is unresolved "
                              "(owner-confirmed postal address not configured)")
        unresolved.append("business_postal_address")
        addr = UNRESOLVED.format(name="business_postal_address")
    lines = [ln.strip() for ln in addr.splitlines() if ln.strip()]
    vals["business_postal_address"] = "<br>\n              ".join(esc(l) for l in lines) if for_html else "\n".join(lines)
    vals["first_name"] = esc(sanitize_first_name(record.get("first_name", "")))
    vals["business_phone"] = esc((cfg.get("business_phone") or "").strip())
    vals["qr_image_url"] = esc((cfg.get("qr_image_url") or "").strip())
    return vals, unresolved


def _fill(tpl, vals, for_html, preview):
    if not vals["first_name"]:
        tpl = GREETING_RE.sub("Hello,", tpl)

    def repl(m):
        name = m.group(1)
        if name not in vals:
            raise RenderError(f"template uses unknown placeholder {{{{{name}}}}}")
        value = vals[name]
        if value == "" and name in REQUIRED:
            raise RenderError(f"required placeholder {{{{{name}}}}} is empty")
        return value

    out = PLACEHOLDER_RE.sub(repl, tpl)
    leftover = ANY_TAG_RE.findall(out)
    if leftover:
        raise RenderError(f"unfilled template tags remain: {sorted(set(leftover))}")
    if for_html and preview and "UNRESOLVED" in out:
        # never leave a clickable stand-in link in a preview
        out = out.replace('href="' + html.escape(UNRESOLVED.format(name="google_review_url"), quote=True) + '"',
                          'href="#unresolved-google-review-url"')
    return out


def render(kind, record, cfg, preview=False):
    """Render one message. preview=True allows unresolved blockers, clearly marked."""
    record = record or {}
    enabled = {"qr_block": qr_ready(cfg), "phone_block": phone_ready(cfg)}

    raw_txt = _read_template(kind, "txt")
    meta, body_txt = _parse_text_header(raw_txt)
    vals_t, unresolved = _values(record, cfg, preview, for_html=False)
    text = _fill(_apply_sections(body_txt, enabled), vals_t, False, preview)

    raw_html = _read_template(kind, "html")
    vals_h, _ = _values(record, cfg, preview, for_html=True)
    html_tpl = _apply_sections(DEV_COMMENT_RE.sub("", raw_html), enabled)
    html_out = _fill(html_tpl, vals_h, True, preview)

    version = meta.get("template_version", "")
    if version not in raw_html:
        raise RenderError(f"HTML and text template versions differ for {kind!r}")
    if preview and unresolved:
        banner = "*** PREVIEW ONLY - NOT FOR SEND - unresolved: " + ", ".join(unresolved) + " ***\n\n"
        text = banner + text
        html_banner = ('<div style="background:#B00020;color:#FFFFFF;font:bold 16px Arial,sans-serif;'
                       'padding:12px;text-align:center;">PREVIEW ONLY - NOT FOR SEND - unresolved: '
                       + html.escape(", ".join(unresolved)) + '</div>')
        html_out = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + html_banner, html_out, count=1)
    return RenderedMessage(kind=kind, template_version=version, subject=meta.get("subject", ""),
                           preheader=meta.get("preheader", ""), text=text, html=html_out,
                           preview=preview, unresolved=unresolved)
