from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@app.get("/solar-activity/sunspots", response_model=list[SolarActivity])
async def get_sunspots(start_date: str = "2000-01-01", end_date: str = "2023-12-31"):
    """
    Obtiene el índice de manchas solares para un rango de fechas.
    """
    df = fetch_sunspot_data(start_date, end_date)
    # ... lógica para procesar y devolver los datos en formato JSON
    return df.to_dict('records')
