# 🌞 HelioBio-API v8.0.0 "Cosmic Odyssey" 🚀

**Sistema Avanzado de Análisis Heliobiológico**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-27%2F27-success.svg)]()
[![Version](https://img.shields.io/badge/Version-8.0.0-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**44 endpoints · 27 tests · 6 fuentes de datos · 8 versiones**

Sistema científico basado en las investigaciones pioneras de **Alexander Leonidovich Chizhevsky** (1897-1964), fundador de la Heliobiología.

> *"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"* — A.L. Chizhevsky

---

## 📋 Tabla de Contenidos

- [El Viaje](#-el-viaje-cósmico)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Endpoints](#-endpoints-principales)
- [Teoría Científica](#-teoría-científica)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Desarrollo](#-desarrollo)
- [Testing](#-testing)
- [Despliegue](#-despliegue)
- [Contribuir](#-contribuir)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

---

## 🌌 El Viaje Cósmico

| Versión | Tema | Endpoints | Estado |
|---------|------|-----------|--------|
| v3.0.0 | ☀️ Fundación Solar (SILSO real, Dashboard) | 9 | ✅ |
| v3.1.0 | 📊 Expansión (PDFs, Webhooks, OMS, CDC) | 17 | ✅ |
| v3.2.0 | 🧠 Deep Learning + Auth JWT + GraphQL | 23 | ✅ |
| v4.0.0 | 🌐 Android + WebSocket + Sentimiento + IoT | 31 | ✅ |
| v5.0.0 | ⚛️ Ionismo Digital + Resonancia Schumann | 34 | ✅ |
| v6.0.0 | 📜 Historiometría + Índice Excitabilidad Social | 37 | ✅ |
| v7.0.0 | 🧬 DePIN Ciudadana + Epigenética + Gemelo Digital | 41 | ✅ |
| v8.0.0 | 🚀 Especie Multiplanetaria + GCR + Exoplanetas | **44** | ✅ |

---

## 🚀 Instalación

### Requisitos
- **Python**: 3.10+ | **RAM**: 4GB+ | **Disco**: 2GB
- **SO**: Linux, macOS, Termux (Android)

### Instalación Rápida (Linux/macOS)
```bash
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Instalación en Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python python-pip rust binutils cmake build-essential git
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

💻 Uso Rápido

```bash
# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

URL Descripción
http://localhost:8000 API
http://localhost:8000/dashboard Panel interactivo
http://localhost:8000/docs Swagger UI
http://localhost:8000/graphql GraphQL

Ejemplos curl

```bash
# Actividad solar real
curl "http://localhost:8000/solar/activity?start_date=2024-01-01&end_date=2024-12-31"

# Análisis de correlación
curl "http://localhost:8000/analysis/correlate?years_before=15&years_after=5"

# Resonancia Schumann
curl http://localhost:8000/ionosphere/schumann

# Índice de Excitabilidad Social (Chizhevsky)
curl http://localhost:8000/historiometry/sei

# Misión a Marte
curl "http://localhost:8000/space/mission-briefing?destination=Mars&crew_size=6"

# Predicción Deep Learning
curl "http://localhost:8000/predict/deep-learning?months_ahead=12"
```

---

📡 Endpoints Principales

Categoría Endpoints
☀️ Solar /solar/activity, /space-weather, /solar-cycles
🏥 Salud /health/events, /who/pandemics, /cdc/influenza
🔬 Análisis /analysis/correlate, /predict/deep-learning, /predict/multi-parametric
⚛️ Ionismo /ionosphere/schumann, /ionosphere/tec, /ionosphere/bio-effects
📜 Historiometría /historiometry/sei, /historiometry/events, /historiometry/analysis
🧬 DePIN /depin/network-status, /depin/hyperlocal-alert
🚀 Espacio /space/mission-briefing, /space/galactic-cosmic-rays, /space/exoplanet-habitability
📄 Reportes /report/solar, /report/correlation
🔔 Notificaciones /notify/subscribe, /notify/test
🔗 Webhooks /webhooks, /webhooks/register, /webhooks/test
🔐 Auth /auth/login, /auth/me, /admin/stats
📊 GraphQL /graphql
🎨 UI /dashboard, /docs, /redoc

Total: 44 endpoints

---

🔬 Teoría Científica

Alexander Leonidovich Chizhevsky (1897-1964)

Científico ruso pionero en Heliobiología y Cosmobiología.

"Alexander Chizhevsky, el hombre que miró al sol y vio el pulso de la humanidad, fue nuestro Leonardo. Su estudio principal no era solo la geofísica o la historia, sino la sintaxis oculta del cosmos."

Principios Fundamentales

1. Conexión Solar-Terrestre: Toda la vida es influenciada por la actividad solar
2. Ciclos de 11 años: Correlacionan con pandemias, revoluciones y guerras
3. Teoría del Ionismo: Los iones negativos atmosféricos, modulados por el sol, afectan la fisiología
4. Historiometría: Los máximos solares coinciden con picos de excitabilidad social

Fases del Ciclo Solar

Fase Duración Características
Mínimo 3 años Apatía social, menor actividad biológica
Ascendente 2 años Reorganización, activación inmunológica
Máximo 3 años Máxima excitabilidad, revoluciones, pandemias
Declinante 3 años Estabilización, normalización

---

📁 Estructura del Proyecto

```
HelioBio-API/
├── app/
│   ├── main.py                    # Punto de entrada
│   ├── dashboard.py               # Panel HTML interactivo
│   ├── solar_fetcher.py           # Datos SILSO reales
│   ├── pandemic_data.py           # Dataset epidemiológico
│   ├── space_weather.py           # NOAA tiempo real
│   ├── solar_cycles.py            # 25 ciclos solares
│   ├── ionosphere.py              # Resonancia Schumann + TEC
│   ├── historiometry.py           # Índice Excitabilidad Social
│   ├── depin_network.py           # Red Ciudadana + Epigenética
│   ├── space_biology.py           # Biología Espacial
│   ├── deep_learning.py           # LSTM + Transformer
│   ├── sentiment_analyzer.py      # Análisis de sentimiento
│   ├── auth.py                    # Autenticación JWT
│   ├── graphql_api.py             # API GraphQL
│   ├── report_generator.py        # PDFs
│   ├── email_notifier.py          # Notificaciones email
│   ├── webhooks.py                # Sistema de webhooks
│   ├── who_data.py                # Datos OMS
│   ├── cdc_data.py                # Datos CDC
│   ├── websocket_handler.py       # WebSocket streaming
│   ├── config/                    # Configuración
│   ├── models/                    # Modelos de datos
│   ├── core/                      # Lógica de negocio
│   └── utils/                     # Utilidades
├── tests/                         # 27 tests automatizados
├── docs/                          # Documentación
├── scripts/                       # Scripts de utilidad
├── .github/                       # CI/CD + Dependabot
├── Dockerfile                     # Imagen Docker
├── docker-compose.yml
└── requirements.txt
```

---

🧪 Testing

27 tests automatizados - 100% pasando

```bash
python -m pytest tests/ -v
python -m pytest tests/ -v --cov=app --cov-report=term
```

---

🚀 Despliegue

Docker

```bash
docker build -t heliobio-api:8.0.0 .
docker run -d -p 8000:8000 --name heliobio-api heliobio-api:8.0.0
```

Docker Compose

```bash
docker-compose up -d
```

Systemd

```bash
sudo systemctl enable heliobio-api
sudo systemctl start heliobio-api
```

---

📈 Roadmap

✅ Completado

· v3.0.0: API Solar, SILSO real, Dashboard, Tests
· v3.1.0: PDFs, Webhooks, Email, OMS, CDC
· v3.2.0: Deep Learning, Auth JWT, GraphQL
· v4.0.0: WebSocket, Sentimiento, IoT, Android
· v5.0.0: Resonancia Schumann, Ionismo Digital
· v6.0.0: Historiometría, Índice Excitabilidad Social
· v7.0.0: DePIN, Epigenética, Gemelo Digital
· v8.0.0: Especie Multiplanetaria, GCR, Exoplanetas

🔜 Futuro

· v9.0.0: Computación Cuántica + Blockchain + TSDB

---

🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama (git checkout -b feature/AmazingFeature)
3. Commit (git commit -m 'Add AmazingFeature')
4. Push (git push origin feature/AmazingFeature)
5. Abre un Pull Request

---

🔒 Seguridad

Reporta vulnerabilidades a: ia.mechmind@gmail.com

---

📝 Licencia

MIT License - LICENSE

---

👨‍💻 Autor

mechmind-dwv

· 📧 ia.mechmind@gmail.com
· 🐙 @mechmind-dwv

---

🙏 Agradecimientos

· Alexander Leonidovich Chizhevsky (1897-1964)
· SILSO - Royal Observatory of Belgium
· NOAA - Space Weather Prediction Center
· NASA - DONKI
· OMS/WHO - Global Health Observatory
· CDC - Centers for Disease Control

---

<div align="center">

Hecho con ❤️ por mechmind-dwv

"El campo magnético terrestre es el sistema nervioso del planeta. La heliosfera es nuestro escudo." — A.L. Chizhevsky

🔝 Volver arriba

</div>
