#!/usr/bin/env python3
"""
Email outreach tool for Utah contractor directory.

Workflow:
  1. python3 outreach.py lookup   — searches online for company emails, saves to emails.csv
  2. python3 outreach.py send     — sends pitch emails to addresses in emails.csv
  3. python3 outreach.py run      — lookup + send in one shot

Configuration (environment variables):
  GMAIL_USER          — your Gmail address (e.g. you@gmail.com)
  GMAIL_APP_PASSWORD  — your Gmail App Password (not your account password)
  FROM_NAME           — display name shown in the From field (default: "Roofers AI")
  SITE_BASE_URL       — base URL where sample sites are hosted
                        (default: https://boosthousellc-byte.github.io/roofers-ai)
  DRY_RUN             — set to "1" to skip actually sending emails (default: "0")
"""

import csv
import os
import re
import smtplib
import ssl
import sys
import time
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── Company data ─────────────────────────────────────────────────────────────

COMPANIES = [
    {"name": "LH Custom Contracting LLC",                    "type": "Bathroom remodeler",            "phone": "+1 435-229-1535", "city": "Utah"},
    {"name": "Desert Plumbing Corporation",                  "type": "Plumber",                       "phone": "+1 435-668-1430", "city": "Utah"},
    {"name": "Digital Marble and Granite",                   "type": "Marble contractor",             "phone": "+1 435-680-8050", "city": "Utah"},
    {"name": "Magicman Handyman LLC",                        "type": "Handyman",                      "phone": "+1 435-635-3095", "city": "Utah"},
    {"name": "Wasatch Mountain Electrical Services",         "type": "Electrician",                   "phone": "+1 385-206-5462", "city": "Utah"},
    {"name": "Shalom Electrical Services",                   "type": "Electrical installation service","phone": "+1 201-424-7624", "city": "Utah"},
    {"name": "PoPo's Remodeling",                            "type": "Handyman",                      "phone": "+1 801-200-3404", "city": "Utah"},
    {"name": "Eagle Valley Design",                          "type": "Cabinet maker",                 "phone": "+1 801-854-8762", "city": "Utah"},
    {"name": "RCI Drywall",                                  "type": "Drywall contractor",            "phone": "+1 801-420-7905", "city": "Utah"},
    {"name": "Kstone & Tile",                                "type": "Tile contractor",               "phone": "+1 801-427-2745", "city": "Utah"},
    {"name": "Caron Electric LLC",                           "type": "Electrician",                   "phone": "+1 435-790-4457", "city": "Utah"},
    {"name": "Bright Electric LLC",                          "type": "Electrician",                   "phone": "+1 435-592-1315", "city": "Utah"},
    {"name": "Heber City Utah Kitchen Remodeling",           "type": "Kitchen remodeler",             "phone": "+1 435-236-3299", "city": "Heber City, UT"},
    {"name": "C J Electrical",                               "type": "Electrician",                   "phone": "+1 435-787-1865", "city": "Utah"},
    {"name": "Lowery Electric",                              "type": "Electrician",                   "phone": "+1 435-753-0343", "city": "Utah"},
    {"name": "DREAM KITCHEN and COUNTERTOP INC",             "type": "Cabinet maker",                 "phone": "+1 801-809-9199", "city": "Utah"},
    {"name": "Intermountain Kitchen and Bath Design",        "type": "Kitchen remodeler",             "phone": "+1 801-548-0160", "city": "Utah"},
    {"name": "Joshua & Sons Electricians Company",           "type": "Electrician",                   "phone": "+1 385-348-4906", "city": "Utah"},
    {"name": "Ramirez Brothers Electricians",                "type": "Electrician",                   "phone": "+1 385-330-4243", "city": "Utah"},
    {"name": "First Choice Home Electrician Salt Lake City", "type": "Electrician",                   "phone": "+1 801-657-4857", "city": "Salt Lake City, UT"},
    {"name": "Utah Electric Co",                             "type": "Electrician",                   "phone": "+1 801-998-8527", "city": "Utah"},
    {"name": "Electrician Salt Lake City",                   "type": "Electrician",                   "phone": "+1 801-516-3723", "city": "Salt Lake City, UT"},
    {"name": "Falcon Electric LLC",                          "type": "Electrician",                   "phone": "+1 801-486-0185", "city": "Utah"},
    {"name": "Any Electrical Co",                            "type": "Electrician",                   "phone": "+1 801-888-2772", "city": "Utah"},
    {"name": "Velmex USA Electrical & Mechanical Repair",    "type": "Auto repair shop",              "phone": "+1 385-259-9079", "city": "Utah"},
    {"name": "Cedar City Electric Contractors",              "type": "Electrician",                   "phone": "+1 435-592-0063", "city": "Cedar City, UT"},
    {"name": "Elkhorn Construction",                         "type": "General contractor",            "phone": "+1 801-690-6860", "city": "Utah"},
    {"name": "Crimson Rock Construction",                    "type": "General contractor",            "phone": "+1 801-859-8764", "city": "Utah"},
    {"name": "Ram Construction",                             "type": "General contractor",            "phone": "+1 801-298-2262", "city": "Utah"},
    {"name": "Affordable Drywall Repair Salt Lake City",     "type": "Drywall contractor",            "phone": "+1 801-801-4090", "city": "Salt Lake City, UT"},
    {"name": "Salt Lake City Service",                       "type": "Water damage restoration",      "phone": "+1 385-480-1052", "city": "Salt Lake City, UT"},
    {"name": "Viana's Services",                             "type": "Handyman",                      "phone": "+1 801-231-0571", "city": "Utah"},
    {"name": "Simmons Construction & Contracting",           "type": "General contractor",            "phone": "+1 435-313-9146", "city": "Utah"},
    {"name": "Davis & Sons Electrical",                      "type": "Electrician",                   "phone": "+1 801-935-1221", "city": "Utah"},
    {"name": "Edmonds Handyman Services",                    "type": "Handyman",                      "phone": "+1 707-601-3080", "city": "Utah"},
    {"name": "Next Level Refinishing",                       "type": "Bathroom remodeler",            "phone": "+1 801-633-4814", "city": "Utah"},
    {"name": "Safeway Electric",                             "type": "Electrician",                   "phone": "+1 385-600-6109", "city": "Utah"},
    {"name": "Electrical Consulting Engineers LLC",          "type": "Electrical installation service","phone": "+1 801-521-8007", "city": "Utah"},
    {"name": "Trejos Mobile Mechanic",                       "type": "Auto repair shop",              "phone": "+1 702-372-3901", "city": "Utah"},
    {"name": "Mortenson Electric Inc",                       "type": "Electrician",                   "phone": "+1 435-757-6500", "city": "Utah"},
    {"name": "Stateline Electric",                           "type": "Electrician",                   "phone": "+1 435-279-7626", "city": "Utah"},
    {"name": "Custom Built Woodworks LLC",                   "type": "Contractor",                    "phone": "+1 801-388-9583", "city": "Utah"},
    {"name": "Gary Tolman Construction",                     "type": "Home builder",                  "phone": "+1 801-776-4668", "city": "Utah"},
    {"name": "Bell-Built Homes",                             "type": "Home builder",                  "phone": "+1 801-458-1685", "city": "Utah"},
    {"name": "Handyman Direct LLC",                          "type": "Handyman",                      "phone": "+1 801-759-3773", "city": "Utah"},
    {"name": "West Coast Refinishing Tub LLC",               "type": "Bathroom remodeler",            "phone": "+1 801-243-5569", "city": "Utah"},
    {"name": "KV Construction",                              "type": "General contractor",            "phone": "+1 435-680-0664", "city": "Utah"},
    {"name": "TILEDGE",                                      "type": "Tile contractor",               "phone": "+1 435-282-0543", "city": "Utah"},
    {"name": "Infinite Tile And Stone",                      "type": "Tile contractor",               "phone": "+1 435-375-8452", "city": "Utah"},
    {"name": "Salt Creek Builders LLC",                      "type": "Kitchen remodeler",             "phone": "+1 801-641-5300", "city": "Utah"},
    {"name": "Color Country Electric",                       "type": "Electrician",                   "phone": "+1 435-680-8898", "city": "Utah"},
    {"name": "Park City Electrical Contractors",             "type": "Electrician",                   "phone": "+1 435-647-0040", "city": "Park City, UT"},
]

