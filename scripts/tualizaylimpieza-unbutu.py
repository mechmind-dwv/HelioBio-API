#!/bin/bash

# Este script actualiza los paquetes del sistema y limpia los archivos de caché.
# Es una buena práctica ejecutarlo regularmente para mantener tu sistema optimizado.

# 1. Actualiza la lista de paquetes.
echo "Actualizando la lista de paquetes..."
sudo apt update

# 2. Actualiza todos los paquetes instalados a sus últimas versiones.
echo "Actualizando todos los paquetes instalados..."
sudo apt upgrade -y

# 3. Elimina paquetes que ya no son necesarios (autoremove).
echo "Eliminando paquetes obsoletos y dependencias no utilizadas..."
sudo apt autoremove -y

# 4. Limpia la caché local de archivos de paquetes.
echo "Limpiando la caché de paquetes..."
sudo apt clean

echo "Proceso de actualización y limpieza completado."
