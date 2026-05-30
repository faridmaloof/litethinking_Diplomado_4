# Laboratorio 1 - OWASP ZAP DAST

Este laboratorio expone una aplicacion realista de comercio academico para ejecutar un baseline scan con OWASP ZAP.

## Estructura

- `src/`: aplicacion completa.
- `qa/`: herramientas de escaneo y validacion.

## Levantar la aplicacion

```powershell
cd src
docker compose -f docker-compose.app.yml up --build -d
```

URLs:

- Frontend: http://localhost:4173
- Backend: http://localhost:8000

## Ejecutar ZAP

Ver `qa/README.md` para el comando de escaneo con Docker.

## Objetivo pedagogico

- Mostrar una app funcional que el alumnado pueda explorar.
- Ejecutar DAST sobre un sitio vivo y entender los hallazgos.
- Conectar el escaneo con el concepto de quality gate.
