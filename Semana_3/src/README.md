# Aplicacion del Taller (frontend + backend)

Este directorio contiene solamente el codigo de la aplicacion:

- Frontend React + Vite + TypeScript en `src/frontend`.
- Backend FastAPI en `src/backend`.

## Arquitectura (organizada)

Frontend (`src/frontend`):

- `src/`: componentes React y pantalla principal.
- `types/lab.ts`: contrato de datos que consume la UI.
- `hooks/useLabData.ts`: acceso a `/api/lab` y manejo de estado de carga.
- `components/*`: secciones de pantalla separadas por responsabilidad.
- `App.tsx`: orquestacion de estado y armado de la pagina.

Backend (`src/backend/app`):

- `config.py`: configuracion del servicio.
- `lab_service.py`: reglas de dominio (cache + construccion de payload).
- `main.py`: endpoints HTTP y wiring del servicio.

La idea didactica es mantener capa de UI y capa de dominio separadas para facilitar mantenimiento y lectura.

## Flujo de llamados

1. El frontend hace `fetch('/api/lab?...')`.
2. Nginx del frontend recibe `/api/*` y lo proxya al servicio `backend:8000`.
3. FastAPI resuelve la solicitud en `main.py` y delega en `LabService`.
4. `LabService` aplica cache/latencia simulada y devuelve un payload unico para la UI.

## Levantar aplicacion

```bash
cd src
docker compose -f docker-compose.app.yml up --build -d
```

## Detener aplicacion

```bash
cd src
docker compose -f docker-compose.app.yml down
```

## URLs

- Frontend: http://localhost:4173
- Backend: http://localhost:8000

## Checklist rapido (3 minutos)

1. Levantar app:

```bash
cd src
docker compose -f docker-compose.app.yml up --build -d
```

2. Verificar contenedores:

```bash
docker compose -f docker-compose.app.yml ps
```

3. Verificar backend:

```bash
curl http://localhost:8000/api/health
```

4. Verificar frontend:

```bash
curl http://localhost:4173/
```

5. Verificar flujo frontend -> backend por proxy:

```bash
curl "http://localhost:4173/api/lab?mode=cached&locale=es"
```
