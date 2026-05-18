# Imagen base Python optimizada
FROM python:3.12-slim

# Metadatos del proyecto
LABEL maintainer="ia.mechmind@gmail.com"
LABEL description="HelioBio-API - Sistema Avanzado de Análisis Heliobiológico"
LABEL version="3.0.0"

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes científicos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/cache data/logs data/models data/exports

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV HOST=0.0.0.0
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
