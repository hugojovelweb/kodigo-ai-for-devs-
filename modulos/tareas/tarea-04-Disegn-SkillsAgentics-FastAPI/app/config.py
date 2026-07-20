"""Configuración centralizada y validada de la aplicación."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Valores de configuración que no deben dispersarse entre rutas."""

    app_name: str = "API de Análisis de Texto Agentico"
    api_version: str = "1.0.0"
    max_text_length: int = 2000
    default_max_response_chars: int = 500


settings = Settings(
    max_text_length=int(os.getenv("MAX_TEXT_LENGTH", "2000")),
    default_max_response_chars=int(os.getenv("DEFAULT_MAX_RESPONSE_CHARS", "500")),
)
