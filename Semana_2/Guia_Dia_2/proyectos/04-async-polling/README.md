# Modulo 4 - Asincronia y Active Polling

## Archivo
- `python/polling_demo.py`

## Ejecutar
```powershell
python python/polling_demo.py
```

## Resultado esperado
1. Mensaje de procesamiento asincrono en background.
2. Polling cada 0.5 segundos.
3. Cambio de estado a `CANCELADO` alrededor de 4 segundos.
4. Mensaje final de prueba SDET exitosa.

## Objetivo QA
Comparar anti-patron (`sleep` fijo) vs espera activa (polling) para pruebas robustas en flujos asincronos.
