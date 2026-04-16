#!/usr/bin/env python3
"""
Funnel Automations — Email + SMS Sequence Engine
=================================================
7-step email nurture sequence (21 days) with SMS touchpoints,
lead scoring, re-engagement triggers, and automation logging.

Jobs:
  1. notify_new_lead(lead)  — on form submission: confirmation email + SMS + owner alert
  2. run_sequence()         — daily cron: advance email + SMS sequences
  3. run_reengagement()     — re-engage stale leads (30+ days post-sequence)
  4. recalculate_scores()   — update lead scores for all leads
  5. get_automation_stats() — return analytics dict for the dashboard

CLI:
  python funnel_automations.py                   # run email + SMS sequences
  python funnel_automations.py --dry-run         # preview mode
  python funnel_automations.py --stats           # print analytics
  python funnel_automations.py --reengage        # re-engagement campaign
  python funnel_automations.py --score           # recalculate all lead scores
"""

import csv
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────────
SMTP_HOST   = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER   = os.getenv("SMTP_USER", "")
SMTP_PASS   = os.getenv("SMTP_PASS", "")
FROM_EMAIL  = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME   = os.getenv("FROM_NAME", "Derek Lee | RoofersAI")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", SMTP_USER)

TWILIO_SID    = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM   = os.getenv("TWILIO_FROM_NUMBER", "")

BASE_DIR = os.path.dirname(__file__)
FUNNEL_LEADS_CSV = os.path.join(BASE_DIR, "funnel_leads.csv")
AUTOMATION_LOG   = os.path.join(BASE_DIR, "automation_log.csv")

FUNNEL_LEADS_FIELDS = [
    "id", "first_name", "last_name", "email", "phone",
    "business_name", "website", "google_customers",
    "submitted_at", "status", "sequence_step", "last_emailed_at",
    "lead_score", "sms_step", "last_sms_at",
]

LOG_FIELDS = ["timestamp", "lead_id", "event_type", "details"]

AUDIT_LANDING_URL = os.getenv("AUDIT_LANDING_URL", "https://roofers-ai.netlify.app/funnel/audit-landing.html")
BOOKING_URL       = os.getenv("BOOKING_URL", "https://calendly.com/derek-roofers-ai/30min")


# ── Email sequence definitions (7 steps, 21 days) ─────────────────────────────

def _email_step_1(lead):
    """Day 0: Confirmation + audit incoming."""
    subject = f"Got it, {lead['first_name']}! Your free SEO audit is on the way"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>Thanks for requesting your free SEO audit &mdash; you're in the right place.</p>
<p>Here's what happens next:</p>
<ol>
  <li>I'll personally scan <strong>{lead['website']}</strong> against your top local competitors.</li>
  <li>I'll record a <strong>3-5 minute Loom video</strong> walking through the actual issues holding you back.</li>
  <li>You'll receive the video link in a follow-up email within <strong>48 hours</strong>.</li>
