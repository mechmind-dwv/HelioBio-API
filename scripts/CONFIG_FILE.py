#!/bin/bash

# Este script interactivo ayuda a configurar tus tokens y claves de API
# guardándolos en un archivo .env.
# Esto es una buena práctica para mantener tus credenciales fuera de tu código fuente.

# Nombre del archivo de configuración.
CONFIG_FILE=".env"

echo "--- Configuración de Credenciales ---"
echo "Este script creará un archivo '${CONFIG_FILE}' con tus credenciales."
echo "Si el archivo ya existe, su contenido será reemplazado."
echo "-------------------------------------"

# Pide al usuario que introduzca el token de API.
read -p "Introduce tu Token de API: " API_TOKEN

# Pide al usuario que introduzca la clave secreta.
# La opción '-s' hace que el texto introducido no se muestre en la terminal.
read -s -p "Introduce tu Clave Secreta: " SECRET_KEY
echo "" # Agrega una nueva línea después de la entrada de la clave oculta.

# Verifica si las variables no están vacías
if [ -z "$API_TOKEN" ] || [ -z "$SECRET_KEY" ]; then
    echo "Error: El token o la clave no pueden estar vacíos. Terminando el script."
    exit 1
fi

# Crea el archivo .env con las variables de entorno.
# Usamos 'cat >' para sobrescribir el archivo si ya existe.
# Es importante usar comillas simples para que las variables no se expandan aquí.
cat <<EOF > "$CONFIG_FILE"
# Variables de entorno para la aplicación
# Este archivo es generado por scripts/configurar_credenciales.sh
API_TOKEN="$API_TOKEN"
SECRET_KEY="$SECRET_KEY"
EOF

# Verifica si el archivo se creó correctamente.
if [ -f "$CONFIG_FILE" ]; then
    echo "¡Éxito! Archivo '${CONFIG_FILE}' creado con tus credenciales."
    echo "Para cargar estas variables en tu entorno, ejecuta:"
    echo "source $CONFIG_FILE"
    echo "O, si usas la línea de comandos en un proyecto, las librerías de entorno como 'dotenv' las cargarán automáticamente."
else
    echo "Error: Fallo al crear el archivo '${CONFIG_FILE}'."
    exit 1
fi
