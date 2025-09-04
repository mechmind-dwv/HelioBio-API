from typing import List, Dict, Any
from app.database.repositories.solar_repo import SolarRepository

class SolarService:
    """
    Gestiona la lógica de negocio para los eventos solares.
    Se comunica con el repositorio para obtener o guardar datos.
    """
    def __init__(self):
        self.solar_repo = SolarRepository()

    def get_latest_data(self, count: int) -> List[Dict[str, Any]]:
        """
        Obtiene los eventos solares más recientes del repositorio.
        
        Args:
            count (int): El número de eventos a recuperar.
            
        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios con los eventos solares.
        """
        print(f"Obteniendo los {count} eventos solares más recientes...")
        # Lógica de negocio adicional, como filtrado o validación, podría ir aquí.
        return self.solar_repo.get_all_solar_events()

    def add_new_event(self, event_data: Dict[str, Any]) -> int:
        """
        Añade un nuevo evento solar.
        
        Args:
            event_data (dict): Los datos del evento.
            
        Returns:
            int: El ID del evento recién creado.
        """
        print(f"Validando y añadiendo un nuevo evento solar: {event_data['event_type']}")
        # Lógica de validación de datos podría ir aquí antes de guardar en el repositorio.
        return self.solar_repo.add_solar_event(event_data)
