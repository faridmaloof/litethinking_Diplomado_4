# QA Engineering Testing Infrastructure

Este proyecto contiene una infraestructura de pruebas de QA completa que incluye herramientas de proxy, seguridad, rendimiento y caos para pruebas de resistencia y calidad de software.

## Componentes

### 1. Proxy (mitmproxy)
- **Puerto**: 8080 (proxy HTTP/HTTPS), 8081 (UI web)
- **Función**: Intercepta y registra solicitudes HTTP/HTTPS para análisis
- **Herramienta**: mitmproxy
- **Características**:
  - Intercepción de requests/responses
  - Modificación de headers, body y otros elementos
  - Soporte para valores dinámicos (<UUID>, <FechaActual>, <Aleatorio>, etc.)
  - Reglas configurables para diferentes tipos de manipulación

### 2. OWASP ZAP (Zed Attack Proxy)
- **Puerto**: 8090 (API)
- **Función**: Pruebas de seguridad automatizadas
- **Herramienta**: OWASP ZAP

### 3. ToxiProxy
- **Puertos**: 8474 (API), 8475 (endpoint proxy)
- **Función**: Simulación de condiciones de red deficientes (latencia, cortes, etc.)
- **Herramienta**: ToxiProxy

### 4. K6 (Opcional)
- **Función**: Pruebas de rendimiento
- **Perfil**: `performance`
- **Uso**: `docker compose --profile performance up`

## Requisitos Previos

- Docker y Docker Compose instalados
- Podman (opcional, usado en el ejemplo)
- Acceso a internet para descargar imágenes Docker
- Navegador web moderno

## Configuración Inicial

### Estructura de Directorios Necesaria

Antes de ejecutar el contenedor proxy, asegúrate de que existan los siguientes directorios:

```
Semana_5/Ejercicio_Final/
├── proxy/
│   ├── certs/                # Directorio para certificados
│   ├── mitmproxy/
│   │   └── config/
│   │       └── rules/        # Reglas de proxy
│   └── secrets/              # Secretos (opcional)
```

Si los directorios no existen, créelos manualmente:

```bash
mkdir -p proxy/certs
mkdir -p proxy/mitmproxy/config/rules
mkdir -p secrets
```

## Ejecución

### 1. Ejecución Básica

```bash
# Navega al directorio del proyecto
cd Semana_5/Ejercicio_Final

# Levanta los servicios principales
podman compose up -d
# o con Docker
docker compose up -d
```

### 2. Ejecución con Pruebas de Rendimiento

```bash
# Levanta todos los servicios incluyendo K6
podman compose --profile performance up -d
```

### 3. Verificación del Estado

```bash
# Verifica que todos los contenedores estén corriendo
podman compose ps
# o
docker compose ps
```

## Uso de las Herramientas

### Proxy (mitmproxy)

#### Interfaz Web
- Accede a: http://localhost:8081
- Permite visualizar y analizar todas las solicitudes interceptadas
- Puedes filtrar, buscar y exportar solicitudes

#### Configuración de Proxy en tu máquina
Para usar el proxy, debes configurar tu navegador o aplicación para que use el proxy en `localhost:8080`:

**En navegadores web:**
- Configuración de red/proxy → Usar proxy manual
- Servidor proxy: `localhost` o `127.0.0.1`
- Puerto: `8080`

**En aplicaciones cURL:**
```bash
curl --proxy http://localhost:8080 https://www.google.com
```

**En aplicaciones Python:**
```python
import requests

proxies = {
    'http': 'http://localhost:8080',
    'https': 'http://localhost:8080'
}

response = requests.get('https://api.example.com/data', proxies=proxies, verify=False)
```

#### Tipos de Reglas Disponibles

El proxy soporta diferentes tipos de reglas para interceptar y modificar solicitudes:

1. **Request** - Interceptar y modificar la solicitud completa
2. **RequestHeader** - Modificar solo los headers de la solicitud
3. **RequestBody** - Modificar solo el cuerpo de la solicitud
4. **Response** - Interceptar y modificar la respuesta completa
5. **ResponseHeader** - Modificar solo los headers de la respuesta
6. **ResponseBody** - Modificar solo el cuerpo de la respuesta

#### Valores Dinámicos Disponibles

Puedes usar valores dinámicos en tus reglas escribiéndolos entre `< >`:

