# Modulo 2 - mitmweb (Intercepcion y alteracion)

## Archivos
- `start_mitmweb.ps1`
- `mitm_addon_response_override.py`

## Primera ejecucion (Windows)
1. Verificar Python:

```powershell
python --version
```

2. Instalar mitmproxy (una sola vez):

```powershell
python -m pip install --upgrade pip
python -m pip install mitmproxy
```

3. Permitir scripts de PowerShell en la sesion actual (si aplica):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. Ir a la carpeta del modulo:

```powershell
cd D:\Curso\Certificacion_4\Semana_2\Guia_Dia_2\proyectos\02-mitmproxy
```

## Levantar mitmweb
Ejecutar:

```powershell
.\start_mitmweb.ps1
```

El script intenta en este orden:
1. `mitmweb` en PATH.
2. `python -m mitmproxy.tools.main mitmweb`.

Si falla, mostrará el comando exacto para corregir la instalación.

Queda disponible:
- Proxy: `127.0.0.1:8080`
- Web UI: `http://127.0.0.1:8081`

## Configurar navegador o cliente
Configurar proxy HTTP/HTTPS a `127.0.0.1:8080`.

## Pruebas demo sin backend real (reglas locales)
Con cliente que use proxy (curl o Postman):

```powershell
curl -x 127.0.0.1:8080 -X POST http://example.com/mitm/demo/pagos
curl -x 127.0.0.1:8080 http://example.com/mitm/demo/orden/123
```

Resultado esperado:
- `POST /mitm/demo/pagos`: responde `504` con delay de 6 segundos.
- `GET /mitm/demo/orden/123`: responde `200` con JSON simulado.

## Prueba de mutacion sobre sitio publico
Con proxy activo:

```powershell
curl -x 127.0.0.1:8080 https://httpbin.org/json
```

Resultado esperado:
- Respuesta alterada por el addon (JSON didactico).

## Nota SSL
Si el navegador muestra advertencias TLS, instalar certificado de mitmproxy para pruebas HTTPS.

Comando útil para abrir instalación local de certificados:

```powershell
python -m mitmproxy.tools.main mitmweb
```

Luego abrir en navegador: `http://mitm.it`
