---
title: "HelioBio-API"
description: "Sistema Avanzado de Análisis Heliobiológico basado en Alexander Chizhevsky"
---

# ☀️ HelioBio-API

**Sistema Avanzado de Análisis Heliobiológico**

Basado en los estudios pioneros de **Alexander Leonidovich Chizhevsky** (1897-1964), fundador de la Heliobiología.

---

## 🚀 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página de inicio |
| `/dashboard` | GET | Dashboard interactivo |
| `/solar/activity` | GET | Actividad solar (SILSO/NOAA) |
| `/health/events` | GET | Eventos epidemiológicos históricos |
| `/analysis/correlate` | GET | Análisis de correlación solar-biológica |
| `/alerts/current` | GET | Alertas de salud basadas en actividad solar |
| `/chizhevsky/knowledge` | GET | Base de conocimiento de Chizhevsky |
| `/docs` | GET | Documentación Swagger UI |
| `/redoc` | GET | Documentación ReDoc |

---

## 📊 Dashboard

Accede al dashboard interactivo en: `/dashboard`

- Monitoreo de actividad solar
- Visualización de datos históricos
- Análisis predictivo de ciclos solares

---

## 🔬 Base Científica

### Alexander Chizhevsky (1897-1964)

- Padre de la **Heliobiología**
- Descubrió correlaciones entre actividad solar y eventos terrestres
- Documentó ciclos de 11 años en pandemias, revoluciones y guerras

### Principios Fundamentales

1. **Conexión Solar-Terrestre**: La vida es influenciada por la actividad solar
2. **Ciclos de 11 años**: Correlacionan con eventos históricos y biológicos
3. **Sincronización Biosférica**: Los organismos responden a ritmos cósmicos

---

## 🛠️ Instalación

```bash
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docker

```bash
docker build -t heliobio-api .
docker run -p 8000:8000 heliobio-api
```

---

🌐 Documentación API

· Swagger UI: /docs
· ReDoc: /redoc

---

🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (git checkout -b feature/AmazingFeature)
3. Commit (git commit -m 'Add AmazingFeature')
4. Push (git push origin feature/AmazingFeature)
5. Abre un Pull Request

---

📜 Licencia

MIT License - LICENSE

---

"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol" — Alexander Chizhevsky
