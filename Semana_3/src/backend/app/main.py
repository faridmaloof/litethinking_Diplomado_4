from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import AppConfig
from .lab_service import AppMode, LabService, Locale

app = FastAPI(title='PulseLab API', version='1.0.0')
config = AppConfig()
# Instancia unica del servicio de dominio para conservar el cache
# en memoria durante la vida del proceso.
service = LabService(config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.app_origin],
    allow_methods=['GET'],
    allow_headers=['*'],
)


@app.get('/api/health')
async def health() -> dict[str, object]:
    # Endpoint tecnico para validar disponibilidad del backend.
    return service.health_payload()


@app.get('/api/lab')
async def lab(
    mode: AppMode = Query(default='cached'),
    locale: Locale = Query(default='es'),
) -> dict[str, object]:
    # Endpoint principal del laboratorio: entrega performance,
    # accesibilidad, SEO y contenido localizado en una sola respuesta.
    return await service.build_lab_payload(mode, locale)
