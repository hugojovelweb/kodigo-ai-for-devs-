"""Punto de composición de la aplicación FastAPI."""

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description=(
        "API educativa con operaciones de análisis de texto deterministas. "
        "La documentación interactiva está disponible en /docs."
    ),
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    """Normaliza errores 422 para que el agente pueda corregir la solicitud."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "La solicitud no cumple el contrato de la API.",
            # Pydantic agrega la excepción original en ``ctx.error`` para
            # validadores personalizados. JSONResponse no puede codificar una
            # instancia de ValueError, así que se transforma a texto antes de
            # construir la respuesta HTTP.
            "details": jsonable_encoder(
                exc.errors(),
                custom_encoder={Exception: lambda error: str(error)},
            ),
        },
    )
