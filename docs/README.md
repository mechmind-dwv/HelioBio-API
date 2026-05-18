# 🌞 HelioBio-API v3.0.0

**Sistema Avanzado de Análisis Heliobiológico**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

Sistema científico basado en las investigaciones pioneras de **Alexander Leonidovich Chizhevsky** (1897-1964), fundador de la Heliobiología, que estudió las correlaciones entre la actividad solar y los procesos biológicos terrestres.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Teoría Científica](#-teoría-científica)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Documentación de la API](#-documentación-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Desarrollo](#-desarrollo)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Autor](#-autor)

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

- **Sistema Operativo**: Linux Mint 22.1+ / Ubuntu 22.04+ / Debian 11+
- **Python**: 3.8 o superior
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
- ✅ Verifica el sistema operativo
- ✅ Instala dependencias del sistema
- ✅ Crea entorno virtual Python
- ✅ Instala dependencias de Python
- ✅ Crea estructura de directorios
- ✅ Configura archivos de configuración

### Instalación Manual

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

---

## 💻 Uso Rápido

### Iniciar el Servidor

```bash
# Método 1: Script de inicio
./start.sh

# Método 2: Comando directo
source venv/bin/activate
cd app && python main.py

# Método 3: Uvicorn directo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

### Ejemplos de Uso

#### Obtener Actividad Solar Actual

```bash
curl http://localhost:8000/solar/activity
```

#### Obtener Datos Históricos

```bash
curl "http://localhost:8000/solar/historical?start_year=2000&end_year=2023"
```

#### Análisis de Correlación

```bash
curl "http://localhost:8000/analysis/correlate?start_year=2000&end_year=2023"
```

#### Predicción Solar

```bash
curl "http://localhost:8000/predictions/solar?months_ahead=24"
```

#### Predicción de Eventos Biológicos

```bash
curl "http://localhost:8000/predictions/biological?months_ahead=24"
```

---

## 📖 Documentación de la API

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página de inicio |
| `/health` | GET | Estado del sistema |
| `/solar/activity` | GET | Actividad solar actual |
| `/solar/historical` | GET | Datos históricos de manchas solares |
| `/solar/cycle/current` | GET | Información del ciclo solar actual |
| `/health/events` | GET | Eventos epidemiológicos históricos |
| `/analysis/correlate` | GET | Análisis de correlación completo |
| `/predictions/solar` | GET | Predicción de actividad solar |
| `/predictions/biological` | GET | Predicción de riesgo biológico |
| `/alerts/current` | GET | Alertas de salud actuales |
| `/chizhevsky` | GET | Información sobre Chizhevsky |
| `/chizhevsky/knowledge` | GET | Base de conocimiento completa |

### Documentación Detallada

Accede a la documentación interactiva completa en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Estructura del Proyecto

```
HelioBio-API/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada principal
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
│   └── backup_db.py               # Backup de base de datos
├── tests/
│   ├── test_api/                  # Tests de API
│   ├── test_core/                 # Tests de módulos core
│   └── test_utils/                # Tests de utilidades
├── static/                        # Archivos estáticos
├── backups/                       # Backups del sistema
├── .env                           # Variables de entorno
├── .env.example                   # Ejemplo de configuración
├── .gitignore                     # Archivos ignorados por Git
├── config.json                    # Configuración JSON
├── requirements.txt               # Dependencias Python
├── README.md                      # Este archivo
├── LICENSE                        # Licencia MIT
└── start.sh                       # Script de inicio rápido
```

---

## 🛠️ Desarrollo

### Configurar Entorno de Desarrollo

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-cov

# Configurar pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_core/test_analyzer.py -v

# Tests de integración
pytest tests/test_api/ -v
```

### Formato de Código

```bash
# Formatear código con Black
black app/ tests/

# Verificar con Flake8
flake8 app/ tests/

# Type checking con MyPy
mypy app/
```

### Agregar Nuevos Módulos

1. Crear el archivo del módulo en el directorio apropiado
2. Agregar tests correspondientes en `tests/`
3. Actualizar documentación en `docs/`
4. Ejecutar tests para verificar

---

## 🧪 Testing

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas
├── test_api/
│   ├── test_solar_endpoints.py
│   ├── test_health_endpoints.py
│   └── test_analysis_endpoints.py
├── test_core/
│   ├── test_data_fetcher.py
│   ├── test_analyzer.py
│   ├── test_predictor.py
│   └── test_chizhevsky_kb.py
└── test_utils/
    ├── test_statistics.py
    └── test_visualizations.py
```

### Ejemplo de Test

```python
import pytest
from app.core.analyzer import ChizhevskAnalyzer

@pytest.mark.asyncio
async def test_correlation_analysis():
    analyzer = ChizhevskAnalyzer()
    
    # Datos de prueba
    solar_data = create_mock_solar_data()
    biological_data = create_mock_biological_data()
    
    # Ejecutar análisis
    results = analyzer.comprehensive_correlation_analysis(
        solar_data, biological_data, []
    )
    
    # Verificaciones
    assert 'correlations' in results
    assert 'chizhevsky_assessment' in results
    assert results['correlations']['pearson']['p_value'] < 1.0
```

---

## 📊 Visualizaciones

El sistema genera automáticamente:

- 📈 **Gráficos de series temporales** de actividad solar
- 🔗 **Diagramas de correlación** entre variables
- 📊 **Espectrogramas** de análisis de frecuencias
- 🗺️ **Mapas de calor** de coherencia wavelet
- 📉 **Predicciones con intervalos de confianza**

Las visualizaciones se generan en formato PNG/SVG y se pueden obtener vía API.

---

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

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

### Configuración de Análisis (config.json)

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

## 🚀 Despliegue en Producción

### Docker (Recomendado)

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

### Servidor con Systemd

Crear `/etc/systemd/system/heliobio-api.service`:

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

### Nginx como Proxy Inverso

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

## 📚 Recursos Adicionales

### Sobre Alexander Chizhevsky

- 📖 **Libros**:
  - "Physical Factors of the Historical Process" (1924)
  - "The Terrestrial Echo of Solar Storms" (1976)
  - "The Earth in the Embrace of the Sun" (1931)

- 🔗 **Enlaces**:
  - [Wikipedia - Alexander Chizhevsky](https://en.wikipedia.org/wiki/Alexander_Chizhevsky)
  - [Artículo sobre Heliobiología](https://www.nature.com/articles/scientificamerican0238-14)

### Fuentes de Datos

- 🌐 [SILSO - Sunspot Index](https://www.sidc.be/silso/)
- 🌐 [NOAA Space Weather](https://www.swpc.noaa.gov/)
- 🌐 [WHO Global Health Observatory](https://www.who.int/data/gho)

### Artículos Científicos Relacionados

1. Chizhevsky, A.L. (1976). "The Terrestrial Echo of Solar Storms"
2. Stoupel, E. (2002). "The effect of geomagnetic activity on cardiovascular parameters"
3. Palmer, S.J. et al. (2006). "Solar and geomagnetic activity, extremely low frequency magnetic fields and human health"

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

### Guías de Contribución

- Seguir el estilo de código existente (PEP 8)
- Agregar tests para nuevas funcionalidades
- Actualizar documentación cuando sea necesario
- Commits descriptivos y claros

### Reportar Bugs

Usa GitHub Issues para reportar bugs. Incluye:
- Descripción detallada del problema
- Pasos para reproducir
- Comportamiento esperado vs. actual
- Sistema operativo y versión de Python
- Logs relevantes

---

## 🔒 Seguridad

Si encuentras una vulnerabilidad de seguridad, por favor **NO** abras un issue público. En su lugar, envía un email a:

📧 **ia.mechmind@gmail.com**

---

## 📝 Licencia

Este proyecto está licenciado bajo la **MIT License** - ver el archivo [LICENSE](LICENSE) para más detalles.

### MIT License

```
Copyright (c) 2024 mechmind-dwv

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

## 👨‍💻 Autor

**mechmind-dwv**

- 📧 Email: [ia.mechmind@gmail.com](mailto:ia.mechmind@gmail.com)
- 🐙 GitHub: [@mechmind-dwv](https://github.com/mechmind-dwv)
- 🔗 Repositorio: [HelioBio-API](https://github.com/mechmind-dwv/HelioBio-API)

---

## 🙏 Agradecimientos

- **Alexander Leonidovich Chizhevsky** (1897-1964) - Por su trabajo pionero en Heliobiología
- **SILSO** - Royal Observatory of Belgium - Por datos de manchas solares
- **NOAA** - Por datos de clima espacial en tiempo real
- **Comunidad científica** - Por continuar validando las teorías heliobiológicas

---

## 📊 Estado del Proyecto

- ✅ **Core Analysis Engine**: Completado
- ✅ **Data Fetching System**: Completado
- ✅ **Prediction Models**: Completado
- ✅ **API Endpoints**: Completado
- 🚧 **Dashboard Web**: En desarrollo
- 🚧 **Mobile App**: Planeado
- 📅 **v4.0.0**: Planeado para Q2 2025

---

## 📈 Roadmap

### v3.1.0 (Q4 2024)
- [ ] Dashboard web interactivo
- [ ] Exportación de reportes PDF
- [ ] Sistema de notificaciones por email
- [ ] API de webhooks

### v3.2.0 (Q1 2025)
- [ ] Integración con más fuentes de datos
- [ ] Modelos de deep learning (LSTM, Transformers)
- [ ] Sistema de usuarios y autenticación
- [ ] API GraphQL

### v4.0.0 (Q2 2025)
- [ ] Aplicación móvil (iOS/Android)
- [ ] Machine Learning en tiempo real
- [ ] Análisis de sentimiento en redes sociales
- [ ] Predicción multiparamétrica avanzada

---

## 💡 Casos de Uso

### 1. Investigación Científica
Validar correlaciones heliobiológicas usando datos actualizados y metodologías estadísticas modernas.

### 2. Salud Pública
Sistema de alerta temprana para preparación de sistemas de salud ante posibles incrementos en demanda.

### 3. Educación
Herramienta educativa para enseñar conceptos de heliobiología, estadística y análisis de datos.

### 4. Análisis Histórico
Estudiar correlaciones entre actividad solar y eventos históricos documentados.

---

## 🌟 Características Destacadas

### 🔬 Rigor Científico
- Implementación fiel a las teorías de Chizhevsky
- Validación estadística rigurosa
- Múltiples métodos de análisis

### 🚀 Tecnología Moderna
- API RESTful moderna con FastAPI
- Análisis asíncrono para mejor rendimiento
- Machine Learning y modelos estadísticos avanzados

### 📊 Datos Oficiales
- Conexión directa con fuentes oficiales (NOAA, SILSO)
- Actualización automática de datos
- Sistema de cache inteligente

### 🛡️ Código Abierto
- Totalmente open source
- Bien documentado
- Fácil de extender

---

## 📞 Soporte

¿Necesitas ayuda? Contacta a través de:

- 📧 **Email**: ia.mechmind@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/mechmind-dwv/HelioBio-API/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mechmind-dwv/HelioBio-API/discussions)

---

## ⭐ Star History

Si este proyecto te resulta útil, por favor considera darle una ⭐ en GitHub!

---

<div align="center">

**Hecho con ❤️ por mechmind-dwv**

*Basado en el trabajo pionero de Alexander Leonidovich Chizhevsky*

*"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"*

[🔝 Volver arriba](#-heliobio-api-v300)

</div>
