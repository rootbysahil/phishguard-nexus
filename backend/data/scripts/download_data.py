"""
PHISHGUARD//NEXUS - Dataset Preparation & Manifest Generator
Creates balanced, realistic URL dataset with domain-level groupings.
Includes benign deep paths to prevent path-length shortcut learning.
"""

import json
import hashlib
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Seed for reproducibility
random.seed(42)

# Benign Root Domains & Realistic Internal Paths
BENIGN_DOMAINS = [
    "google.com", "youtube.com", "wikipedia.org", "amazon.com", "github.com",
    "microsoft.com", "apple.com", "linkedin.com", "netflix.com", "reddit.com",
    "stackoverflow.com", "twitter.com", "instagram.com", "adobe.com", "nytimes.com",
    "cnn.com", "bbc.com", "medium.com", "spotify.com", "quora.com",
    "wordpress.org", "mozilla.org", "cloudflare.com", "zoom.us", "dropbox.com",
    "salesforce.com", "oracle.com", "ibm.com", "intel.com", "cisco.com",
    "nature.com", "sciencedirect.com", "nationalgeographic.com", "reuters.com",
    "mit.edu", "stanford.edu", "harvard.edu", "cambridge.org", "nih.gov", "who.int"
]

BENIGN_PATHS = [
    "", "/about", "/contact", "/terms-of-service", "/privacy-policy",
    "/docs/v2/getting-started", "/blog/2024/05/security-updates", "/research/publications",
    "/products/enterprise/overview", "/community/forum/topic/12398", "/help/faq",
    "/category/technology/artificial-intelligence", "/wiki/Computer_security",
    "/explore/trending", "/search?q=machine+learning+tutorial", "/user/profile/settings",
    "/download/releases/v1.4.2", "/support/knowledge-base/article-994"
]

# Phishing archetypes
PHISHING_BRANDS = ["paypal", "chase", "wellsfargo", "appleid", "netflix", "bankofamerica", "microsoft", "google"]
PHISHING_TLDS = [".xyz", ".top", ".click", ".work", ".loan", ".gq", ".tk", ".cf", ".cam", ".vip"]
PHISHING_HOMOGLYPHS = [
    ("paypal", "paypa1-security.xyz"), ("paypal", "paypaI-verify.net"),
    ("apple", "app1e-id-support.com"), ("netflix", "netfl1x-billing.top"),
    ("google", "goog1e-account-recovery.click"), ("microsoft", "micros0ft-login.work")
]

def generate_samples(count_per_class: int = 1500):
    samples = []
    
    # 1. Benign Samples (Roots + Deep Paths to eliminate path-length bias)
    for _ in range(count_per_class):
        domain = random.choice(BENIGN_DOMAINS)
        path = random.choice(BENIGN_PATHS)
        scheme = "https://" if random.random() > 0.08 else "http://"
        url = f"{scheme}{domain}{path}"
        samples.append({"url": url, "label": 0, "domain": domain})

    # 2. Phishing Samples
    for _ in range(count_per_class):
        strategy = random.choice(["homoglyph", "brand_subdomain", "ip_host", "suspicious_tld", "deep_spoof"])
        
        if strategy == "homoglyph":
            brand, spoof = random.choice(PHISHING_HOMOGLYPHS)
            url = f"http://{spoof}/login?token={random.randint(10000, 99999)}"
            domain = spoof
        elif strategy == "brand_subdomain":
            brand = random.choice(PHISHING_BRANDS)
            tld = random.choice([".net", ".com", ".org", ".info"])
            fake_root = f"secure-auth{random.randint(1,99)}{tld}"
            url = f"http://{brand}.login.{fake_root}/verify/account.php"
            domain = fake_root
        elif strategy == "ip_host":
            ip = f"{random.randint(100,200)}.{random.randint(10,250)}.{random.randint(10,250)}.{random.randint(10,250)}"
            url = f"http://{ip}/session/{random.randint(1000,9999)}/update"
            domain = ip
        elif strategy == "suspicious_tld":
            brand = random.choice(PHISHING_BRANDS)
            tld = random.choice(PHISHING_TLDS)
            domain = f"{brand}-account-alert{tld}"
            url = f"http://{domain}/signin"
        else: # deep spoof
            domain = f"server-{random.randint(100,999)}-gateway.com"
            url = f"http://{domain}/paypal/login.action?ref=suspended"

        samples.append({"url": url, "label": 1, "domain": domain})

    random.shuffle(samples)
    return samples


def main():
    print("[*] Generating dataset with realistic benign deep paths and phishing vectors...")
    data = generate_samples(1500) # 3,000 total samples
    
    output_path = RAW_DIR / "dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Compute checksum
    hasher = hashlib.sha256()
    with open(output_path, "rb") as f:
        hasher.update(f.read())
    digest = hasher.hexdigest()

    manifest = {
        "dataset_file": "dataset.json",
        "total_records": len(data),
        "benign_count": sum(1 for d in data if d["label"] == 0),
        "phishing_count": sum(1 for d in data if d["label"] == 1),
        "sha256": digest
    }

    with open(RAW_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[+] Dataset saved to {output_path}")
    print(f"[+] Total samples: {manifest['total_records']}, SHA-256: {digest[:16]}...")

if __name__ == "__main__":
    main()
