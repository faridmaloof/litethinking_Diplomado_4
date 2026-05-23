# Semana 3 - Rendimiento, Accesibilidad y SEO

Este laboratorio quedo separado en dos zonas para no mezclar responsabilidades:

- `src/`: solo codigo de la aplicacion (frontend y backend).
- `qa/`: solo pruebas y perfiles por lenguaje.

## 1) Aplicacion (solo src)

La app ahora esta separada fisicamente en:

- `src/frontend`
- `src/backend`

Levantar aplicacion:

```bash
cd src
docker compose -f docker-compose.app.yml up --build -d
```

Servicios esperados:

- Frontend: http://localhost:4173
- Backend: http://localhost:8000

## 2) QA (solo qa)

Cada lenguaje tiene su propio compose y sus propios scripts:

- `qa/python`
- `qa/javascript`
- `qa/typescript`
- `qa/java`
- `qa/csharp`
- `qa/k6`

Ver comandos detallados en `qa/README.md`.

## Notas del taller

La guia sintetizada del material de catedra sigue en `qa/material/guia_dia3.md`.
