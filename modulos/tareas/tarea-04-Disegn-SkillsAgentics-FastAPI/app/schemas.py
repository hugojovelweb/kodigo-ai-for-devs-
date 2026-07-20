"""Contratos HTTP: validación de entrada y documentación OpenAPI."""

from enum import Enum
from pydantic import BaseModel, Field, field_validator

from app.config import settings


class AnalysisMode(str, Enum):
    summary = "summary"
    statistics = "statistics"
    keywords = "keywords"


class TextAnalysisRequest(BaseModel):
    """Solicitud de análisis sin datos sensibles ni instrucciones ejecutables."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=settings.max_text_length,
        description="Texto plano que se desea analizar.",
        examples=["FastAPI permite crear APIs rápidas y documentadas."],
    )
    mode: AnalysisMode = Field(
        default=AnalysisMode.statistics,
        description="Operación determinista solicitada.",
    )
    max_response_chars: int = Field(
        default=settings.default_max_response_chars,
        ge=50,
        le=1000,
        description="Límite de caracteres para una respuesta de resumen.",
    )

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("El texto no puede contener únicamente espacios.")
        return normalized


class TextAnalysisResponse(BaseModel):
    """Respuesta uniforme, trazable y fácil de consumir por un agente."""

    mode: AnalysisMode
    result: str | None = None
    character_count: int
    word_count: int
    unique_word_count: int
    keywords: list[str] = Field(default_factory=list)
    notice: str = "Análisis local, determinista y sin llamadas a modelos externos."


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
