@echo off
echo Verificando la infraestructura de pruebas QA...
echo.

echo 1. Verificando estado de contenedores:
podman compose ps
echo.

echo 2. Verificando conexion al proxy (puerto 8080):
curl -I http://localhost:8080 2>nul || echo "No se pudo conectar al puerto 8080"
echo.

echo 3. Verificando conexion a la UI web (puerto 8081):
curl -I http://localhost:8081 2>nul || echo "No se pudo conectar al puerto 8081"
echo.

echo 4. Verificando conexion a ZAP (puerto 8090):
curl -I http://localhost:8090 2>nul || echo "No se pudo conectar al puerto 8090"
echo.

echo 5. Verificando conexion a ToxiProxy (puerto 8474):
curl -I http://localhost:8474 2>nul || echo "No se pudo conectar al puerto 8474"
echo.

echo.
echo Verificacion completa!
echo.
echo Accede a las interfaces:
echo   - Proxy UI: http://localhost:8081
echo   - ZAP API: http://localhost:8090
echo   - ToxiProxy API: http://localhost:8474
echo.
pause