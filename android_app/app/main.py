"""
HelioBio-API - Aplicación Android
Servidor FastAPI embebido para análisis heliobiológico
"""
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="HelioBio-API",
    description="Sistema Avanzado de Análisis Heliobiológico - Alexander Chizhevsky",
    version="3.0.0"
)

DASHBOARD = """<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>☀️ HelioBio-API</title>
<style>body{font-family:sans-serif;background:#0a1628;color:#e0e0e0;padding:20px;text-align:center}
h1{color:#ffd700}a{color:#87ceeb;display:block;padding:10px;margin:5px;background:#1a2a4a;text-decoration:none;border-radius:8px}
.status{color:#2d7d46}</style></head>
<body><h1>☀️ HelioBio-API</h1><p class="status">🟢 Servidor Activo</p>
<a href="/solar/activity">📊 Actividad Solar</a>
<a href="/health/events">🏥 Eventos de Salud</a>
<a href="/analysis/correlate">🔬 Análisis de Correlación</a>
<a href="/alerts/current">⚠️ Alertas</a>
<a href="/chizhevsky/knowledge">📚 Base de Conocimiento</a>
<a href="/docs">📖 Documentación API</a>
<p>"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"<br>- Alexander Chizhevsky</p></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return DASHBOARD

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
