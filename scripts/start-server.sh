#!/bin/bash
# start-server.sh - Inicia el servidor HelioBio-API

cd "$(dirname "$0")"

echo "Iniciando HelioBio-API..."
echo "========================="
echo "Servidor disponible en: http://localhost:8000"
echo "Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"

# Iniciar servidor
python main.py
