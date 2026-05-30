# Aplicacion del Laboratorio 1

La aplicacion modela una tienda academica con catalogo, pedidos, login demo y panel de estado.

## Arquitectura

- `backend/app/main.py`: API FastAPI con endpoints del taller.
- `backend/app/catalog.py`: datos de demostracion.
- `frontend/`: interfaz web servida por Nginx.
- `docker-compose.app.yml`: orquestacion de frontend y backend.

## Flujo

1. El navegador carga la UI desde el frontend.
2. La UI consume la API a traves del proxy de Nginx.
3. FastAPI responde con datos de negocio realistas para el laboratorio.
