import os
from fastapi import APIRouter, HTTPException, Request, status
from schemas.auth import LoginRequest, TokenResponse
from utils.auth import create_access_token
from dotenv import load_dotenv

from utils.rate_limiter import check_login_attempts, register_failed_attempt, reset_login_attempts


router = APIRouter(prefix="/auth", tags=["Autenticação"])

load_dotenv(override=True)

# Carrega as variáveis do .env com fallbacks de segurança para não quebrar o código
MOCK_USERNAME = os.getenv("USERNAME", "admin")
MOCK_PASSWORD = os.getenv("PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Exemplo simples de usuário fixo para testes
USER_MOCK = {
    "username": MOCK_USERNAME.strip(),
    "password": MOCK_PASSWORD.strip()
}

@router.post("/token", response_model=TokenResponse)
async def login(credentials: LoginRequest, request: Request):
    client_ip = request.client.host
    # Normaliza o username removendo espaços extras nas pontas
    clean_username = credentials.username.strip()
    clean_password = credentials.password.strip()
    
    
    
    # 1. Verifica bloqueio baseado no IP + Usuário
    await check_login_attempts(client_ip, clean_username)

    # 2. Valida credenciais
    if clean_username != USER_MOCK["username"] or clean_password != USER_MOCK["password"]:
        await register_failed_attempt(client_ip, clean_username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos."
        )
    
    # 3. Reseta contador em caso de sucesso
    await reset_login_attempts(client_ip, clean_username)

    token = create_access_token(data={"sub": clean_username})
    return {"access_token": token, "token_type": "bearer"}