"""Endpoints de la API; la lógica se delega a servicios."""

from fastapi import APIRouter, status

from app.config import settings
from app.schemas import HealthResponse, TextAnalysisRequest, TextAnalysisResponse
from app.services.text_analysis import analyze_text

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["operación"])
def health_check() -> HealthResponse:
    """Confirma disponibilidad de la API sin exponer configuración sensible."""
    return HealthResponse(version=settings.api_version)


@router.post(
    "/v1/text/analyze",
    response_model=TextAnalysisResponse,
    status_code=status.HTTP_200_OK,
    tags=["análisis"],
    summary="Analiza texto mediante operaciones locales y deterministas",
)
def analyze(request: TextAnalysisRequest) -> TextAnalysisResponse:
    """Valida la solicitud mediante el esquema y devuelve su análisis."""
    return analyze_text(request)
