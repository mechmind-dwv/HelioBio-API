"""Dashboard HTML para HelioBio-API"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☀️ HelioBio-API Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 100%); color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { text-align: center; padding: 40px 0; }
        h1 { font-size: 2.5em; color: #ffd700; text-shadow: 0 0 20px rgba(255,215,0,0.5); }
        h2 { color: #87ceeb; margin-top: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
        .card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s, box-shadow 0.3s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .card h3 { color: #ffd700; margin-bottom: 10px; }
        .card p { color: #aaa; margin-bottom: 15px; }
        .btn { display: inline-block; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; transition: background 0.3s; }
        .btn-primary { background: #00509d; color: white; }
        .btn-primary:hover { background: #003f7d; }
        .btn-success { background: #2d7d46; color: white; }
        .btn-success:hover { background: #1e5c32; }
        .btn-warning { background: #b8860b; color: white; }
        .btn-warning:hover { background: #8b6508; }
        .status { text-align: center; padding: 15px; border-radius: 10px; margin: 20px 0; }
        .status.online { background: rgba(45,125,70,0.3); border: 1px solid #2d7d46; }
        .quote { font-style: italic; text-align: center; color: #aaa; margin: 30px 0; padding: 20px; border-left: 3px solid #ffd700; }
        footer { text-align: center; padding: 20px; color: #666; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>☀️ HelioBio-API</h1>
            <h2>Sistema Avanzado de Análisis Heliobiológico</h2>
            <p>Basado en los estudios pioneros de Alexander Leonidovich Chizhevsky (1897-1964)</p>
        </header>

        <div class="status online">
            🟢 API Operativa | Versión 3.0.0
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 Actividad Solar</h3>
                <p>Consulta los datos actuales de manchas solares y actividad solar.</p>
                <a href="/solar/activity" class="btn btn-primary">Ver Datos</a>
                <a href="/docs#/default/get_solar_activity_solar_activity_get" class="btn btn-primary" style="margin-left:10px">API Doc</a>
            </div>

            <div class="card">
                <h3>🏥 Eventos de Salud</h3>
                <p>Base de datos histórica de pandemias y su correlación solar.</p>
                <a href="/health/events" class="btn btn-success">Ver Eventos</a>
            </div>

            <div class="card">
                <h3>🔬 Análisis de Correlación</h3>
                <p>Análisis estadístico avanzado entre actividad solar y eventos.</p>
                <a href="/analysis/correlate" class="btn btn-warning">Ejecutar Análisis</a>
            </div>

            <div class="card">
                <h3>⚠️ Alertas Actuales</h3>
                <p>Sistema de alertas tempranas basado en actividad solar.</p>
                <a href="/alerts/current" class="btn btn-primary">Ver Alertas</a>
            </div>

            <div class="card">
                <h3>📚 Base de Conocimiento</h3>
                <p>Teorías y descubrimientos de Alexander Chizhevsky.</p>
                <a href="/chizhevsky/knowledge" class="btn btn-success">Explorar</a>
            </div>

            <div class="card">
                <h3>📖 Documentación API</h3>
                <p>Documentación interactiva Swagger UI completa.</p>
                <a href="/docs" class="btn btn-warning">Swagger UI</a>
                <a href="/redoc" class="btn btn-warning" style="margin-left:10px">ReDoc</a>
            </div>
        </div>

        <div class="quote">
            "Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"<br>
            <strong>— Alexander Leonidovich Chizhevsky</strong>
        </div>

        <footer>
            <p>© 2024-2026 mechmind-dwv | HelioBio-API v3.0.0 | Licencia MIT</p>
            <p style="margin-top:10px">
                <a href="https://github.com/mechmind-dwv/HelioBio-API" style="color:#87ceeb">GitHub</a> |
                <a href="mailto:ia.mechmind@gmail.com" style="color:#87ceeb">Contacto</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD_HTML
