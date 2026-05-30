# QA del Laboratorio 3 - SonarQube

Este directorio contiene solo el stack de analisis estatico y el script de scanner.

## Requisito previo

La aplicacion debe estar levantada desde `src/docker-compose.app.yml`.

## Levantar SonarQube

```powershell
cd qa/sonarqube
docker compose up -d
```

Espera unos minutos hasta que el servidor responda en:

- http://localhost:9000

Credenciales iniciales habituales:

- Usuario: `admin`
- Contrasena: `admin`

## Crear un token

Desde la UI de SonarQube, crea un token para el proyecto del laboratorio.

## Ejecutar el scanner con Docker

```powershell
cd qa/sonarqube
$env:SONAR_TOKEN = '<tu-token>'
.\run-scan.ps1
```

Tambien puedes pasar el token directamente:

```powershell
cd qa/sonarqube
.\run-scan.ps1 -SonarToken '<tu-token>'
```

## Resultado esperado

- SonarQube analiza `src/backend` y `src/frontend`.
- Se visualizan smells, cobertura pendiente y calidad general.
- El alumnado entiende el concepto de quality gate antes de mergear.
