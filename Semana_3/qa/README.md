# QA del Dia 3 (separado por lenguaje)

Este directorio solo contiene pruebas. Cada lenguaje tiene implementaciones independientes de:

- `validate_api`
- `profile_cache`
- `audit_frontend`

Requisito previo para todas las pruebas: la app debe estar arriba desde `src/docker-compose.app.yml`.

## Python

```bash
cd qa/python
docker compose up --build --abort-on-container-exit
docker compose run --rm qa-python python scripts/validate_api.py
docker compose run --rm qa-python python scripts/profile_cache.py
docker compose run --rm qa-python python scripts/audit_frontend.py
```

## JavaScript

```bash
cd qa/javascript
docker compose up --build --abort-on-container-exit
docker compose run --rm qa-javascript npm run validate
docker compose run --rm qa-javascript npm run profile
docker compose run --rm qa-javascript npm run audit
```

## TypeScript

```bash
cd qa/typescript
docker compose up --build --abort-on-container-exit
docker compose run --rm qa-typescript npm run validate
docker compose run --rm qa-typescript npm run profile
docker compose run --rm qa-typescript npm run audit
```

## Java

```bash
cd qa/java
docker compose up --build --abort-on-container-exit
docker compose run --rm qa-java sh -lc "javac -d out src/main/java/com/pulselab/qa/*.java && java -cp out com.pulselab.qa.ValidateApi && java -cp out com.pulselab.qa.ProfileCache && java -cp out com.pulselab.qa.AuditFrontend"
```

## C#

```bash
cd qa/csharp
docker compose up --build --abort-on-container-exit
docker compose run --rm qa-csharp dotnet /app/QaChecks.dll validate
docker compose run --rm qa-csharp dotnet /app/QaChecks.dll profile
docker compose run --rm qa-csharp dotnet /app/QaChecks.dll audit
```

## k6 (performance)

```bash
cd qa/k6
docker compose up --abort-on-container-exit
```

## Notas

- `material/guia_dia3.md` mantiene el resumen del contenido de catedra.
- Cada carpeta de lenguaje es autocontenida para que el ejercicio sea facil de entender y ejecutar.
