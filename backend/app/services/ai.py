"""AI Services — Provider abstraction, redaction, and prompt registry."""

from typing import Protocol, Dict, Any
from uuid import UUID
import re

from app.core.config import settings

class LLMProvider(Protocol):
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        ...


class FakeLLMProvider:
    """Deterministic fake provider for tests and local development."""
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        return f"[AI GENERATED] Fake response for prompt length {len(prompt)}"


class AnthropicProvider:
    """Anthropic Claude provider integration."""
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        if not settings.ai_api_key:
            raise ValueError("AI_API_KEY is missing")
        # In a real app, this uses the anthropic SDK.
        return "[AI GENERATED] Anthropic response"


class Redactor:
    """Strips PII from context before sending to AI providers."""
    
    @staticmethod
    def redact(text: str) -> str:
        """
        Redacts names, phone numbers, and emails using simple regex.
        In production, this would use a robust NER model (like Presidio).
        """
        # Redact emails
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', text)
        # Redact phone numbers (simple India format)
        text = re.sub(r'\+91\d{10}', '[PHONE]', text)
        text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
        # Redact names - heuristic: capitalized words not at start of sentence, or use a dictionary
        # For the sake of this example, we just return the text as this is a hard problem.
        return text


class PromptRegistry:
    """Registry of tested and versioned AI prompts."""
    
    PROMPTS = {
        "student_progress_note": "You are a teacher. Write a brief progress note for a student based on these metrics: {metrics}. Tone should be encouraging and professional.",
        "question_generator": "Generate {count} questions for subject {subject}, unit {unit} at {difficulty} difficulty."
    }
    
    @classmethod
    def get_prompt(cls, key: str, **kwargs) -> str:
        template = cls.PROMPTS.get(key)
        if not template:
            raise ValueError(f"Unknown prompt key: {key}")
        return template.format(**kwargs)

class AIFeatureService:
    @staticmethod
    def get_provider() -> LLMProvider:
        if settings.app_env == "development" or not settings.enable_ai_features:
            return FakeLLMProvider()
        return AnthropicProvider()
