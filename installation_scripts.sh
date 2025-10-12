#!/bin/bash
# =================================================================
# HelioBio-API - Script de Instalación Completo
# Sistema operativo: Linux Mint 22.1 / Ubuntu 22.04+
# Autor: mechmind-dwv (ia.mechmind@gmail.com)
# =================================================================

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Banner
clear
print_header "HelioBio-API - Sistema de Instalación v3.0.0"
echo -e "${BLUE}Basado en las investigaciones de Alexander Chizhevsky${NC}"
echo -e "${BLUE}Autor: mechmind-dwv (ia.mechmind@gmail.com)${NC}\n"

# Verificar sistema operativo
print_header "1. Verificando Sistema Operativo"
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    echo "Sistema detectado: $NAME $VERSION"
    print_success "Sistema compatible"
else
    print_error "No se pudo detectar el sistema operativo"
    exit 1
fi

# Verificar permisos
if [[ $EUID -eq 0 ]]; then
   print_error "No ejecutar este script como root. Use su usuario normal."
   exit 1
fi

# Actualizar sistema
print_header "2. Actualizando Sistema"
echo "Actualizando lista de paquetes..."
sudo apt update
print_success "Lista de paquetes actualizada"

# Instalar dependencias del sistema
print_header "3. Instalando Dependencias del Sistema"

SYSTEM_DEPS=(
    "python3.10"
    "python3.10-venv"
    "python3-pip"
    "python3-dev"
    "build-essential"
    "git"
    "curl"
    "wget"
    "nano"
    "vim"
    "libssl-dev"
    "libffi-dev"
    "libxml2-dev"
    "libxslt1-dev"
    "zlib1g-dev"
    "libbz2-dev"
    "libreadline-dev"
    "libsqlite3-dev"
    "llvm"
    "libncurses5-dev"
    "libncursesw5-dev"
    "xz-utils"
    "tk-dev"
)

for dep in "${SYSTEM_DEPS[@]}"; do
    if dpkg -l | grep -q "^ii  $dep "; then
        print_success "$dep ya instalado"
    else
        echo "Instalando $dep..."
        sudo apt install -y "$dep"
        print_success "$dep instalado"
    fi
done

# Verificar Python
print_header "4. Verificando Python"
PYTHON_VERSION=$(python3 --version)
echo "Versión de Python: $PYTHON_VERSION"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_success "Versión de Python compatible (>=3.8)"
else
    print_error "Se requiere Python 3.8 o superior"
    exit 1
fi

# Crear entorno virtual
print_header "5. Configurando Entorno Virtual"
if [[ -d "venv" ]]; then
    print_warning "El entorno virtual ya existe"
    read -p "¿Desea recrearlo? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Entorno virtual recreado"
    fi
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
source venv/bin/activate
print_success "Entorno virtual activado"

# Actualizar pip, setuptools y wheel
print_header "6. Actualizando Herramientas de Python"
pip install --upgrade pip setuptools wheel
print_success "Herramientas actualizadas"

# Instalar dependencias de Python
print_header "7. Instalando Dependencias de Python"
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    print_success "Dependencias instaladas desde requirements.txt"
else
    print_warning "requirements.txt no encontrado, instalando dependencias manualmente..."
    
    # Core dependencies
    pip install fastapi==0.104.1
    pip install uvicorn[standard]==0.24.0
    pip install pydantic==2.5.0
    pip install python-multipart==0.0.6
    
    # HTTP and async
    pip install aiohttp==3.9.1
    pip install aiofiles==23.2.1
    pip install requests==2.31.0
    
    # Data processing
    pip install pandas==2.1.3
    pip install numpy==1.24.3
    pip install scipy==1.11.4
    
    # Statistical analysis
    pip install statsmodels==0.14.0
    pip install scikit-learn==1.3.2
    
    # Machine Learning
    pip install xgboost==2.0.2
    
    # Time series
    pip install prophet==1.1.5 || echo "Prophet opcional, continuando..."
    
    # Visualization
    pip install matplotlib==3.8.2
    pip install seaborn==0.13.0
    pip install plotly==5.18.0
    
    # Wavelets
    pip install PyWavelets==1.5.0
    
    # Database
    pip install sqlalchemy==2.0.23
    pip install alembic==1.13.0
    
    # Testing
    pip install pytest==7.4.3
    pip install pytest-asyncio==0.21.1
    pip install httpx==0.25.2
    
    print_success "Dependencias básicas instaladas"
