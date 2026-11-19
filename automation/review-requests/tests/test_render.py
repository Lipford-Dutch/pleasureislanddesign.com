import re
import tempfile
import unittest
from pathlib import Path

from helpers import FAKE_ADDRESS, FAKE_REVIEW_URL, cfg, ready_cfg
from pid_reviews.config import config_blockers
from pid_reviews.render import RenderError, render, sanitize_first_name, validate_review_url


class RequiredPlaceholders(unittest.TestCase):
    def test_real_render_refuses_without_review_url(self):
        with self.assertRaises(RenderError) as ctx:
            render("initial", {}, ready_cfg(google_review_url=""))
        self.assertIn("google_review_url", str(ctx.exception))

    def test_real_render_refuses_unverified_review_url(self):
        with self.assertRaises(RenderError):
            render("initial", {}, ready_cfg(google_review_url_verified=False))

    def test_real_render_refuses_without_postal_address(self):
        for c in (ready_cfg(business_postal_address=""), ready_cfg(business_postal_address_confirmed_by_owner=False)):
            with self.assertRaises(RenderError) as ctx:
                render("reminder", {}, c)
            self.assertIn("business_postal_address", str(ctx.exception))

    def test_default_config_is_blocked(self):
        self.assertEqual(len(config_blockers(cfg())), 2)
        self.assertEqual(config_blockers(ready_cfg()), [])

    def test_preview_marks_unresolved_and_has_no_clickable_stand_in(self):
        m = render("initial", {}, cfg(), preview=True)
        self.assertEqual(m.unresolved, ["google_review_url", "business_postal_address"])
        self.assertTrue(m.text.startswith("*** PREVIEW ONLY - NOT FOR SEND"))
        self.assertIn("PREVIEW ONLY - NOT FOR SEND", m.html)
        self.assertIn('href="#unresolved-google-review-url"', m.html)
        self.assertNotIn("{{", m.text + m.html)

    def test_full_render_has_no_tags_and_includes_values(self):
        for kind in ("initial", "reminder"):
            m = render(kind, {"first_name": "Sam"}, ready_cfg())
            self.assertEqual(m.unresolved, [])
            self.assertNotIn("{{", m.text + m.html)
            self.assertIn(FAKE_REVIEW_URL, m.text)
            self.assertIn(f'href="{FAKE_REVIEW_URL}"', m.html)
            self.assertIn(FAKE_ADDRESS.splitlines()[1], m.text)
            self.assertIn("Hi Sam,", m.text)
            self.assertIn("Nicole Rayment", m.text)
            self.assertIn("unsubscribe", m.text)
            self.assertTrue(m.template_version.startswith(f"pid-review-{kind}-v"))
            self.assertNotIn("RENDERER RULES", m.html)  # dev comments stripped
            self.assertIn("<!--[if mso]>", m.html)       # Outlook conditionals kept

    def test_unknown_placeholder_fails_loudly(self):
        from pid_reviews import render as r
        with self.assertRaises(RenderError):
            r._fill("Hi {{surname}}", {"first_name": "x"}, False, False)

    def test_unclosed_section_tag_fails_loudly(self):
        from pid_reviews import render as r
        with self.assertRaises(RenderError):
            r._fill("x {{#qr_block}} y", {"first_name": "x"}, False, False)


class GreetingAndEscaping(unittest.TestCase):
    def test_blank_or_untrusted_name_falls_back_to_hello(self):
        for name in ("", "   ", "<script>", "a@b.c", "x" * 60, "Robert'); DROP", "\x00"):
            m = render("initial", {"first_name": name}, ready_cfg())
            self.assertIn("Hello,", m.text, name)
            self.assertNotIn("Hi ,", m.text)
            self.assertNotIn("<script>", m.html)

    def test_sanitize_keeps_real_names(self):
        self.assertEqual(sanitize_first_name(" Mary  Ann "), "Mary Ann")
        self.assertEqual(sanitize_first_name("O'Neil"), "O'Neil")
        self.assertEqual(sanitize_first_name("José"), "José")


class ReviewUrlValidation(unittest.TestCase):
    def check(self, url):
        validate_review_url(url, ready_cfg(google_review_url=url))

    def test_search_url_rejected(self):
        with self.assertRaises(RenderError):
            self.check("https://www.google.com/search?q=Pleasure+Island+Design+Wilmington+NC")

    def test_non_https_and_other_hosts_rejected(self):
        for bad in ("http://g.page/r/X/review", "https://evil.example/review", "javascript:alert(1)",
                    "https://g.page/r/X/review?utm_source=email", "https://g.page/r/X\"onclick=1"):
            with self.assertRaises(RenderError, msg=bad):
                self.check(bad)

    def test_verifier_and_date_required(self):
        with self.assertRaises(RenderError):
            validate_review_url(FAKE_REVIEW_URL, ready_cfg(google_review_url_verified_by=""))


class OptionalBlocks(unittest.TestCase):
    def test_qr_omitted_by_default(self):
        m = render("initial", {}, ready_cfg())
        self.assertNotIn("Scan this code", m.html)
        self.assertNotIn("qr_block", m.html)

    def test_qr_requires_generated_file_and_verified_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "qr.png"
            png.write_bytes(b"\x89PNG fake")
            url = "https://www.pleasureislanddesign.com/img/FAKE-test-qr.png"
            self.assertIn("Scan this code", render("initial", {}, ready_cfg(qr_image_url=url, qr_image_file=str(png))).html)
            self.assertNotIn("Scan this code", render("initial", {}, ready_cfg(qr_image_url=url, qr_image_file=str(png) + ".missing")).html)
            self.assertNotIn("Scan this code", render("initial", {}, cfg(qr_image_url=url, qr_image_file=str(png)), preview=True).html)

    def test_phone_optional_and_needs_owner_confirmation(self):
        self.assertNotIn("555-0100", render("initial", {}, ready_cfg(business_phone="555-0100")).text)
        m = render("initial", {}, ready_cfg(business_phone="555-0100", business_phone_confirmed_by_owner=True))
        self.assertIn("555-0100", m.text)
        self.assertIn("555-0100", m.html)

    def test_plain_text_keeps_blank_line_before_footer(self):
        m = render("initial", {}, ready_cfg())
        self.assertRegex(m.text, re.compile(r"pleasureislanddesign@gmail\.com\n\n-----"))


if __name__ == "__main__":
    unittest.main()
