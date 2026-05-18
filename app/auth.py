"""Sistema de autenticación JWT para HelioBio-API"""
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET", "heliobio-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

security = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed

USERS_DB = {
    "admin": {"username": "admin", "hashed_password": hash_password("heliobio2024"), "role": "admin"},
    "researcher": {"username": "researcher", "hashed_password": hash_password("chizhevsky"), "role": "researcher"},
}

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Dict:
    if credentials is None:
        return {"username": "anonymous", "role": "public"}
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username in USERS_DB:
            return {"username": username, "role": USERS_DB[username]["role"]}
    except JWTError:
        pass
    return {"username": "anonymous", "role": "public"}

async def require_admin(user: Dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin requerido")
    return user
