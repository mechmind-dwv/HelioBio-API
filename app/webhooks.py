"""Sistema de Webhooks para HelioBio-API"""
from typing import List, Dict, Optional
import json
import aiohttp
from datetime import datetime

# Almacenamiento simple (en producción usar BD)
_webhook_subscribers: List[Dict] = []

async def register_webhook(url: str, events: List[str] = None) -> Dict:
    """Registra un nuevo webhook"""
    webhook = {
        "id": len(_webhook_subscribers) + 1,
        "url": url,
        "events": events or ["alert", "solar_update"],
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    _webhook_subscribers.append(webhook)
    return webhook

async def list_webhooks() -> List[Dict]:
    """Lista todos los webhooks registrados"""
    return _webhook_subscribers

async def delete_webhook(webhook_id: int) -> bool:
    """Elimina un webhook"""
    global _webhook_subscribers
    _webhook_subscribers = [w for w in _webhook_subscribers if w["id"] != webhook_id]
    return True

async def trigger_webhooks(event_type: str, payload: Dict) -> int:
    """Dispara webhooks para un evento específico"""
    triggered = 0
    async with aiohttp.ClientSession() as session:
        for webhook in _webhook_subscribers:
            if webhook["active"] and event_type in webhook["events"]:
                try:
                    async with session.post(
                        webhook["url"],
                        json={"event": event_type, "data": payload, "timestamp": datetime.now().isoformat()},
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as resp:
                        if resp.status == 200:
                            triggered += 1
                except Exception:
                    pass
    return triggered
