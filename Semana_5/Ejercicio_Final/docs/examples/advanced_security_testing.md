# Ejemplo Avanzado: Pruebas de Seguridad con Interceptación

## Objetivo

Demostrar cómo combinar la interceptación de tráfico con pruebas de seguridad para identificar vulnerabilidades en tiempo real.

## Escenario

Supongamos que estamos probando una API de autenticación que debería validar correctamente los tokens JWT. Queremos verificar si la API es vulnerable a ataques de token manipulation.

## Configuración de Reglas

Creamos una regla que intercepta las solicitudes de autenticación y manipula los tokens:

### Archivo: `proxy/mitmproxy/config/rules/security_auth_bypass.json`

```json
{
  "Auth_Bypass_Test": {
    "Tipo_intercepcion": "Request",
    "Ruta": "/api/auth/protected",
    "Metodo": "GET",
    "Descripcion": "Prueba de bypass de autenticación manipulando token JWT",
    "Tipo_modificacion": "Parcial",
    "Datos": {
      "headers": {
        "Authorization": "Bearer <TextoAleatorio(100)>"
      }
    }
  },
  "Login_Fuzzing": {
    "Tipo_intercepcion": "Request",
    "Ruta": "/api/auth/login",
    "Metodo": "POST",
    "Descripcion": "Inyección de payloads maliciosos en login",
    "Tipo_modificacion": "Parcial",
    "Datos": {
      "username": "<Aleatorio(['admin', 'root', 'administrator', '../../../etc/passwd'])>",
      "password": "<Aleatorio(['123456', \"' OR '1'='1\", '<script>alert(1)</script>', 'password123'])>"
    }
  }
}
```

## Ejecución de la Prueba

1. **Configurar el proxy**: Asegurarse de que la regla esté activa
2. **Enviar tráfico de prueba**: Dirigir solicitudes a la API a través del proxy
3. **Monitorear respuestas**: Observar si se obtienen accesos indebidos
4. **Analizar resultados**: Verificar si la aplicación responde de manera inapropiada

## Integración con OWASP ZAP

Combinamos la interceptación con ZAP para un análisis más profundo:

```bash
# Iniciar ZAP en daemon mode
docker compose up zap

# Enviar tráfico interceptado a ZAP para escaneo
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"method":"traditional","url":"http://target-app/api/auth/protected","postData":"{\"test\":\"data\"}"}' \
     http://localhost:8090/OTHER/customscan/action/scan/
```

## Interpretación de Resultados

- Si la regla de bypass devuelve respuestas exitosas (200), indica posible vulnerabilidad
- Si ZAP detecta nuevas vulnerabilidades después de la manipulación, señala problemas de seguridad
- Las respuestas inesperadas pueden indicar errores de validación

## Buenas Prácticas

- **Documentar todas las pruebas**: Registrar los payloads utilizados y los resultados obtenidos
- **Usar datos realistas**: Los payloads deben simular ataques reales
- **Monitorear impacto**: Asegurarse de que las pruebas no afecten el sistema de producción
- **Automatizar cuando sea posible**: Crear scripts que ejecuten estas pruebas regularmente

## Consideraciones Éticas

- Solo ejecutar estas pruebas en sistemas autorizados
- Documentar y reportar todas las vulnerabilidades encontradas
- Obtener permiso explícito antes de probar sistemas de terceros