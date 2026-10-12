"""
PHISHGUARD//NEXUS - System Endpoints
GET /api/health, GET /api/config, and POST /api/translate.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.db.models import ScanRecord
from backend.app.llm.watsonx_provider import WatsonxProvider
from backend.app.ml.predictor import predictor
from backend.app.schemas.system import HealthResponse, ConfigResponse
from backend.app.schemas.scan import TranslateRequest, TranslateResponse

router = APIRouter(tags=["System"])
llm_provider = WatsonxProvider()


@router.get("/health", response_model=HealthResponse)
def get_health():
    watsonx_status = "ready" if llm_provider.is_healthy() else "offline"
    ml_status = "loaded" if predictor.model is not None else "heuristic_fallback"
    return HealthResponse(
        status="ok",
        version="1.0.0",
        components={
            "database": "connected",
            "ml_model": ml_status,
            "explainer": "ready",
            "watsonx_ai": watsonx_status
        }
    )


@router.get("/config", response_model=ConfigResponse)
def get_config():
    return ConfigResponse(
        threshold_safe=settings.THRESHOLD_SAFE,
        threshold_suspicious=settings.THRESHOLD_SUSPICIOUS,
        reporting_region="IN",
        reporting_authorities={
            "primary_portal": "https://cybercrime.gov.in",
            "helpline": "1930",
            "global_portal": "reportphishing@apwg.org"
        },
        features_enabled={
            "host_features": settings.HOST_FEATURES_ENABLED,
            "distilbert": settings.DISTILBERT_ENABLED
        }
    )


@router.post("/translate", response_model=TranslateResponse)
def translate_explanation(req: TranslateRequest, db: Session = Depends(get_db)):
    record = db.query(ScanRecord).filter(ScanRecord.id == req.scan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found")

    import json
    expl_data = json.loads(record.explanation_json)
    english_text = expl_data.get("en", "")
    what_to_do_text = expl_data.get("what_to_do", "")

    translated_en = llm_provider.translate(english_text, req.target_language)
    translated_action = llm_provider.translate(what_to_do_text, req.target_language)

    return TranslateResponse(
        scan_id=req.scan_id,
        language=req.target_language,
        translated_explanation=translated_en,
        what_to_do=translated_action
    )
