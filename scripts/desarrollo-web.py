#!/bin/bash

# Este script instala herramientas de desarrollo web comunes como Git y Node.js.

# 1. Instala Git. Git es un sistema de control de versiones esencial.
echo "Instalando Git..."
sudo apt install git -y

# 2. Instala NVM (Node Version Manager) para gestionar múltiples versiones de Node.js.
echo "Instalando NVM (Node Version Manager)..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Source the NVM script to make it available in the current shell session.
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# 3. Instala la última versión de Node.js LTS (Long-Term Support).
echo "Instalando la última versión LTS de Node.js..."
nvm install --lts

# 4. Establece la versión LTS como la versión por defecto.
echo "Estableciendo la versión LTS de Node.js como predeterminada..."
nvm use --lts

# 5. Verifica las versiones instaladas para confirmar.
echo "Verificando las instalaciones..."
node -v
npm -v
git --version

echo "Configuración de desarrollo web completada."
echo "¡Recuerda abrir una nueva terminal para que NVM esté disponible!"