fi

# Crear estructura de directorios
print_header "8. Creando Estructura de Directorios"

DIRECTORIES=(
    "data/cache"
    "data/logs"
    "data/models"
    "data/exports"
    "data/solar"
    "data/health"
    "data/analysis"
    "static"
    "backups"
)

for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"
    print_success "Directorio creado: $dir"
done

# Crear archivos de configuración
print_header "9. Configurando Archivos de Configuración"

# Crear .env si no existe
if [[ ! -f ".env" ]]; then
    cat > .env << 'EOF'
# HelioBio-API Configuration
PROJECT_NAME=HelioBio-API
PROJECT_VERSION=3.0.0
AUTHOR_NAME=mechmind-dwv
AUTHOR_EMAIL=ia.mechmind@gmail.com

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True

# Database
DATABASE_URL=sqlite:///./data/heliobio_database.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/heliobio.log

# Cache
CACHE_DURATION_HOURS=1
MAX_CACHE_SIZE_MB=100

# API URLs (no cambiar a menos que sea necesario)
SILSO_SUNSPOT_URL=https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv
NOAA_SOLAR_URL=https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json
NOAA_GEOMAG_URL=https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json
NOAA_SPACE_WEATHER_URL=https://services.swpc.noaa.gov/products/summary.json
EOF
    print_success "Archivo .env creado"
else
    print_warning "Archivo .env ya existe, no se sobrescribe"
fi

# Crear config.json
if [[ ! -f "config.json" ]]; then
    cat > config.json << 'EOF'
{
  "app": {
    "name": "HelioBio-API",
    "version": "3.0.0",
    "description": "Sistema de análisis heliobiológico basado en Alexander Chizhevsky",
    "author": "mechmind-dwv",
    "email": "ia.mechmind@gmail.com",
    "github": "https://github.com/mechmind-dwv/HelioBio-API"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "log_level": "info"
  },
  "data_sources": {
    "silso": {
      "name": "SILSO - Royal Observatory of Belgium",
      "url": "https://www.sidc.be/silso/",
      "enabled": true
    },
    "noaa": {
      "name": "NOAA Space Weather Prediction Center",
      "url": "https://services.swpc.noaa.gov/",
      "enabled": true
    }
  },
  "analysis": {
    "min_data_points": 50,
    "correlation_significance_level": 0.05,
    "bootstrap_iterations": 1000,
    "max_lag_months": 24
  },
  "predictions": {
    "default_horizon_months": 24,
    "max_horizon_months": 120,
    "models_enabled": ["arima", "random_forest", "solar_cycle"],
    "ensemble_weights": {
      "arima": 0.3,
      "random_forest": 0.3,
      "solar_cycle": 0.4
    }
  }
}
EOF
    print_success "Archivo config.json creado"
else
    print_warning "Archivo config.json ya existe"
fi

# Crear script de inicio
print_header "10. Creando Scripts de Inicio"

cat > start.sh << 'EOF'
#!/bin/bash
# Script de inicio para HelioBio-API

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "============================================================"
echo "HelioBio-API v3.0.0 - Iniciando Servidor"
echo "Basado en Alexander Chizhevsky"
echo "Autor: mechmind-dwv (ia.mechmind@gmail.com)"
echo "============================================================"
echo -e "${NC}"

# Activar entorno virtual
if [[ -d "venv" ]]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Entorno virtual activado${NC}"
else
    echo "Error: No se encuentra el entorno virtual"
    echo "Ejecute: python3 -m venv venv"
    exit 1
fi

# Verificar dependencias críticas
echo "Verificando dependencias..."
python -c "import fastapi; import uvicorn; import pandas; import numpy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencias verificadas${NC}"
else
    echo "Error: Faltan dependencias. Ejecute: pip install -r requirements.txt"
    exit 1