# ── Configuration ─────────────────────────────────────────────────────────────

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

GMAIL_USER         = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
FROM_NAME          = os.environ.get("FROM_NAME", "Roofers AI")
SITE_BASE_URL      = os.environ.get(
    "SITE_BASE_URL",
    "https://boosthousellc-byte.github.io/roofers-ai/companies",
)
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"

EMAILS_CSV = Path(__file__).parent / "emails.csv"
CSV_FIELDS = ["name", "type", "phone", "city", "email", "status", "notes"]

# Seconds to wait between search requests to avoid rate limiting
SEARCH_DELAY = 2.0

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def site_url(company: dict) -> str:
    return f"{SITE_BASE_URL}/{slugify(company['name'])}.html"


def extract_emails(text: str) -> list[str]:
    """Pull all email addresses found in raw text/HTML."""
    pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    found = re.findall(pattern, text)
    # Filter out common false positives
    blocked = {"example.com", "sentry.io", "w3.org", "schema.org",
               "wixpress.com", "squarespace.com", "shopify.com"}
    results = []
    seen = set()
    for email in found:
        email = email.lower()
        domain = email.split("@")[-1]
        if domain not in blocked and email not in seen:
            seen.add(email)
            results.append(email)
    return results


# ── Online email search ───────────────────────────────────────────────────────

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


