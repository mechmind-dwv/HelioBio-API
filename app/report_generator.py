from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def _safe_date(val):
    if hasattr(val, 'strftime'):
        return val.strftime('%Y-%m-%d')
    return str(val)[:10]

def _safe_float(val):
    try: return f"{float(val):.1f}"
    except: return str(val)

def _safe_str(val):
    return str(val).upper()

def generate_solar_report(solar_data, include_chart=True):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="HelioBio-API Solar")
    styles = getSampleStyleSheet()
    S = []
    
    S.append(Paragraph("☀️ Informe Solar", ParagraphStyle('T', parent=styles['Heading1'], fontSize=22, textColor=HexColor('#002848'))))
    S.append(Spacer(1, 12))
    S.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    S.append(Spacer(1, 20))
    
    records = solar_data.to_dict('records') if hasattr(solar_data, 'to_dict') else solar_data
    
    if records:
        ssn = [r.get('sunspot_number',0) or 0 for r in records]
        avg = sum(ssn)/len(ssn) if ssn else 0
        cl = "ALTA" if avg>100 else ("MODERADA" if avg>50 else "BAJA")
        
        data = [["Indicador","Valor"], ["Registros",str(len(records))], ["SSN Promedio",f"{avg:.1f}"],
                ["SSN Máximo",f"{max(ssn):.1f}"], ["SSN Mínimo",f"{min(ssn):.1f}"], ["Clasificación",cl]]
        t = Table(data, colWidths=[5*cm,5*cm])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#00509d')), ('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),
                              ('GRID',(0,0),(-1,-1),1,HexColor('#cccccc')), ('BACKGROUND',(0,1),(-1,-1),HexColor('#f5f5f5'))]))
        S.append(t)
    
    S.append(Spacer(1,20))
    S.append(Paragraph("📈 Datos Recientes", styles['Heading2']))
    
    if records:
        rows = [["Fecha","SSN","Clasificación"]]
        for r in records[-10:]:
            rows.append([_safe_date(r.get('date','N/A')), _safe_float(r.get('sunspot_number',0)), _safe_str(r.get('classification','N/A'))])
        t = Table(rows, colWidths=[4*cm,3*cm,4*cm])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#00509d')), ('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),
                              ('GRID',(0,0),(-1,-1),1,HexColor('#cccccc'))]))
        S.append(t)
    
    S.append(Spacer(1,40))
    S.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv", ParagraphStyle('F', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    doc.build(S)
    buffer.seek(0)
    return buffer.getvalue()

def generate_correlation_report(correlation_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="HelioBio-API Correlación")
    styles = getSampleStyleSheet()
    S = []
    S.append(Paragraph("🔬 Informe de Correlación", ParagraphStyle('T', parent=styles['Heading1'], fontSize=22, textColor=HexColor('#002848'))))
    S.append(Spacer(1,12))
    S.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    S.append(Spacer(1,20))
    
    data = [["Métrica","Valor"], ["Correlación",f"{correlation_data.get('correlation_score',0):.4f}"],
            ["P-valor",f"{correlation_data.get('p_value',0):.6f}"], ["Riesgo",correlation_data.get('prediction',{}).get('current_risk_level','N/A')]]
    t = Table(data, colWidths=[5*cm,5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#00509d')), ('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),
                          ('GRID',(0,0),(-1,-1),1,HexColor('#cccccc'))]))
    S.append(t)
    
    for rec in correlation_data.get('recommendations',[]):
        if rec: S.append(Paragraph(f"• {rec}", styles['Normal']))
    
    S.append(Spacer(1,40))
    S.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv", ParagraphStyle('F', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    doc.build(S)
    buffer.seek(0)
    return buffer.getvalue()
