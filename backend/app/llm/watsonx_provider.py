"""
PHISHGUARD//NEXUS - IBM watsonx.ai Granite Provider
Interfaces with IBM Cloud watsonx.ai Granite LLM models.
Falls back seamlessly to TemplateProvider if credentials are missing or offline.
"""

import json
from typing import Any, Dict
from backend.app.core.config import settings
from backend.app.llm.provider import LLMProvider
from backend.app.llm.template_provider import TemplateProvider


class WatsonxProvider(LLMProvider):
    def __init__(self):
        self.fallback = TemplateProvider()
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        if settings.WATSONX_APIKEY and settings.WATSONX_PROJECT_ID:
            try:
                from ibm_watsonx_ai import Credentials
                from ibm_watsonx_ai.foundation_models import ModelInference
                
                credentials = Credentials(
                    url=settings.WATSONX_URL,
                    api_key=settings.WATSONX_APIKEY
                )
                self.client = ModelInference(
                    model_id=settings.WATSONX_MODEL_ID,
                    credentials=credentials,
                    project_id=settings.WATSONX_PROJECT_ID,
                    params={"max_new_tokens": 250, "temperature": 0.2}
                )
            except Exception as e:
                # Fallback enabled
                self.client = None

    def generate_explanation(self, findings: Dict[str, Any]) -> Dict[str, str]:
        if not self.client:
            return self.fallback.generate_explanation(findings)

        try:
            prompt = (
                f"You are PhishGuard AI, a SOC cybersecurity expert. Analyze these structured findings:\n"
                f"Target: {findings.get('target')}\n"
                f"Verdict: {findings.get('verdict')}\n"
                f"Confidence: {findings.get('probability')}\n"
                f"Red Flags: {', '.join(findings.get('red_flags', []))}\n\n"
                f"Provide a 2-sentence plain-English security summary advising the user:"
            )
            response = self.client.generate_text(prompt=prompt)
            result = self.fallback.generate_explanation(findings)
            result["en"] = response.strip()
            result["powered_by"] = "watsonx"
            return result
        except Exception:
            return self.fallback.generate_explanation(findings)

    def translate(self, text: str, target_lang: str) -> str:
        if not self.client:
            return self.fallback.translate(text, target_lang)

        try:
            lang_name = "Hindi" if target_lang == "hi" else "Punjabi"
            prompt = f"Translate the following cybersecurity advisory into formal {lang_name}:\n{text}"
            response = self.client.generate_text(prompt=prompt)
            return response.strip()
        except Exception:
            return self.fallback.translate(text, target_lang)

    def is_healthy(self) -> bool:
        return self.client is not None
