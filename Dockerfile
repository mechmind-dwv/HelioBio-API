# Usa una imagen base de Python oficial, que es ligera y optimizada
FROM python:3.10-slim-buster

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos y los instala para aprovechar el caché de capas de Docker
# Esto acelera las reconstrucciones si el requirements.txt no ha cambiado
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente de la aplicación al directorio de trabajo del contenedor
COPY . .

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn, el servidor ASGI
# La bandera --host 0.0.0.0 permite que la aplicación sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
