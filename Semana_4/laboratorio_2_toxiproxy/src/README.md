# Aplicacion del Laboratorio 2

La aplicacion es la misma tienda academica del curso, pero el guion del laboratorio se enfoca en observabilidad y latencia de red.

## Arquitectura

- `backend/app/main.py`: FastAPI con catalogo, pedidos y login demo.
- `backend/app/catalog.py`: datos de demostracion.
- `frontend/`: interfaz web servida por Nginx.
- `docker-compose.app.yml`: orquestacion de frontend y backend.

## Flujo

1. El navegador carga la UI desde el frontend.
2. El frontend consume la API via Nginx.
3. Toxiproxy se levanta aparte en `qa/` para que el alumnado pueda redirigir el trafico y degradar la red.
