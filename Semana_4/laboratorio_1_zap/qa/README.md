# QA del Laboratorio 1 - ZAP

Este directorio contiene solo herramientas de validacion para el laboratorio.

## Requisito previo

La aplicacion debe estar levantada desde `src/docker-compose.app.yml`.

## Escaneo con OWASP ZAP

```powershell
cd qa/zap
docker compose up --abort-on-container-exit
```

## Escaneo personalizado

```powershell
cd qa/zap
docker compose -f docker-compose.custom.yml up --abort-on-container-exit
```

## Resultado esperado

- ZAP ejecuta un baseline scan sobre http://host.docker.internal:4173.
- Se genera un reporte en `qa/zap/reports/`.
- El flujo custom tambien usa ZAP, pero con reporte `zap-report-custom.html`.
- El resultado se usa como evidencia del taller de DAST.

