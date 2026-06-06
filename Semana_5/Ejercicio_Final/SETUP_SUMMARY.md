# QA Engineering Testing Infrastructure - Resumen de Configuración

## Estado Actual

✅ Todos los contenedores están corriendo correctamente:
- `qa-proxy`: Proxy mitmproxy en puertos 8080 (proxy) y 8081 (UI web)
- `qa-zap`: OWASP ZAP en puerto 8090
- `qa-toxiproxy`: ToxiProxy en puerto 8474

## Acceso a Interfaces

### Proxy (mitmproxy)
- **Interfaz Web**: http://localhost:8081
- **Puerto Proxy**: 8080 (usar como proxy HTTP/HTTPS)
- **Reglas**: Configuradas en `proxy/mitmproxy/config/rules/`

### OWASP ZAP
- **API**: http://localhost:8090
- **Documentación**: http://localhost:8090/UI/

### ToxiProxy
- **API**: http://localhost:8090
- **Endpoint**: http://localhost:8475

## Uso de Reglas

Las reglas de modificación del proxy están almacenadas en:
- `proxy/mitmproxy/config/rules/`

Ejemplos incluidos:
- `example_modifications.json`: Reglas de ejemplo para diferentes tipos de interceptación
- `test_rules.json`: Reglas de prueba para validar funcionalidades

## Gestión de Reglas

Para añadir nuevas reglas:
1. Crea un archivo JSON en `proxy/mitmproxy/config/rules/`
2. Define tus reglas siguiendo el formato existente
3. Reconstruye el contenedor si es necesario: `podman compose down && podman compose build proxy && podman compose up -d`

## Scripts de Utilidad

- `verify_setup.bat`: Verifica que todo esté funcionando correctamente
- `utils/rules_manager.bat`: Administra reglas entre host y contenedor

## Comandos Básicos

```bash
# Iniciar la infraestructura
podman compose up -d

# Verificar estado
podman compose ps

# Detener la infraestructura
podman compose down

# Reconstruir imagen del proxy (cuando se cambian reglas)
podman compose down && podman compose build proxy && podman compose up -d
```

## Pruebas Rápidas

1. **Verificar conectividad**:
   ```bash
   curl -I http://localhost:8080  # Debe responder con 502 Bad Gateway (normal)
   curl -I http://localhost:8081  # Debe responder con 405 Method Not Allowed (normal)
   ```

2. **Usar el proxy**:
   - Configura tu navegador o aplicación para usar `localhost:8080` como proxy
   - Las solicitudes serán interceptadas y modificadas según las reglas

## Solución de Problemas

- Si los contenedores no inician: Verifica que los puertos 8080, 8081, 8090, 8474 y 8475 no estén ocupados
- Si el proxy no responde: Ejecuta `verify_setup.bat` para diagnóstico
- Si las reglas no se aplican: Verifica que estén en el formato correcto y reconstruye el contenedor