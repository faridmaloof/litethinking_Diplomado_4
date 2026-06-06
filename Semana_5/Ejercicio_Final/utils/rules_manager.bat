@echo off
REM Script para gestionar reglas del proxy mitmproxy

set RULES_DIR=proxy\mitmproxy\config\rules
set CONTAINER_NAME=qa-proxy

echo Gestion de Reglas para QA Engineering Testing Infrastructure
echo ===========================================================

if "%1"=="copy-to-container" (
    echo Copiando reglas al contenedor...
    podman cp %RULES_DIR%\ %CONTAINER_NAME%:/home/mitmproxy/config/rules/
    echo Reglas copiadas al contenedor %CONTAINER_NAME%
    goto :eof
)

if "%1"=="copy-from-container" (
    echo Copiando reglas desde el contenedor...
    mkdir %RULES_DIR% 2>nul
    podman cp %CONTAINER_NAME%:/home/mitmproxy/config/rules/. %RULES_DIR%\
    echo Reglas copiadas desde el contenedor %CONTAINER_NAME%
    goto :eof
)

if "%1"=="restart-with-rules" (
    echo Reiniciando contenedor con nuevas reglas...
    podman compose down
    podman compose build proxy
    podman compose up -d
    echo Contenedor reiniciado con nuevas reglas
    goto :eof
)

echo.
echo Uso:
echo   rules_manager.bat copy-to-container    - Copia reglas locales al contenedor
echo   rules_manager.bat copy-from-container  - Copia reglas desde contenedor a local
echo   rules_manager.bat restart-with-rules   - Reconstruye y reinicia contenedor con reglas locales
echo.