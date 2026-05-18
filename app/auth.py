"""Sistema de autenticación JWT para HelioBio-API"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET", "heliobio-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# Base de datos simulada (en producción usar BD real)
USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("heliobio2024"),
        "role": "admin",
        "email": "ia.mechmind@gmail.com"
    },
    "researcher": {
        "username": "researcher",
        "hashed_password": pwd_context.hash("chizhevsky"),
        "role": "researcher",
        "email": "researcher@heliobio.org"
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Dict:
    if credentials is None:
        return {"username": "anonymous", "role": "public"}
    try:
        payload = decode_token(credentials.credentials)
        username = payload.get("sub")
        if username in USERS_DB:
            return {"username": username, "role": USERS_DB[username]["role"]}
    except HTTPException:
        pass
    return {"username": "anonymous", "role": "public"}

async def require_admin(user: Dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return user

async def require_auth(user: Dict = Depends(get_current_user)):
    if user.get("role") == "public":
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    return user
