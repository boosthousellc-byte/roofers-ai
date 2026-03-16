"""Extended tests for audit_engine — edge cases, run_audit, PDF/JSON export."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from audit_engine import (
    check_ssl,
    check_mobile,
    check_page_speed,
    check_title_tag,
    check_meta_description,
    check_h1_tag,
    check_images,
    check_cta,
    check_social_links,
    check_analytics,
    check_local_seo,
    check_industry_keywords,
    fetch_page,
    run_audit,
    export_json,
    generate_pdf,
    _grade_color,
    INDUSTRY_PROFILES,
)


# ── check_page_speed edge cases ─────────────────────────────────────────────

def test_page_speed_medium():
    result = check_page_speed(2.5)
    assert result["pass"] is True
    assert result["score"] == 7


def test_page_speed_slow_but_under_5():
    result = check_page_speed(4.0)
    assert result["pass"] is False
    assert result["score"] == 4


# ── check_mobile edge cases ─────────────────────────────────────────────────

def test_mobile_viewport_and_responsive():
    html = '<meta name="viewport" content="width=device-width"><style>@media (max-width:600px){}</style>'
    result = check_mobile(html)
    assert result["pass"] is True
    assert result["score"] == 10


def test_mobile_viewport_only():
    html = '<meta name="viewport" content="width=device-width"><p>plain</p>'
    result = check_mobile(html)
    assert result["pass"] is True
    assert result["score"] == 7


# ── check_title_tag edge cases ──────────────────────────────────────────────

def test_title_optimal_length():
    title = "A" * 40  # 40 chars, within 30-65
    html = f"<title>{title}</title>"
    result = check_title_tag(html)
    assert result["score"] == 10


def test_title_short():
    html = "<title>Hi</title>"
    result = check_title_tag(html)
    assert result["pass"] is True
    assert result["score"] == 6  # present but not optimal length


def test_title_too_long():
    title = "A" * 80  # > 65 chars
    html = f"<title>{title}</title>"
    result = check_title_tag(html)
    assert result["pass"] is True
    assert result["score"] == 6


# ── check_meta_description edge cases ───────────────────────────────────────

def test_meta_description_optimal_length():
    desc = "A" * 140  # within 120-160
    html = f'<meta name="description" content="{desc}">'
    result = check_meta_description(html)
    assert result["score"] == 10


def test_meta_description_short():
    html = '<meta name="description" content="Short desc">'
    result = check_meta_description(html)
    assert result["pass"] is True
    assert result["score"] == 6


def test_meta_description_reversed_attribute_order():
    html = '<meta content="Some description here" name="description">'
    result = check_meta_description(html)
    assert result["pass"] is True


# ── check_images edge cases ─────────────────────────────────────────────────

def test_images_no_images():
    result = check_images("<html><body>No images</body></html>")
    assert result["pass"] is True
    assert result["score"] == 7


def test_images_partial_alt():
    html = '<img src="a.jpg" alt="A"><img src="b.jpg"><img src="c.jpg" alt="C">'
    result = check_images(html)
    # 2/3 = 66%, between 50% and 90%
    assert result["pass"] is False
    assert result["score"] == 6


# ── check_cta edge cases ────────────────────────────────────────────────────

def test_cta_weak():
    html = "<p>Just some text about our services</p>"
    result = check_cta(html)
    assert result["pass"] is False
    assert result["score"] <= 2


def test_cta_moderate():
    html = '<button>Submit</button><a href="tel:555-1234">Call</a>'
    result = check_cta(html)
    assert result["pass"] is True
    assert result["score"] == 6


# ── check_social_links edge cases ───────────────────────────────────────────

def test_social_links_single():
    html = '<a href="https://facebook.com/biz">FB</a>'
    result = check_social_links(html)
    assert result["pass"] is True
    assert result["score"] == 5


def test_social_links_none():
    result = check_social_links("<html><body>nothing</body></html>")
    assert result["pass"] is False
    assert result["score"] == 0


# ── check_local_seo edge cases ──────────────────────────────────────────────

def test_local_seo_no_signals():
    result = check_local_seo("<html><body>nothing</body></html>", "Denver")
    assert result["pass"] is False


def test_local_seo_with_schema_and_maps():
    html = """
    <p>Visit us in Denver</p>
    <p>(303) 555-1234</p>
    <p>123 Main Street</p>
    <script type="application/ld+json">{"@type": "LocalBusiness"}</script>
    <iframe src="https://google.com/maps/embed"></iframe>
    """
    result = check_local_seo(html, "Denver")
    assert result["pass"] is True
    assert result["score"] == 10


# ── check_industry_keywords edge cases ──────────────────────────────────────

def test_industry_keywords_generic():
    result = check_industry_keywords("<html>anything</html>", "generic")
    assert result["pass"] is True
    assert result["score"] == 7


def test_industry_keywords_low_ratio():
    html = "We are a business"
    result = check_industry_keywords(html, "dentist")
    assert result["pass"] is False


def test_industry_keywords_unknown_falls_back_to_generic():
    result = check_industry_keywords("<html>anything</html>", "unknown_type")
    assert result["pass"] is True


# ── check_ssl edge case ─────────────────────────────────────────────────────

def test_ssl_http_with_https_available():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    with patch("audit_engine.requests.head", return_value=mock_resp):
        result = check_ssl("http://example.com")
        assert result["pass"] is True
        assert result["score"] == 8  # accessible but not enforced


def test_ssl_http_no_https():
    with patch("audit_engine.requests.head", side_effect=Exception("timeout")):
        result = check_ssl("http://example.com")
        assert result["pass"] is False
        assert result["score"] == 0


# ── fetch_page ───────────────────────────────────────────────────────────────

def test_fetch_page_success():
    mock_resp = MagicMock()
    mock_resp.text = "<html>OK</html>"
    mock_resp.status_code = 200
    with patch("audit_engine.requests.get", return_value=mock_resp):
        resp, elapsed, error = fetch_page("https://example.com")
        assert resp is not None
        assert error is None
        assert elapsed >= 0


def test_fetch_page_timeout():
    from requests.exceptions import Timeout
    with patch("audit_engine.requests.get", side_effect=Timeout("timed out")):
        resp, elapsed, error = fetch_page("https://example.com", timeout=1)
        assert resp is None
        assert "timed out" in error


# ── run_audit ────────────────────────────────────────────────────────────────

def _mock_run_audit(url="https://example.com", business="Test Biz",
                    city="SLC", industry="generic", html=None):
    """Helper to run audit with mocked network."""
    if html is None:
        html = """
        <html>
        <head>
            <title>Test Business in Salt Lake City</title>
            <meta name="viewport" content="width=device-width">
            <meta name="description" content="We are a great business serving the SLC area with top quality service and affordable prices for all customers.">
        </head>
        <body>
            <h1>Welcome to Test Biz</h1>
            <img src="hero.jpg" alt="Hero image">
            <a href="tel:801-555-1234">Call Us</a>
            <button>Get Free Quote</button>
            <a href="/contact">Contact Us</a>
            <a href="https://facebook.com/test">FB</a>
            <a href="https://instagram.com/test">IG</a>
            <a href="https://youtube.com/test">YT</a>
            <script src="https://www.google-analytics.com/analytics.js"></script>
            <p>Salt Lake City SLC area</p>
            <p>(801) 555-1234</p>
            <p>123 Main Street</p>
        </body>
        </html>
        """
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.status_code = 200
    with patch("audit_engine.fetch_page", return_value=(mock_resp, 0.5, None)):
        return run_audit(url, business, city, industry)


def test_run_audit_returns_expected_keys():
    result = _mock_run_audit()
    assert result is not None
    for key in ["url", "domain", "business_name", "city", "industry",
                "overall_score", "grade", "checks", "recommendations",
                "must_haves", "audit_date"]:
        assert key in result


def test_run_audit_score_range():
    result = _mock_run_audit()
    assert 0 <= result["overall_score"] <= 100


def test_run_audit_grade_assignment():
    result = _mock_run_audit()
    assert result["grade"] in ("A", "B", "C", "D", "F")


def test_run_audit_url_normalization():
    result = _mock_run_audit(url="example.com")
    assert result["url"].startswith("https://")


def test_run_audit_fetch_failure():
    with patch("audit_engine.fetch_page", return_value=(None, 0, "Connection refused")):
        result = run_audit("https://bad.invalid", "Biz", "City")
        assert result is None


def test_run_audit_industry_weights_applied():
    result = _mock_run_audit(industry="restaurant")
    # Restaurant has weight_mobile=1.4, verify weights are in check results
    mobile_check = result["checks"]["Mobile Friendliness"]
    assert mobile_check["weight"] == 1.4


def test_run_audit_recommendations_only_for_failures():
    result = _mock_run_audit()
    for rec in result["recommendations"]:
        check_name = rec["category"]
        assert result["checks"][check_name]["pass"] is False


def test_run_audit_check_count():
    result = _mock_run_audit()
    assert len(result["checks"]) == 12  # all 12 audit checks


# ── grade_color ──────────────────────────────────────────────────────────────

def test_grade_color_all_grades():
    from reportlab.lib import colors
    for grade in ("A", "B", "C", "D", "F"):
        color = _grade_color(grade)
        assert color is not None
        assert color != colors.gray


def test_grade_color_unknown():
    from reportlab.lib import colors
    assert _grade_color("Z") == colors.gray


# ── export_json ──────────────────────────────────────────────────────────────

def test_export_json(tmp_path):
    audit_data = {
        "business_name": "Test Co",
        "overall_score": 80,
        "grade": "B",
    }
    out = str(tmp_path / "test_output.json")
    result_path = export_json(audit_data, out)
    assert result_path == out
    with open(out) as f:
        loaded = json.load(f)
    assert loaded["overall_score"] == 80


def test_export_json_default_filename():
    audit_data = {"business_name": "My Biz", "overall_score": 50}
    with patch("builtins.open", MagicMock()):
        path = export_json(audit_data)
        assert path.startswith("audit_my_biz_")
        assert path.endswith(".json")


# ── generate_pdf ─────────────────────────────────────────────────────────────

def test_generate_pdf(tmp_path):
    result = _mock_run_audit()
    out = str(tmp_path / "report.pdf")
    pdf_path = generate_pdf(result, out)
    assert pdf_path == out
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_generate_pdf_default_filename():
    result = _mock_run_audit()
    pdf_path = generate_pdf(result)
    assert pdf_path is not None
    assert pdf_path.endswith(".pdf")
    # Clean up
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
