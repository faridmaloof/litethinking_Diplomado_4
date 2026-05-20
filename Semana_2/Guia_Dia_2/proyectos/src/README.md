# NovaShop Checkout (React + TypeScript)

Sitio de ejemplo que simula una navegacion normal de compra:

1. Usuario ve carrito de productos.
2. Usuario completa formulario de pago.
3. Sitio procesa el pago y muestra resultado aprobado o no aprobado.

La aplicacion consume los mocks de WireMock y valida internamente:

- Codigo HTTP esperado.
- Body esperado campo por campo.

El usuario final ve un flujo amigable; el detalle tecnico queda opcional en la pantalla de resultado.

## Endpoints usados

- GET /api/health
- POST /api/pagos/aprobado
- POST /api/pagos

## Requisitos

- Node.js 20 o superior.
- WireMock levantado en http://localhost:8080.

## Ejecutar

1. Levanta WireMock desde el modulo QA.
2. Instala dependencias:

```bash
npm install
```

3. Inicia la app:

```bash
npm run dev
```

4. Abre la URL indicada por Vite (normalmente http://localhost:5173).

## Simulacion de escenarios

En el checkout puedes elegir el canal bancario:

- Banco principal: intenta pago aprobado (201).
- Banco contingencia: simula timeout/rechazo (504).

## Configuracion opcional

El frontend usa proxy de Vite para enviar /api al mock server.

- Destino por defecto: http://localhost:8080
- Variable opcional para cambiarlo: VITE_WIREMOCK_ORIGIN

Tambien puedes definir VITE_API_BASE_URL si quieres prefijar una base URL manualmente.
