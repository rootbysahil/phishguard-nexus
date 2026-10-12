"""
PHISHGUARD//NEXUS - System, History, Stats, and Config Schemas
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    components: Dict[str, str]


class ConfigResponse(BaseModel):
    threshold_safe: float
    threshold_suspicious: float
    reporting_region: str = "IN"
    reporting_authorities: Dict[str, str]
    features_enabled: Dict[str, bool]


class HistoryItem(BaseModel):
    scan_id: str
    target: str
    type: str
    verdict: str
    probability: float
    risk_level: int
    red_flags: List[str]
    created_at: str


class HistoryResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[HistoryItem]


class BrandCount(BaseModel):
    brand: str
    count: int


class DetectionDate(BaseModel):
    date: str
    phishing: int
    suspicious: int
    safe: int


class StatsResponse(BaseModel):
    total_scans: int
    phishing_count: int
    suspicious_count: int
    safe_count: int
    verdict_distribution: Dict[str, float]
    top_spoofed_brands: List[BrandCount]
    detections_over_time: List[DetectionDate]
    scan_type_breakdown: Dict[str, int]


class ModelMetricsResponse(BaseModel):
    model_name: str
    trained_at: Optional[str] = None
    dataset_split: Dict[str, Optional[int]]
    threshold: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    f2: Optional[float] = None
    roc_auc: Optional[float] = None
    pr_auc: Optional[float] = None
    ece: Optional[float] = None
    inference_latency_ms: Dict[str, Optional[float]]
    confusion_matrix: Optional[List[List[int]]] = None
    plot_paths: Dict[str, str]
    fresh_url_eval: Dict[str, Any]
