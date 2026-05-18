# scripts/setup.sh
#!/bin/bash

# --- Script de Configuración de HelioBio-API ---
# Este script automatiza el proceso de instalación de dependencias,
# configuración del entorno y preparación del proyecto para su ejecución.

# 1. Crear un entorno virtual
echo "Paso 1: Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: No se pudo crear el entorno virtual. Asegúrate de que python3 esté instalado."
    exit 1
fi

# 2. Activar el entorno virtual
echo "Paso 2: Activando entorno virtual..."
source venv/bin/activate

# 3. Instalar dependencias desde requirements.txt
echo "Paso 3: Instalando dependencias de Python..."
if [ ! -f requirements.txt ]; then
    echo "Error: El archivo requirements.txt no se encontró. No se puede continuar."
    deactivate
    exit 1
fi
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Falló la instalación de dependencias."
    deactivate
    exit 1
fi

# 4. Verificar la instalación
echo "Paso 4: Verificando instalación..."
# Aquí puedes añadir comandos para verificar bibliotecas clave
python -c "import fastapi; print('FastAPI instalado.')"
python -c "import uvicorn; print('Uvicorn instalado.')"
python -c "import pydantic; print('Pydantic instalado.')"

echo "¡Configuración completada exitosamente!"
echo "Para iniciar el servidor, ejecuta: ./scripts/start_server.sh"
