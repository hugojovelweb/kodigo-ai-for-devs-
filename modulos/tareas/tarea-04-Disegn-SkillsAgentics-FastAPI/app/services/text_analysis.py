"""Reglas de negocio deterministas para el análisis de texto."""

from collections import Counter
import re

from app.schemas import AnalysisMode, TextAnalysisRequest, TextAnalysisResponse

WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)
STOP_WORDS = {
    "a", "al", "ante", "con", "de", "del", "el", "en", "es", "la", "las",
    "lo", "los", "o", "para", "por", "que", "se", "su", "un", "una", "y",
}


def tokenize(text: str) -> list[str]:
    """Extrae palabras Unicode y normaliza el uso de mayúsculas."""
    return [word.lower() for word in WORD_PATTERN.findall(text)]


def extract_keywords(words: list[str], limit: int = 5) -> list[str]:
    """Devuelve términos frecuentes relevantes con desempate alfabético."""
    counts = Counter(word for word in words if len(word) > 2 and word not in STOP_WORDS)
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def summarize(text: str, max_chars: int) -> str:
    """Resumen extractivo sencillo: primera oración, acotada al límite indicado."""
    first_sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    if len(first_sentence) <= max_chars:
        return first_sentence
    return first_sentence[: max_chars - 1].rstrip() + "…"


def analyze_text(request: TextAnalysisRequest) -> TextAnalysisResponse:
    """Orquesta el cálculo sin depender de FastAPI ni de un proveedor de IA."""
    words = tokenize(request.text)
    keywords = extract_keywords(words)
    result = None
    if request.mode == AnalysisMode.summary:
        result = summarize(request.text, request.max_response_chars)
    elif request.mode == AnalysisMode.keywords:
        result = ", ".join(keywords) if keywords else "No se identificaron palabras clave."

    return TextAnalysisResponse(
        mode=request.mode,
        result=result,
        character_count=len(request.text),
        word_count=len(words),
        unique_word_count=len(set(words)),
        keywords=keywords,
    )
