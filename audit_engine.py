#!/usr/bin/env python3
"""
Website Audit Engine
Analyzes any business website and generates a professional PDF audit report.

Usage:
    python audit_engine.py --url https://example.com --business "Acme Roofing" \
        --city "Salt Lake City" --industry dentist --generate-pdf

Supports industries: dentist, roofer, plumber, electrician, hvac, lawyer,
    chiropractor, realtor, contractor, restaurant, auto_repair, salon, gym, generic
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, urljoin

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    print("Missing dependency: requests")
    print("Run: pip install requests")
    sys.exit(1)

# PDF generation is optional for audit-only mode
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, Image
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


# ---------------------------------------------------------------------------
# Industry-specific scoring weights & recommendations
# ---------------------------------------------------------------------------
INDUSTRY_PROFILES = {
    "dentist": {
        "label": "Dental Practice",
        "critical_keywords": ["dentist", "dental", "teeth", "smile", "oral", "cleaning", "whitening", "implant", "orthodont", "crown", "filling"],
        "must_haves": ["online booking", "insurance info", "patient forms", "emergency contact"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
    "roofer": {
        "label": "Roofing Company",
        "critical_keywords": ["roof", "shingle", "leak", "gutter", "siding", "storm", "repair", "replacement", "inspection", "flashing"],
        "must_haves": ["free estimate", "before/after photos", "license info", "service areas"],
        "weight_local_seo": 1.4,
        "weight_mobile": 1.1,
        "weight_speed": 1.0,
    },
    "plumber": {
        "label": "Plumbing Company",
        "critical_keywords": ["plumb", "drain", "pipe", "leak", "water heater", "sewer", "faucet", "toilet", "emergency"],
        "must_haves": ["24/7 emergency", "service areas", "license number", "pricing"],
        "weight_local_seo": 1.4,
        "weight_mobile": 1.3,
        "weight_speed": 1.0,
    },
    "electrician": {
        "label": "Electrical Contractor",
        "critical_keywords": ["electric", "wiring", "panel", "outlet", "lighting", "circuit", "generator", "ev charger"],
        "must_haves": ["license info", "emergency service", "service areas", "free estimate"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
    "hvac": {
        "label": "HVAC Company",
        "critical_keywords": ["hvac", "heating", "cooling", "air condition", "furnace", "ac ", "duct", "thermostat", "heat pump"],
        "must_haves": ["emergency service", "maintenance plans", "financing", "service areas"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
    "lawyer": {
        "label": "Law Firm",
        "critical_keywords": ["attorney", "lawyer", "law firm", "legal", "case", "court", "litigation", "counsel"],
        "must_haves": ["free consultation", "practice areas", "attorney bios", "case results"],
        "weight_local_seo": 1.1,
        "weight_mobile": 1.0,
        "weight_speed": 1.1,
    },
    "chiropractor": {
        "label": "Chiropractic Practice",
        "critical_keywords": ["chiropractic", "spine", "adjustment", "back pain", "neck pain", "wellness", "posture"],
        "must_haves": ["online booking", "new patient forms", "insurance info", "treatment types"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
    "realtor": {
        "label": "Real Estate Agent",
        "critical_keywords": ["real estate", "home", "property", "listing", "buy", "sell", "agent", "realtor", "mls"],
        "must_haves": ["listings/IDX", "agent bio", "testimonials", "market reports"],
        "weight_local_seo": 1.2,
        "weight_mobile": 1.3,
        "weight_speed": 1.1,
    },
    "contractor": {
        "label": "General Contractor",
        "critical_keywords": ["contractor", "remodel", "renovation", "construction", "build", "addition", "deck", "basement"],
        "must_haves": ["portfolio/gallery", "license info", "free estimate", "service areas"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.1,
        "weight_speed": 1.0,
    },
    "restaurant": {
        "label": "Restaurant",
        "critical_keywords": ["menu", "restaurant", "dining", "food", "chef", "reservation", "catering", "cuisine"],
        "must_haves": ["online menu", "hours", "reservation/ordering", "location map"],
        "weight_local_seo": 1.4,
        "weight_mobile": 1.4,
        "weight_speed": 1.1,
    },
    "auto_repair": {
        "label": "Auto Repair Shop",
        "critical_keywords": ["auto", "car", "mechanic", "brake", "oil change", "transmission", "engine", "tire"],
        "must_haves": ["services list", "appointment booking", "hours", "certifications"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
    "salon": {
        "label": "Hair/Beauty Salon",
        "critical_keywords": ["salon", "hair", "beauty", "stylist", "color", "cut", "spa", "nail", "facial"],
        "must_haves": ["online booking", "service menu/pricing", "stylist bios", "gallery"],
        "weight_local_seo": 1.3,
        "weight_mobile": 1.3,
        "weight_speed": 1.0,
    },
    "gym": {
        "label": "Gym / Fitness Studio",
        "critical_keywords": ["gym", "fitness", "workout", "training", "class", "membership", "personal trainer"],
        "must_haves": ["class schedule", "membership pricing", "trial offer", "trainer bios"],
        "weight_local_seo": 1.2,
        "weight_mobile": 1.3,
        "weight_speed": 1.0,
    },
    "generic": {
        "label": "Local Business",
        "critical_keywords": [],
        "must_haves": ["contact info", "about page", "services/products", "testimonials"],
        "weight_local_seo": 1.2,
        "weight_mobile": 1.2,
        "weight_speed": 1.0,
    },
}


# ---------------------------------------------------------------------------
# Website fetcher
# ---------------------------------------------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_page(url, timeout=15):
    """Fetch a URL and return (response, elapsed_seconds, error_string)."""
    try:
        start = time.time()
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        elapsed = time.time() - start
        return resp, elapsed, None
    except RequestException as e:
        return None, 0, str(e)


# ---------------------------------------------------------------------------
# Audit checks
# ---------------------------------------------------------------------------

def check_ssl(url):
    """Check if site uses HTTPS."""
    parsed = urlparse(url)
    uses_https = parsed.scheme == "https"
    # Also check if HTTP redirects to HTTPS
    if not uses_https:
        try:
            resp = requests.head(url.replace("http://", "https://"), headers=HEADERS, timeout=5)
            if resp.status_code < 400:
                return {"pass": True, "score": 8, "max": 10,
                        "detail": "Site accessible via HTTPS but not enforced. Add redirect."}
        except Exception:
            pass
        return {"pass": False, "score": 0, "max": 10,
                "detail": "No SSL certificate detected. Visitors see 'Not Secure' warning."}
    return {"pass": True, "score": 10, "max": 10,
            "detail": "SSL certificate active. Site loads over HTTPS."}


def check_mobile(html):
    """Check for mobile-friendly viewport meta tag."""
    has_viewport = bool(re.search(r'<meta[^>]*name=["\']viewport["\']', html, re.I))
    has_responsive = bool(re.search(r'@media|responsive|bootstrap|tailwind', html, re.I))

    if has_viewport and has_responsive:
        return {"pass": True, "score": 10, "max": 10,
                "detail": "Mobile viewport set and responsive CSS detected."}
    elif has_viewport:
        return {"pass": True, "score": 7, "max": 10,
                "detail": "Viewport meta tag found but limited responsive CSS detected."}
    else:
        return {"pass": False, "score": 2, "max": 10,
                "detail": "No mobile viewport tag. Site likely unusable on phones."}


def check_page_speed(elapsed):
    """Score based on load time."""
    if elapsed < 1.5:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"Page loaded in {elapsed:.2f}s. Excellent speed."}
    elif elapsed < 3.0:
        return {"pass": True, "score": 7, "max": 10,
                "detail": f"Page loaded in {elapsed:.2f}s. Acceptable but could improve."}
    elif elapsed < 5.0:
        return {"pass": False, "score": 4, "max": 10,
                "detail": f"Page loaded in {elapsed:.2f}s. Slow — visitors may leave."}
    else:
        return {"pass": False, "score": 1, "max": 10,
                "detail": f"Page loaded in {elapsed:.2f}s. Very slow — high bounce risk."}


def check_title_tag(html):
    """Check for <title> tag."""
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    if match:
        title = match.group(1).strip()
        length = len(title)
        if 30 <= length <= 65:
            return {"pass": True, "score": 10, "max": 10,
                    "detail": f'Title: "{title}" ({length} chars). Good length for SEO.'}
        elif length > 0:
            return {"pass": True, "score": 6, "max": 10,
                    "detail": f'Title: "{title}" ({length} chars). Ideally 30-65 characters.'}
    return {"pass": False, "score": 0, "max": 10,
            "detail": "No title tag found. Critical for SEO and browser tabs."}


def check_meta_description(html):
    """Check for meta description."""
    match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)', html, re.I)
    if not match:
        match = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', html, re.I)
    if match:
        desc = match.group(1).strip()
        length = len(desc)
        if 120 <= length <= 160:
            return {"pass": True, "score": 10, "max": 10,
                    "detail": f"Meta description found ({length} chars). Optimal length."}
        elif length > 0:
            return {"pass": True, "score": 6, "max": 10,
                    "detail": f"Meta description found ({length} chars). Best at 120-160 chars."}
    return {"pass": False, "score": 0, "max": 10,
            "detail": "No meta description. Google will auto-generate one (usually badly)."}


def check_h1_tag(html):
    """Check for H1 heading."""
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if len(h1s) == 1:
        text = re.sub(r'<[^>]+>', '', h1s[0]).strip()
        return {"pass": True, "score": 10, "max": 10,
                "detail": f'Single H1 found: "{text[:60]}". Good for SEO.'}
    elif len(h1s) > 1:
        return {"pass": True, "score": 5, "max": 10,
                "detail": f"{len(h1s)} H1 tags found. Use exactly one H1 per page."}
    return {"pass": False, "score": 0, "max": 10,
            "detail": "No H1 tag found. Every page needs one primary heading."}


def check_images(html):
    """Check image alt tags."""
    images = re.findall(r'<img[^>]*>', html, re.I)
    if not images:
        return {"pass": True, "score": 7, "max": 10,
                "detail": "No images found on page. Consider adding visuals."}
    with_alt = sum(1 for img in images if re.search(r'alt=["\'][^"\']+', img, re.I))
    ratio = with_alt / len(images) if images else 0
    score = int(ratio * 10)
    if ratio >= 0.9:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"{with_alt}/{len(images)} images have alt text. Great for accessibility."}
    elif ratio >= 0.5:
        return {"pass": False, "score": score, "max": 10,
                "detail": f"Only {with_alt}/{len(images)} images have alt text. Add alt to all."}
    return {"pass": False, "score": score, "max": 10,
            "detail": f"Only {with_alt}/{len(images)} images have alt text. Bad for SEO & accessibility."}


def check_local_seo(html, city):
    """Check for local SEO signals."""
    signals = 0
    details = []
    html_lower = html.lower()

    # City name mention
    if city and city.lower() in html_lower:
        signals += 2
        details.append(f"City name '{city}' found on page")
    else:
        details.append(f"City name '{city}' NOT found on page")

    # Phone number
    if re.search(r'[\(]?\d{3}[\)\-\.\s]?\s?\d{3}[\-\.\s]\d{4}', html):
        signals += 2
        details.append("Phone number detected")
    else:
        details.append("No phone number found")

    # Address pattern
    if re.search(r'\d+\s+[\w\s]+(?:st|street|ave|avenue|blvd|boulevard|rd|road|dr|drive|ln|lane|way|ct|court)', html_lower):
        signals += 2
        details.append("Physical address detected")
    else:
        details.append("No physical address found")

    # Schema/structured data
    if re.search(r'schema\.org|application/ld\+json|itemtype', html_lower):
        signals += 2
        details.append("Schema markup detected")
    else:
        details.append("No schema markup found")

    # Google Maps embed
    if re.search(r'google\.com/maps|maps\.googleapis', html_lower):
        signals += 1
        details.append("Google Maps embed found")

    # NAP consistency check (Name, Address, Phone on page)
    if signals >= 5:
        return {"pass": True, "score": 10, "max": 10,
                "detail": " | ".join(details)}
    elif signals >= 3:
        return {"pass": True, "score": 6, "max": 10,
                "detail": " | ".join(details)}
    return {"pass": False, "score": max(signals, 1), "max": 10,
            "detail": " | ".join(details)}


def check_cta(html):
    """Check for calls-to-action."""
    cta_patterns = [
        r'call\s+(?:us|now|today)',
        r'(get|request|schedule).{0,20}(quote|estimate|appointment|consultation|demo)',
        r'(book|schedule)\s+(now|today|online|appointment)',
        r'free\s+(quote|estimate|consultation|assessment|audit)',
        r'contact\s+us',
        r'<a[^>]*href=["\']tel:',
        r'<button[^>]*>',
        r'class=["\'][^"\']*cta[^"\']*["\']',
    ]
    found = sum(1 for p in cta_patterns if re.search(p, html, re.I))
    if found >= 4:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"{found} CTA signals found. Strong conversion elements."}
    elif found >= 2:
        return {"pass": True, "score": 6, "max": 10,
                "detail": f"{found} CTA signals found. Could add more conversion elements."}
    return {"pass": False, "score": max(found * 2, 1), "max": 10,
            "detail": f"Only {found} CTA signal(s). Add clear calls-to-action."}


def check_social_links(html):
    """Check for social media links."""
    platforms = ["facebook", "instagram", "twitter", "x.com", "linkedin",
                 "youtube", "tiktok", "yelp", "google.com/maps", "nextdoor"]
    found = [p for p in platforms if p in html.lower()]
    if len(found) >= 3:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"Social profiles linked: {', '.join(found)}"}
    elif len(found) >= 1:
        return {"pass": True, "score": 5, "max": 10,
                "detail": f"Social profiles linked: {', '.join(found)}. Add more platforms."}
    return {"pass": False, "score": 0, "max": 10,
            "detail": "No social media links found. Add social profiles for trust & SEO."}


def check_analytics(html):
    """Check for analytics/tracking scripts."""
    trackers = {
        "Google Analytics": r"google-analytics\.com|gtag|googletagmanager",
        "Facebook Pixel": r"facebook\.net/en_US/fbevents|fbq\(",
        "Google Tag Manager": r"googletagmanager\.com/gtm",
        "Hotjar": r"hotjar\.com",
    }
    found = [name for name, pattern in trackers.items() if re.search(pattern, html, re.I)]
    if found:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"Tracking found: {', '.join(found)}"}
    return {"pass": False, "score": 0, "max": 10,
            "detail": "No analytics tracking found. You're flying blind on traffic data."}


def check_industry_keywords(html, industry):
    """Check for industry-specific keywords."""
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["generic"])
    keywords = profile["critical_keywords"]
    if not keywords:
        return {"pass": True, "score": 7, "max": 10,
                "detail": "Generic industry — keyword check skipped."}
    html_lower = html.lower()
    found = [kw for kw in keywords if kw in html_lower]
    ratio = len(found) / len(keywords) if keywords else 0
    if ratio >= 0.5:
        return {"pass": True, "score": 10, "max": 10,
                "detail": f"Found {len(found)}/{len(keywords)} industry keywords: {', '.join(found[:5])}"}
    elif ratio >= 0.25:
        return {"pass": True, "score": 5, "max": 10,
                "detail": f"Found {len(found)}/{len(keywords)} industry keywords. Add more relevant terms."}
    return {"pass": False, "score": max(int(ratio * 10), 1), "max": 10,
            "detail": f"Only {len(found)}/{len(keywords)} industry keywords found. Content needs optimization."}


# ---------------------------------------------------------------------------
# Run full audit
# ---------------------------------------------------------------------------

def run_audit(url, business_name, city, industry="generic"):
    """Run all audit checks and return structured results."""
    # Normalize URL
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    domain = parsed.netloc

    print(f"\n{'='*60}")
    print(f"  WEBSITE AUDIT: {business_name}")
    print(f"  URL: {url}")
    print(f"  Industry: {INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES['generic'])['label']}")
    print(f"  City: {city}")
    print(f"{'='*60}\n")

    # Fetch the page
    print("[1/2] Fetching website...")
    resp, elapsed, error = fetch_page(url)
    if error:
        print(f"  ERROR: Could not fetch {url}")
        print(f"  {error}")
        return None

    html = resp.text
    status_code = resp.status_code
    print(f"  Status: {status_code} | Load time: {elapsed:.2f}s | Size: {len(html):,} bytes")

    # Run checks
    print("[2/2] Running audit checks...\n")
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["generic"])

    checks = {
        "SSL / HTTPS Security": check_ssl(url),
        "Mobile Friendliness": check_mobile(html),
        "Page Load Speed": check_page_speed(elapsed),
        "Title Tag": check_title_tag(html),
        "Meta Description": check_meta_description(html),
        "H1 Heading": check_h1_tag(html),
        "Image Alt Tags": check_images(html),
        "Local SEO Signals": check_local_seo(html, city),
        "Calls-to-Action": check_cta(html),
        "Social Media Links": check_social_links(html),
        "Analytics Tracking": check_analytics(html),
        "Industry Keywords": check_industry_keywords(html, industry),
    }

    # Apply industry weights
    weighted_checks = {}
    for name, result in checks.items():
        weight = 1.0
        if "Local SEO" in name:
            weight = profile.get("weight_local_seo", 1.0)
        elif "Mobile" in name:
            weight = profile.get("weight_mobile", 1.0)
        elif "Speed" in name:
            weight = profile.get("weight_speed", 1.0)
        result["weight"] = weight
        weighted_checks[name] = result

    # Calculate overall score
    total_weighted = sum(r["score"] * r["weight"] for r in weighted_checks.values())
    max_weighted = sum(r["max"] * r["weight"] for r in weighted_checks.values())
    overall_score = int((total_weighted / max_weighted) * 100) if max_weighted > 0 else 0

    # Grade
    if overall_score >= 90:
        grade = "A"
    elif overall_score >= 80:
        grade = "B"
    elif overall_score >= 70:
        grade = "C"
    elif overall_score >= 60:
        grade = "D"
    else:
        grade = "F"

    # Build recommendations
    recommendations = []
    for name, result in weighted_checks.items():
        if not result["pass"]:
            recommendations.append({
                "category": name,
                "priority": "HIGH" if result["score"] <= 3 else "MEDIUM",
                "detail": result["detail"],
            })

    # Print results
    print(f"{'Category':<25} {'Score':>6}  {'Status':<6}  Detail")
    print("-" * 90)
    for name, result in weighted_checks.items():
        status = "PASS" if result["pass"] else "FAIL"
        print(f"{name:<25} {result['score']:>2}/{result['max']:<3}  {status:<6}  {result['detail'][:50]}")
    print("-" * 90)
    print(f"\n  OVERALL SCORE: {overall_score}/100  (Grade: {grade})\n")

    if recommendations:
        print("  TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"    {i}. [{rec['priority']}] {rec['category']}: {rec['detail'][:70]}")
        print()

    return {
        "url": url,
        "domain": domain,
        "business_name": business_name,
        "city": city,
        "industry": industry,
        "industry_label": profile["label"],
        "status_code": status_code,
        "load_time": round(elapsed, 2),
        "page_size_bytes": len(html),
        "overall_score": overall_score,
        "grade": grade,
        "checks": weighted_checks,
        "recommendations": recommendations,
        "must_haves": profile["must_haves"],
        "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ---------------------------------------------------------------------------
# PDF Report Generation
# ---------------------------------------------------------------------------

def _grade_color(grade):
    """Return color for grade."""
    return {
        "A": colors.HexColor("#22c55e"),
        "B": colors.HexColor("#84cc16"),
        "C": colors.HexColor("#eab308"),
        "D": colors.HexColor("#f97316"),
        "F": colors.HexColor("#ef4444"),
    }.get(grade, colors.gray)


def generate_pdf(audit_data, output_path=None):
    """Generate a professional PDF audit report."""
    if not HAS_REPORTLAB:
        print("ERROR: reportlab is required for PDF generation.")
        print("Run: pip install reportlab")
        return None

    if not output_path:
        safe_name = re.sub(r'[^\w\-]', '_', audit_data["business_name"].lower())
        output_path = f"audit_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "AuditTitle", parent=styles["Title"],
        fontSize=26, spaceAfter=6, textColor=colors.HexColor("#1e293b"),
    )
    subtitle_style = ParagraphStyle(
        "AuditSubtitle", parent=styles["Normal"],
        fontSize=12, spaceAfter=20, textColor=colors.HexColor("#64748b"),
    )
    heading_style = ParagraphStyle(
        "AuditHeading", parent=styles["Heading2"],
        fontSize=16, spaceBefore=20, spaceAfter=10,
        textColor=colors.HexColor("#0f172a"),
    )
    body_style = ParagraphStyle(
        "AuditBody", parent=styles["Normal"],
        fontSize=10, spaceAfter=6, leading=14,
        textColor=colors.HexColor("#334155"),
    )
    score_style = ParagraphStyle(
        "ScoreStyle", parent=styles["Title"],
        fontSize=48, alignment=TA_CENTER,
    )
    grade_style = ParagraphStyle(
        "GradeStyle", parent=styles["Title"],
        fontSize=36, alignment=TA_CENTER,
    )

    story = []

    # --- Cover / Header ---
    story.append(Paragraph("Website Audit Report", title_style))
    story.append(Paragraph(
        f"{audit_data['business_name']} &bull; {audit_data['industry_label']} &bull; {audit_data['city']}",
        subtitle_style,
    ))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor("#3b82f6"), spaceAfter=20,
    ))

    # Score summary
    grade_color = _grade_color(audit_data["grade"])
    score_data = [
        [
            Paragraph(f"<font color='{grade_color.hexval()}'>{audit_data['overall_score']}/100</font>", score_style),
            Paragraph(f"<font color='{grade_color.hexval()}'>Grade: {audit_data['grade']}</font>", grade_style),
        ],
    ]
    score_table = Table(score_data, colWidths=[250, 250])
    score_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 15),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 10))

    # Audit info
    info_items = [
        f"<b>URL:</b> {audit_data['url']}",
        f"<b>Audit Date:</b> {audit_data['audit_date']}",
        f"<b>Load Time:</b> {audit_data['load_time']}s",
        f"<b>Page Size:</b> {audit_data['page_size_bytes']:,} bytes",
    ]
    for item in info_items:
        story.append(Paragraph(item, body_style))
    story.append(Spacer(1, 15))

    # --- Detailed Results ---
    story.append(Paragraph("Detailed Results", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    table_data = [["Category", "Score", "Status", "Details"]]
    for name, result in audit_data["checks"].items():
        status = "PASS" if result["pass"] else "FAIL"
        status_color = "#22c55e" if result["pass"] else "#ef4444"
        table_data.append([
            name,
            f"{result['score']}/{result['max']}",
            Paragraph(f"<font color='{status_color}'><b>{status}</b></font>", body_style),
            Paragraph(result["detail"][:80], body_style),
        ])

    detail_table = Table(table_data, colWidths=[120, 50, 50, 280])
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(detail_table)

    # --- Recommendations ---
    if audit_data["recommendations"]:
        story.append(Spacer(1, 15))
        story.append(Paragraph("Priority Recommendations", heading_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

        for i, rec in enumerate(audit_data["recommendations"], 1):
            priority_color = "#ef4444" if rec["priority"] == "HIGH" else "#f97316"
            story.append(Paragraph(
                f"<b>{i}. <font color='{priority_color}'>[{rec['priority']}]</font> "
                f"{rec['category']}</b>",
                body_style,
            ))
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{rec['detail']}", body_style))
            story.append(Spacer(1, 4))

    # --- Industry Must-Haves ---
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        f"Must-Haves for {audit_data['industry_label']} Websites", heading_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    for item in audit_data["must_haves"]:
        story.append(Paragraph(f"&bull; {item.title()}", body_style))

    # --- Footer ---
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    footer_style = ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=8, textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"Generated by Roofers AI Audit Engine &bull; {audit_data['audit_date']}", footer_style
    ))

    doc.build(story)
    print(f"  PDF saved: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def export_json(audit_data, output_path=None):
    """Export audit results as JSON."""
    if not output_path:
        safe_name = re.sub(r'[^\w\-]', '_', audit_data["business_name"].lower())
        output_path = f"audit_{safe_name}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_path, "w") as f:
        json.dump(audit_data, f, indent=2, default=str)
    print(f"  JSON saved: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Website Audit Engine — analyze any business website",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audit_engine.py --url https://example.com --business "Acme Roofing" --city "Denver" --industry roofer
  python audit_engine.py --url example.com --business "Smile Dental" --city "Austin" --industry dentist --generate-pdf
  python audit_engine.py --url example.com --business "Test" --city "NYC" --json
        """,
    )
    parser.add_argument("--url", required=True, help="Website URL to audit")
    parser.add_argument("--business", required=True, help="Business name")
    parser.add_argument("--city", required=True, help="City/location for local SEO check")
    parser.add_argument("--industry", default="generic",
                        choices=list(INDUSTRY_PROFILES.keys()),
                        help="Business industry (default: generic)")
    parser.add_argument("--generate-pdf", action="store_true", help="Generate PDF report")
    parser.add_argument("--json", action="store_true", help="Export results as JSON")
    parser.add_argument("--output", help="Output file path (for PDF or JSON)")

    args = parser.parse_args()

    results = run_audit(args.url, args.business, args.city, args.industry)
    if not results:
        sys.exit(1)

    if args.generate_pdf:
        pdf_path = generate_pdf(results, args.output)
        if not pdf_path:
            sys.exit(1)

    if args.json:
        export_json(results, args.output if not args.generate_pdf else None)

    return results


if __name__ == "__main__":
    main()
