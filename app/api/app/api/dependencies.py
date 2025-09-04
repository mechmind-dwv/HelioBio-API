# app/api/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

# ==================== DEPENDENCIAS ====================

# En una aplicación real, este token se obtendría de una base de datos o de un sistema de configuración.
# Para este ejemplo, usamos un token fijo.
API_TOKEN = "HelioBio-API-Secret-Key"

# Instancia de un esquema de seguridad de portador HTTP.
bearer_scheme = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """
    Dependencia de FastAPI para verificar la clave de la API en la cabecera de la solicitud.
    
    Esta función se encarga de:
    1. Obtener el token de autorización de la cabecera 'Authorization'.
    2. Comparar el token con una clave de API predefinida.
    3. Si el token no coincide, levanta una excepción HTTP 401.
    4. Si coincide, retorna el token, permitiendo que el endpoint se ejecute.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El esquema de autenticación debe ser 'Bearer'."
        )
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave de API inválida."
        )
    return credentials.credentials

def get_db_session() -> Dict[str, Any]:
    """
    Dependencia de ejemplo para una sesión de base de datos.
    
    En una aplicación real, esta función inicializaría una sesión de base de datos
    (por ejemplo, con SQLAlchemy o un cliente de Firestore) y la cerraría
    al finalizar la solicitud.
    """
    # Lógica de sesión de base de datos simulada.
    try:
        # Aquí iría el código para conectarse a la base de datos.
        db_session = {"status": "connected"}
        yield db_session
    finally:
        # Aquí iría el código para cerrar la conexión.
        print("Sesión de base de datos cerrada.")
