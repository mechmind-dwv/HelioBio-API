"""Dashboard interactivo profesional para HelioBio-API"""
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg: #0a1628;
            --card: #112240;
            --accent: #ffd700;
            --blue: #58c7e9;
            --green: #2d7d46;
            --red: #d73a4a;
            --text: #e0e0e0;
            --muted: #8892b0;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }
        header {
            background: linear-gradient(135deg, #002848 0%, #00509d 100%);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--accent);
        }
        header h1 { font-size: 1.8em; color: var(--accent); }
        header .status { display: flex; gap: 15px; align-items: center; }
        .badge {
            padding: 6px 14px; border-radius: 20px; font-size: 0.85em; font-weight: bold;
        }
        .badge-online { background: var(--green); color: white; }
        .badge-version { background: var(--card); color: var(--accent); border: 1px solid var(--accent); }
        .container { max-width: 1400px; margin: 0 auto; padding: 25px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .card {
            background: var(--card);
            border-radius: 15px;
            padding: 22px;
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
        .card h3 { color: var(--accent); margin-bottom: 12px; font-size: 1.1em; }
        .stat-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .stat-label { color: var(--muted); }
        .stat-value { font-weight: bold; font-size: 1.1em; }
        .stat-high { color: var(--red); }
        .stat-moderate { color: var(--accent); }
        .stat-low { color: var(--green); }
        .chart-container { position: relative; height: 250px; width: 100%; }
        canvas { width: 100% !important; height: 100% !important; }
        .endpoint-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .endpoint-btn {
            display: block; padding: 12px; text-align: center;
            background: var(--bg); color: var(--blue); text-decoration: none;
            border-radius: 10px; border: 1px solid var(--blue);
            transition: all 0.2s; font-size: 0.9em;
        }
        .endpoint-btn:hover { background: var(--blue); color: var(--bg); }
        .quote {
            text-align: center; padding: 25px; font-style: italic; color: var(--muted);
            border-left: 3px solid var(--accent); margin: 25px 0;
        }
        footer { text-align: center; padding: 20px; color: var(--muted); font-size: 0.85em; }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .alert-card {
            border-left: 4px solid var(--accent);
            animation: pulse 3s infinite;
        }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>☀️ HelioBio-API</h1>
            <span style="color:var(--muted);font-size:0.9em;">Sistema Avanzado de Análisis Heliobiológico</span>
        </div>
        <div class="status">
            <span class="badge badge-online pulse">🟢 Operativa</span>
            <span class="badge badge-version">v3.1.0</span>
        </div>
    </header>

    <div class="container">
        <!-- KPIs -->
        <div class="grid" id="kpi-grid">
            <div class="card">
                <h3>📊 Actividad Solar</h3>
                <div class="stat-row"><span class="stat-label">SSN Actual</span><span class="stat-value" id="ssn-value">--</span></div>
                <div class="stat-row"><span class="stat-label">Clasificación</span><span class="stat-value" id="ssn-class">--</span></div>
                <div class="stat-row"><span class="stat-label">Flujo Solar</span><span class="stat-value" id="flare-value">--</span></div>
            </div>
            <div class="card">
                <h3>🔬 Correlación</h3>
                <div class="stat-row"><span class="stat-label">Pearson</span><span class="stat-value" id="corr-value">--</span></div>
                <div class="stat-row"><span class="stat-label">P-valor</span><span class="stat-value" id="pvalue">--</span></div>
                <div class="stat-row"><span class="stat-label">Significancia</span><span class="stat-value" id="signif">--</span></div>
            </div>
            <div class="card">
                <h3>⚠️ Alerta Actual</h3>
                <div class="stat-row"><span class="stat-label">Nivel</span><span class="stat-value" id="alert-level">--</span></div>
                <div class="stat-row"><span class="stat-label">Riesgo</span><span class="stat-value" id="risk-level">--</span></div>
                <div class="stat-row"><span class="stat-label">Medidas</span><span class="stat-value" id="measures">--</span></div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="grid">
            <div class="card" style="grid-column: span 2;">
                <h3>📈 Actividad Solar (12 meses)</h3>
                <div class="chart-container"><canvas id="solarChart"></canvas></div>
            </div>
            <div class="card">
                <h3>🎯 Distribución por Fase</h3>
                <div class="chart-container"><canvas id="phaseChart"></canvas></div>
            </div>
        </div>

        <!-- Endpoints rápidos -->
        <div class="card">
            <h3>🔗 Endpoints Rápidos</h3>
            <div class="endpoint-grid">
                <a href="/solar/activity" class="endpoint-btn">☀️ Solar</a>
                <a href="/health/events" class="endpoint-btn">🏥 Salud</a>
                <a href="/analysis/correlate" class="endpoint-btn">🔬 Correlación</a>
                <a href="/alerts/current" class="endpoint-btn">⚠️ Alertas</a>
                <a href="/chizhevsky/knowledge" class="endpoint-btn">📚 Chizhevsky</a>
                <a href="/space-weather" class="endpoint-btn">🌌 NOAA</a>
                <a href="/solar-cycles" class="endpoint-btn">🔄 Ciclos</a>
                <a href="/report/solar" class="endpoint-btn">📄 PDF Solar</a>
                <a href="/docs" class="endpoint-btn">📖 Swagger</a>
                <a href="/redoc" class="endpoint-btn">📕 ReDoc</a>
            </div>
        </div>

        <div class="quote">
            "Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"<br>
            <strong>— Alexander Leonidovich Chizhevsky (1897-1964)</strong>
        </div>
    </div>

    <footer>
        <p>© 2024-2026 mechmind-dwv | HelioBio-API v3.1.0 | MIT License</p>
        <p style="margin-top:8px;">
            <a href="https://github.com/mechmind-dwv/HelioBio-API" style="color:var(--blue);">GitHub</a> |
            <a href="mailto:ia.mechmind@gmail.com" style="color:var(--blue);">Contacto</a>
        </p>
    </footer>

    <script>
    const API = '';
    
    async function fetchData() {
        try {
            // Datos solares recientes (último año)
            const solarRes = await fetch(`${API}/solar/activity?start_date=2024-01-01&end_date=2024-12-31`);
            const solarData = await solarRes.json();
            
            // Correlación
            const corrRes = await fetch(`${API}/analysis/correlate?years_before=5&years_after=3`);
            const corrData = await corrRes.json();
            
            // Alertas
            const alertRes = await fetch(`${API}/alerts/current`);
            const alertData = await alertRes.json();
            
            updateKPIs(solarData, corrData, alertData);
            updateSolarChart(solarData);
            updatePhaseChart(solarData);
            
        } catch (e) {
            console.log('Cargando datos...', e);
        }
    }
    
    function updateKPIs(solar, corr, alert) {
        if (solar.length > 0) {
            const last = solar[solar.length - 1];
            document.getElementById('ssn-value').textContent = last.sunspot_number.toFixed(1);
            document.getElementById('ssn-class').innerHTML = `<span class="stat-${last.classification}">${last.classification.toUpperCase()}</span>`;
            document.getElementById('flare-value').textContent = last.flare_activity.toFixed(1);
        }
        if (corr) {
            document.getElementById('corr-value').textContent = corr.correlation_score.toFixed(4);
            document.getElementById('pvalue').textContent = corr.p_value.toFixed(4);
            document.getElementById('signif').innerHTML = corr.p_value < 0.05 ? '<span class="stat-high">✅ Significativo</span>' : '❌ No significativo';
        }
        if (alert.length > 0) {
            document.getElementById('alert-level').innerHTML = `<span class="stat-${alert[0].level.toLowerCase()}">${alert[0].level}</span>`;
            document.getElementById('risk-level').textContent = corr?.prediction?.current_risk_level || '--';
            document.getElementById('measures').textContent = alert[0].protective_measures[0] || '--';
        }
    }
    
    function updateSolarChart(data) {
        const labels = data.slice(-12).map(d => d.date.slice(0,7));
        const values = data.slice(-12).map(d => d.sunspot_number);
        
        new Chart(document.getElementById('solarChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Manchas Solares (SSN)',
                    data: values,
                    borderColor: '#ffd700',
                    backgroundColor: 'rgba(255,215,0,0.15)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#ffd700',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#e0e0e0' } } },
                scales: {
                    x: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(255,255,255,0.05)' }, title: { display: true, text: 'SSN', color: '#8892b0' } }
                }
            }
        });
    }
    
    function updatePhaseChart(data) {
        const counts = { high: 0, moderate: 0, low: 0 };
        data.forEach(d => counts[d.classification]++);
        
        new Chart(document.getElementById('phaseChart'), {
            type: 'doughnut',
            data: {
                labels: ['ALTA', 'MODERADA', 'BAJA'],
                datasets: [{
                    data: [counts.high, counts.moderate, counts.low],
                    backgroundColor: ['#d73a4a', '#ffd700', '#2d7d46'],
                    borderColor: '#112240',
                    borderWidth: 3,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#e0e0e0', padding: 15 } }
                }
            }
        });
    }
    
    fetchData();
    // Actualizar cada 5 minutos
    setInterval(fetchData, 300000);
    </script>
</body>
</html>
"""

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD_HTML
