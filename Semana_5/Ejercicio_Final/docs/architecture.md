# Arquitectura de la Plataforma de Pruebas QA

## Visión General

La plataforma de pruebas QA es una solución completa que integra múltiples herramientas de calidad de software en un entorno contenerizado. Permite a los estudiantes experimentar con pruebas de seguridad, rendimiento, ingeniería del caos y automatización de pruebas en un entorno realista.

## Componentes Principales

### 1. Proxy de Interceptación (mitmproxy)

#### Características:
- Interceptación de tráfico HTTP/HTTPS
- Sistema de reglas basado en JSON con hot-reload
- Soporte para funciones dinámicas en tiempo de ejecución
- Modificaciones completas o parciales de requests/responses

#### Tecnología:
- **Base**: mitmproxy 9.0.1
- **Puertos expuestos**: 8080 (proxy), 8081 (UI web)
- **Volúmenes**: 
  - Reglas de interceptación
  - Certificados CA
  - Secretos de Docker

#### Arquitectura Interna:
- [interceptor.py](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/proxy/mitmproxy/addons/interceptor.py): Punto de entrada principal
- [config_loader.py](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/proxy/mitmproxy/addons/config_loader.py): Carga y monitoreo de reglas con hot-reload
- [rule_engine.py](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/proxy/mitmproxy/addons/rule_engine.py): Procesamiento de reglas
- [modifiers.py](file:///d%3A/Curso/Certificacion_4/Semana_5/Ejercicio_Final/proxy/mitmproxy/addons/modifiers.py): Aplicación de modificaciones

### 2. Seguridad (ZAP + SonarQube)

#### OWASP ZAP:
- Escaneo de vulnerabilidades web
- Integración con pipeline de pruebas
- Políticas de seguridad configurables
- API para automatización

#### SonarQube:
- Análisis estático de calidad de código
- Quality gates configurables
- Métricas de cobertura y deuda técnica

### 3. Rendimiento (k6)

- Pruebas de carga programáticas
- Escenarios de usuario virtualizados
- Métricas de rendimiento detalladas
- Integración con CI/CD

### 4. Ingeniería del Caos (ToxiProxy)

- Simulación de fallos de red
- Latencias artificiales
- Pérdida de paquetes
- Tiempo de actividad reducido para pruebas de resistencia

## Flujo de Datos

1. **Tráfico HTTP/HTTPS** entra al proxy
2. **Reglas de interceptación** se aplican en tiempo real
3. **Modificaciones** se realizan según configuración
4. **Tráfico modificado** continúa al destino original
5. **Herramientas de QA** analizan el comportamiento resultante

## Seguridad y Gestión de Credenciales

- **Docker Secrets**: Para credenciales en producción
- **Variables de entorno**: Solo placeholders en .env.example
- **Montaje de volúmenes**: Para archivos de configuración sensibles
- **Ningún secreto en código**: Archivos excluidos en .gitignore

## Escalabilidad

- **Contenerizado**: Cada componente es independiente
- **Configurable**: Parámetros ajustables por entorno
- **Extensible**: Nuevo sistema de reglas fácilmente ampliable
- **Monitorizable**: Logs y métricas disponibles para cada servicio

## Patrones de Diseño Implementados

- **Observador**: Para hot-reload de reglas
- **Motor de Reglas**: Sistema de matching dinámico
- **Evaluación Lazy**: Funciones dinámicas ejecutadas en tiempo de uso
- **Fachada**: Interfaz simple para sistemas complejos