"""
PHISHGUARD//NEXUS - SQLite Database Models
Stores scan history and feature logs. Email/SMS content is strictly never persisted.
"""

from datetime import datetime, timezone
import json
from typing import Any, Dict, List
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ScanRecord(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, index=True)
    type = Column(String(10), nullable=False)
    target = Column(String(2048), nullable=False, index=True) # Domain or URL
    content_hash = Column(String(64), nullable=False, index=True)
    verdict = Column(String(20), nullable=False, index=True)
    probability = Column(Float, nullable=False)
    risk_level = Column(Integer, nullable=False)
    
    # Serialized feature payloads
    features_json = Column(Text, nullable=False)
    shap_json = Column(Text, nullable=False)
    red_flags_json = Column(Text, nullable=False)
    explanation_json = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_history_dict(self) -> Dict[str, Any]:
        return {
            "scan_id": self.id,
            "target": self.target,
            "type": self.type,
            "verdict": self.verdict,
            "probability": round(self.probability, 4),
            "risk_level": self.risk_level,
            "red_flags": json.loads(self.red_flags_json),
            "created_at": self.created_at.isoformat() if self.created_at else datetime.now(timezone.utc).isoformat()
        }
