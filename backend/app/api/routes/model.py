"""
PHISHGUARD//NEXUS - Model Metrics Endpoint
GET /api/model/metrics
Serves real evaluation metrics and curves generated during Phase 3 training.
"""

import json
from pathlib import Path
from fastapi import APIRouter
from backend.app.schemas.system import ModelMetricsResponse

router = APIRouter(tags=["Model"])

EVAL_PATHS = [
    Path("models/eval/metrics.json"),
    Path("backend/models/eval/metrics.json")
]


@router.get("/model/metrics", response_model=ModelMetricsResponse)
def get_model_metrics():
    for p in EVAL_PATHS:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ModelMetricsResponse(**data)

    # Return empty placeholder if not yet evaluated
    return ModelMetricsResponse(
        model_name="LightGBM",
        trained_at=None,
        dataset_split={"train": None, "val": None, "test": None},
        threshold=None,
        precision=None,
        recall=None,
        f1=None,
        f2=None,
        roc_auc=None,
        pr_auc=None,
        ece=None,
        inference_latency_ms={"p50": None, "p95": None},
        confusion_matrix=None,
        plot_paths={
            "roc_curve": "/static/eval/roc_curve.png",
            "pr_curve": "/static/eval/pr_curve.png",
            "confusion_matrix": "/static/eval/confusion_matrix.png",
            "calibration_curve": "/static/eval/calibration_curve.png",
            "shap_global": "/static/eval/shap_global.png"
        },
        fresh_url_eval={"f2": None, "roc_auc": None, "sample_size": None, "note": "Evaluated on held-out feed"}
    )
