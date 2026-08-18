import os
from fastapi import APIRouter, HTTPException, status
from schemas.auth import LoginRequest, TokenResponse
from utils.auth import create_access_token
from dotenv import load_dotenv


router = APIRouter(prefix="/auth", tags=["Autenticação"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Exemplo simples de usuário fixo para testes
USER_MOCK = {"username": "admin", "password": "secretpassword"}

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if credentials.username != USER_MOCK["username"] or credentials.password != USER_MOCK["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos."
        )
    
    token = create_access_token(data={"sub": credentials.username})
    return {"access_token": token, "token_type": "bearer"}