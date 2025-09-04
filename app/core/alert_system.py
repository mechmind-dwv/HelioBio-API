#!/usr/bin/env python3
"""
Sistema de generación de alertas para eventos heliobiológicos
Monitorea la actividad solar y biológica para emitir notificaciones
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

from app.config.settings import settings
from app.models.alerts import AlertEvent
from app.core.data_fetcher import SolarDataFetcher
from app.core.analyzer import AdvancedHeliobiologicalAnalyzer
from app.models.solar import SolarActivityLevel, SolarCyclePhase
from app.models.biological import BiologicalEvent

logger = logging.getLogger(__name__)

class AlertManager:
    """Gestor principal para el sistema de alertas"""

    def __init__(self):
        self.fetcher = SolarDataFetcher()
        self.analyzer = AdvancedHeliobiologicalAnalyzer()

    async def check_solar_activity_thresholds(self, latest_solar_data: Dict[str, Any]) -> List[AlertEvent]:
        """
        Verifica si los datos solares recientes superan los umbrales de alerta.
        """
        alerts = []
        if not settings.ALERT_SYSTEM_ENABLED:
            return alerts

        solar_data = latest_solar_data.get('noaa_solar', [])
        geomag_data = latest_solar_data.get('geomagnetic', [])
        
        latest_ssn = solar_data[-1].get('sunspot_number') if solar_data else None
        latest_kp = geomag_data[-1].get('kp_index') if geomag_data else None

        # Alerta por alto SSN
        if latest_ssn is not None and latest_ssn > settings.MIN_SSN_THRESHOLD_ALERT:
            alerts.append(AlertEvent(
                alert_id=f"SSN_HIGH_{datetime.now().strftime('%Y%m%d%H%M')}",
                alert_type="HIGH_SOLAR_ACTIVITY",
                timestamp=datetime.now(),
                message=f"Alerta: El número de manchas solares (SSN) ha superado el umbral. Valor actual: {latest_ssn}",
                source_data={"ssn": latest_ssn},
                severity="WARNING",
                triggered_by="ssn_threshold"
            ))

        # Alerta por alto índice Kp (tormenta geomagnética)
        if latest_kp is not None and latest_kp >= settings.MIN_KP_THRESHOLD_ALERT:
            alerts.append(AlertEvent(
                alert_id=f"KP_HIGH_{datetime.now().strftime('%Y%m%d%H%M')}",
                alert_type="GEOMAGNETIC_STORM",
                timestamp=datetime.now(),
                message=f"Alerta: Se detecta una tormenta geomagnética. Índice Kp actual: {latest_kp}",
                source_data={"kp_index": latest_kp},
                severity="CRITICAL",
                triggered_by="kp_threshold"
            ))
            
        return alerts

    async def check_for_chizhevsky_correlations(self, solar_data: List[SolarActivity], bio_events: List[BiologicalEvent]) -> List[AlertEvent]:
        """
        Verifica si hay correlaciones heliobiológicas significativas.
        """
        alerts = []
        if not settings.ALERT_SYSTEM_ENABLED or not bio_events:
            return alerts
            
        try:
            # Preparamos los datos para el análisis
            df = self.analyzer.prepare_time_series_data(solar_data, bio_events)

            # Buscamos correlaciones con un retraso
            result = self.analyzer.calculate_correlation(
                x=df['sunspot_number'],
                y=df['death_count'],
                method='cross_correlation'
            )

            # Si la correlación es significativa, disparamos una alerta
            if result.statistical_significance and abs(result.correlation_coefficient) > 0.5:
                alerts.append(AlertEvent(
                    alert_id=f"CHIZHEVSKY_CORRELATION_{datetime.now().strftime('%Y%m%d%H%M')}",
                    alert_type="HELIOBIOLOGICAL_CORRELATION_DETECTED",
                    timestamp=datetime.now(),
                    message=f"Alerta: Se ha detectado una correlación significativa (r={result.correlation_coefficient:.2f}) con un retraso de {result.lag_days} días entre las manchas solares y un evento biológico.",
                    source_data={
                        "correlation_result": result,
                        "bio_event_type": bio_events[0].event_type,
                    },
                    severity="WARNING",
                    triggered_by="statistical_correlation"
                ))
        except Exception as e:
            logger.error(f"Error checking for Chizhevsky correlations: {e}")
            
        return alerts

    async def run_alert_system(self):
        """
        Función principal para ejecutar el ciclo de alertas.
        """
        if not settings.ALERT_SYSTEM_ENABLED:
            logger.info("Alert system is disabled.")
            return

        logger.info("Starting alert system checks...")
        
        # 1. Obtener los últimos datos solares
        try:
            latest_solar_data = await self.fetcher.fetch_comprehensive_solar_data(years_back=2)
            
            # Convertir a Pydantic models para el análisis
            solar_activities = [SolarActivity.from_dict(d) for d in latest_solar_data['noaa_solar']]
            
            # 2. Verificar umbrales solares
            solar_alerts = await self.check_solar_activity_thresholds(latest_solar_data)
            
            # 3. Verificar correlaciones con datos biológicos (requiere datos de ejemplo)
            # bio_events_example = [BiologicalEvent(...)]  # Aquí iría la lógica para obtener datos biológicos
            # correlation_alerts = await self.check_for_chizhevsky_correlations(solar_activities, bio_events_example)

            all_alerts = solar_alerts # + correlation_alerts
            
            # 4. Procesar y enviar alertas
            if all_alerts:
                logger.warning(f"Total alerts generated: {len(all_alerts)}")
                for alert in all_alerts:
                    # Lógica para enviar notificaciones (email, webhook, etc.)
                    logger.warning(f"Alert: Type={alert.alert_type}, Severity={alert.severity}, Message={alert.message}")
            else:
                logger.info("No significant alerts triggered.")

        except Exception as e:
            logger.error(f"Alert system failed to run: {e}")
