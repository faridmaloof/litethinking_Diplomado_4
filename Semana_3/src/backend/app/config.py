from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    # Origen del frontend usado para construir canonical URLs.
    app_origin: str = os.getenv('APP_ORIGIN', 'http://localhost:4173')
    # TTL de cache para la ruta agregada /api/lab.
    cache_ttl_seconds: int = 45