fi

# Crear directorios si no existen
mkdir -p data/cache data/logs data/models

echo ""
echo "Iniciando servidor..."
echo "Documentación: http://localhost:8000/docs"
echo "Dashboard: http://localhost:8000/dashboard"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar servidor
cd app && python main.py
EOF

chmod +x start.sh
print_success "Script start.sh creado"

# Crear script de prueba
cat > test.sh << 'EOF'
#!/bin/bash
# Script de prueba para HelioBio-API

source venv/bin/activate

echo "Ejecutando tests..."
pytest tests/ -v --cov=app --cov-report=html

echo ""
echo "Reporte de cobertura generado en: htmlcov/index.html"
EOF

chmod +x test.sh
print_success "Script test.sh creado"

# Crear script de backup
cat > backup.sh << 'EOF'
#!/bin/bash
# Script de backup para HelioBio-API

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="heliobio_backup_${TIMESTAMP}.tar.gz"

mkdir -p $BACKUP_DIR

echo "Creando backup..."
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='data/cache' \
    app/ data/ config.json .env 2>/dev/null

echo "✓ Backup creado: ${BACKUP_DIR}/${BACKUP_FILE}"
ls -lh "${BACKUP_DIR}/${BACKUP_FILE}"
EOF

chmod +x backup.sh
print_success "Script backup.sh creado"

# Verificar instalación
print_header "11. Verificando Instalación"

echo "Verificando módulos de Python..."
python -c "
import sys
modules = [
    'fastapi', 'uvicorn', 'pydantic', 'pandas', 'numpy', 
    'scipy', 'sklearn', 'statsmodels', 'matplotlib'
]
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        missing.append(module)
        print(f'✗ {module} - FALTANTE')

if missing:
    print(f'\nMódulos faltantes: {missing}')
    sys.exit(1)
else:
    print('\n✓ Todos los módulos críticos están instalados')
"

if [ $? -eq 0 ]; then
    print_success "Verificación completada exitosamente"
else
    print_error "Algunos módulos faltan. Revise la instalación."
    exit 1
fi

# Crear archivo __init__.py en app/core si no existe
print_header "12. Verificando Módulos del Proyecto"

INIT_FILES=(
    "app/__init__.py"
    "app/api/__init__.py"
    "app/config/__init__.py"
    "app/core/__init__.py"
    "app/database/__init__.py"
    "app/models/__init__.py"
    "app/services/__init__.py"
    "app/utils/__init__.py"
    "tests/__init__.py"
)

for init_file in "${INIT_FILES[@]}"; do
    mkdir -p "$(dirname "$init_file")"
    if [[ ! -f "$init_file" ]]; then
        touch "$init_file"
        print_success "Creado: $init_file"
    fi
done

# Resumen final
print_header "INSTALACIÓN COMPLETADA"

echo -e "${GREEN}"
echo "✓ Sistema operativo verificado"
echo "✓ Dependencias del sistema instaladas"
echo "✓ Python y entorno virtual configurados"
echo "✓ Dependencias de Python instaladas"
echo "✓ Estructura de directorios creada"
echo "✓ Archivos de configuración generados"
echo "✓ Scripts de utilidad creados"
echo -e "${NC}"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Próximos pasos:${NC}"
echo ""
echo "1. Copiar los módulos del core:"
echo "   - app/core/data_fetcher.py"
echo "   - app/core/analyzer.py"
echo "   - app/core/predictor.py"
echo "   - app/core/chizhevsky_kb.py"
echo "   - app/core/alert_system.py"
echo ""
echo "2. Iniciar el servidor:"
echo "   ${YELLOW}./start.sh${NC}"
echo ""
echo "3. Acceder a la documentación:"
echo "   ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo "4. Ver el dashboard:"
echo "   ${YELLOW}http://localhost:8000/dashboard${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Desarrollado por: mechmind-dwv (ia.mechmind@gmail.com)${NC}"
echo -e "${BLUE}Basado en: Alexander Chizhevsky's Heliobiology${NC}"
echo ""
