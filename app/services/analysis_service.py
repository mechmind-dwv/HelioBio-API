from app.database.repositories.solar_repo import SolarRepository
from app.database.repositories.biological_repo import BiologicalRepository
from app.database.repositories.analysis_repo import AnalysisRepository
from app.services.notification_service import NotificationService
from typing import Dict, Any

class AnalysisService:
    """
    Implementa la lógica de negocio para el análisis de correlación.
    Coordina las operaciones entre los repositorios y los servicios de notificación.
    """
    def __init__(self):
        self.solar_repo = SolarRepository()
        self.biological_repo = BiologicalRepository()
        self.analysis_repo = AnalysisRepository()
        self.notification_service = NotificationService()

    def run_correlation_analysis(self) -> Dict[str, Any]:
        """
        Ejecuta el análisis de correlación entre datos solares y biológicos.
        
        Returns:
            Dict[str, Any]: Un diccionario con el resultado del análisis.
        """
        print("Iniciando análisis de correlación entre eventos solares y datos biológicos...")
        
        # Simula la obtención de datos de ambos repositorios
        solar_data = self.solar_repo.get_all_solar_events()
        biological_data = self.biological_repo.get_recent_biological_data()

        # Simula el algoritmo de correlación
        if solar_data and biological_data:
            correlation_score = 0.95 # Simulación de un resultado de alta correlación
            analysis_result = {
                "solar_event_id": solar_data[0]['id'],
                "biological_data_ids": [d['id'] for d in biological_data],
                "correlation_score": correlation_score,
                "notes": "Fuerte correlación detectada."
            }
            
            # Guarda el resultado del análisis
            self.analysis_repo.save_analysis_result(analysis_result)
            
            # Si la correlación es alta, envía una alerta
            if correlation_score > 0.8:
                alert_message = f"ALERTA: Fuerte correlación detectada (Score: {correlation_score}) entre la actividad solar y los datos biológicos recientes."
                self.notification_service.send_alert(alert_message)
                
            return analysis_result
        else:
            return {"status": "Error", "message": "No hay suficientes datos para realizar el análisis."}
