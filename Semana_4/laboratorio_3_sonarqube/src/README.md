# Aplicacion del Laboratorio 3

La aplicacion mantiene el mismo dominio de tienda academica, pero con mas modularidad para que el analisis de SonarQube tenga una base real.

## Arquitectura

- `backend/app/main.py`: API FastAPI.
- `backend/app/catalog.py`: datos de demostracion.
- `backend/app/metrics.py`: calculos de resumen.
- `frontend/`: interfaz web dividida en modulos pequenos.
- `docker-compose.app.yml`: orquestacion de frontend y backend.

## Flujo

1. El navegador carga la UI desde el frontend.
2. La UI consume la API via Nginx.
3. SonarQube analiza el codigo del backend y frontend como parte del taller de calidad.
