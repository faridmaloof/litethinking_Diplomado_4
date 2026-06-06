#!/bin/bash
# Script para gestionar reglas del proxy mitmproxy

RULES_DIR="proxy/mitmproxy/config/rules"
CONTAINER_NAME="qa-proxy"

echo "Gestion de Reglas para QA Engineering Testing Infrastructure"
echo "==========================================================="

case "$1" in
    "copy-to-container")
        echo "Copiando reglas al contenedor..."
        podman cp $RULES_DIR/. $CONTAINER_NAME:/home/mitmproxy/config/rules/
        echo "Reglas copiadas al contenedor $CONTAINER_NAME"
        ;;
    "copy-from-container")
        echo "Copiando reglas desde el contenedor..."
        mkdir -p $RULES_DIR
        podman cp $CONTAINER_NAME:/home/mitmproxy/config/rules/. $RULES_DIR/
        echo "Reglas copiadas desde el contenedor $CONTAINER_NAME"
        ;;
    "restart-with-rules")
        echo "Reiniciando contenedor con nuevas reglas..."
        podman compose down
        podman compose build proxy
        podman compose up -d
        echo "Contenedor reiniciado con nuevas reglas"
        ;;
    *)
        echo
        echo "Uso:"
        echo "  ./rules_manager.sh copy-to-container    - Copia reglas locales al contenedor"
        echo "  ./rules_manager.sh copy-from-container  - Copia reglas desde contenedor a local"
        echo "  ./rules_manager.sh restart-with-rules   - Reconstruye y reinicia contenedor con reglas locales"
        echo
        ;;
esac