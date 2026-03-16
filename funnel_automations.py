#!/usr/bin/env python3
"""
Funnel Automations — Email Sequence Engine
==========================================
Handles two jobs:

1. notify_new_lead(lead)  — called immediately when a lead submits the form.
   Sends:
     • Confirmation email to the lead (sequence step 0 → 1)
     • Internal alert to Derek Lee

2. run_sequence()         — called daily by GitHub Actions (or a cron job).
   Advances each lead through the follow-up email sequence:
     • Step 1  → sent on submission (confirmation + "audit incoming" email)
     • Step 2  → Day 2: "Your audit is ready" delivery email
     • Step 3  → Day 4: follow-up / reply prompt
     • Step 4  → Day 7: paid audit upsell

Setup:
  1. Copy .env.example → .env and fill in SMTP_* vars
  2. Run: python3 funnel_automations.py          (advances all pending sequences)
  3. Or import notify_new_lead from server.py
"""

import csv
import os
import smtplib
import sys
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
SMTP_HOST   = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER   = os.getenv("SMTP_USER", "")
SMTP_PASS   = os.getenv("SMTP_PASS", "")
FROM_EMAIL  = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME   = os.getenv("FROM_NAME", "Derek Lee | RoofersAI")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", SMTP_USER)   # Derek's inbox for alerts

FUNNEL_LEADS_CSV = os.path.join(os.path.dirname(__file__), "funnel_leads.csv")
FUNNEL_LEADS_FIELDS = [
    "id", "first_name", "last_name", "email", "phone",
    "business_name", "website", "google_customers",
    "submitted_at", "status", "sequence_step", "last_emailed_at",
]

AUDIT_LANDING_URL = os.getenv("AUDIT_LANDING_URL", "https://roofers-ai.netlify.app/funnel/audit-landing.html")
BOOKING_URL       = os.getenv("BOOKING_URL", "https://calendly.com/derek-roofers-ai/30min")


# ── Email sequence definitions ─────────────────────────────────────────────────

def _seq_step_1_subject(lead: dict) -> str:
    return f"Got it, {lead['first_name']}! Your free SEO audit is on the way"


def _seq_step_1_html(lead: dict) -> str:
    return f"""
<p>Hi {lead['first_name']},</p>

<p>Thanks for requesting your free SEO audit — you're in the right place.</p>

<p>Here's what happens next:</p>
<ol>
  <li>I'll personally scan <strong>{lead['website']}</strong> against your top local competitors.</li>
  <li>I'll record a <strong>3-5 minute Loom video</strong> walking through the actual issues holding you back.</li>
  <li>You'll receive the video link in a follow-up email within <strong>48 hours</strong>.</li>
</ol>

<p>Keep an eye on your inbox — and if you land in spam, please move me to your primary folder so you don't miss the video.</p>

<p>Talk soon,<br>
Derek Lee<br>
<em>RoofersAI — Local SEO for Contractors</em></p>
"""


def _seq_step_2_subject(lead: dict) -> str:
    return f"[Your Audit] {lead['business_name']} — here's what I found, {lead['first_name']}"


def _seq_step_2_html(lead: dict) -> str:
    return f"""
<p>Hi {lead['first_name']},</p>

<p>Your free SEO audit for <strong>{lead['business_name']}</strong> is ready.</p>

<p>I recorded a short Loom walkthrough covering:</p>
<ul>
  <li>How you stack up against your top 3 local competitors</li>
  <li>The #1 technical issue hurting your Google rankings right now</li>
  <li>Your Google Business Profile completeness score</li>
  <li>2-3 quick wins you can implement this week</li>
</ul>

<p><strong>👉 Watch your audit video here:</strong> [INSERT LOOM LINK]</p>

<p>If you want to talk through the findings — and learn what a full deep-dive audit would uncover — I have a few spots open this week:</p>

<p><a href="{BOOKING_URL}">Book a free 15-minute call →</a></p>

<p>No pressure, no pitch. Just an honest conversation about what's possible for {lead['business_name']}.</p>

<p>Best,<br>
Derek Lee<br>
<em>RoofersAI — Local SEO for Contractors</em></p>
"""


