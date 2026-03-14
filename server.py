#!/usr/bin/env python3
"""
Audit Engine API Server
Lightweight Flask backend for the website audit tool.

Run locally:
    python server.py

Deploy to DigitalOcean:
    gunicorn server:app --bind 0.0.0.0:8080
"""

import io
import os

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from audit_engine import run_audit, generate_pdf, export_json, INDUSTRY_PROFILES

app = Flask(__name__)
CORS(app)


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
