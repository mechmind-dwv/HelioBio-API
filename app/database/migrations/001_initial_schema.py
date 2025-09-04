# app/database/migrations/001_initial_schema.py

import sqlite3 # Usamos SQLite3 como ejemplo de una base de datos simple
from typing import Callable, Any

# Funciones de utilidad para simular el proceso de migración
def execute_sql(conn: sqlite3.Connection, sql_script: str):
    """Ejecuta un script SQL."""
    try:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        print("Script SQL ejecutado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el script SQL: {e}")
        conn.rollback()

def up(conn: sqlite3.Connection):
    """
    Función 'up' para la migración.
    Crea las tablas iniciales para los datos solares y biológicos.
    """
    print("Aplicando migración 001: Creando el esquema inicial...")

    # SQL para crear la tabla de eventos solares
    solar_table_sql = """
    CREATE TABLE IF NOT EXISTS solar_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME,
        severity TEXT,
        region TEXT,
        geomagnetic_index REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    # SQL para crear la tabla de datos biológicos
    biological_table_sql = """
    CREATE TABLE IF NOT EXISTS biological_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organism_type TEXT NOT NULL,
        observation_date DATETIME NOT NULL,
        event_description TEXT,
        response_level INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    execute_sql(conn, solar_table_sql)
    execute_sql(conn, biological_table_sql)

    print("Migración 001 aplicada.")


def down(conn: sqlite3.Connection):
    """
    Función 'down' para la migración.
    Elimina las tablas creadas por la migración 'up'.
    """
    print("Revirtiendo migración 001: Eliminando tablas...")

    drop_solar_table_sql = "DROP TABLE IF EXISTS solar_events;"
    drop_biological_table_sql = "DROP TABLE IF EXISTS biological_data;"
    
    execute_sql(conn, drop_solar_table_sql)
    execute_sql(conn, drop_biological_table_sql)

    print("Migración 001 revertida.")