def _seq_step_3_subject(lead: dict) -> str:
    return f"Did you get a chance to watch your audit, {lead['first_name']}?"


def _seq_step_3_html(lead: dict) -> str:
    return f"""
<p>Hi {lead['first_name']},</p>

<p>Just checking in — did you get a chance to watch the Loom audit I sent for {lead['business_name']}?</p>

<p>If you have any questions about anything I covered, just hit reply. I respond to every message personally.</p>

<p>And if you want to talk through a plan to actually fix the issues — here's my calendar:</p>

<p><a href="{BOOKING_URL}">Grab a free 15-minute slot →</a></p>

<p>Talk soon,<br>
Derek</p>
"""


def _seq_step_4_subject(lead: dict) -> str:
    return f"One more thing for {lead['business_name']}, {lead['first_name']}"


def _seq_step_4_html(lead: dict) -> str:
    return f"""
<p>Hi {lead['first_name']},</p>

<p>I don't want to clog your inbox, so this will be my last follow-up for now.</p>

<p>I wanted to mention: for contractors who want to go deeper, I offer a <strong>comprehensive paid audit ($297–$499)</strong> that includes:</p>
<ul>
  <li>Full technical site crawl</li>
  <li>Complete keyword gap analysis vs. competitors</li>
  <li>Backlink profile audit</li>
  <li>Citation audit across 50+ directories</li>
  <li>Prioritized 90-day action plan</li>
</ul>

<p>Most clients recoup that in a single new job. If {lead['business_name']} gets even one extra call per month from better Google visibility, it pays for itself many times over.</p>

<p>Interested? Just reply to this email or <a href="{BOOKING_URL}">book a quick call</a>.</p>

<p>Either way — good luck with the business. I'm rooting for you.</p>

<p>Derek Lee<br>
<em>RoofersAI — Local SEO for Contractors</em><br>
<small><a href="{AUDIT_LANDING_URL}">Unsubscribe / audit landing page</a></small></p>
"""


def _owner_alert_html(lead: dict) -> str:
    return f"""
<h2>New Funnel Lead #{lead['id']}</h2>
<table>
  <tr><td><strong>Name</strong></td><td>{lead['first_name']} {lead['last_name']}</td></tr>
  <tr><td><strong>Email</strong></td><td>{lead['email']}</td></tr>
  <tr><td><strong>Phone</strong></td><td>{lead['phone'] or '—'}</td></tr>
  <tr><td><strong>Business</strong></td><td>{lead['business_name']}</td></tr>
  <tr><td><strong>Website</strong></td><td><a href="{lead['website']}">{lead['website']}</a></td></tr>
  <tr><td><strong>Google customers/mo</strong></td><td>{lead['google_customers'] or '—'}</td></tr>
  <tr><td><strong>Submitted</strong></td><td>{lead['submitted_at']}</td></tr>
</table>
<p><strong>Next step:</strong> Record their Loom audit within 48 hours and reply to this email thread once done.</p>
"""


# ── SMTP helpers ──────────────────────────────────────────────────────────────

def _build_message(to_email: str, to_name: str, subject: str, html_body: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"]      = f"{to_name} <{to_email}>" if to_name else to_email
    msg.attach(MIMEText(html_body, "html"))
    return msg


def _send(msg: MIMEMultipart) -> bool:
    """Return True on success, False on failure (prints error)."""
    if not SMTP_USER or not SMTP_PASS:
        print("⚠️  SMTP credentials not configured — skipping send.")
        return False
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, msg["To"], msg.as_string())
        return True
    except Exception as e:
        print(f"❌  SMTP error: {e}")
        return False


# ── CSV helpers ───────────────────────────────────────────────────────────────

def _load_leads() -> list[dict]:
    if not os.path.exists(FUNNEL_LEADS_CSV):
        return []
    with open(FUNNEL_LEADS_CSV, newline="") as f:
        return list(csv.DictReader(f))


