"""Generador de reportes PDF para HelioBio-API"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import pandas as pd

def generate_solar_report(solar_data: list, include_chart: bool = True) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Informe HelioBio-API")
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                fontSize=22, textColor=HexColor('#002848'))
    story.append(Paragraph("☀️ Informe de Actividad Solar", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} | HelioBio-API v3.1", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Convertir a DataFrame para manejo seguro
    if isinstance(solar_data, list):
        df = pd.DataFrame(solar_data)
    else:
        df = solar_data
    
    # Resumen
    story.append(Paragraph("📊 Resumen", styles['Heading2']))
    if len(df) > 0:
        ssn_values = df['sunspot_number'].dropna()
        avg_ssn = ssn_values.mean()
        max_ssn = ssn_values.max()
        min_ssn = ssn_values.min()
        
        classification = "ALTA" if avg_ssn > 100 else ("MODERADA" if avg_ssn > 50 else "BAJA")
        
        summary_data = [
            ["Indicador", "Valor"],
            ["Registros", str(len(df))],
            ["SSN Promedio", f"{avg_ssn:.1f}"],
            ["SSN Máximo", f"{max_ssn:.1f}"],
            ["SSN Mínimo", f"{min_ssn:.1f}"],
            ["Clasificación", classification],
        ]
        
        table = Table(summary_data, colWidths=[5*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00509d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f5f5f5')),
        ]))
        story.append(table)
    
    # Datos recientes
    story.append(Spacer(1, 20))
    story.append(Paragraph("📈 Datos Recientes", styles['Heading2']))
    
    if len(df) > 0:
        data_rows = [["Fecha", "SSN", "Clasificación"]]
        for i in range(max(0, len(df)-10), len(df)):
            row = df.iloc[i]
            try:
                date_val = row['date']
                if hasattr(date_val, 'strftime'):
                    date_str = date_val.strftime('%Y-%m-%d')
                else:
                    date_str = str(date_val)[:10]
                ssn_str = f"{float(row['sunspot_number']):.1f}"
                cls_str = str(row['classification']).upper()
            except Exception as e:
                date_str = 'N/A'
                ssn_str = 'N/A'
                cls_str = 'N/A'
            
            data_rows.append([date_str, ssn_str, cls_str])
        
        table = Table(data_rows, colWidths=[4*cm, 3*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00509d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
        ]))
        story.append(table)
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv | Basado en los estudios de A.L. Chizhevsky",
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_correlation_report(correlation_data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Informe de Correlación HelioBio-API")
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                fontSize=22, textColor=HexColor('#002848'))
    story.append(Paragraph("🔬 Informe de Análisis de Correlación", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("📊 Métricas de Correlación", styles['Heading2']))
    metrics_data = [
        ["Métrica", "Valor", "Interpretación"],
        ["Correlación Pearson", f"{correlation_data.get('correlation_score', 0):.4f}",
         "Significativa" if abs(correlation_data.get('correlation_score', 0)) > 0.5 else "Débil"],
        ["P-valor", f"{correlation_data.get('p_value', 0):.6f}",
         "Significativo ✅" if correlation_data.get('p_value', 1) < 0.05 else "No significativo ❌"],
        ["Riesgo actual", correlation_data.get('prediction', {}).get('current_risk_level', 'N/A'), ""],
    ]
    
    table = Table(metrics_data, colWidths=[4*cm, 3*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00509d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
    ]))
    story.append(table)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("💡 Recomendaciones", styles['Heading2']))
    for rec in correlation_data.get('recommendations', []):
        if rec:
            story.append(Paragraph(f"• {rec}", styles['Normal']))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv | Basado en los estudios de A.L. Chizhevsky",
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
