"""HelioBio-API Android App"""
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="HelioBio-API Mobile")

@app.get("/", response_class=HTMLResponse)
async def mobile_dashboard():
    return """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>☀️ HelioBio</title>
<style>body{font-family:sans-serif;background:#0a1628;color:#e0e0e0;padding:15px;text-align:center}
h1{color:#ffd700;font-size:1.5em}.card{background:#112240;border-radius:12px;padding:15px;margin:10px 0;text-align:left}
.card h3{color:#58c7e9;margin:0 0 8px}.value{font-size:1.8em;font-weight:bold;color:#ffd700}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.btn{display:block;padding:12px;background:#00509d;color:white;text-decoration:none;border-radius:8px;margin:5px 0}
</style></head><body><h1>☀️ HelioBio-API</h1><p style="color:#2d7d46">🟢 v4.0.0</p>
<div class="grid"><div class="card"><h3>SSN Actual</h3><div class="value" id="ssn">--</div></div>
<div class="card"><h3>Alerta</h3><div class="value" id="alert">--</div></div></div>
<a href="/solar/activity" class="btn">☀️ Actividad Solar</a>
<a href="/analysis/correlate" class="btn">🔬 Correlación</a>
<a href="/chizhevsky/knowledge" class="btn">📚 Chizhevsky</a>
<a href="/docs" class="btn">📖 API Docs</a>
<p style="margin-top:20px;color:#666;font-style:italic">"Toda la vida orgánica de la Tierra existe en el océano de energía radiante del Sol"<br>- A.L. Chizhevsky</p>
<script>fetch('/solar/activity?start_date=2024-12-01&end_date=2024-12-31').then(r=>r.json()).then(d=>{document.getElementById('ssn').textContent=d[d.length-1]?.sunspot_number?.toFixed(1)||'--'})</script></body></html>"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
