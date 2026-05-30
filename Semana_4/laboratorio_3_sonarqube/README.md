# Laboratorio 3 - SonarQube

Este laboratorio usa una aplicacion modular de referencia para mostrar analisis estatico y quality gates con SonarQube.

## Estructura

- `src/`: aplicacion completa.
- `qa/`: servidor de SonarQube, base de datos y script de analisis.

## Levantar la aplicacion

```powershell
cd src
docker compose -f docker-compose.app.yml up --build -d
```

URLs:

- Frontend: http://localhost:4173
- Backend: http://localhost:8000

## Levantar SonarQube

Ver `qa/README.md` para iniciar SonarQube con Docker y correr el scanner.

## Objetivo pedagogico

- Introducir deuda tecnica y calidad automatizada.
- Mostrar como un quality gate acompaña al pipeline.
- Analizar codigo backend y frontend con un criterio repetible.
