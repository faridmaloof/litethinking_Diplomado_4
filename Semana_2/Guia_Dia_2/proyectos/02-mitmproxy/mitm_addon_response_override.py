"""
Addon para mitmproxy/mitmweb.

Objetivo:
1) Simular respuestas totalmente controladas para demo (sin depender del backend).
2) Mostrar cómo mutar una respuesta real de un sitio publico.

Reglas demo (locales):
- POST /mitm/demo/pagos      -> 504 con 6s de delay
- GET  /mitm/demo/orden/123  -> 200 con JSON de orden aprobada

Regla publica (mutacion de respuesta real):
- Host: httpbin.org, Path: /json
  Se reemplaza la respuesta por un JSON didactico.
"""

import json
import time
from mitmproxy import ctx, http


def load(loader):
    ctx.log.info("Addon cargado: mitm_addon_response_override.py")


def request(flow: http.HTTPFlow) -> None:
    path = flow.request.path
    method = flow.request.method.upper()

    # Regla 1: simular timeout de banco en pagos
    if method == "POST" and path == "/mitm/demo/pagos":
        time.sleep(6)
        flow.response = http.Response.make(
            504,
            json.dumps(
                {
                    "error": "Gateway Timeout - Banco Caido",
                    "codigo": "ERR_504",
                    "origen": "mitmweb-addon",
                }
            ),
            {"Content-Type": "application/json"},
        )
        ctx.log.info("[OVERRIDE] POST /mitm/demo/pagos -> 504 (delay 6s)")
        return

    # Regla 2: simular consulta de orden aprobada
    if method == "GET" and path == "/mitm/demo/orden/123":
        flow.response = http.Response.make(
            200,
            json.dumps(
                {
                    "orden": "123",
                    "estado": "APROBADO",
                    "monto": 1000,
                    "origen": "mitmweb-addon",
                }
            ),
            {"Content-Type": "application/json"},
        )
        ctx.log.info("[OVERRIDE] GET /mitm/demo/orden/123 -> 200")
        return


def response(flow: http.HTTPFlow) -> None:
    host = flow.request.pretty_host.lower()
    path = flow.request.path

    # Regla 3: mutar respuesta real publica para demo
    if host == "httpbin.org" and path == "/json":
        flow.response.status_code = 200
        flow.response.headers["Content-Type"] = "application/json"
        flow.response.text = json.dumps(
            {
                "mensaje": "Respuesta mutada por mitmweb",
                "host_original": host,
                "path_original": path,
                "objetivo": "Demostracion QA de intercepcion",
            }
        )
        ctx.log.info("[MUTATION] httpbin.org/json fue alterado por el addon")
