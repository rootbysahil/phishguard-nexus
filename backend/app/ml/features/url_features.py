"""
PHISHGUARD//NEXUS - URL Feature Extraction Pipeline
Extracts 28+ deterministic lexical, statistical, and structural features from URL strings.
Pure Python, 0 external network calls, zero train/serve skew.
"""

import math
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import parse_qs, urlparse

# Curated list of high-profile target brands for homoglyph / typosquat detection
TOP_BRANDS = [
    "paypal", "google", "microsoft", "apple", "amazon", "netflix",
    "facebook", "instagram", "whatsapp", "bankofamerica", "chase",
    "wellsfargo", "citibank", "yahoo", "linkedin", "dropbox", "adobe",
    "github", "twitter", "ebay", "walmart", "target", "binance",
    "coinbase", "telegram", "steam", "spotify", "roblox", "discord",
    "statebankofindia", "hdfcbank", "icicibank", "axisbank", "paytm"
]

# Common URL Shortener domains
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "tiny.cc", "lnkd.in", "rebrand.ly", "cutt.ly"
}

# High-risk / abuse-prevalent TLDs
SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "loan", "click", "country", "gq", "ml",
    "cf", "ga", "fit", "tk", "men", "buzz", "rest", "cam", "kim",
    "surf", "wang", "link", "party", "date", "racing", "vip"
}

# Common homoglyph substitutions
HOMOGLYPH_MAP = {
    '1': 'l', '0': 'o', '5': 's', '8': 'b', '3': 'e', '4': 'a',
    'vv': 'w', 'rn': 'm', 'cl': 'd'
}

IPV4_REGEX = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def calculate_entropy(text: str) -> float:
    """Calculates Shannon entropy of a given string."""
    if not text:
        return 0.0
    probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return -sum(p * math.log(p, 2) for p in probabilities if p > 0)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes Levenshtein edit distance without external C-extensions."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def parse_url_components(url: str) -> Tuple[str, str, str, str, str, str, str]:
    """
    Parses a URL into (scheme, netloc, subdomain, domain, tld, path, query).
    Uses lightweight manual parsing when tldextract is unavailable.
    """
    if not url.startswith(("http://", "https://")):
        url_to_parse = "http://" + url
    else:
        url_to_parse = url

    parsed = urlparse(url_to_parse)
    scheme = parsed.scheme
    netloc = parsed.netloc.split(":")[0].lower() # strip port
    path = parsed.path
    query = parsed.query

    # Split domain segments
    parts = netloc.split(".")
    if len(parts) >= 2:
        tld = parts[-1]
        domain = parts[-2]
        subdomain = ".".join(parts[:-2])
    elif len(parts) == 1:
        domain = parts[0]
        subdomain = ""
        tld = ""
    else:
        domain = ""
        subdomain = ""
        tld = ""

    return scheme, netloc, subdomain, domain, tld, path, query


def detect_homoglyph(text: str) -> Dict[str, Any]:
    """Checks if a string uses homoglyph substitution targeting known brands."""
    lowered = text.lower()
    
    # Check normalized version
    normalized = lowered
    for fake, real in HOMOGLYPH_MAP.items():
        normalized = normalized.replace(fake, real)

    for brand in TOP_BRANDS:
        if brand in normalized and brand not in lowered:
            # Found substitution!
            for fake, real in HOMOGLYPH_MAP.items():
                if fake in lowered:
                    pos = lowered.find(fake)
                    return {
                        "detected": True,
                        "original": brand,
                        "found": text,
                        "swapped_pos": pos,
                        "swapped_char": fake
                    }
    return {
        "detected": False,
        "original": "",
        "found": "",
        "swapped_pos": -1,
        "swapped_char": ""
    }


def find_closest_brand(text: str) -> Tuple[int, str]:
    """Returns minimum Levenshtein distance to any top brand and the target brand."""
    min_dist = 999
    closest = ""
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", text.lower())
    for brand in TOP_BRANDS:
        dist = levenshtein_distance(cleaned, brand)
        if dist < min_dist:
            min_dist = dist
            closest = brand
    return min_dist, closest


