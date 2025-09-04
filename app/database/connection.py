# app/database/connection.py

from typing import Dict, Any

class DatabaseManager:
    """
    Clase para gestionar la conexión a la base de datos.
    
    Este diseño permite una fácil migración a diferentes bases de datos
    o el uso de un pool de conexiones en el futuro.
    """
    def __init__(self):
        self._connection = None

    def connect(self) -> Dict[str, Any]:
        """
        Establece una conexión simulada con la base de datos.
        
        En una aplicación real, aquí iría la lógica para conectarse a una
        base de datos específica, como MySQL, PostgreSQL, o Firestore,
        utilizando las credenciales de configuración.
        """
        if self._connection is None:
            # Simulación de la conexión
            print("Estableciendo conexión a la base de datos...")
            self._connection = {"status": "connected", "type": "mock_db"}
        return self._connection

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self._connection:
            print("Cerrando la conexión a la base de datos...")
            self._connection = None

# Una instancia global del gestor de base de datos para ser importada
db_manager = DatabaseManager()

def get_db_connection() -> Dict[str, Any]:
    """
    Función de utilidad para obtener la conexión a la base de datos.
    
    Otros módulos, como los repositorios, la usarán para interactuar con la DB.
    """
    return db_manager.connect()
