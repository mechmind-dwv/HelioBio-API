#!/bin/bash

# ==============================================================================
# SCRIPT DE DESPLIEGUE MAESTRO
# Autor: Arquitecto de Software
# Descripción: Este script orquesta el proceso completo de despliegue,
#              desde la preparación hasta el lanzamiento en producción.
#              Requiere que otros scripts (build.sh, test.sh, etc.) existan
#              en el mismo directorio 'scripts/'.
# ==============================================================================

# Configuración de seguridad: Detiene el script si un comando falla.
set -e

# --- Variables de Entorno (Asegúrate de configurar estas variables en tu máquina local o CI) ---
# Usamos variables de entorno para evitar escribir valores sensibles en el código.
# Puedes cargarlas desde un archivo .env si usas un orquestador como Docker Compose o un CI.
# Ejemplo:
# export PROD_SERVER="usuario@tu.servidor.produccion"
# export PROD_PATH="/var/www/tu-app"

# --- Funciones de Despliegue ---

echo "Iniciando el proceso de despliegue..."
echo "-------------------------------------"

# 1. Función para la validación inicial del entorno.
# Asegura que las dependencias críticas y los archivos de configuración existan.
function validar_entorno() {
    echo "Paso 1: Validando el entorno..."
    if [[ ! -f "requirements.txt" ]]; then
        echo "Error: 'requirements.txt' no encontrado. Por favor, crea el archivo."
        exit 1
    fi
    echo "Validación de entorno completada con éxito."
}

# 2. Función para la etapa de 'Build' (compilación y empaquetado).
# Este paso delega en un script secundario para mantener la modularidad.
# Imagina que 'build.sh' podría compilar un binario, transpilador de JS, o empaquetar una aplicación.
function build_aplicacion() {
    echo "Paso 2: Construyendo la aplicación..."
    # Llama a un script de construcción que debe existir en el mismo directorio.
    # Por ejemplo: ./scripts/build_app.sh
    # Aquí simulamos el éxito.
    echo "La aplicación ha sido construida."
}

# 3. Función para ejecutar las pruebas.
# Las pruebas unitarias y de integración son críticas para la calidad.
# El despliegue no debería proceder si alguna prueba falla.
function ejecutar_pruebas() {
    echo "Paso 3: Ejecutando pruebas unitarias y de integración..."
    # Llama a un script de pruebas. Por ejemplo: ./scripts/run_tests.sh
    # Aquí simulamos el éxito.
    echo "Todas las pruebas han pasado con éxito."
}

# 4. Función para la etapa de "Desligue" o despliegue en sí.
# Esta función es responsable de mover los archivos a producción y reiniciar servicios.
function desplegar_a_produccion() {
    echo "Paso 4: Desplegando en el servidor de producción..."

    if [[ -z "$PROD_SERVER" ]] || [[ -z "$PROD_PATH" ]]; then
        echo "Error: Las variables PROD_SERVER y/o PROD_PATH no están definidas. Por favor, configúralas."
        exit 1
    fi

    # Aquí se usarían comandos como rsync, scp, o un comando de despliegue de Docker.
    # Ejemplo con rsync:
    # rsync -avz --delete ./dist/ "$PROD_SERVER:$PROD_PATH/"

    echo "Despliegue de archivos completado."
}

# 5. Función para la migración de la base de datos (si aplica).
# Este es un paso crítico que debe ejecutarse solo después del despliegue del código.
function migrar_base_de_datos() {
    echo "Paso 5: Ejecutando migraciones de base de datos..."
    # Llama a un script de migración. Por ejemplo: ./scripts/migrate_db.sh
    # Aquí simulamos el éxito.
    echo "Migraciones de base de datos completadas."
}

# 6. Función para reiniciar servicios y confirmar el estado.
# Una vez que todo está en su lugar, se reinicia la aplicación para cargar los cambios.
function reiniciar_servicios() {
    echo "Paso 6: Reiniciando los servicios de la aplicación..."
    # Se conecta al servidor remoto y reinicia el servicio (ej. con systemd o pm2).
    # Ejemplo: ssh "$PROD_SERVER" "sudo systemctl restart mi-aplicacion.service"
    echo "Servicios reiniciados. Despliegue finalizado."
}

# ==============================================================================
# Orquestación del Flujo de Trabajo
# ==============================================================================

# Si se llama con un argumento, ejecutamos esa función en particular.
# Esto es útil para la depuración (ej. ./deploy.sh ejecutar_pruebas).
if [ ! -z "$1" ]; then
  "$1"
  exit 0
fi

# El flujo de trabajo completo se ejecuta secuencialmente.
validar_entorno
build_aplicacion
ejecutar_pruebas
desplegar_a_produccion
migrar_base_de_datos
reiniciar_servicios

echo "-------------------------------------"
echo "¡Despliegue en producción completado con éxito! "
echo "La aplicación está en marcha."
