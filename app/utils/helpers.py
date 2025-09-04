# app/utils/helpers.py

from datetime import datetime, date
from typing import Any

def is_valid_date(date_string: str) -> bool:
    """
    Verifica si una cadena es una fecha válida.
    
    Args:
        date_string (str): La cadena de fecha a verificar.
        
    Returns:
        bool: True si la cadena es una fecha válida, False en caso contrario.
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def convert_to_isoformat(input_date: Any) -> str:
    """
    Convierte un objeto de fecha/hora a un string en formato ISO.
    
    Args:
        input_date (Any): El objeto de fecha a convertir.
        
    Returns:
        str: La fecha en formato ISO 8601.
    """
    if isinstance(input_date, (datetime, date)):
        return input_date.isoformat()
    return str(input_date)
    
def log_message(message: str, level: str = "INFO"):
    """
    Simula el registro de un mensaje.
    
    Args:
        message (str): El mensaje a registrar.
        level (str): El nivel del mensaje (INFO, WARNING, ERROR).
    """
    current_time = datetime.now().isoformat()
    print(f"[{level}] [{current_time}] {message}")
