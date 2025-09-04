# app/config/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

# Crea un motor de base de datos asíncrono. La URL se obtiene de las configuraciones.
engine = create_async_engine(
    settings.DATABASE_URL.unicode_string(),
    pool_size=20,  # Tamaño del pool de conexiones
    max_overflow=0,
    future=True
)

# Configura una factoría de sesiones asíncrona.
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base para los modelos declarativos de SQLAlchemy.
# Todos los modelos de la base de datos heredarán de esta base.
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos en los endpoints.
async def get_db_session():
    """
    Proporciona una sesión de base de datos asíncrona.
    Se usa como una dependencia en las rutas de la API.
    """
    async with AsyncSessionLocal() as session:
        yield session
