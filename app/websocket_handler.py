"""WebSocket para streaming de datos en tiempo real"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)
    
    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)
    
    async def broadcast(self, data: dict):
        for conn in self.active_connections:
            try:
                await conn.send_json(data)
            except:
                pass

manager = ConnectionManager()

async def stream_solar_data(ws: WebSocket):
    """Streaming de datos solares en tiempo real"""
    await manager.connect(ws)
    try:
        while True:
            from app.main import fetch_solar_data
            end = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now().strftime("%Y-%m-%d"))
            df = await fetch_solar_data(start, end)
            if len(df) > 0:
                last = df.iloc[-1]
                await ws.send_json({
                    "timestamp": datetime.now().isoformat(),
                    "ssn": float(last['sunspot_number']),
                    "classification": str(last['classification']),
                    "alert": "ALTA" if last['sunspot_number'] > 100 else "MODERADA" if last['sunspot_number'] > 50 else "BAJA"
                })
            await asyncio.sleep(60)  # Actualizar cada minuto
    except WebSocketDisconnect:
        manager.disconnect(ws)
