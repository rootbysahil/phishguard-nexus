"""
PHISHGUARD//NEXUS - Application Configuration
Loaded from environment variables with strong Pydantic validation.
"""

from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return [orig.strip() for orig in v.split(",") if orig.strip()]
        return v

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # ML Model & Thresholds
    MODEL_PATH: str = "models/best_model.joblib"
    EXPLAINER_PATH: str = "models/shap_explainer.joblib"
    THRESHOLD_SAFE: float = 0.35
    THRESHOLD_SUSPICIOUS: float = 0.70
    HOST_FEATURES_ENABLED: bool = False
    DISTILBERT_ENABLED: bool = False

    # IBM watsonx.ai Settings
    WATSONX_APIKEY: str = ""
    WATSONX_PROJECT_ID: str = ""
    WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_MODEL_ID: str = "ibm/granite-13b-chat-v2"

    # Security & Input Constraints
    MAX_URL_LENGTH: int = 2048
    MAX_BODY_BYTES: int = 51200  # 50 KB


settings = Settings()