</ol>
<p>Keep an eye on your inbox &mdash; and if I land in spam, please move me to your primary folder so you don't miss the video.</p>
<p>Talk soon,<br>Derek Lee<br><em>RoofersAI &mdash; Local SEO for Contractors</em></p>
"""
    return subject, html

def _email_step_2(lead):
    """Day 2: Value add - one actionable tip from audit."""
    subject = f"One thing from your audit I keep thinking about, {lead['first_name']}"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>I've been thinking about one finding from your audit for <strong>{lead['business_name']}</strong> that could make a quick difference.</p>
<p>Your Google Business Profile likely isn't fully optimized. Businesses with complete profiles get <strong>7x more clicks</strong> than incomplete ones.</p>
<p>Here's one thing you can do right now (takes about 10 minutes):</p>
<p>Log into your Google Business Profile and add your complete list of services. Go to your GBP dashboard &gt; Edit profile &gt; Services, and add every service you offer with descriptions.</p>
<p>Did you get a chance to watch the video? I'd love to hear your thoughts.</p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


def _email_step_3(lead):
    """Day 5: Social proof - case study angle."""
    subject = f"How a contractor in your area went from invisible to #1"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>Quick story I thought you'd find interesting.</p>
<p>A contractor in a similar spot — decent business, loyal customers, but invisible on Google. They were getting maybe 2-3 calls a month from search.</p>
<p>We identified similar issues to what we found in your audit for <strong>{lead['business_name']}</strong>.</p>
<p>After 90 days of focused work:</p>
<ul>
  <li>Phone calls from Google increased by 340%</li>
  <li>They moved from page 3 to the local 3-pack for their top 5 keywords</li>
  <li>Monthly leads from organic search went from 3 to 18</li>
</ul>
<p>Your situation reminds me a lot of theirs. The potential is definitely there.</p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


def _email_step_4(lead):
    """Day 8: Paid audit offer ($297-$499)."""
    subject = f"Your custom SEO roadmap for {lead['business_name']}"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>The free audit I did for you scratched the surface. Based on what I found, I think there's a lot of untapped opportunity for <strong>{lead['business_name']}</strong>.</p>
<p>I'd like to offer you a comprehensive deep audit that goes 10x further. Here's exactly what you'd get:</p>
<ol>
  <li>Full technical crawl of your entire website</li>
  <li>Complete keyword gap analysis vs. competitors</li>
  <li>Backlink profile audit with actionable opportunities</li>
  <li>Citation audit across 50+ directories</li>
  <li>Page-by-page content assessment</li>
  <li>Prioritized 90-day action plan</li>
</ol>
<p>The investment is <strong>$297-$499</strong>. I only take on 3-5 of these per month to ensure quality.</p>
<p>The free audit tips are yours to keep either way — no pressure at all.</p>
<p>Interested? Just reply "interested" or <a href="{BOOKING_URL}">book a quick call</a>.</p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


def _email_step_5(lead):
    """Day 12: Objection handling - 'can't I do this myself?'"""
    subject = f"Totally fair question about the audit..."
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>A lot of business owners I talk to have the same thought: "Can't I just do this myself?"</p>
<p>And honestly? Yes, you could. All the information is out there.</p>
<p>But here's the thing — SEO isn't really about knowing what to do. It's about knowing what to do <strong>FIRST</strong>. There are literally hundreds of things you could work on. The deep audit is like GPS vs. wandering.</p>
<p>Without it, you might spend 3 months optimizing page speed when the real issue is your Google Business Profile categories. Or spend weeks writing blog posts when your site has technical errors blocking Google from even indexing your pages.</p>
<p>The audit tells you: "Do THIS first, then THIS, then THIS." It turns months of guesswork into a clear 90-day roadmap.</p>
<p>No pressure at all. If you'd like to chat about it for 10 minutes, here's my calendar: <a href="{BOOKING_URL}">Grab a slot</a></p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


def _email_step_6(lead):
    """Day 16: Urgency - competitor pulling ahead."""
    subject = f"Heads up — your competitors are pulling ahead, {lead['first_name']}"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>I noticed something while doing research this week. Your top competitors in the area have been actively optimizing their Google presence — adding reviews, updating their profiles, building citations.</p>
<p>The gap between {lead['business_name']}'s online presence and theirs is growing. And with local SEO, these gaps compound — the longer you wait, the harder it is to catch up.</p>
<p>I still have a couple spots open for deep audits this month. If you want that clear roadmap for how to close the gap, just reply and I'll get you set up.</p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


def _email_step_7(lead):
    """Day 21: Breakup - 'should I close your file?'"""
    subject = f"Should I close your file, {lead['first_name']}?"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>I know you're busy running <strong>{lead['business_name']}</strong>, so I'll keep this short.</p>
<p>I'm cleaning up my audit pipeline and wanted to check in one last time before I close out your file.</p>
<p>No hard feelings at all — I know the timing isn't always right.</p>
<p>One last thought: even if you don't go with the full audit, please do that Google Business Profile update I mentioned in my second email. It's free, takes 10 minutes, and could genuinely help.</p>
<p>If you ever want a second pair of eyes on your website or Google presence, the offer stands. Just reply to this email.</p>
<p>And if you know another business owner who might benefit from a free audit, I'd really appreciate the introduction.</p>
<p>Wishing you all the best!</p>
<p>Derek Lee<br><em>RoofersAI — Local SEO for Contractors</em><br>
<small><a href="{AUDIT_LANDING_URL}">Unsubscribe</a></small></p>
"""
    return subject, html


def _owner_alert_html(lead):
    return f"""
