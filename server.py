#!/usr/bin/env python3
"""
Audit Engine API Server
Lightweight Flask backend for the website audit tool.

Run locally:
    python server.py

Deploy to DigitalOcean:
    gunicorn server:app --bind 0.0.0.0:8080
"""

import csv
import io
import os
from datetime import date, datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from audit_engine import run_audit, generate_pdf, export_json, INDUSTRY_PROFILES

app = Flask(__name__)
CORS(app)

FUNNEL_LEADS_CSV = os.path.join(os.path.dirname(__file__), "funnel_leads.csv")
FUNNEL_LEADS_FIELDS = [
    "id", "first_name", "last_name", "email", "phone",
    "business_name", "website", "google_customers",
    "submitted_at", "status", "sequence_step", "last_emailed_at",
]


def _next_lead_id():
    if not os.path.exists(FUNNEL_LEADS_CSV):
        return 1
    with open(FUNNEL_LEADS_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    return len(rows) + 1


def _append_lead(lead: dict):
    exists = os.path.exists(FUNNEL_LEADS_CSV)
    with open(FUNNEL_LEADS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FUNNEL_LEADS_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({k: lead.get(k, "") for k in FUNNEL_LEADS_FIELDS})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/industries", methods=["GET"])
def list_industries():
    """Return available industry profiles."""
    industries = {k: v["label"] for k, v in INDUSTRY_PROFILES.items()}
    return jsonify(industries)


@app.route("/api/audit", methods=["POST"])
def audit():
    """Run a website audit and return JSON results."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    url = data.get("url", "").strip()
    business = data.get("business", "").strip()
    city = data.get("city", "").strip()
    industry = data.get("industry", "generic").strip()

    if not url or not business or not city:
        return jsonify({"error": "url, business, and city are required"}), 400

    if industry not in INDUSTRY_PROFILES:
        industry = "generic"

    results = run_audit(url, business, city, industry)
    if not results:
        return jsonify({"error": "Could not fetch the website. Check the URL and try again."}), 502

    return jsonify(results)


@app.route("/api/audit/pdf", methods=["POST"])
def audit_pdf():
    """Run audit and return PDF report."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    url = data.get("url", "").strip()
    business = data.get("business", "").strip()
    city = data.get("city", "").strip()
    industry = data.get("industry", "generic").strip()

    if not url or not business or not city:
        return jsonify({"error": "url, business, and city are required"}), 400

    if industry not in INDUSTRY_PROFILES:
        industry = "generic"

    results = run_audit(url, business, city, industry)
    if not results:
        return jsonify({"error": "Could not fetch the website. Check the URL and try again."}), 502

    # Generate PDF to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    pdf_path = generate_pdf(results, tmp_path)
    if not pdf_path:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        return jsonify({"error": "PDF generation failed. Install reportlab."}), 500

    try:
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"audit_{business.replace(' ', '_').lower()}.pdf",
        )
    finally:
        try:
            os.unlink(pdf_path)
        except OSError:
            pass


@app.route("/api/leads", methods=["POST"])
def capture_lead():
    """Receive a funnel lead form submission, persist it, and trigger notifications."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["first_name", "email", "business_name", "website"]
    missing = [f for f in required if not data.get(f, "").strip()]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    lead = {
        "id": _next_lead_id(),
        "first_name": data.get("first_name", "").strip(),
        "last_name": data.get("last_name", "").strip(),
        "email": data.get("email", "").strip().lower(),
        "phone": data.get("phone", "").strip(),
        "business_name": data.get("business_name", "").strip(),
        "website": data.get("website", "").strip(),
        "google_customers": data.get("google_customers", "").strip(),
        "submitted_at": datetime.utcnow().isoformat(),
        "status": "new",
        "sequence_step": "0",
        "last_emailed_at": "",
    }

    _append_lead(lead)

    # Kick off async notification (non-blocking; ignore import error if deps missing)
    try:
        from funnel_automations import notify_new_lead
        notify_new_lead(lead)
    except Exception:
        pass

    return jsonify({"ok": True, "id": lead["id"]}), 201


@app.route("/api/leads", methods=["GET"])
def list_leads():
    """Return all captured funnel leads (internal use)."""
    if not os.path.exists(FUNNEL_LEADS_CSV):
        return jsonify([])
    with open(FUNNEL_LEADS_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    return jsonify(rows)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
