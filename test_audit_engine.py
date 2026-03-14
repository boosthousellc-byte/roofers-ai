"""Basic tests for the audit engine."""

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
    INDUSTRY_PROFILES,
)


def test_check_ssl_https():
    result = check_ssl("https://example.com")
    assert result["pass"] is True
    assert result["score"] == 10


def test_check_ssl_http():
    result = check_ssl("http://example.com")
    assert result["score"] < 10


def test_check_mobile_with_viewport():
    html = '<meta name="viewport" content="width=device-width">'
    result = check_mobile(html)
    assert result["pass"] is True


def test_check_mobile_without_viewport():
    result = check_mobile("<html><body>No viewport</body></html>")
    assert result["pass"] is False


def test_check_page_speed_fast():
    result = check_page_speed(0.5)
    assert result["pass"] is True
    assert result["score"] == 10


def test_check_page_speed_slow():
    result = check_page_speed(6.0)
    assert result["pass"] is False


def test_check_title_tag_good():
    html = "<title>Best Dentist in Salt Lake City | Smile Dental</title>"
    result = check_title_tag(html)
    assert result["pass"] is True


def test_check_title_tag_missing():
    result = check_title_tag("<html><body>No title</body></html>")
    assert result["pass"] is False
    assert result["score"] == 0


def test_check_meta_description_present():
    html = '<meta name="description" content="We are the best roofing company in Denver, offering free estimates and quality service for residential and commercial roofs.">'
    result = check_meta_description(html)
    assert result["pass"] is True


def test_check_meta_description_missing():
    result = check_meta_description("<html><body>No meta</body></html>")
    assert result["pass"] is False


def test_check_h1_single():
    html = "<h1>Welcome to Our Business</h1>"
    result = check_h1_tag(html)
    assert result["pass"] is True
    assert result["score"] == 10


def test_check_h1_multiple():
    html = "<h1>First</h1><h1>Second</h1>"
    result = check_h1_tag(html)
    assert result["score"] == 5


def test_check_h1_missing():
    result = check_h1_tag("<html><body>No heading</body></html>")
    assert result["pass"] is False


def test_check_images_all_alt():
    html = '<img src="a.jpg" alt="Photo A"><img src="b.jpg" alt="Photo B">'
    result = check_images(html)
    assert result["pass"] is True


def test_check_images_no_alt():
    html = '<img src="a.jpg"><img src="b.jpg">'
    result = check_images(html)
    assert result["pass"] is False


def test_check_cta_strong():
    html = """
    <a href="tel:555-1234">Call Us</a>
    <button>Get Free Quote</button>
    <a href="/contact">Contact Us</a>
    <div class="cta-button">Schedule Now</div>
    """
    result = check_cta(html)
    assert result["pass"] is True


def test_check_social_links():
    html = '<a href="https://facebook.com/biz">FB</a><a href="https://instagram.com/biz">IG</a><a href="https://youtube.com/biz">YT</a>'
    result = check_social_links(html)
    assert result["pass"] is True


def test_check_analytics_present():
    html = '<script src="https://www.google-analytics.com/analytics.js"></script>'
    result = check_analytics(html)
    assert result["pass"] is True


def test_check_analytics_missing():
    result = check_analytics("<html><body>No tracking</body></html>")
    assert result["pass"] is False


def test_check_local_seo():
    html = """
    <p>Serving Salt Lake City and surrounding areas</p>
    <p>Call us: (801) 555-1234</p>
    <p>123 Main Street, SLC</p>
    """
    result = check_local_seo(html, "Salt Lake City")
    assert result["score"] >= 5


def test_check_industry_keywords():
    html = "We are a dental office offering teeth cleaning, whitening, and dental implants."
    result = check_industry_keywords(html, "dentist")
    assert result["pass"] is True


def test_industry_profiles_exist():
    assert len(INDUSTRY_PROFILES) >= 14
    for key, profile in INDUSTRY_PROFILES.items():
        assert "label" in profile
        assert "critical_keywords" in profile
        assert "must_haves" in profile
