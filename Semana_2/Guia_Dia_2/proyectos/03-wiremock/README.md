# Modulo 3 - WireMock (Aislamiento de API)

## Ubicacion
- `container/compose.yml`
- `container/mappings/api-pagos-timeout-504.json`
- `container/mappings/api-pagos-aprobado-201.json`
- `container/mappings/api-health-200.json`
- `container/mapping_postman_body.json`

## ¿WireMock soporta varios JSON?
Si. WireMock carga automaticamente TODOS los archivos `.json` dentro de `container/mappings/`.
Puedes tener multiples escenarios al mismo tiempo (timeout, aprobado, health, etc.).

Tip:
- Usa rutas distintas para evitar choques (`/api/pagos`, `/api/pagos/aprobado`, `/api/health`).
- Si dos mappings compiten, agrega `priority` (numero menor = mayor prioridad).

## Levantar con Docker
```powershell
cd container
docker compose up
```

## Levantar con Podman
```powershell
cd container
podman compose up
```

## Probar endpoint simulado
En otra terminal:

```powershell
curl -X POST http://localhost:8080/api/pagos
curl -X POST http://localhost:8080/api/pagos/aprobado
curl http://localhost:8080/api/health
```

Resultado esperado:
- HTTP `504`
- Delay de `6` segundos
- JSON: `Gateway Timeout - Banco Caido`

Resultado adicional esperado:
- `POST /api/pagos/aprobado` -> `201` con estado `APROBADO`
- `GET /api/health` -> `200` con estado `UP`

## Prueba via Postman (Admin API)
1. POST `http://localhost:8080/__admin/mappings`
2. Body raw JSON con contenido de `container/mapping_postman_body.json`
3. Luego probar POST `http://localhost:8080/api/pagos`
