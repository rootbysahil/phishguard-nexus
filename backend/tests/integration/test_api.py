"""
PHISHGUARD//NEXUS - Integration Tests for FastAPI Endpoints
Tests /api/health, /api/config, /api/model/metrics, /api/scan, and /api/history.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "components" in data


def test_config_endpoint():
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "threshold_safe" in data
    assert "threshold_suspicious" in data
    assert data["reporting_region"] == "IN"


def test_model_metrics_endpoint():
    response = client.get("/api/model/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "plot_paths" in data


def test_submit_scan_endpoint():
    payload = {
        "type": "url",
        "content": "http://paypa1.secure-verify.net/account/login"
    }
    response = client.post("/api/scan", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert "scan_id" in data
    assert "stream_url" in data


def test_payload_too_large_413():
    payload = {
        "type": "url",
        "content": "http://example.com/" + ("a" * 2100)
    }
    response = client.post("/api/scan", json=payload)
    assert response.status_code == 413