<h2>New Funnel Lead #{lead['id']}</h2>
<table>
  <tr><td><strong>Name</strong></td><td>{lead['first_name']} {lead['last_name']}</td></tr>
  <tr><td><strong>Email</strong></td><td>{lead['email']}</td></tr>
  <tr><td><strong>Phone</strong></td><td>{lead.get('phone') or '—'}</td></tr>
  <tr><td><strong>Business</strong></td><td>{lead['business_name']}</td></tr>
  <tr><td><strong>Website</strong></td><td><a href="{lead['website']}">{lead['website']}</a></td></tr>
  <tr><td><strong>Google customers/mo</strong></td><td>{lead.get('google_customers') or '—'}</td></tr>
  <tr><td><strong>Submitted</strong></td><td>{lead['submitted_at']}</td></tr>
</table>
<p><strong>Next step:</strong> Record their Loom audit within 48 hours.</p>
"""


def _reengagement_email(lead):
    """Re-engagement email for stale leads (30+ days post-sequence)."""
    subject = f"Quick update for {lead['business_name']}, {lead['first_name']}"
    html = f"""
<p>Hi {lead['first_name']},</p>
<p>It's been a while since we connected about <strong>{lead['business_name']}</strong>'s online presence. A lot has changed in local SEO recently, and I wanted to share a quick update.</p>
<p>Google has rolled out several algorithm updates that affect local businesses. Some of your competitors may have already adapted — which means the window to catch up is getting smaller.</p>
<p>I'd love to do a quick refresh audit of your site to see where things stand now. Completely free, just like last time.</p>
<p>Interested? Just reply to this email or <a href="{BOOKING_URL}">book a quick call</a>.</p>
<p>Best,<br>Derek Lee<br><em>RoofersAI</em></p>
"""
    return subject, html


# ── SMS templates ─────────────────────────────────────────────────────────────

def _sms_step_1(lead):
    """Day 0: Welcome text after form submission."""
    return (
        f"Hi {lead['first_name']}! This is Derek from RoofersAI. "
        f"Thanks for requesting your free SEO audit for {lead['business_name']}. "
        f"I'll have your personalized video audit ready within 48 hours. "
        f"Reply STOP to opt out."
    )


def _sms_step_2(lead):
    """Day 3: Audit video ready nudge."""
    return (
        f"Hi {lead['first_name']}, your SEO audit video for {lead['business_name']} "
        f"was sent to your email. Did you get a chance to watch it? "
        f"Let me know if you have any questions! - Derek, RoofersAI"
    )


def _sms_step_3(lead):
    """Day 9: Check-in after paid offer email."""
    return (
        f"Hey {lead['first_name']}, just checking in. I sent over some info about "
        f"a deeper SEO analysis for {lead['business_name']}. "
        f"Happy to answer any questions — just text back. - Derek"
    )


# ── SMTP helpers ──────────────────────────────────────────────────────────────

def _build_message(to_email, to_name, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"]      = f"{to_name} <{to_email}>" if to_name else to_email
    msg.attach(MIMEText(html_body, "html"))
    return msg


def _send(msg):
    """Return True on success, False on failure."""
    if not SMTP_USER or not SMTP_PASS:
        print("  SMTP credentials not configured — skipping send.")
        return False
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, msg["To"], msg.as_string())
        return True
    except Exception as e:
        print(f"  SMTP error: {e}")
        return False


# ── SMS helper ────────────────────────────────────────────────────────────────

def _send_sms(to_number, body):
    """Send SMS via Twilio. Returns True on success."""
    if not TWILIO_SID or not TWILIO_TOKEN or not TWILIO_FROM:
        print("  Twilio credentials not configured — skipping SMS.")
        return False
    if not to_number:
        return False
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(body=body, from_=TWILIO_FROM, to=to_number)
        return True
    except ImportError:
        print("  twilio package not installed — skipping SMS.")
        return False
    except Exception as e:
        print(f"  Twilio error: {e}")
        return False


# ── CSV helpers ───────────────────────────────────────────────────────────────

def _load_leads():
    if not os.path.exists(FUNNEL_LEADS_CSV):
        return []
    with open(FUNNEL_LEADS_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    # Backfill new fields for old CSVs
    for row in rows:
        for field in FUNNEL_LEADS_FIELDS:
            if field not in row:
                row[field] = ""
    return rows


def _save_leads(rows):
    with open(FUNNEL_LEADS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FUNNEL_LEADS_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FUNNEL_LEADS_FIELDS})


def _days_since(iso_str):
    """Return days elapsed since an ISO-format timestamp string."""
    if not iso_str:
        return 0
    try:
        dt = datetime.fromisoformat(iso_str)
        return (datetime.utcnow() - dt).days
    except ValueError:
        return 0


# ── Logging ───────────────────────────────────────────────────────────────────

def log_event(lead_id, event_type, details=""):
    """Append an event to the automation log CSV."""
    exists = os.path.exists(AUTOMATION_LOG)
    with open(AUTOMATION_LOG, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "lead_id": str(lead_id),
            "event_type": event_type,
            "details": details,
        })


# ── Lead Scoring ──────────────────────────────────────────────────────────────

def calculate_lead_score(lead):
    """Calculate a lead score (0-100) based on profile completeness and engagement."""
    score = 0
    # Profile completeness
    if lead.get("phone"):
        score += 10
    if lead.get("website"):
        score += 10
    if lead.get("last_name"):
        score += 5

    # Google customers value
    gc = lead.get("google_customers", "").strip().lower()
    if gc:
        try:
            gc_num = int(gc.replace("+", "").replace(",", "").split("-")[0])
            if gc_num >= 50:
                score += 15
            elif gc_num >= 20:
                score += 10
            elif gc_num >= 1:
                score += 5
        except (ValueError, IndexError):
            if gc in ("50+", "many", "lots"):
                score += 15
            elif gc not in ("0", "none", ""):
                score += 5

    # Sequence engagement (further = more engaged)
    step = int(lead.get("sequence_step", "0"))
    score += min(step * 5, 35)  # up to 35 points for reaching step 7

    # SMS engagement
    sms_step = int(lead.get("sms_step", "0"))
    score += min(sms_step * 5, 15)  # up to 15 points for SMS touchpoints

    # Status bonuses
    status = lead.get("status", "")
    if status == "converted":
        score = 100
    elif status == "sequence_complete":
        score += 10

    return min(score, 100)


def recalculate_scores():
    """Recalculate lead scores for all leads."""
    rows = _load_leads()
    updated = 0
    for row in rows:
        old_score = row.get("lead_score", "0")
        new_score = calculate_lead_score(row)
        if str(new_score) != str(old_score):
            row["lead_score"] = str(new_score)
            updated += 1
    _save_leads(rows)
    print(f"Scores updated for {updated} lead(s).")
    return updated


# ── Public API ────────────────────────────────────────────────────────────────

def notify_new_lead(lead):
    """
    Send step-1 confirmation email + welcome SMS + owner alert.
    Called immediately on form submission from server.py.
    """
    # Confirmation email to lead
    subject, html = _email_step_1(lead)
    msg = _build_message(
        to_email=lead["email"],
        to_name=f"{lead['first_name']} {lead.get('last_name', '')}".strip(),
        subject=subject,
        html_body=html,
    )
    sent = _send(msg)

    # Owner alert
    alert = _build_message(
        to_email=OWNER_EMAIL,
        to_name="Derek Lee",
        subject=f"New lead: {lead['business_name']} ({lead['email']})",
        html_body=_owner_alert_html(lead),
    )
    _send(alert)

    # Welcome SMS
    phone = lead.get("phone", "").strip()
    sms_sent = False
    if phone:
        sms_body = _sms_step_1(lead)
        sms_sent = _send_sms(phone, sms_body)

    # Advance sequence step and log
    if sent:
        _advance_lead(lead["id"], email_step=1, sms_step=1 if sms_sent else 0)
        log_event(lead["id"], "email_sent", "Step 1: Confirmation")
    if sms_sent:
        log_event(lead["id"], "sms_sent", "SMS 1: Welcome text")

    # Calculate initial score
    lead["sequence_step"] = "1" if sent else "0"
    lead["sms_step"] = "1" if sms_sent else "0"
    score = calculate_lead_score(lead)
    _update_lead_field(lead["id"], "lead_score", str(score))
    log_event(lead["id"], "score_updated", f"Initial score: {score}")


def _advance_lead(lead_id, email_step=None, sms_step=None):
    """Update a lead's sequence step, SMS step, and timestamps."""
    rows = _load_leads()
    for row in rows:
        if str(row["id"]) == str(lead_id):
            if email_step is not None:
                row["sequence_step"] = str(email_step)
                row["last_emailed_at"] = datetime.utcnow().isoformat()
            if sms_step is not None:
                row["sms_step"] = str(sms_step)
                row["last_sms_at"] = datetime.utcnow().isoformat()
            if email_step and email_step >= 7:
                row["status"] = "sequence_complete"
    _save_leads(rows)


