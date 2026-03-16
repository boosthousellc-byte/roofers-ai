"""Tests for the Flask API server."""

import json
from unittest.mock import patch, MagicMock

import pytest

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_industries(client):
    resp = client.get("/api/industries")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "dentist" in data
    assert "generic" in data
    assert data["roofer"] == "Roofing Company"


def test_audit_missing_json(client):
    resp = client.post("/api/audit", content_type="application/json")
    assert resp.status_code == 400


def test_audit_missing_required_fields(client):
    resp = client.post("/api/audit", json={"url": "https://example.com"})
    assert resp.status_code == 400
    assert "required" in resp.get_json()["error"]


def test_audit_invalid_industry_falls_back_to_generic(client):
    fake_results = {
        "overall_score": 75,
        "grade": "C",
        "checks": {},
        "recommendations": [],
    }
    with patch("server.run_audit", return_value=fake_results) as mock_audit:
        resp = client.post("/api/audit", json={
            "url": "https://example.com",
            "business": "Test Biz",
            "city": "Denver",
            "industry": "nonexistent_industry",
        })
        assert resp.status_code == 200
        mock_audit.assert_called_once_with(
            "https://example.com", "Test Biz", "Denver", "generic"
        )


def test_audit_success(client):
    fake_results = {"overall_score": 85, "grade": "B"}
    with patch("server.run_audit", return_value=fake_results):
        resp = client.post("/api/audit", json={
            "url": "https://example.com",
            "business": "Acme",
            "city": "SLC",
            "industry": "roofer",
        })
        assert resp.status_code == 200
        assert resp.get_json()["overall_score"] == 85


def test_audit_fetch_failure_returns_502(client):
    with patch("server.run_audit", return_value=None):
        resp = client.post("/api/audit", json={
            "url": "https://bad-url.invalid",
            "business": "Acme",
            "city": "SLC",
        })
        assert resp.status_code == 502


def test_audit_pdf_missing_fields(client):
    resp = client.post("/api/audit/pdf", json={"url": "https://example.com"})
    assert resp.status_code == 400


def test_audit_pdf_fetch_failure_returns_502(client):
    with patch("server.run_audit", return_value=None):
        resp = client.post("/api/audit/pdf", json={
            "url": "https://bad.invalid",
            "business": "Acme",
            "city": "SLC",
        })
        assert resp.status_code == 502


def test_audit_pdf_success(client, tmp_path):
    fake_results = {
        "business_name": "Test Co",
        "overall_score": 90,
        "grade": "A",
    }
    fake_pdf = tmp_path / "test.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")

    with patch("server.run_audit", return_value=fake_results), \
         patch("server.generate_pdf", return_value=str(fake_pdf)):
        resp = client.post("/api/audit/pdf", json={
            "url": "https://example.com",
            "business": "Test Co",
            "city": "SLC",
        })
        assert resp.status_code == 200
        assert resp.content_type == "application/pdf"
