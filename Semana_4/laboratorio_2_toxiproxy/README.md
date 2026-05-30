# Laboratorio 2 - Toxiproxy

Este laboratorio reutiliza una aplicacion realista de tienda academica para practicar resiliencia de red con Toxiproxy.

## Estructura

- `src/`: aplicacion completa.
- `qa/`: servidor de Toxiproxy y comandos de inyeccion de latencia.

## Levantar la aplicacion

```powershell
cd src
docker compose -f docker-compose.app.yml up --build -d
```

URLs:

- Frontend: http://localhost:4173
- Backend: http://localhost:8000

## Ejecutar Toxiproxy

Ver `qa/README.md` para crear el proxy y el toxic de latencia.

## Objetivo pedagogico

- Mostrar una aplicacion viva mientras la red se degrada.
- Inyectar latencia sin tocar el codigo de negocio.
- Explicar blast radius y recuperacion controlada.
