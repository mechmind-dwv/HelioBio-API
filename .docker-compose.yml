version: '3.8'

services:
  # Servicio de la aplicación principal (FastAPI)
  app:
    build: .
    container_name: heliobio-api
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    depends_on:
      - db
    networks:
      - heliobio-network

  # Servicio de la base de datos PostgreSQL
  db:
    image: postgres:16.1-alpine
    container_name: heliobio-db
    restart: always
    env_file:
      - .env
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - heliobio-network

# Definición de redes para la comunicación interna entre servicios
networks:
  heliobio-network:
    driver: bridge

# Definición de volúmenes para persistir los datos
volumes:
  postgres-data:
