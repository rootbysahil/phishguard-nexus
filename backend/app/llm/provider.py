"""
PHISHGUARD//NEXUS - Abstract LLM Provider Interface (ADR-002)
Defines uniform contract for AI explanation generation and translations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMProvider(ABC):
    @abstractmethod
    def generate_explanation(self, findings: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates structured advisory explanations.
        Returns dict with keys: 'en', 'why_flagged', 'what_to_do', 'powered_by'.
        """
        pass

    @abstractmethod
    def translate(self, text: str, target_lang: str) -> str:
        """Translates advice text to Hindi ('hi') or Punjabi ('pa')."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Returns True if the LLM provider service is active and responsive."""
        pass
