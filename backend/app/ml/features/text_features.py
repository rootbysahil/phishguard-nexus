"""
PHISHGUARD//NEXUS - Email and SMS Text Feature Extraction Pipeline
Extracts lexical, semantic intent, and hyperlink indicators from text bodies.
"""

import re
from typing import Any, Dict, List
from bs4 import BeautifulSoup

URGENCY_KEYWORDS = [
    "verify now", "account suspended", "immediate action", "unauthorized access",
    "security alert", "limited time", "act now", "action required", "urgent",
    "within 24 hours", "locked", "compromised", "update your account",
    "billing problem", "confirm identity", "unusual activity", "final notice"
]

CREDENTIAL_KEYWORDS = [
    "enter your password", "login credentials", "verify pin", "credit card",
    "social security", "ssn", "cvv", "bank account", "security question",
    "sign in below", "password reset", "claim reward", "tax refund"
]

URL_REGEX = re.compile(
    r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)


def extract_text_features(content: str, is_html: bool = False) -> Dict[str, Any]:
    """
    Extracts heuristic scam indicators and hyperlink counts from message content.
    """
    text_lower = content.lower()
    
    # Keyword intent counters
    urgency_count = sum(text_lower.count(kw) for kw in URGENCY_KEYWORDS)
    credential_count = sum(text_lower.count(kw) for kw in CREDENTIAL_KEYWORDS)
    
    # URL extraction
    embedded_urls = URL_REGEX.findall(content)
    link_count = len(embedded_urls)
    
    mismatched_links = 0
    form_count = 0

    if is_html or "<a " in text_lower or "<form" in text_lower:
        soup = BeautifulSoup(content, "html.parser")
        forms = soup.find_all("form")
        form_count = len(forms)

        anchors = soup.find_all("a")
        for a in anchors:
            href = a.get("href", "")
            anchor_text = a.get_text().strip().lower()
            if href and anchor_text:
                if any(ext in anchor_text for ext in [".com", ".net", ".org", "http://", "https://"]):
                    if anchor_text not in href.lower():
                        mismatched_links += 1

    return {
        "text_length": len(content),
        "urgency_count": float(urgency_count),
        "credential_request_count": float(credential_count),
        "link_count": float(link_count),
        "link_text_href_mismatch": float(mismatched_links),
        "html_form_count": float(form_count),
        "embedded_urls": embedded_urls
    }
