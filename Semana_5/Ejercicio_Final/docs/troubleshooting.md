# Troubleshooting

## Problemas Comunes y Soluciones

### 1. Proxy no intercepta tráfico

**Síntomas:**
- Navegador no reconoce el proxy
- No se ven solicitudes en la UI de mitmproxy

**Soluciones:**
1. Verificar que el puerto 8080 esté disponible
2. Confirmar que el navegador esté configurado con proxy `localhost:8080`
3. Asegurarse de que el certificado CA esté instalado en el navegador
4. Revisar logs del contenedor: `docker compose logs proxy`

### 2. Hot-reload de reglas no funciona

**Síntomas:**
- Cambios en archivos JSON no se aplican
- Reglas antiguas persisten después de edición

**Soluciones:**
1. Verificar permisos de escritura en el directorio de reglas
2. Confirmar que los archivos JSON tienen sintaxis válida
3. Revisar logs del proxy en busca de errores de parsing
4. Asegurarse de que el observador de archivos esté funcionando

### 3. Funciones dinámicas no se evalúan

**Síntomas:**
- Valores como `<UUID()>` aparecen literales
- Funciones como `<Aleatorio(...)>` no se ejecutan

**Soluciones:**
1. Verificar que el patrón de expresión regular sea correcto
2. Confirmar que las funciones dinámicas están implementadas en [modifiers.py](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/proxy/mitmproxy/addons/modifiers.py)
3. Revisar logs en busca de errores de evaluación

### 4. Docker Compose no inicia servicios

**Síntomas:**
- Error al construir imágenes
- Contenedores fallan inmediatamente

**Soluciones:**
1. Verificar versión de Docker Compose (requiere v2.0+)
2. Confirmar que Docker Desktop esté corriendo
3. Limpiar imágenes y volumenes antiguos: `docker system prune`
4. Verificar que los Dockerfiles sean válidos

### 5. Problemas de conexión con servicios externos

**Síntomas:**
- Conexiones fallidas a través del proxy
- Timeouts en solicitudes interceptadas

**Soluciones:**
1. Verificar reglas de firewall locales
2. Confirmar que el proxy permite conexiones salientes
3. Revisar configuración de red en docker-compose.yml
4. Probar conectividad directa sin proxy

## Diagnóstico de Problemas

### Verificar estado de servicios
```bash
docker compose ps
docker compose logs <servicio>
```

### Probar conectividad básica
```bash
# Probar proxy
curl -x localhost:8080 http://httpbin.org/json

# Probar ZAP
curl http://localhost:8090

# Probar ToxiProxy
curl http://localhost:8474/proxies
```

### Verificar reglas de interceptación
1. Acceder a `http://localhost:8081` (UI de mitmproxy)
2. Verificar que las reglas se hayan cargado correctamente
3. Monitorear tráfico en tiempo real

## Optimización de Rendimiento

### Recomendaciones:
- No usar demasiadas reglas simultáneas
- Evitar funciones dinámicas costosas en rutas críticas
- Usar `Tipo_modificacion: Parcial` cuando sea posible
- Limitar el tamaño de payloads modificados

### Monitoreo:
- Supervisar uso de CPU y memoria
- Verificar tiempos de respuesta adicionales por interceptación
- Revisar logs de desempeño periódicamente

## Recursos Adicionales

- [Documentación oficial de mitmproxy](https://docs.mitmproxy.org/)
- [Guía de expresiones regulares de Python](https://docs.python.org/3/library/re.html)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)