def _save_leads(rows: list[dict]):
    with open(FUNNEL_LEADS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FUNNEL_LEADS_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _days_since(iso_str: str) -> int:
    """Return days elapsed since an ISO-format timestamp string."""
    if not iso_str:
        return 0
    try:
        dt = datetime.fromisoformat(iso_str)
        return (datetime.utcnow() - dt).days
    except ValueError:
        return 0


# ── Public API ────────────────────────────────────────────────────────────────

def notify_new_lead(lead: dict):
    """
    Send step-1 confirmation email to the lead and an alert to the owner.
    Called immediately on form submission from server.py.
    """
    # Confirmation to lead
    msg = _build_message(
        to_email=lead["email"],
        to_name=f"{lead['first_name']} {lead['last_name']}".strip(),
        subject=_seq_step_1_subject(lead),
        html_body=_seq_step_1_html(lead),
    )
    sent = _send(msg)

    # Internal alert to owner
    alert = _build_message(
        to_email=OWNER_EMAIL,
        to_name="Derek Lee",
        subject=f"🔔 New lead: {lead['business_name']} ({lead['email']})",
        html_body=_owner_alert_html(lead),
    )
    _send(alert)

    # Advance sequence step
    if sent:
        _advance_lead_step(lead["id"], new_step=1)


def _advance_lead_step(lead_id, new_step: int):
    rows = _load_leads()
    for row in rows:
        if str(row["id"]) == str(lead_id):
            row["sequence_step"] = str(new_step)
            row["last_emailed_at"] = datetime.utcnow().isoformat()
            if new_step >= 4:
                row["status"] = "sequence_complete"
    _save_leads(rows)


def run_sequence(dry_run: bool = False):
    """
    Advance all active leads through their email sequence based on elapsed days.
    Run this daily (e.g. via GitHub Actions cron).

    Sequence timing:
      Step 0 → 1 : on submission (handled by notify_new_lead)
      Step 1 → 2 : Day 2 after submission  (audit delivery)
      Step 2 → 3 : Day 4 after submission  (follow-up)
      Step 3 → 4 : Day 7 after submission  (upsell)
    """
    rows = _load_leads()
    if not rows:
        print("No leads found.")
        return

    STEP_DAYS   = {1: 2, 2: 4, 3: 7}     # step → days since submitted_at to trigger next email
    STEP_FUNCS  = {
        2: (_seq_step_2_subject, _seq_step_2_html),
        3: (_seq_step_3_subject, _seq_step_3_html),
        4: (_seq_step_4_subject, _seq_step_4_html),
    }

    updated = 0
    for row in rows:
        if row.get("status") in ("sequence_complete", "unsubscribed", "converted"):
            continue

        current_step = int(row.get("sequence_step", "0"))
        next_step    = current_step + 1

        if next_step not in STEP_FUNCS:
            continue  # sequence finished

        days_since_submission = _days_since(row.get("submitted_at", ""))
        trigger_day = STEP_DAYS.get(current_step)

        if trigger_day is None or days_since_submission < trigger_day:
            continue

        subj_fn, body_fn = STEP_FUNCS[next_step]
        subject   = subj_fn(row)
        html_body = body_fn(row)

        if dry_run:
            print(f"[DRY RUN] Would send step {next_step} to {row['email']} ({row['business_name']})")
            print(f"          Subject: {subject}\n")
            continue

        print(f"Sending step {next_step} to {row['email']} ({row['business_name']})...")
        msg = _build_message(
            to_email=row["email"],
            to_name=f"{row['first_name']} {row['last_name']}".strip(),
            subject=subject,
            html_body=html_body,
        )
        if _send(msg):
            row["sequence_step"]   = str(next_step)
            row["last_emailed_at"] = datetime.utcnow().isoformat()
            if next_step >= 4:
                row["status"] = "sequence_complete"
            updated += 1
            print(f"  ✅ Sent.")
        else:
            print(f"  ❌ Failed — will retry on next run.")

    if not dry_run:
        _save_leads(rows)
        print(f"\nDone. {updated} email(s) sent.")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    if dry:
        print("=== DRY RUN — no emails will be sent ===\n")
    run_sequence(dry_run=dry)
