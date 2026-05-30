# QA del Laboratorio 2 - Toxiproxy

Este directorio contiene solo la infraestructura de inyeccion de latencia.

## Requisito previo

La aplicacion debe estar levantada desde `src/docker-compose.app.yml`.

## Levantar Toxiproxy

```powershell
cd qa/toxiproxy
docker compose up -d
```

## Crear el proxy

```powershell
docker compose exec toxiproxy /go/bin/toxiproxy-cli create api_proxy --listen 0.0.0.0:8666 --upstream host.docker.internal:8000
```

## Probar sin toxic

```powershell
curl http://localhost:8666/api/health
```

## Inyectar latencia

```powershell
docker compose exec toxiproxy /go/bin/toxiproxy-cli toxic add -t latency -a latency=5000 api_proxy
```

## Probar con toxic

```powershell
curl http://localhost:8666/api/health
```

## Resultado esperado

- La respuesta sigue existiendo.
- El tiempo de espera aumenta de forma visible.
- El alumnado puede comparar antes y despues sin modificar el codigo.