def _update_lead_field(lead_id, field, value):
    """Update a single field for a lead."""
    rows = _load_leads()
    for row in rows:
        if str(row["id"]) == str(lead_id):
            row[field] = value
    _save_leads(rows)


def run_sequence(dry_run=False):
    """
    Advance all active leads through the 7-step email + 3-step SMS sequence.
    Run daily via GitHub Actions cron or manually.

    Email timing (days since submission):
      Step 0 -> 1 : Day 0  (handled by notify_new_lead)
      Step 1 -> 2 : Day 2  (value add)
      Step 2 -> 3 : Day 5  (social proof)
      Step 3 -> 4 : Day 8  (paid offer)
      Step 4 -> 5 : Day 12 (objection handling)
      Step 5 -> 6 : Day 16 (urgency)
      Step 6 -> 7 : Day 21 (breakup)

    SMS timing (days since submission):
      SMS 0 -> 1 : Day 0  (handled by notify_new_lead)
      SMS 1 -> 2 : Day 3  (audit ready nudge)
      SMS 2 -> 3 : Day 9  (check-in after paid offer)
    """
    rows = _load_leads()
    if not rows:
        print("No leads found.")
        return

    EMAIL_SCHEDULE = {1: 2, 2: 5, 3: 8, 4: 12, 5: 16, 6: 21}
    EMAIL_FUNCS = {
        2: _email_step_2,
        3: _email_step_3,
        4: _email_step_4,
        5: _email_step_5,
        6: _email_step_6,
        7: _email_step_7,
    }

    SMS_SCHEDULE = {1: 3, 2: 9}
    SMS_FUNCS = {
        2: _sms_step_2,
        3: _sms_step_3,
    }

    emails_sent = 0
    sms_sent = 0

    for row in rows:
        if row.get("status") in ("sequence_complete", "unsubscribed", "converted", "paused"):
            continue

        days = _days_since(row.get("submitted_at", ""))

        # --- Email sequence ---
        current_email = int(row.get("sequence_step", "0"))
        next_email = current_email + 1

        if next_email in EMAIL_FUNCS:
            trigger_day = EMAIL_SCHEDULE.get(current_email)
            if trigger_day is not None and days >= trigger_day:
                subj_fn = EMAIL_FUNCS[next_email]
                subject, html = subj_fn(row)

                if dry_run:
                    print(f"[DRY RUN] Email step {next_email} -> {row['email']} ({row['business_name']})")
                    print(f"          Subject: {subject}")
                else:
                    print(f"Sending email step {next_email} to {row['email']}...")
                    msg = _build_message(
                        to_email=row["email"],
                        to_name=f"{row['first_name']} {row.get('last_name', '')}".strip(),
                        subject=subject,
                        html_body=html,
                    )
                    if _send(msg):
                        row["sequence_step"] = str(next_email)
                        row["last_emailed_at"] = datetime.utcnow().isoformat()
                        if next_email >= 7:
                            row["status"] = "sequence_complete"
                        emails_sent += 1
                        log_event(row["id"], "email_sent", f"Step {next_email}: {subject[:50]}")
                        if next_email >= 7:
                            log_event(row["id"], "sequence_complete", "7-step sequence finished")
                        print(f"  Sent.")
                    else:
                        print(f"  Failed — will retry next run.")

        # --- SMS sequence ---
        current_sms = int(row.get("sms_step", "0"))
        next_sms = current_sms + 1

        if next_sms in SMS_FUNCS and row.get("phone"):
            sms_trigger_day = SMS_SCHEDULE.get(current_sms)
            if sms_trigger_day is not None and days >= sms_trigger_day:
                sms_body = SMS_FUNCS[next_sms](row)

                if dry_run:
                    print(f"[DRY RUN] SMS step {next_sms} -> {row.get('phone')} ({row['business_name']})")
                    print(f"          Body: {sms_body[:60]}...")
                else:
                    print(f"Sending SMS step {next_sms} to {row.get('phone')}...")
                    if _send_sms(row["phone"], sms_body):
                        row["sms_step"] = str(next_sms)
                        row["last_sms_at"] = datetime.utcnow().isoformat()
                        sms_sent += 1
                        log_event(row["id"], "sms_sent", f"SMS {next_sms}")
                        print(f"  Sent.")
                    else:
                        print(f"  SMS failed — will retry next run.")

        # Recalculate score
        if not dry_run:
            new_score = calculate_lead_score(row)
            if str(new_score) != str(row.get("lead_score", "0")):
                row["lead_score"] = str(new_score)

    if not dry_run:
        _save_leads(rows)
        print(f"\nDone. {emails_sent} email(s) and {sms_sent} SMS sent.")
    else:
        print(f"\n[DRY RUN] Would send {emails_sent} emails and {sms_sent} SMS.")


