"""
PHISHGUARD//NEXUS - Pydantic v2 Request and Response Schemas for Scans
Strictly compliant with docs/API_CONTRACT.md.
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    type: Literal["url", "email", "sms"] = Field(
        description="Type of input content submitted"
    )
    content: str = Field(
        min_length=1,
        description="Raw URL or message text (max 2048 chars for URL, 50 KB for text)"
    )


class ScanQueuedResponse(BaseModel):
    scan_id: str
    status: str = "queued"
    stream_url: str


class ShapContribution(BaseModel):
    feature: str
    value: float
    direction: Literal["phishing", "safe"]


class ExplanationModel(BaseModel):
    en: str
    why_flagged: str
    what_to_do: str
    powered_by: Literal["watsonx", "template"]


class ScanResponse(BaseModel):
    scan_id: str
    type: str
    target: str
    content_hash: str
    verdict: Literal["SAFE", "SUSPICIOUS", "PHISHING"]
    probability: float
    risk_level: int
    features: Dict[str, float]
    shap_contributions: List[ShapContribution]
    red_flags: List[str]
    url_anatomy: Optional[Dict[str, Any]] = None
    explanation: ExplanationModel
    inference_latency_ms: int
    created_at: str


class TranslateRequest(BaseModel):
    scan_id: str
    target_language: Literal["hi", "pa"]


class TranslateResponse(BaseModel):
    scan_id: str
    language: str
    translated_explanation: str
    what_to_do: str
