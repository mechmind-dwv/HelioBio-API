"""Generador de reportes PDF para HelioBio-API"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
import base64

def generate_solar_report(solar_data: list, include_chart: bool = True) -> bytes:
    """Genera un informe PDF con datos de actividad solar"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Informe HelioBio-API")
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                fontSize=22, textColor=HexColor('#002848'))
    story.append(Paragraph("☀️ Informe de Actividad Solar", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} | HelioBio-API v3.0", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Resumen
    story.append(Paragraph("📊 Resumen", styles['Heading2']))
    if solar_data:
        ssn_values = [d['sunspot_number'] for d in solar_data]
        avg_ssn = sum(ssn_values) / len(ssn_values)
        max_ssn = max(ssn_values)
        min_ssn = min(ssn_values)
        
        summary_data = [
            ["Indicador", "Valor"],
            ["Registros analizados", str(len(solar_data))],
            ["SSN Promedio", f"{avg_ssn:.1f}"],
            ["SSN Máximo", f"{max_ssn:.1f}"],
            ["SSN Mínimo", f"{min_ssn:.1f}"],
            ["Clasificación", "ALTA" if avg_ssn > 100 else ("MODERADA" if avg_ssn > 50 else "BAJA")],
        ]
        
        table = Table(summary_data, colWidths=[5*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00509d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f5f5f5')),
        ]))
        story.append(table)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("📈 Datos Recientes", styles['Heading2']))
    
    # Tabla de datos
    if solar_data:
        data_rows = [["Fecha", "SSN", "Clasificación"]]
        for d in solar_data[-10:]:
            data_rows.append([
                d['date'][:10],
                f"{d['sunspot_number']:.1f}",
                d['classification'].upper()
            ])
        
        table = Table(data_rows, colWidths=[4*cm, 3*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00509d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
        ]))
        story.append(table)
    
    # Pie de página
    story.append(Spacer(1, 40))
    story.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv | Basado en los estudios de A.L. Chizhevsky", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_correlation_report(correlation_data: dict) -> bytes:
    """Genera un informe PDF con resultados de correlación"""
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
    
    # Métricas
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
    
    # Recomendaciones
    story.append(Spacer(1, 20))
    story.append(Paragraph("💡 Recomendaciones", styles['Heading2']))
    for rec in correlation_data.get('recommendations', []):
        story.append(Paragraph(f"• {rec}", styles['Normal']))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("HelioBio-API © 2024-2026 mechmind-dwv | Basado en los estudios de A.L. Chizhevsky",
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'))))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