def run_reengagement(dry_run=False):
    """
    Send re-engagement emails to leads that completed the sequence 30+ days ago
    without converting.
    """
    rows = _load_leads()
    count = 0

    for row in rows:
        if row.get("status") != "sequence_complete":
            continue
        days_since_last = _days_since(row.get("last_emailed_at", ""))
        if days_since_last < 30:
            continue

        subject, html = _reengagement_email(row)

        if dry_run:
            print(f"[DRY RUN] Re-engage -> {row['email']} ({row['business_name']})")
            count += 1
            continue

        print(f"Re-engaging {row['email']} ({row['business_name']})...")
        msg = _build_message(
            to_email=row["email"],
            to_name=f"{row['first_name']} {row.get('last_name', '')}".strip(),
            subject=subject,
            html_body=html,
        )
        if _send(msg):
            row["last_emailed_at"] = datetime.utcnow().isoformat()
            count += 1
            log_event(row["id"], "email_sent", "Re-engagement email")
            print(f"  Sent.")

    if not dry_run:
        _save_leads(rows)
    print(f"Re-engaged {count} lead(s).")
    return count


# ── Analytics ─────────────────────────────────────────────────────────────────

def get_automation_stats():
    """Return analytics dict for the dashboard API."""
    rows = _load_leads()
    today = datetime.utcnow().date().isoformat()

    by_status = {}
    by_step = {}
    scores = []
    active = 0

    for row in rows:
        status = row.get("status", "new")
        by_status[status] = by_status.get(status, 0) + 1

        step = row.get("sequence_step", "0")
        by_step[step] = by_step.get(step, 0) + 1

        score = int(row.get("lead_score", "0"))
        scores.append(score)

        if status not in ("sequence_complete", "unsubscribed", "converted", "paused"):
            active += 1

    # Count today's sends from log
    emails_today = 0
    sms_today = 0
    if os.path.exists(AUTOMATION_LOG):
        with open(AUTOMATION_LOG, newline="") as f:
            for entry in csv.DictReader(f):
                ts = entry.get("timestamp", "")
                if ts.startswith(today):
                    if entry.get("event_type") == "email_sent":
                        emails_today += 1
                    elif entry.get("event_type") == "sms_sent":
                        sms_today += 1

    return {
        "total_leads": len(rows),
        "active_sequences": active,
        "by_status": by_status,
        "by_step": by_step,
        "avg_lead_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "emails_sent_today": emails_today,
        "sms_sent_today": sms_today,
    }


