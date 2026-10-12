"""
PHISHGUARD//NEXUS - ML Inference Engine & Predictor
Loads calibrated model pipeline, computes probability, and returns structured verdict.
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
import joblib
import numpy as np

from backend.app.core.config import settings
from backend.app.ml.explainer import Explainer
from backend.app.ml.features.url_features import extract_url_features, analyze_url_anatomy

FEATURE_NAMES = [
    "url_length", "host_length", "path_length", "digit_ratio", "special_char_ratio",
    "dot_count", "hyphen_count", "at_symbol_present", "subdomain_depth", "path_depth",
    "digit_run_max", "query_param_count", "fragment_present", "double_slash_in_path",
    "ip_in_host", "punycode_detected", "homoglyph_detected", "shortener_detected",
    "suspicious_tld", "https_present", "shannon_entropy", "brand_kw_in_subdomain",
    "brand_kw_in_path", "typosquat_distance"
]


class Predictor:
    def __init__(self):
        self.model = None
        self.explainer = Explainer(FEATURE_NAMES)
        self._load_model()

    def _load_model(self):
        model_file = Path(settings.MODEL_PATH)
        if not model_file.exists():
            # Check backend/models as alternative path
            alt = Path("backend") / settings.MODEL_PATH
            if alt.exists():
                model_file = alt

        if model_file.exists():
            try:
                self.model = joblib.load(model_file)
            except Exception:
                self.model = None
        else:
            self.model = None

    def predict_url(self, url: str) -> Dict[str, Any]:
        """
        Executes feature extraction, model inference, SHAP explanation, and anatomy parsing.
        """
        features = extract_url_features(url)
        anatomy = analyze_url_anatomy(url)
        
        feature_vec = np.array([[features[k] for k in FEATURE_NAMES]])

        if self.model is not None:
            try:
                prob = float(self.model.predict_proba(feature_vec)[0][1])
            except Exception:
                prob = self._heuristic_probability(features)
        else:
            prob = self._heuristic_probability(features)

        # Calibrated verdict thresholds
        if prob >= settings.THRESHOLD_SUSPICIOUS:
            verdict = "PHISHING"
        elif prob >= settings.THRESHOLD_SAFE:
            verdict = "SUSPICIOUS"
        else:
            verdict = "SAFE"

        risk_level = min(10, max(0, int(round(prob * 10))))
        shap_contributions = self.explainer.explain(features, prob)

        return {
            "verdict": verdict,
            "probability": round(prob, 4),
            "risk_level": risk_level,
            "features": features,
            "shap_contributions": shap_contributions,
            "red_flags": anatomy["red_flags"],
            "url_anatomy": anatomy
        }

    def _heuristic_probability(self, features: Dict[str, float]) -> float:
        """Deterministic baseline probability estimator when model artifact is loading."""
        score = 0.05
        if features.get("ip_in_host"): score += 0.40
        if features.get("homoglyph_detected"): score += 0.35
        if features.get("brand_kw_in_subdomain"): score += 0.30
        if features.get("suspicious_tld"): score += 0.25
        if not features.get("https_present"): score += 0.15
        if features.get("shannon_entropy", 0) > 4.1: score += 0.15
        if features.get("typosquat_distance", 99) <= 2: score += 0.20
        return min(0.99, max(0.01, score))


# Singleton instance
predictor = Predictor()
