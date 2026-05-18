"""Sistema de notificaciones por email para HelioBio-API"""
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from typing import List, Optional

SMTP_CONFIG = {
    "hostname": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", "587")),
    "username": os.getenv("SMTP_USER", ""),
    "password": os.getenv("SMTP_PASS", ""),
    "use_tls": True,
}

FROM_EMAIL = os.getenv("FROM_EMAIL", "ia.mechmind@gmail.com")

async def send_alert_notification(alert_data: dict, recipients: List[str]) -> bool:
    """Envía notificación de alerta por email"""
    try:
        subject = f"[HelioBio-API] ⚠️ Alerta {alert_data['level']}: {alert_data['message'][:50]}"
        body = f"""
        <html>
        <body style='font-family: Arial; background: #0a1628; color: #e0e0e0; padding: 20px;'>
            <h2 style='color: #ffd700;'>☀️ HelioBio-API - Alerta de Salud</h2>
            <table style='border-collapse: collapse; width: 100%;'>
                <tr><td style='padding: 10px;'><b>Nivel:</b></td><td style='color: {"#ff4444" if alert_data["level"] == "Alto" else "#ffaa00"};'>{alert_data['level']}</td></tr>
                <tr><td style='padding: 10px;'><b>Mensaje:</b></td><td>{alert_data['message']}</td></tr>
                <tr><td style='padding: 10px;'><b>Impacto:</b></td><td>{alert_data['expected_impact']}</td></tr>
                <tr><td style='padding: 10px;'><b>Período:</b></td><td>{alert_data['timeframe']}</td></tr>
            </table>
            <h3>🛡️ Medidas de Protección:</h3>
            <ul>
                {''.join(f'<li>{m}</li>' for m in alert_data['protective_measures'])}
            </ul>
            <p style='color: #666; font-size: 12px;'>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = FROM_EMAIL
        message["To"] = ", ".join(recipients)
        message.attach(MIMEText(body, "html", "utf-8"))
        
        await aiosmtplib.send(
            message,
            hostname=SMTP_CONFIG["hostname"],
            port=SMTP_CONFIG["port"],
            username=SMTP_CONFIG["username"],
            password=SMTP_CONFIG["password"],
            use_tls=SMTP_CONFIG["use_tls"],
        )
        print(f"✅ Email enviado a {len(recipients)} destinatarios")
        return True
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False