def print_stats():
    """Print automation stats to console."""
    stats = get_automation_stats()
    print("=" * 50)
    print("FUNNEL AUTOMATIONS — DASHBOARD")
    print("=" * 50)
    print(f"Total Leads:       {stats['total_leads']}")
    print(f"Active Sequences:  {stats['active_sequences']}")
    print(f"Avg Lead Score:    {stats['avg_lead_score']}")
    print(f"Emails Today:      {stats['emails_sent_today']}")
    print(f"SMS Today:         {stats['sms_sent_today']}")
    print()
    print("By Status:")
    for s, c in sorted(stats["by_status"].items()):
        print(f"  {s:20s} {c}")
    print()
    print("By Sequence Step:")
    step_names = {
        "0": "New", "1": "Confirmed", "2": "Value Add",
        "3": "Social Proof", "4": "Paid Offer", "5": "Objection",
        "6": "Urgency", "7": "Breakup",
    }
    for s in sorted(stats["by_step"].keys(), key=lambda x: int(x)):
        name = step_names.get(s, f"Step {s}")
        print(f"  {name:20s} {stats['by_step'][s]}")
    print("=" * 50)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv

    if "--stats" in sys.argv:
        print_stats()
    elif "--reengage" in sys.argv:
        if dry:
            print("=== DRY RUN — no emails will be sent ===\n")
        run_reengagement(dry_run=dry)
    elif "--score" in sys.argv:
        recalculate_scores()
    else:
        if dry:
            print("=== DRY RUN — no emails/SMS will be sent ===\n")
        run_sequence(dry_run=dry)
