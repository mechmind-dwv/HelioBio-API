import sqlite3
from typing import List, Dict, Any
from app.database.connection import get_db_connection

class SolarRepository:
    """
    Gestiona las operaciones de la base de datos para los eventos solares.
    Esta capa de repositorio abstrae la lógica SQL de los servicios de negocio.
    """
    def __init__(self):
        self.conn = get_db_connection()

    def get_all_solar_events(self) -> List[Dict[str, Any]]:
        """
        Recupera todos los eventos solares registrados en la base de datos.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM solar_events ORDER BY start_time DESC")
            rows = cursor.fetchall()
            # En una aplicación real, se mapearían a objetos de modelo.
            return [{"id": row[0], "event_type": row[1], "start_time": row[2]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener eventos solares: {e}")
            return []

    def add_solar_event(self, event_data: Dict[str, Any]) -> int:
        """
        Agrega un nuevo evento solar a la base de datos.
        
        Args:
            event_data (dict): Un diccionario con los datos del evento.
        
        Returns:
            int: El ID del nuevo evento.
        """
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO solar_events (event_type, start_time, end_time, severity, region, geomagnetic_index)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (
                event_data.get("event_type"),
                event_data.get("start_time"),
                event_data.get("end_time"),
                event_data.get("severity"),
                event_data.get("region"),
                event_data.get("geomagnetic_index")
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al agregar evento solar: {e}")
            self.conn.rollback()
            return -1
