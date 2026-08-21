import os
from fastapi import APIRouter, HTTPException, Request, status
from schemas.auth import LoginRequest, TokenResponse
from utils.auth import create_access_token
from dotenv import load_dotenv

from utils.rate_limiter import check_login_attempts, register_failed_attempt, reset_login_attempts


router = APIRouter(prefix="/auth", tags=["Autenticação"])

load_dotenv()

USERNAME = os.getenv("USERNAME") #MOCK
PASSWORD = os.getenv("PASSWORD") #MOCK
SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Exemplo simples de usuário fixo para testes
USER_MOCK = {USERNAME, PASSWORD}

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, request: Request):
    client_ip = request.client.host

    # 1. Verifica bloqueio baseado no IP + Usuário
    check_login_attempts(client_ip, credentials.username)

    # 2. Valida credenciais
    if credentials.username != USER_MOCK["username"] or credentials.password != USER_MOCK["password"]:
        register_failed_attempt(client_ip, credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos."
        )
    
    # 3. Reseta contador em caso de sucesso
    reset_login_attempts(client_ip, credentials.username)

    token = create_access_token(data={"sub": credentials.username})
    return {"access_token": token, "token_type": "bearer"}