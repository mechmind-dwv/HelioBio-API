# config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from functools import lru_cache

class Settings(BaseSettings):
    """
    Clase de configuración de la aplicación que carga las variables de entorno.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore' # Ignora claves no declaradas en el modelo
    )

    PROJECT_NAME: str = "HelioBio-API"
    PROJECT_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # Configuración de la Base de Datos
    DATABASE_URL: PostgresDsn
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    # Configuración de Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # URLs de Fuentes de Datos
    SILSO_SUNSPOT_URL: str
    NOAA_SOLAR_URL: str
    NOAA_GEOMAG_URL: str

@lru_cache()
def get_settings():
    """
    Función de utilidad para obtener una instancia de Settings en caché.
    Esto previene la sobrecarga de leer el archivo .env repetidamente.
    """
    return Settings()

settings = get_settings()
