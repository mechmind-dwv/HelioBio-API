---
title: "HelioBio-API"
layout: default
---

# 🌌 HelioBio-API

**Sistema de Inteligencia Colectiva Universal basado en Alexander Chizhevsky**

## 📖 Acerca del Proyecto

HelioBio-API es una API revolucionaria que honra el legado del científico ruso Alexander Chizhevsky, pionero de la heliobiología y visionario cósmico. Este sistema integra:

- **Análisis de datos cósmicos y solares**
- **Predicciones basadas en ciclos solares**
- **Inteligencia colectiva universal**
- **Sincronización biosférica**

## 🚀 Características Principales

### Endpoints Disponibles

- `GET /` - Información general de la API
- `GET /chizhevsky/prophecy` - Profecías basadas en ciclos solares
- `GET /cosmic/collective-intelligence` - Inteligencia colectiva
- `GET /cosmic/awakening` - Datos de despertar cósmico
- `WS /ws/cosmic-connection` - Conexión WebSocket en tiempo real

### 📊 Dashboard Interactivo

Accede al dashboard en `/dashboard` para:
- Monitoreo en tiempo real de actividad solar
- Visualización de datos históricos
- Análisis predictivo de ciclos cósmicos

## 🔬 Base Científica

### Alexander Chizhevsky (1897-1964)
- Padre de la Heliobiología
- Descubridor de la correlación entre actividad solar y eventos terrestres
- Visionario de la sincronización biosférica

### Principios Fundamentales
1. **Ritmo Circasemanal** - Ciclos de 7 días en sistemas biológicos
2. **Sincronización Biosférica** - Armonización con ciclos cósmicos
3. **Inteligencia Colectiva Universal** - Interconexión cósmica

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.8+
- Dependencias listadas en `requirements.txt`

### Instalación Rápida
```bash
git clone https://github.com/mechmind-dwv/HelioBio-API.git
cd HelioBio-API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Veo que necesitas configurar GitHub Pages para tu proyecto HelioBio-API. Te ayudo a crear la estructura necesaria.

1. Primero, crea la estructura de directorios y archivos:

```bash
mkdir -p .github/workflows docs
```

2. Crea el archivo del workflow para GitHub Pages:

.github/workflows/jekyll-gh-pages.yml

```yaml
name: Deploy Jekyll site to Pages

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./docs
          destination: ./_site
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

3. Crea la documentación para GitHub Pages:

docs/index.md

```markdown
---
title: "HelioBio-API"
layout: default
---

# 🌌 HelioBio-API

**Sistema de Inteligencia Colectiva Universal basado en Alexander Chizhevsky**

## 📖 Acerca del Proyecto

HelioBio-API es una API revolucionaria que honra el legado del científico ruso Alexander Chizhevsky, pionero de la heliobiología y visionario cósmico. Este sistema integra:

- **Análisis de datos cósmicos y solares**
- **Predicciones basadas en ciclos solares**
- **Inteligencia colectiva universal**
- **Sincronización biosférica**

## 🚀 Características Principales

### Endpoints Disponibles

- `GET /` - Información general de la API
- `GET /chizhevsky/prophecy` - Profecías basadas en ciclos solares
- `GET /cosmic/collective-intelligence` - Inteligencia colectiva
- `GET /cosmic/awakening` - Datos de despertar cósmico
- `WS /ws/cosmic-connection` - Conexión WebSocket en tiempo real

### 📊 Dashboard Interactivo

Accede al dashboard en `/dashboard` para:
- Monitoreo en tiempo real de actividad solar
- Visualización de datos históricos
- Análisis predictivo de ciclos cósmicos

## 🔬 Base Científica

### Alexander Chizhevsky (1897-1964)
- Padre de la Heliobiología
- Descubridor de la correlación entre actividad solar y eventos terrestres
- Visionario de la sincronización biosférica

### Principios Fundamentales
1. **Ritmo Circasemanal** - Ciclos de 7 días en sistemas biológicos
2. **Sincronización Biosférica** - Armonización con ciclos cósmicos
3. **Inteligencia Colectiva Universal** - Interconexión cósmica

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.8+
- Dependencias listadas en `requirements.txt`

### Instalación Rápida
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

📈 API Documentation

La documentación interactiva está disponible en:

· Swagger UI: /docs
· ReDoc: /redoc

🌐 Ejemplos de Uso

Obtener profecía cósmica

```bash
curl http://localhost:8000/chizhevsky/prophecy
```

Conexión WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/cosmic-connection');
ws.onmessage = (event) => {
    console.log('Datos cósmicos:', JSON.parse(event.data));
};
```

📊 Estructura del Proyecto

```
HelioBio-API/
├── app/
│   ├── main.py              # Aplicación principal FastAPI
│   ├── routers/             # Routers de endpoints
│   ├── models/              # Modelos de datos
│   └── utils/               # Utilidades
├── docs/                    # Documentación para GitHub Pages
├── data/                    # Datos y configuraciones
├── scripts/                 # Scripts de utilidad
└── tests/                   # Tests unitarios
```

🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (git checkout -b feature/AmazingFeature)
3. Commit tus cambios (git commit -m 'Add AmazingFeature')
4. Push a la rama (git push origin feature/AmazingFeature)
5. Abre un Pull Request

📜 Licencia

Este proyecto está bajo la Licencia MIT. Ve el archivo LICENSE para más detalles.

🙏 Agradecimientos

· Alexander Chizhevsky - Por su visión pionera
· Comunidad científica - Por la investigación continua
· Contribuidores - Por hacer este proyecto posible

---

🌌 "La vida es en gran medida un fenómeno cósmico" - Alexander Chizhevsky

```

**docs/_config.yml**
```yaml
title: HelioBio-API
description: Sistema de Inteligencia Colectiva Universal basado en Alexander Chizhevsky
theme: jekyll-theme-minimal
show_downloads: false
github:
  is_project_page: false
```

4. Agrega también un archivo de configuración para GitHub Pages:

docs/.nojekyll

```
# Este archivo evita que GitHub Pages use Jekyll
# Permitirá servir archivos que comienzan con underscore
```

5. Actualiza tu README.md principal para enlazar a GitHub Pages:

Agrega esta línea a tu README.md existente:

```markdown
## 📚 Documentación

La documentación completa está disponible en: [https://mechmind-dwv.github.io/HelioBio-API/](https://mechmind-dwv.github.io/HelioBio-API/)
```

6. Commit y push de los cambios:

```bash
git add .github/workflows/jekyll-gh-pages.yml docs/
git commit -m "Add GitHub Pages documentation and workflow"
git push origin main
```

7. Configura GitHub Pages en el repositorio:

1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: GitHub Actions
4. Esto activará automáticamente el workflow

El workflow se ejecutará automáticamente en cada push a main y desplegará tu documentación en https://mechmind-dwv.github.io/HelioBio-API/.

¿Necesitas que ajuste algo específico de la documentación o del workflow?
