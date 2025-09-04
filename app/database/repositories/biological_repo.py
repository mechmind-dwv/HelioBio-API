import sqlite3
from typing import List, Dict, Any
from app.database.connection import get_db_connection

class BiologicalRepository:
    """
    Gestiona las operaciones de la base de datos para los datos biológicos.
    """
    def __init__(self):
        self.conn = get_db_connection()

    def add_biological_data(self, data: Dict[str, Any]) -> int:
        """
        Agrega un nuevo registro de datos biológicos a la base de datos.
        
        Args:
            data (dict): Un diccionario con los datos de observación biológica.
        
        Returns:
            int: El ID del nuevo registro.
        """
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO biological_data (organism_type, observation_date, event_description, response_level)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (
                data.get("organism_type"),
                data.get("observation_date"),
                data.get("event_description"),
                data.get("response_level")
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al agregar datos biológicos: {e}")
            self.conn.rollback()
            return -1

    def get_recent_biological_data(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Recupera los registros biológicos más recientes.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM biological_data ORDER BY observation_date DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [{"id": row[0], "organism_type": row[1], "observation_date": row[2]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener datos biológicos recientes: {e}")
            return []
