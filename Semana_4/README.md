# Semana 4 - DevSecOps y Chaos Engineering

La Semana 4 queda organizada por laboratorios independientes para que cada tema se pueda explicar, ejecutar y validar sin mezclar responsabilidades.

Estructura general:

- `laboratorio_1_zap/`: app realista de referencia para escaneo DAST con OWASP ZAP.
- `laboratorio_2_toxiproxy/`: app con proxy de red para inyectar latencia y fallos controlados.
- `laboratorio_3_sonarqube/`: app de referencia para analisis estatico con SonarQube.

Regla de organizacion:

- `src/` contiene solo codigo de aplicacion.
- `qa/` contiene solo herramientas, contenedores y scripts de validacion.

Cada laboratorio incluye su propio `src/docker-compose.app.yml` para levantar la aplicacion y su propio `qa/README.md` para ejecutar las herramientas del taller.

## Orden sugerido para la clase

1. Levantar el laboratorio 1 y ejecutar ZAP.
2. Levantar el laboratorio 2 e inyectar latencia con Toxiproxy.
3. Levantar el laboratorio 3 y correr el analisis de SonarQube.

## Comandos rapidos

### Laboratorio 1

```powershell
cd Semana_4/laboratorio_1_zap/src
docker compose -f docker-compose.app.yml up --build -d
```

### Laboratorio 2

```powershell
cd Semana_4/laboratorio_2_toxiproxy/src
docker compose -f docker-compose.app.yml up --build -d
```

### Laboratorio 3

```powershell
cd Semana_4/laboratorio_3_sonarqube/src
docker compose -f docker-compose.app.yml up --build -d
```

## Enfoque didactico

- ZAP: comprobar que el pipeline detecta riesgos antes de llegar a produccion.
- Toxiproxy: demostrar resiliencia frente a latencia y degradacion de red.
- SonarQube: introducir calidad de codigo, deuda tecnica y quality gates.
