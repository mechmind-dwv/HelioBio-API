#!/bin/bash
# setup.sh - Script de instalación para HelioBio-API

echo "Instalando HelioBio-API..."
echo "============================"

# Actualizar sistema
pkg update && pkg upgrade -y

# Instalar dependencias
pkg install python git curl nano -y

# Instalar dependencias Python
pip install fastapi uvicorn requests pandas matplotlib numpy scipy statsmodels aiohttp python-multipart pydantic

# Clonar repositorio (si no existe)
if [ ! -d "HelioBio-API" ]; then
    git clone https://github.com/tuusuario/HelioBio-API.git
fi

cd HelioBio-API

# Crear directorio de datos
mkdir -p data

# Dar permisos de ejecución al script principal
chmod +x main.py

echo "Instalación completada."
echo "Para iniciar el servidor:"
echo "cd HelioBio-API && python main.py"
echo ""
echo "O ejecutar: ./start-server.sh"
