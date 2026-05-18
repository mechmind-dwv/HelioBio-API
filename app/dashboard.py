"""Dashboard interactivo profesional para HelioBio-API v8.0.0"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☀️ HelioBio-API v8.0.0 | Dashboard Cósmico</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg-deep: #060d1a;
            --bg-card: #0d1a30;
            --bg-card-hover: #111d38;
            --gold: #ffd700;
            --blue: #58c7e9;
            --green: #2d7d46;
            --red: #d73a4a;
            --purple: #8b5cf6;
            --text: #e0e0e0;
            --muted: #8892b0;
            --border: rgba(255,255,255,0.06);
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg-deep);
            color: var(--text);
            min-height: 100vh;
        }
        /* Header */
        .header {
            background: linear-gradient(135deg, #001a33 0%, #003366 50%, #001a33 100%);
            padding: 16px 32px;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid var(--gold);
            position: sticky; top:0; z-index:100;
        }
        .header h1 { font-size:1.6em; color:var(--gold); letter-spacing:1px; }
        .header .version { font-size:0.8em; color:var(--muted); }
        .badge { padding:6px 14px; border-radius:20px; font-size:0.8em; font-weight:bold; }
        .badge-online { background:var(--green); color:#fff; animation:pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
        /* Layout */
        .container { max-width:1440px; margin:0 auto; padding:24px; }
        .grid { display:grid; gap:20px; }
        .grid-4 { grid-template-columns:repeat(4,1fr); }
        .grid-3 { grid-template-columns:repeat(3,1fr); }
        .grid-2 { grid-template-columns:repeat(2,1fr); }
        @media(max-width:1200px){ .grid-4{grid-template-columns:repeat(2,1fr)} .grid-3{grid-template-columns:1fr} }
        @media(max-width:768px){ .grid-4,.grid-3,.grid-2{grid-template-columns:1fr} .header{flex-direction:column;gap:10px} }
        /* Cards */
        .card {
            background: var(--bg-card);
            border-radius:16px;
            padding:20px;
            border:1px solid var(--border);
            transition: all .2s;
        }
        .card:hover { background:var(--bg-card-hover); transform:translateY(-2px); box-shadow:0 8px 30px rgba(0,0,0,.4); }
        .card-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
        .card-title { font-size:1em; font-weight:600; color:var(--text); }
        .card-icon { font-size:1.4em; }
        .kpi-value { font-size:2.2em; font-weight:800; color:var(--gold); }
        .kpi-label { font-size:0.8em; color:var(--muted); margin-top:4px; }
        .chart-wrap { position:relative; width:100%; height:280px; }
        .chart-wrap-lg { height:350px; }
        canvas { width:100%!important; height:100%!important; }
        /* Stats row */
        .stat-row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border); }
        .stat-row:last-child { border:none; }
        .stat-label { color:var(--muted); font-size:0.9em; }
        .stat-value { font-weight:600; }
        /* Buttons */
        .btn {
            display:inline-block; padding:10px 20px; border-radius:10px;
            text-decoration:none; font-weight:600; font-size:0.85em;
            transition:all .2s; border:none; cursor:pointer;
        }
        .btn-gold { background:var(--gold); color:#000; }
        .btn-gold:hover { background:#e6c200; }
        .btn-outline { background:transparent; color:var(--blue); border:1px solid var(--blue); }
        .btn-outline:hover { background:var(--blue); color:#000; }
        .endpoint-grid { display:flex; flex-wrap:wrap; gap:8px; }
        .endpoint-tag {
            padding:6px 12px; border-radius:8px; font-size:0.75em; font-family:monospace;
            background:rgba(88,199,233,.1); color:var(--blue); border:1px solid rgba(88,199,233,.2);
            text-decoration:none; transition:all .2s;
        }
        .endpoint-tag:hover { background:rgba(88,199,233,.2); }
        .endpoint-tag.post { color:var(--purple); border-color:rgba(139,92,246,.3); background:rgba(139,92,246,.1); }
        /* Footer */
        .footer { text-align:center; padding:20px; color:var(--muted); font-size:0.8em; border-top:1px solid var(--border); margin-top:40px; }
        .quote { text-align:center; padding:24px; font-style:italic; color:var(--muted); border-left:3px solid var(--gold); margin:24px 0; }
        /* Tabs */
        .tabs { display:flex; gap:8px; margin-bottom:20px; flex-wrap:wrap; }
        .tab {
            padding:8px 16px; border-radius:8px; cursor:pointer; font-size:0.85em; font-weight:600;
            background:var(--bg-card); color:var(--muted); border:1px solid var(--border); transition:all .2s;
        }
        .tab.active { background:var(--gold); color:#000; border-color:var(--gold); }
        .tab:hover:not(.active) { background:var(--bg-card-hover); color:var(--text); }
        .tab-content { display:none; }
        .tab-content.active { display:block; }
    </style>
</head>
<body>

<header class="header">
    <div>
        <h1>☀️ HelioBio-API</h1>
        <span class="version">v8.0.0 "Cosmic Odyssey" — Sistema Avanzado de Análisis Heliobiológico</span>
    </div>
    <div style="display:flex;gap:12px;align-items:center;">
        <span class="badge badge-online">🟢 Operativa</span>
        <span class="badge" style="background:var(--bg-card);color:var(--gold);border:1px solid var(--gold);">44 Endpoints</span>
        <span class="badge" style="background:var(--bg-card);color:var(--green);">27 Tests</span>
    </div>
</header>

<div class="container">

    <!-- KPIs -->
    <div class="grid grid-4" style="margin-bottom:24px;">
        <div class="card" style="text-align:center;">
            <div class="card-icon">☀️</div>
            <div class="kpi-value" id="kpi-ssn">—</div>
            <div class="kpi-label">Manchas Solares (SSN)</div>
        </div>
        <div class="card" style="text-align:center;">
            <div class="card-icon">📊</div>
            <div class="kpi-value" id="kpi-corr">—</div>
            <div class="kpi-label">Correlación Pearson</div>
        </div>
        <div class="card" style="text-align:center;">
            <div class="card-icon">⚠️</div>
            <div class="kpi-value" id="kpi-alert">—</div>
            <div class="kpi-label">Alerta Actual</div>
        </div>
        <div class="card" style="text-align:center;">
            <div class="card-icon">📜</div>
            <div class="kpi-value" id="kpi-sei">—</div>
            <div class="kpi-label">Índice Excitabilidad Social</div>
        </div>
    </div>

    <!-- Gráficos principales -->
    <div class="grid grid-2" style="margin-bottom:24px;">
        <div class="card">
            <div class="card-header"><span class="card-title">📈 Actividad Solar (12 meses)</span></div>
            <div class="chart-wrap chart-wrap-lg"><canvas id="chartSolar"></canvas></div>
        </div>
        <div class="card">
            <div class="card-header"><span class="card-title">🎯 Distribución por Fase Solar</span></div>
            <div class="chart-wrap chart-wrap-lg"><canvas id="chartPhase"></canvas></div>
        </div>
    </div>

    <!-- Tabs de secciones -->
    <div class="tabs">
        <div class="tab active" data-tab="tab-solar">☀️ Solar</div>
        <div class="tab" data-tab="tab-health">🏥 Salud</div>
        <div class="tab" data-tab="tab-ai">🧠 IA & Predicción</div>
        <div class="tab" data-tab="tab-space">🚀 Espacio</div>
        <div class="tab" data-tab="tab-ion">⚛️ Ionismo</div>
        <div class="tab" data-tab="tab-history">📜 Historiometría</div>
        <div class="tab" data-tab="tab-endpoints">🔗 Endpoints</div>
    </div>

    <!-- Contenido de tabs -->
    <div id="tab-solar" class="tab-content active">
        <div class="grid grid-3">
            <div class="card"><div class="card-header"><span class="card-title">☀️ SILSO Real</span></div><div class="stat-row" id="solar-detail"></div></div>
            <div class="card"><div class="card-header"><span class="card-title">🌌 Clima Espacial</span></div><div id="space-weather-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">🔄 Ciclos Solares</span></div><div id="cycles-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-health" class="tab-content">
        <div class="grid grid-3">
            <div class="card"><div class="card-header"><span class="card-title">🦠 OMS Pandemias</span></div><div id="who-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">🩺 CDC Influenza</span></div><div id="cdc-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">⚠️ Alertas</span></div><div id="alerts-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-ai" class="tab-content">
        <div class="grid grid-2">
            <div class="card"><div class="card-header"><span class="card-title">🧠 Deep Learning</span></div><div id="dl-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">💬 Sentimiento</span></div><div id="sentiment-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-space" class="tab-content">
        <div class="grid grid-3">
            <div class="card"><div class="card-header"><span class="card-title">🚀 Misión a Marte</span></div><div id="mars-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">🌌 Rayos Cósmicos</span></div><div id="gcr-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">🪐 Exoplanetas</span></div><div id="exo-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-ion" class="tab-content">
        <div class="grid grid-3">
            <div class="card"><div class="card-header"><span class="card-title">⚛️ Resonancia Schumann</span></div><div id="schumann-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">📡 TEC Ionosférico</span></div><div id="tec-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">🧬 Efectos Biológicos</span></div><div id="bio-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-history" class="tab-content">
        <div class="grid grid-2">
            <div class="card"><div class="card-header"><span class="card-title">📜 SEI</span></div><div id="sei-detail">Cargando...</div></div>
            <div class="card"><div class="card-header"><span class="card-title">📋 Eventos Históricos</span></div><div id="events-detail">Cargando...</div></div>
        </div>
    </div>

    <div id="tab-endpoints" class="tab-content">
        <div class="card">
            <div class="card-header"><span class="card-title">🔗 44 Endpoints Disponibles</span></div>
            <div class="endpoint-grid" id="endpoint-list"></div>
        </div>
    </div>

    <!-- Quote -->
    <div class="quote">
        "Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"<br>
        <strong>— Alexander Leonidovich Chizhevsky (1897-1964)</strong>
    </div>

</div>

<footer class="footer">
    <p>© 2024-2026 mechmind-dwv | HelioBio-API v8.0.0 "Cosmic Odyssey" | MIT License | 44 endpoints · 27 tests · 6 fuentes de datos</p>
    <p style="margin-top:8px;"><a href="/docs" style="color:var(--blue);">Swagger</a> | <a href="/redoc" style="color:var(--blue);">ReDoc</a> | <a href="/graphql" style="color:var(--blue);">GraphQL</a> | <a href="https://github.com/mechmind-dwv/HelioBio-API" style="color:var(--blue);">GitHub</a></p>
</footer>

<script>
// ============ TABS ============
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

// ============ CHARTS ============
async function loadSolarChart() {
    try {
        const res = await fetch('/solar/activity?start_date=2023-01-01&end_date=2024-12-31');
        const data = await res.json();
        const last12 = data.slice(-12);
        new Chart(document.getElementById('chartSolar'), {
            type:'line', data:{labels:last12.map(d=>d.date.slice(0,7)), datasets:[{label:'SSN',data:last12.map(d=>d.sunspot_number),borderColor:'#ffd700',backgroundColor:'rgba(255,215,0,.1)',fill:true,tension:.4,pointRadius:3}]},
            options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#e0e0e0'}}},scales:{x:{ticks:{color:'#8892b0'}},y:{ticks:{color:'#8892b0'}}}}
        });
        const counts = {high:0,moderate:0,low:0};
        data.forEach(d => { if(d.classification==='high')counts.high++; else if(d.classification==='moderate')counts.moderate++; else counts.low++; });
        new Chart(document.getElementById('chartPhase'), {
            type:'doughnut', data:{labels:['ALTA','MODERADA','BAJA'],datasets:[{data:[counts.high,counts.moderate,counts.low],backgroundColor:['#d73a4a','#ffd700','#2d7d46'],borderColor:'#0d1a30',borderWidth:3}]},
            options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{color:'#e0e0e0'}}}}
        });
    } catch(e) { console.log('Charts loading...'); }
}

// ============ KPI UPDATES ============
async function updateKPIs() {
    try {
        const solarRes = await fetch('/solar/activity?start_date=2024-12-01&end_date=2024-12-31');
        const solarData = await solarRes.json();
        if(solarData.length>0) document.getElementById('kpi-ssn').textContent = solarData[solarData.length-1].sunspot_number.toFixed(1);
        
        const corrRes = await fetch('/analysis/correlate?years_before=5&years_after=3');
        const corrData = await corrRes.json();
        document.getElementById('kpi-corr').textContent = corrData.correlation_score?.toFixed(4) || '—';
        
        const alertRes = await fetch('/alerts/current');
        const alertData = await alertRes.json();
        if(alertData.length>0) document.getElementById('kpi-alert').textContent = alertData[0].level;
        
        const seiRes = await fetch('/historiometry/sei?ssn=120');
        const seiData = await seiRes.json();
        document.getElementById('kpi-sei').textContent = seiData.sei_index?.toFixed(1) || '—';
    } catch(e) { console.log('KPIs loading...'); }
}

// ============ DETAIL LOADERS ============
async function loadSolarDetail() {
    try {
        const res = await fetch('/solar/activity?start_date=2024-01-01&end_date=2024-12-31');
        const data = await res.json();
        const last = data[data.length-1];
        document.getElementById('solar-detail').innerHTML = `<div class="stat-row"><span class="stat-label">SSN Actual</span><span class="stat-value">${last.sunspot_number.toFixed(1)}</span></div><div class="stat-row"><span class="stat-label">Clasificación</span><span class="stat-value">${last.classification.toUpperCase()}</span></div><div class="stat-row"><span class="stat-label">Flare Activity</span><span class="stat-value">${last.flare_activity.toFixed(1)}</span></div><div class="stat-row"><span class="stat-label">Registros</span><span class="stat-value">${data.length}</span></div>`;
        
        const swRes = await fetch('/space-weather');
        const swData = await swRes.json();
        document.getElementById('space-weather-detail').innerHTML = swData ? `<div class="stat-row"><span class="stat-label">Fuente</span><span class="stat-value">${swData.source||'NOAA'}</span></div>` : 'No disponible';
        
        const cyRes = await fetch('/solar-cycles');
        const cyData = await cyRes.json();
        document.getElementById('cycles-detail').innerHTML = cyData.length ? `<div class="stat-row"><span class="stat-label">Total Ciclos</span><span class="stat-value">${cyData.length}</span></div><div class="stat-row"><span class="stat-label">Último</span><span class="stat-value">Ciclo 25 (2019-)</span></div>` : 'No disponible';
    } catch(e) {}
}

async function loadHealthDetail() {
    try {
        const res = await fetch('/who/pandemics');
        const data = await res.json();
        document.getElementById('who-detail').innerHTML = data.slice(0,4).map(p => `<div class="stat-row"><span class="stat-label">${p.name}</span><span class="stat-value">${(p.total_deaths||p.death_count||0).toLocaleString()} muertes</span></div>`).join('');
        
        const cdcRes = await fetch('/cdc/influenza');
        const cdc = await cdcRes.json();
        document.getElementById('cdc-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Temporada</span><span class="stat-value">${cdc.current_season}</span></div><div class="stat-row"><span class="stat-label">Casos USA</span><span class="stat-value">${(cdc.total_cases_usa||0).toLocaleString()}</span></div><div class="stat-row"><span class="stat-label">Cepa</span><span class="stat-value">${cdc.predominant_strain}</span></div>`;
        
        const alertRes = await fetch('/alerts/current');
        const alerts = await alertRes.json();
        document.getElementById('alerts-detail').innerHTML = alerts.map(a => `<div class="stat-row"><span class="stat-label">${a.level}</span><span class="stat-value">${a.message}</span></div>`).join('');
    } catch(e) {}
}

async function loadAIDetail() {
    try {
        const dlRes = await fetch('/predict/deep-learning?months_ahead=6');
        const dl = await dlRes.json();
        document.getElementById('dl-detail').innerHTML = dl.predictions ? dl.predictions.map(p => `<div class="stat-row"><span class="stat-label">${p.month}</span><span class="stat-value">SSN: ${p.predicted_ssn}</span></div>`).join('') : 'Cargando...';
        
        const sentRes = await fetch('/sentiment/public');
        const sent = await sentRes.json();
        document.getElementById('sentiment-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Sentimiento</span><span class="stat-value">${sent.overall||'N/A'}</span></div><div class="stat-row"><span class="stat-label">Textos</span><span class="stat-value">${sent.texts_analyzed||0}</span></div>`;
    } catch(e) {}
}

async function loadSpaceDetail() {
    try {
        const marsRes = await fetch('/space/mission-briefing?destination=Mars&crew_size=6&ssn=120&duration_days=500');
        const mars = await marsRes.json();
        document.getElementById('mars-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Radiación Total</span><span class="stat-value">${mars.radiation?.total_mSv?.toFixed(0)||'—'} mSv</span></div><div class="stat-row"><span class="stat-label">Riesgo</span><span class="stat-value">${mars.radiation?.risk||'—'}</span></div><div class="stat-row"><span class="stat-label">Duración</span><span class="stat-value">${mars.duration_days} días</span></div>`;
        
        const gcrRes = await fetch('/space/galactic-cosmic-rays?ssn=120');
        const gcr = await gcrRes.json();
        document.getElementById('gcr-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Flujo GCR</span><span class="stat-value">${gcr.gcr_flux?.toFixed(2)||'—'}</span></div><div class="stat-row"><span class="stat-label">Impacto</span><span class="stat-value">${gcr.biological_impact||'—'}</span></div>`;
        
        const exoRes = await fetch('/space/exoplanet-habitability?star_type=K&orbital_distance_au=1.2&magnetic_field=true');
        const exo = await exoRes.json();
        document.getElementById('exo-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Habitabilidad</span><span class="stat-value">${exo.habitability_index?.toFixed(1)||'—'}</span></div><div class="stat-row"><span class="stat-label">Rating</span><span class="stat-value">${exo.rating||'—'}</span></div>`;
    } catch(e) {}
}

async function loadIonDetail() {
    try {
        const schRes = await fetch('/ionosphere/schumann');
        const sch = await schRes.json();
        document.getElementById('schumann-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Frecuencia</span><span class="stat-value">${sch.schumann_fundamental?.toFixed(2)||'—'} Hz</span></div><div class="stat-row"><span class="stat-label">Variación</span><span class="stat-value">${sch.variation_percent?.toFixed(1)||'—'}%</span></div><div class="stat-row"><span class="stat-label">Estado</span><span class="stat-value">${sch.biological_state||'—'}</span></div>`;
        
        const tecRes = await fetch('/ionosphere/tec?ssn=120');
        const tec = await tecRes.json();
        document.getElementById('tec-detail').innerHTML = `<div class="stat-row"><span class="stat-label">TEC</span><span class="stat-value">${tec.tec_value?.toFixed(1)||'—'} TECU</span></div><div class="stat-row"><span class="stat-label">Impacto</span><span class="stat-value">${tec.impact||'—'}</span></div>`;
        
        const bioRes = await fetch('/ionosphere/bio-effects');
        const bio = await bioRes.json();
        document.getElementById('bio-detail').innerHTML = `<div class="stat-row"><span class="stat-label">Riesgo</span><span class="stat-value">${bio.risk_level||'—'}</span></div>` + (bio.predicted_effects||[]).map(e => `<div class="stat-row"><span class="stat-label">•</span><span class="stat-value">${e}</span></div>`).join('');
    } catch(e) {}
}

async function loadHistoryDetail() {
    try {
        const seiRes = await fetch('/historiometry/sei?ssn=120&sentiment=-0.2');
        const sei = await seiRes.json();
        document.getElementById('sei-detail').innerHTML = `<div class="stat-row"><span class="stat-label">SEI</span><span class="stat-value">${sei.sei_index?.toFixed(1)||'—'}</span></div><div class="stat-row"><span class="stat-label">Interpretación</span><span class="stat-value">${sei.interpretation||'—'}</span></div>`;
        
        const evRes = await fetch('/historiometry/events');
        const events = await evRes.json();
        document.getElementById('events-detail').innerHTML = events.slice(0,6).map(e => `<div class="stat-row"><span class="stat-label">${e.year}</span><span class="stat-value">${e.event} (SSN:${e.ssn_peak})</span></div>`).join('');
    } catch(e) {}
}

// ============ ENDPOINTS LIST ============
const endpoints = [
    {m:'GET',p:'/',d:'Inicio'},
    {m:'GET',p:'/dashboard',d:'Dashboard'},
    {m:'GET',p:'/solar/activity',d:'Actividad Solar'},
    {m:'GET',p:'/health/events',d:'Eventos Salud'},
    {m:'GET',p:'/analysis/correlate',d:'Correlación'},
    {m:'GET',p:'/alerts/current',d:'Alertas'},
    {m:'GET',p:'/chizhevsky/knowledge',d:'Chizhevsky KB'},
    {m:'GET',p:'/space-weather',d:'Clima Espacial'},
    {m:'GET',p:'/solar-cycles',d:'Ciclos Solares'},
    {m:'GET',p:'/report/solar',d:'PDF Solar'},
    {m:'GET',p:'/report/correlation',d:'PDF Correlación'},
    {m:'POST',p:'/notify/subscribe',d:'Notificar'},
    {m:'POST',p:'/notify/test',d:'Test Email'},
    {m:'POST',p:'/webhooks/register',d:'Webhook Register'},
    {m:'GET',p:'/webhooks',d:'Webhooks'},
    {m:'GET',p:'/who/pandemics',d:'OMS Pandemias'},
    {m:'GET',p:'/cdc/influenza',d:'CDC Influenza'},
    {m:'POST',p:'/auth/login',d:'Login JWT'},
    {m:'GET',p:'/auth/me',d:'Perfil'},
    {m:'GET',p:'/predict/deep-learning',d:'Deep Learning'},
    {m:'GET',p:'/predict/multi-parametric',d:'Predicción Multi'},
    {m:'GET',p:'/sentiment/public',d:'Sentimiento'},
    {m:'GET',p:'/ionosphere/schumann',d:'Schumann'},
    {m:'GET',p:'/ionosphere/tec',d:'TEC'},
    {m:'GET',p:'/ionosphere/bio-effects',d:'Bio Efectos'},
    {m:'GET',p:'/historiometry/sei',d:'SEI'},
    {m:'GET',p:'/historiometry/events',d:'Eventos Históricos'},
    {m:'GET',p:'/depin/network-status',d:'Red DePIN'},
    {m:'GET',p:'/depin/hyperlocal-alert',d:'Alerta Local'},
    {m:'GET',p:'/epigenetics/viral-mutations',d:'Epigenética'},
    {m:'GET',p:'/earth-digital-twin/telluric',d:'Gemelo Digital'},
    {m:'GET',p:'/space/mission-briefing',d:'Misión Espacial'},
    {m:'GET',p:'/space/galactic-cosmic-rays',d:'Rayos Cósmicos'},
    {m:'GET',p:'/space/exoplanet-habitability',d:'Exoplanetas'},
    {m:'GET',p:'/iot/simulate',d:'IoT Simulator'},
    {m:'GET',p:'/health',d:'Health Check'},
    {m:'GET',p:'/docs',d:'Swagger'},
    {m:'GET',p:'/redoc',d:'ReDoc'},
    {m:'POST',p:'/graphql',d:'GraphQL'},
];
document.getElementById('endpoint-list').innerHTML = endpoints.map(e => `<a href="${e.p}" class="endpoint-tag${e.m==='POST'?' post':''}">${e.m} ${e.p}</a>`).join('');

// ============ INIT ============
loadSolarChart();
updateKPIs();
loadSolarDetail();
loadHealthDetail();
loadAIDetail();
loadSpaceDetail();
loadIonDetail();
loadHistoryDetail();

// Refresh every 5 minutes
setInterval(() => {
    updateKPIs();
    loadSolarDetail();
    loadHealthDetail();
    loadAIDetail();
    loadSpaceDetail();
    loadIonDetail();
    loadHistoryDetail();
}, 300000);
</script>
</body>
</html>
"""

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD_HTML