def _fetch(url: str, timeout: int = 10) -> str:
    """Fetch URL, return text or empty string on error."""
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except Exception as exc:
        print(f"    [fetch error] {exc}")
        return ""


def _duckduckgo_html_search(query: str) -> str:
    """Return raw HTML from a DuckDuckGo HTML search."""
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    return _fetch(url)


def _extract_result_urls(html: str) -> list[str]:
    """Pull result URLs out of DuckDuckGo HTML."""
    # DuckDuckGo HTML wraps links in uddg= params
    pattern = r'uddg=([^"&]+)'
    encoded = re.findall(pattern, html)
    urls = []
    for enc in encoded:
        try:
            url = urllib.parse.unquote(enc)
            if url.startswith("http"):
                urls.append(url)
        except Exception:
            pass
    return urls[:5]  # top 5 results


def search_email_online(company: dict) -> str | None:
    """
    Try to find a contact email for the given company by:
      1. Searching DuckDuckGo for "<name> Utah contact email"
      2. Visiting the top result pages and scanning for email addresses
    Returns the best email found, or None.
    """
    name = company["name"]
    city = company["city"]
    query = f'"{name}" {city} contact email'
    print(f"  Searching: {query}")

    html = _duckduckgo_html_search(query)
    time.sleep(SEARCH_DELAY)

    # First: scan search result page itself for any emails
    emails_in_serp = extract_emails(html)
    if emails_in_serp:
        print(f"    Found in SERP: {emails_in_serp[0]}")
        return emails_in_serp[0]

    # Second: visit top result pages
    result_urls = _extract_result_urls(html)
    for url in result_urls:
        # Skip social-only pages that almost never have raw email addresses
        if any(skip in url for skip in ["facebook.com", "twitter.com", "linkedin.com",
                                         "yelp.com/biz", "bbb.org", "yellowpages.com"]):
            continue
        print(f"    Visiting: {url}")
        page_html = _fetch(url, timeout=8)
        time.sleep(SEARCH_DELAY)
        page_emails = extract_emails(page_html)
        if page_emails:
            print(f"    Found on page: {page_emails[0]}")
            return page_emails[0]

    print("    No email found.")
    return None


# ── CSV management ────────────────────────────────────────────────────────────

