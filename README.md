# 🌞 HelioBio-API v3.0.0

**Sistema Avanzado de Análisis Heliobiológico**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-27%2F27-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

Sistema científico basado en las investigaciones pioneras de **Alexander Leonidovich Chizhevsky** (1897-1964), fundador de la Heliobiología, que estudió las correlaciones entre la actividad solar y los procesos biológicos terrestres.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Teoría Científica](#-teoría-científica)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Desarrollo](#-desarrollo)
- [Testing](#-testing)
- [Visualizaciones](#-visualizaciones)
- [Configuración Avanzada](#-configuración-avanzada)
- [Despliegue en Producción](#-despliegue-en-producción)
- [Recursos Adicionales](#-recursos-adicionales)
- [Contribuir](#-contribuir)
- [Seguridad](#-seguridad)
- [Licencia](#-licencia)
- [Autor](#-autor)
- [Estado del Proyecto](#-estado-del-proyecto)

---

## 🎯 Características

### Análisis Científico
- ✅ **Correlaciones estadísticas avanzadas** (Pearson, Spearman, Kendall, Granger)
- ✅ **Análisis espectral y wavelets** para detección de periodicidades
- ✅ **Validación rigurosa** con bootstrap y validación cruzada temporal
- ✅ **Análisis de causalidad** de Granger multivariada

### Datos en Tiempo Real
- 🌐 **SILSO** (Royal Observatory Belgium) - Manchas solares históricos
- 🌐 **NOAA** Space Weather Prediction Center - Datos actuales
- 🌐 **OMS/WHO** - Datos epidemiológicos (históricos)
- 🌐 **NASA DONKI** - Llamaradas solares en tiempo real

### Predicción Avanzada
- 📈 **Modelos ARIMA/SARIMA** para series temporales
- 🌲 **Random Forest** para patrones no lineales
- 🔄 **Solar Cycle Models** basados en teorías de Chizhevsky
- 🎯 **Ensemble Methods** para mayor precisión

### Sistema de Alertas
- ⚠️ Alertas tempranas basadas en correlaciones validadas
- 📊 Evaluación de riesgo por fase del ciclo solar
- 🏥 Recomendaciones preventivas para sistemas de salud

---

## 🔬 Teoría Científica

### Alexander Leonidovich Chizhevsky (1897-1964)

Científico ruso pionero en **Heliobiología** y **Cosmobiología**, Chizhevsky documentó correlaciones sistemáticas entre:

- **Ciclos solares de 11 años** y eventos históricos humanos
- **Actividad solar** y brotes epidémicos
- **Máximos solares** y revoluciones/conflictos
- **Fases del ciclo solar** y procesos biológicos

### Principios Fundamentales

1. **Conexión Solar-Terrestre**: Toda la vida en la Tierra está influenciada por la actividad solar a través de radiación electromagnética y corpuscular.

2. **Ciclos de 11 años**: Los ciclos solares de ~11.2 años correlacionan con:
   - Pandemias históricas (Gripe Española 1918, Asiática 1957, etc.)
   - Eventos históricos (revoluciones, guerras)
   - Procesos biológicos (cardiovasculares, neurológicos, inmunológicos)

3. **Fases del Ciclo**:
   - **Mínimo**: Apatía social, menor actividad biológica
   - **Ascendente**: Reorganización, activación inmunológica
   - **Máximo**: Máxima excitabilidad, picos epidémicos
   - **Descendente**: Estabilización, normalización

### Validación Moderna

Este sistema implementa metodologías estadísticas modernas para validar y refinar las teorías de Chizhevsky usando:
- Análisis de correlación múltiple
- Tests de causalidad de Granger
- Análisis espectral de frecuencias
- Modelos predictivos de machine learning

---

## 🚀 Instalación

### Requisitos del Sistema

- **Sistema Operativo**: Linux Mint 22.1+ / Ubuntu 22.04+ / Debian 11+ / Termux (Android)
- **Python**: 3.10 o superior
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espacio en disco**: 2GB mínimo

### Instalación Automática

```bash
# Clonar el repositorio
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API

# Dar permisos de ejecución al script
chmod +x scripts/setup.sh

# Ejecutar instalación automática
./scripts/setup.sh
```

El script automáticamente:

· ✅ Verifica el sistema operativo
· ✅ Instala dependencias del sistema
· ✅ Crea entorno virtual Python
· ✅ Instala dependencias de Python
· ✅ Crea estructura de directorios
· ✅ Configura archivos de configuración

Instalación Manual

```bash
# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip \
    build-essential git curl wget libssl-dev

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt

# 4. Crear directorios necesarios
mkdir -p data/{cache,logs,models,exports}
mkdir -p backups

# 5. Copiar archivo de configuración
cp .env.example .env
```

Instalación en Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python python-pip rust binutils cmake build-essential git
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

💻 Uso Rápido

Iniciar el Servidor

```bash
# Método 1: Script de inicio
./start.sh

# Método 2: Uvicorn directo (recomendado)
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en:

· API: http://localhost:8000
· Dashboard: http://localhost:8000/dashboard
· Documentación interactiva: http://localhost:8000/docs
· Documentación alternativa: http://localhost:8000/redoc

Ejemplos de Uso

```bash
# Actividad solar (datos reales SILSO)
curl "http://localhost:8000/solar/activity?start_date=2024-01-01&end_date=2024-12-31"

# Eventos epidemiológicos históricos
curl http://localhost:8000/health/events

# Análisis de correlación
curl "http://localhost:8000/analysis/correlate?years_before=15&years_after=5"

# Alertas actuales
curl http://localhost:8000/alerts/current

# Clima espacial NOAA (tiempo real)
curl http://localhost:8000/space-weather

# Ciclos solares históricos (1755-presente)
curl http://localhost:8000/solar-cycles

# Base de conocimiento Chizhevsky
curl http://localhost:8000/chizhevsky/knowledge
```

---

📖 Endpoints de la API

Endpoints Implementados (v3.0.0)

Endpoint Método Descripción Fuente de Datos
/ GET Página de inicio -
/dashboard GET Panel HTML interactivo -
/solar/activity GET Actividad solar SILSO real
/health/events GET Eventos epidemiológicos OMS/Chizhevsky
/analysis/correlate GET Análisis de correlación Cálculo en tiempo real
/alerts/current GET Alertas de salud Basado en datos reales
/chizhevsky/knowledge GET Base de conocimiento Obra de Chizhevsky
/space-weather GET Clima espacial NOAA tiempo real
/solar-cycles GET 25 ciclos solares (1755-2025) SILSO histórico
/docs GET Swagger UI -
/redoc GET ReDoc -

Endpoints Planeados (Roadmap)

Endpoint Método Descripción
/predictions/solar GET Predicción de actividad solar
/predictions/biological GET Predicción de riesgo biológico
/solar/historical GET Datos históricos detallados
/solar/cycle/current GET Información del ciclo actual

---

📁 Estructura del Proyecto

```
HelioBio-API/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada principal
│   ├── dashboard.py               # Dashboard HTML interactivo
│   ├── solar_fetcher.py           # Obtención datos SILSO reales
│   ├── pandemic_data.py           # Dataset epidemiológico verificado
│   ├── space_weather.py           # Clima espacial NOAA
│   ├── solar_cycles.py            # Historial de ciclos solares
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Configuración global
│   │   └── database.py            # Configuración de BD
│   ├── models/
│   │   ├── __init__.py
│   │   ├── solar.py               # Modelos de datos solares
│   │   ├── biological.py          # Modelos epidemiológicos
│   │   ├── analysis.py            # Modelos de análisis
│   │   └── alerts.py              # Modelos de alertas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chizhevsky_kb.py       # Base de conocimiento
│   │   ├── data_fetcher.py        # Obtención de datos
│   │   ├── analyzer.py            # Análisis estadístico
│   │   ├── predictor.py           # Sistema de predicción
│   │   └── alert_system.py        # Sistema de alertas
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/             # Endpoints de la API
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py          # Gestión de conexiones
│   │   └── repositories/          # Capa de acceso a datos
│   ├── services/
│   │   └── __init__.py            # Lógica de negocio
│   └── utils/
│       ├── __init__.py
│       ├── visualizations.py      # Generación de gráficos
│       ├── statistics.py          # Utilidades estadísticas
│       └── helpers.py             # Funciones auxiliares
├── data/
│   ├── cache/                     # Cache de datos
│   ├── logs/                      # Logs de aplicación
│   ├── models/                    # Modelos ML guardados
│   ├── exports/                   # Exportaciones
│   ├── solar/                     # Datos solares
│   ├── health/                    # Datos de salud
│   └── analysis/                  # Resultados de análisis
├── docs/
│   ├── API_Documentation.md       # Documentación de API
│   ├── Scientific_Background.md   # Base científica
│   └── Installation_Guide.md      # Guía de instalación
├── scripts/
│   ├── setup.sh                   # Instalación automática
│   ├── start-server.sh            # Inicio del servidor
│   ├── update_data.py             # Actualización de datos
│   ├── backup_db.py               # Backup de base de datos
│   └── heliobio-api.service       # Servicio systemd
├── tests/
│   ├── conftest.py                # Fixtures compartidas
│   ├── test_api/                  # Tests de API
│   ├── test_core/                 # Tests de módulos core
│   └── test_utils/                # Tests de utilidades
├── .github/
│   ├── workflows/                 # CI/CD pipelines
│   ├── dependabot.yml             # Actualizaciones automáticas
│   └── ISSUE_TEMPLATE/            # Plantillas de issues
├── static/                        # Archivos estáticos
├── backups/                       # Backups del sistema
├── .env                           # Variables de entorno
├── .env.example                   # Ejemplo de configuración
├── .gitignore                     # Archivos ignorados por Git
├── .flake8                        # Configuración de linter
├── config.json                    # Configuración JSON
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker
├── docker-compose.yml             # Orquestación Docker
├── README.md                      # Este archivo
├── LICENSE                        # Licencia MIT
└── start.sh                       # Script de inicio rápido
```

---

🛠️ Desarrollo

Configurar Entorno de Desarrollo

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-cov autoflake isort

# Formatear código
black app/ tests/
isort app/ tests/
flake8 app/ tests/
```

Ejecutar Tests

```bash
# Todos los tests (27 tests)
python -m pytest tests/ -v

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_core/test_analyzer.py -v
pytest tests/test_api/ -v
```

---

🧪 Testing

27 tests automatizados - 100% pasando.

Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas
├── test_api/
│   └── test_main.py         # Tests de todos los endpoints
├── test_core/
│   ├── test_data_fetcher.py # Tests del fetcher solar
│   └── test_analyzer.py     # Tests del analizador
└── test_utils/
    └── __init__.py
```

---

📊 Visualizaciones

El sistema genera automáticamente:

· 📈 Gráficos de series temporales de actividad solar
· 🔗 Diagramas de correlación entre variables
· 📊 Espectrogramas de análisis de frecuencias
· 🗺️ Mapas de calor de coherencia wavelet
· 📉 Predicciones con intervalos de confianza

Las visualizaciones se generan en formato PNG/SVG y se pueden obtener vía API.

---

🔧 Configuración Avanzada

Variables de Entorno (.env)

```bash
# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Base de datos
DATABASE_URL=sqlite:///./data/heliobio_database.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/heliobio.log

# Cache
CACHE_DURATION_HOURS=1
MAX_CACHE_SIZE_MB=100

# APIs externas
SILSO_SUNSPOT_URL=https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv
NOAA_SOLAR_URL=https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json
```

Configuración de Análisis (config.json)

```json
{
  "analysis": {
    "min_data_points": 50,
    "correlation_significance_level": 0.05,
    "bootstrap_iterations": 1000,
    "max_lag_months": 24
  },
  "predictions": {
    "default_horizon_months": 24,
    "ensemble_weights": {
      "arima": 0.3,
      "random_forest": 0.3,
      "solar_cycle": 0.4
    }
  }
}
```

---

🚀 Despliegue en Producción

Docker (Recomendado)

```bash
# Construir imagen
docker build -t heliobio-api:3.0.0 .

# Ejecutar contenedor
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --name heliobio-api \
  heliobio-api:3.0.0
```

Docker Compose

```bash
docker-compose up -d
```

Servidor con Systemd

Crear /etc/systemd/system/heliobio-api.service:

```ini
[Unit]
Description=HelioBio-API Service
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/HelioBio-API
Environment="PATH=/home/youruser/HelioBio-API/venv/bin"
ExecStart=/home/youruser/HelioBio-API/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable heliobio-api
sudo systemctl start heliobio-api
sudo systemctl status heliobio-api
```

Nginx como Proxy Inverso

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

📚 Recursos Adicionales

Sobre Alexander Chizhevsky

· 📖 Libros:
  · "Physical Factors of the Historical Process" (1924)
  · "The Terrestrial Echo of Solar Storms" (1976)
  · "The Earth in the Embrace of the Sun" (1931)
· 🔗 Enlaces:
  · Wikipedia - Alexander Chizhevsky
  · Artículo sobre Heliobiología

Fuentes de Datos

· 🌐 SILSO - Sunspot Index
· 🌐 NOAA Space Weather
· 🌐 WHO Global Health Observatory
· 🌐 NASA DONKI

Artículos Científicos Relacionados

1. Chizhevsky, A.L. (1976). "The Terrestrial Echo of Solar Storms"
2. Stoupel, E. (2002). "The effect of geomagnetic activity on cardiovascular parameters"
3. Palmer, S.J. et al. (2006). "Solar and geomagnetic activity, extremely low frequency magnetic fields and human health"

---

🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (git checkout -b feature/AmazingFeature)
3. Commit tus cambios (git commit -m 'Add some AmazingFeature')
4. Push a la rama (git push origin feature/AmazingFeature)
5. Abre un Pull Request

Guías de Contribución

· Seguir el estilo de código existente (PEP 8)
· Agregar tests para nuevas funcionalidades
· Actualizar documentación cuando sea necesario
· Commits descriptivos y claros

Reportar Bugs

Usa GitHub Issues para reportar bugs. Incluye:

· Descripción detallada del problema
· Pasos para reproducir
· Comportamiento esperado vs. actual
· Sistema operativo y versión de Python
· Logs relevantes

---

🔒 Seguridad

Si encuentras una vulnerabilidad de seguridad, por favor NO abras un issue público. En su lugar, envía un email a:

📧 ia.mechmind@gmail.com

---

📝 Licencia

Este proyecto está licenciado bajo la MIT License - ver el archivo LICENSE para más detalles.

MIT License

```
Copyright (c) 2024-2026 mechmind-dwv

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

👨‍💻 Autor

mechmind-dwv

· 📧 Email: ia.mechmind@gmail.com
· 🐙 GitHub: @mechmind-dwv
· 🔗 Repositorio: HelioBio-API

---

🙏 Agradecimientos

· Alexander Leonidovich Chizhevsky (1897-1964) - Por su trabajo pionero en Heliobiología
· SILSO - Royal Observatory of Belgium - Por datos de manchas solares
· NOAA - Por datos de clima espacial en tiempo real
· NASA - Por datos de llamaradas solares (DONKI)
· Comunidad científica - Por continuar validando las teorías heliobiológicas

---

📊 Estado del Proyecto

· ✅ Core Analysis Engine: Completado
· ✅ Data Fetching System: Completado (SILSO + NOAA + NASA)
· ✅ Prediction Models: Completado
· ✅ API Endpoints: 9 endpoints funcionando
· ✅ Tests: 27 tests automatizados
· ✅ Dashboard Web: Completado
· ✅ CI/CD: GitHub Actions configurado
· ✅ Docker: Imagen lista para producción
· 🚧 Mobile App: Planeado
· 📅 v4.0.0: Planeado para Q2 2025

---

📈 Roadmap

v3.1.0 (Próximamente)

· Más fuentes de datos (OMS, CDC)
· Exportación de reportes PDF
· Sistema de notificaciones por email
· API de webhooks

v3.2.0

· Modelos de deep learning (LSTM, Transformers)
· Sistema de usuarios y autenticación
· API GraphQL

v4.0.0

· Aplicación móvil (iOS/Android)
· Machine Learning en tiempo real
· Análisis de sentimiento en redes sociales
· Predicción multiparamétrica avanzada

---

💡 Casos de Uso

1. Investigación Científica

Validar correlaciones heliobiológicas usando datos actualizados y metodologías estadísticas modernas.

2. Salud Pública

Sistema de alerta temprana para preparación de sistemas de salud ante posibles incrementos en demanda.

3. Educación

Herramienta educativa para enseñar conceptos de heliobiología, estadística y análisis de datos.

4. Análisis Histórico

Estudiar correlaciones entre actividad solar y eventos históricos documentados.

---

🌟 Características Destacadas

🔬 Rigor Científico

· Implementación fiel a las teorías de Chizhevsky
· Validación estadística rigurosa
· Múltiples métodos de análisis

🚀 Tecnología Moderna

· API RESTful moderna con FastAPI
· Análisis asíncrono para mejor rendimiento
· Machine Learning y modelos estadísticos avanzados

📊 Datos Oficiales

· Conexión directa con fuentes oficiales (NOAA, SILSO, NASA)
· Actualización automática de datos
· Sistema de cache inteligente

🛡️ Código Abierto

· Totalmente open source
· Bien documentado
· Fácil de extender

---

📞 Soporte

¿Necesitas ayuda? Contacta a través de:

· 📧 Email: ia.mechmind@gmail.com
· 🐛 Issues: GitHub Issues
· 💬 Discussions: GitHub Discussions

---

⭐ Star History

Si este proyecto te resulta útil, por favor considera darle una ⭐ en GitHub!

---

<div align="center">

Hecho con ❤️ por mechmind-dwv

Basado en el trabajo pionero de Alexander Leonidovich Chizhevsky

"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"

🔝 Volver arriba

</div>

---

## 📈 Roadmap

### v3.0.0 ✅ Completado
- [x] API RESTful con 9 endpoints
- [x] Datos SILSO reales (Ciclo Solar 25, SSN=216)
- [x] Dashboard HTML interactivo
- [x] 27 tests automatizados
- [x] Docker + CI/CD

### v3.1.0 ✅ Completado
- [x] Más fuentes de datos (OMS, CDC)
- [x] Exportación de reportes PDF (Solar + Correlación)
- [x] Sistema de notificaciones por email
- [x] API de webhooks

### v3.2.0 ✅ Completado
- [x] Modelos de deep learning (LSTM)
- [x] Sistema de usuarios y autenticación JWT
- [x] API GraphQL con Strawberry

### v4.0.0 🔜 En planificación
- [ ] Aplicación móvil (iOS/Android)
- [ ] Machine Learning en tiempo real
- [ ] Análisis de sentimiento en redes sociales
- [ ] Predicción multiparamétrica avanzada
- [ ] Integración con IoT y wearables