- `<UUID>` - Genera un UUID único
- `<FechaActual 'formato'>` - Fecha actual con formato personalizado
- `<Aleatorio [valor1, valor2, valor3]>` - Selecciona aleatoriamente de una lista
- `<Aleatorio min, max>` - Genera un número aleatorio entre min y max
- `<TextoAleatorio longitud>` - Genera texto aleatorio con la longitud especificada
- `<Base64 "texto">` - Codifica texto en Base64
- `<Delay milisegundos>` - Añade un retraso en la respuesta

#### Ejemplo de Uso Completo

1. **Configura tu aplicación para usar el proxy:**
   - Dirección: `localhost`
   - Puerto: `8080`

2. **Crea reglas en `proxy/mitmproxy/config/rules/`:**
   - Archivos `.json` con reglas de modificación
   - Se recargan automáticamente al modificar

3. **Haz solicitudes a través del proxy:**
   - Tu aplicación enviará solicitudes al destino final
   - El proxy interceptará, modificará según reglas y enviará

4. **Monitorea en la interfaz web:**
   - Visita http://localhost:8081
   - Observa todas las solicitudes y respuestas

### OWASP ZAP

- API: http://localhost:8090
- Documentación de la API: http://localhost:8090/UI/
- Usa el cliente ZAP o herramientas REST para interactuar con la API

### ToxiProxy

- API: http://localhost:8474
- Endpoint proxy: http://localhost:8475
- Consulta la documentación de ToxiProxy para crear y gestionar toxics

## Configuración de Reglas de Proxy

Para configurar reglas de modificación, crea archivos JSON en `proxy/mitmproxy/config/rules/`.

### Estructura de una regla:

```json
{
  "nombre_de_la_regla": {
    "Ruta": "/ruta/api",
    "Metodo": "GET|POST|PUT|DELETE",
    "Tipo_intercepcion": "Request|Response|RequestHeader|RequestBody|ResponseHeader|ResponseBody",
    "Tipo_modificacion": "completo|parcial|eliminar|agregar",
    "Headers": {
      "NombreHeader": "ValorHeader"
    },
    "Body": {
      "campo": "valor"
    },
    "Datos": {
      "campo": "valor"
    }
  }
}
```

### Ejemplos de Reglas

Se incluyen ejemplos en `proxy/mitmproxy/config/rules/example_modifications.json`.

### Trabajar con Reglas

#### Crear una nueva regla

1. Crea un nuevo archivo JSON en el directorio `proxy/mitmproxy/config/rules/`
2. Define tu regla siguiendo el formato especificado
3. Guarda el archivo

#### Recargar reglas sin reiniciar

Para recargar las reglas sin reiniciar el contenedor:

```bash
podman exec -it proxy_container_id python3 -c "import os; os.system('pkill -HUP python')"
```

#### Verificar reglas activas

1. Accede a la interfaz web en http://localhost:8081
2. Ve a la pestaña "Rules" o "Reglas"
3. Verifica que tus reglas aparecen listadas

#### Eliminar una regla

1. Elimina el archivo JSON correspondiente al directorio `proxy/mitmproxy/config/rules/`
2. Las reglas se recargan automáticamente al eliminar un archivo



## Solución de Problemas

### Problemas Comunes

#### 1. Error de Imágenes No Encontradas

Si recibes errores como `manifest unknown` o `requested access to the resource is denied`, las imágenes han sido actualizadas en el Dockerfile para usar ubicaciones válidas:

- ToxiProxy: `ghcr.io/shopify/toxiproxy:latest`
- ZAP: `ghcr.io/zaproxy/zaproxy:stable`

#### 2. Problemas con Volúmenes en Windows

En el archivo [docker-compose.yml](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/docker-compose.yml], los volúmenes de bind mount han sido comentados para evitar problemas en entornos Windows/WSL:

```yaml
# volumes:
#   - ./proxy/mitmproxy/config/rules:/home/mitmproxy/config/rules
#   - ./proxy/certs:/home/mitmproxy/.mitmproxy
#   - ./secrets:/run/secrets:ro
```

Si necesitas usar estos volúmenes, asegúrate de que los directorios existan y tengan permisos adecuados.

#### 3. Puerto Ocupado

Si recibes errores de puerto ocupado, verifica que los puertos 8080, 8081, 8090, 8474 y 8475 no estén siendo usados por otras aplicaciones.

## Contribuciones

Este proyecto es parte del curso de QA avanzado. Las contribuciones son bienvenidas siguiendo las guías de estilo y buenas prácticas.

## Pruebas Rápidas

1. **Iniciar servicios**:
```