def load_csv() -> dict[str, dict]:
    """Return {company_name: row_dict} from emails.csv (if it exists)."""
    data = {}
    if EMAILS_CSV.exists():
        with open(EMAILS_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                data[row["name"]] = row
    return data


def save_csv(rows: list[dict]) -> None:
    with open(EMAILS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows → {EMAILS_CSV}")


# ── Email generation ──────────────────────────────────────────────────────────

def generate_email(company: dict) -> tuple[str, str]:
    """Return (subject, plain-text body) for a short & punchy pitch."""
    name = company["name"]
    url  = site_url(company)
    subject = f"Free website for {name} — ready to go live"
    body = f"""\
Hi {name} team,

We built a free sample website for your business — take a look:
{url}

It's professional, mobile-friendly, and ready to rank on Google.
We'd love to hand it over to you at no cost — no strings attached.

Interested? Just reply to this email or call us and we'll get it set up.

Best,
{FROM_NAME}
"""
    return subject, body


# ── Email sending ─────────────────────────────────────────────────────────────

def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send a plain-text email via Gmail SMTP. Returns True on success."""
    if DRY_RUN:
        print(f"    [DRY RUN] Would send to {to_email}: {subject!r}")
        return True

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise EnvironmentError(
            "Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables before sending."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{GMAIL_USER}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())

    return True


# ── Phases ────────────────────────────────────────────────────────────────────

def phase_lookup() -> None:
    """Search for emails and persist results to emails.csv."""
    existing = load_csv()
    rows = []

    for company in COMPANIES:
        name = company["name"]
        existing_row = existing.get(name)

        # Skip if we already have a confirmed email
        if existing_row and existing_row.get("email") and existing_row.get("status") != "not_found":
            print(f"[SKIP] {name} — already have {existing_row['email']}")
            rows.append(existing_row)
            continue

        print(f"[LOOKUP] {name}")
        email = search_email_online(company)

        row = {
            "name":   name,
            "type":   company["type"],
            "phone":  company["phone"],
            "city":   company["city"],
            "email":  email or "",
            "status": "found" if email else "not_found",
            "notes":  "",
        }
        rows.append(row)

    save_csv(rows)
    found = sum(1 for r in rows if r["email"])
    print(f"\nLookup complete: {found}/{len(rows)} emails found.")


def phase_send() -> None:
    """Send pitch emails to all rows in emails.csv that have an address."""
    if not EMAILS_CSV.exists():
        print("No emails.csv found. Run 'python3 outreach.py lookup' first.")
        sys.exit(1)

    rows = list(load_csv().values())
    to_send = [r for r in rows if r.get("email") and r.get("status") != "sent"]

    if not to_send:
        print("Nothing to send — either no emails found or all already sent.")
        return

    print(f"Sending to {len(to_send)} companies…\n")
    sent_count = 0

    for row in to_send:
        company = {k: row[k] for k in ("name", "type", "phone", "city")}
        subject, body = generate_email(company)
        print(f"[SEND] {row['name']} → {row['email']}")
        try:
            success = send_email(row["email"], subject, body)
            if success:
                row["status"] = "sent"
                sent_count += 1
        except Exception as exc:
            print(f"  ERROR: {exc}")
            row["notes"] = str(exc)
        time.sleep(1)  # be polite to Gmail rate limits

    save_csv(rows)
    print(f"\nDone. {sent_count}/{len(to_send)} emails sent.")


# ── Entry point ───────────────────────────────────────────────────────────────

USAGE = """
Usage:
  python3 outreach.py lookup   — find company emails and save to emails.csv
  python3 outreach.py send     — send pitch emails to addresses in emails.csv
  python3 outreach.py run      — lookup then send

Required env vars for 'send':
  GMAIL_USER          your Gmail address
  GMAIL_APP_PASSWORD  your Gmail App Password (enable 2FA first, then create
                      one at https://myaccount.google.com/apppasswords)

Optional env vars:
  FROM_NAME           sender display name  (default: "Roofers AI")
  SITE_BASE_URL       base URL for sample sites
  DRY_RUN             set to "1" to skip actually sending emails
"""

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("lookup", "send", "run"):
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd in ("lookup", "run"):
        phase_lookup()

    if cmd in ("send", "run"):
        phase_send()