def extract_url_features(url: str) -> Dict[str, float]:
    """
    Extracts numerical and categorical feature dictionary suitable for scikit-learn.
    All outputs are float / int compatible.
    """
    scheme, netloc, subdomain, domain, tld, path, query = parse_url_components(url)
    full_url = url.strip()

    # Lengths
    url_len = len(full_url)
    host_len = len(netloc)
    path_len = len(path)

    # Character distributions
    digits = sum(c.isdigit() for c in full_url)
    digit_ratio = digits / max(1, url_len)
    special_chars = sum(c in "!@#$%^&*()-_+=~`[]{}|:;\"'<>,.?" for c in full_url)
    special_char_ratio = special_chars / max(1, url_len)

    # Structural counts
    dot_count = full_url.count(".")
    hyphen_count = full_url.count("-")
    at_symbol_present = 1.0 if "@" in full_url else 0.0
    subdomain_depth = float(len(subdomain.split(".")) if subdomain else 0)
    path_depth = float(len([p for p in path.split("/") if p]))
    
    # Query parameters
    parsed_query = parse_qs(query)
    query_param_count = float(len(parsed_query))
    fragment_present = 1.0 if "#" in full_url else 0.0
    double_slash_in_path = 1.0 if "//" in path else 0.0

    # Max consecutive digits in host
    digit_runs = re.findall(r"\d+", netloc)
    digit_run_max = float(max((len(r) for r in digit_runs), default=0))

    # Host semantics
    ip_in_host = 1.0 if IPV4_REGEX.match(netloc) else 0.0
    punycode_detected = 1.0 if "xn--" in netloc else 0.0
    shortener_detected = 1.0 if netloc in SHORTENER_DOMAINS else 0.0
    suspicious_tld = 1.0 if tld.lower() in SUSPICIOUS_TLDS else 0.0
    https_present = 1.0 if scheme == "https" else 0.0
    shannon_entropy = calculate_entropy(netloc)

    # Brand heuristics
    homo_info = detect_homoglyph(netloc)
    homoglyph_detected = 1.0 if homo_info["detected"] else 0.0

    brand_in_subdomain = 1.0 if any(b in subdomain.lower() for b in TOP_BRANDS) else 0.0
    brand_in_path = 1.0 if any(b in path.lower() for b in TOP_BRANDS) else 0.0

    min_edit_dist, closest_brand = find_closest_brand(netloc)
    typosquat_distance = float(min_edit_dist)

    return {
        "url_length": float(url_len),
        "host_length": float(host_len),
        "path_length": float(path_len),
        "digit_ratio": round(digit_ratio, 4),
        "special_char_ratio": round(special_char_ratio, 4),
        "dot_count": float(dot_count),
        "hyphen_count": float(hyphen_count),
        "at_symbol_present": at_symbol_present,
        "subdomain_depth": subdomain_depth,
        "path_depth": path_depth,
        "digit_run_max": digit_run_max,
        "query_param_count": query_param_count,
        "fragment_present": fragment_present,
        "double_slash_in_path": double_slash_in_path,
        "ip_in_host": ip_in_host,
        "punycode_detected": punycode_detected,
        "homoglyph_detected": homoglyph_detected,
        "shortener_detected": shortener_detected,
        "suspicious_tld": suspicious_tld,
        "https_present": https_present,
        "shannon_entropy": round(shannon_entropy, 4),
        "brand_kw_in_subdomain": brand_in_subdomain,
        "brand_kw_in_path": brand_in_path,
        "typosquat_distance": typosquat_distance,
    }


def analyze_url_anatomy(url: str) -> Dict[str, Any]:
    """Deconstructs URL segments and computes explainable red flags for the UI."""
    scheme, netloc, subdomain, domain, tld, path, query = parse_url_components(url)
    features = extract_url_features(url)
    homo = detect_homoglyph(netloc)
    min_dist, closest_brand = find_closest_brand(netloc)

    suspicious_segments = []
    red_flags = []

    if features["ip_in_host"] == 1.0:
        suspicious_segments.append("host")
        red_flags.append("Bare IP address used as hostname instead of a domain name")
    
    if homo["detected"]:
        suspicious_segments.append("subdomain" if homo["swapped_char"] in subdomain else "domain")
        red_flags.append(f"Homoglyph impersonation: character '{homo['swapped_char']}' used to mimic brand '{homo['original']}'")

    if features["brand_kw_in_subdomain"] == 1.0:
        suspicious_segments.append("subdomain")
        red_flags.append("Recognized corporate brand keyword found inside subdomain")

    if features["suspicious_tld"] == 1.0:
        suspicious_segments.append("tld")
        red_flags.append(f"Domain registered under high-abuse TLD: .{tld}")

    if features["https_present"] == 0.0:
        suspicious_segments.append("protocol")
        red_flags.append("Unencrypted connection: HTTP transport used without TLS/SSL")

    if min_dist == 1 and not homo["detected"]:
        suspicious_segments.append("domain")
        red_flags.append(f"Typosquatting warning: edit distance 1 from trusted brand '{closest_brand}'")

    if features["shannon_entropy"] > 4.2:
        suspicious_segments.append("domain")
        red_flags.append("High hostname entropy suggests an algorithmically generated domain (DGA)")

    return {
        "protocol": scheme,
        "subdomain": subdomain,
        "domain": domain,
        "tld": f".{tld}" if tld else "",
        "path": path,
        "query": f"?{query}" if query else "",
        "suspicious_segments": list(set(suspicious_segments)),
        "homoglyph_detail": homo,
        "typosquat": {
            "detected": min_dist <= 2,
            "target_brand": f"{closest_brand}.com" if closest_brand else "",
            "edit_distance": min_dist
        },
        "red_flags": red_flags
    }
