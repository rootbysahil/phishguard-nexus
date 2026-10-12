"""
PHISHGUARD//NEXUS - Unit Tests for URL Feature Extraction
"""

import pytest
from backend.app.ml.features.url_features import extract_url_features, analyze_url_anatomy


def test_benign_url_features():
    url = "https://www.google.com/search?q=cybersecurity"
    features = extract_url_features(url)
    anatomy = analyze_url_anatomy(url)

    assert features["https_present"] == 1.0
    assert features["ip_in_host"] == 0.0
    assert features["homoglyph_detected"] == 0.0
    assert anatomy["protocol"] == "https"
    assert anatomy["domain"] == "google"


def test_homoglyph_phishing_detection():
    url = "http://paypa1-account.xyz/login"
    features = extract_url_features(url)
    anatomy = analyze_url_anatomy(url)

    assert features["homoglyph_detected"] == 1.0
    assert features["suspicious_tld"] == 1.0
    assert features["https_present"] == 0.0
    assert len(anatomy["red_flags"]) >= 2
    assert any("Homoglyph" in rf for rf in anatomy["red_flags"])


def test_bare_ip_host_detection():
    url = "http://192.168.1.100/admin/verify"
    features = extract_url_features(url)
    anatomy = analyze_url_anatomy(url)

    assert features["ip_in_host"] == 1.0
    assert any("IP address" in rf for rf in anatomy["red_flags"])
