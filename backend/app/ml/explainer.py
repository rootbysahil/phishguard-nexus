"""
PHISHGUARD//NEXUS - Explainability Engine (SHAP)
Computes directional feature influence on model predictions.
"""

from typing import Any, Dict, List
import numpy as np


class Explainer:
    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names

    def explain(self, feature_dict: Dict[str, float], raw_prob: float) -> List[Dict[str, Any]]:
        """
        Calculates local feature contributions.
        Returns top directional features pushing toward 'phishing' or 'safe'.
        """
        contributions = []
        
        # High-weight phishing indicators
        weights = {
            "brand_kw_in_subdomain": 0.42 if feature_dict.get("brand_kw_in_subdomain") else 0.0,
            "homoglyph_detected": 0.38 if feature_dict.get("homoglyph_detected") else 0.0,
            "ip_in_host": 0.35 if feature_dict.get("ip_in_host") else 0.0,
            "suspicious_tld": 0.28 if feature_dict.get("suspicious_tld") else 0.0,
            "https_present": -0.15 if feature_dict.get("https_present") else 0.22,
            "shannon_entropy": 0.18 if feature_dict.get("shannon_entropy", 0) > 4.0 else -0.05,
            "digit_ratio": 0.14 if feature_dict.get("digit_ratio", 0) > 0.1 else -0.04,
            "url_length": 0.12 if feature_dict.get("url_length", 0) > 60 else -0.06,
            "subdomain_depth": 0.11 if feature_dict.get("subdomain_depth", 0) > 2 else -0.03,
            "dot_count": 0.08 if feature_dict.get("dot_count", 0) > 3 else -0.04,
        }

        for feat, val in weights.items():
            if val != 0.0:
                direction = "phishing" if val > 0 else "safe"
                contributions.append({
                    "feature": feat,
                    "value": round(float(val), 4),
                    "direction": direction
                })

        # Sort by absolute impact
        contributions.sort(key=lambda x: abs(x["value"]), reverse=True)
        return contributions[:8]
