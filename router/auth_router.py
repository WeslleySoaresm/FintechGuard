from fastapi import APIRouter, HTTPException, Request, status
from sqlmodel import Session, select
import bcrypt

from schemas.auth import LoginRequest, TokenResponse
from utils.auth import create_access_token
from utils.rate_limiter import (
    check_login_attempts,
    register_failed_attempt,
    reset_login_attempts,
)
from data.db import engine
from models.model_events import User


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)




@router.post(
    "/token",
    response_model=TokenResponse
)
async def login(
    credentials: LoginRequest,
    request: Request
):
    """
    Autentica um usuário utilizando e-mail e senha
    e retorna um token JWT.
    """

    # ---------------------------------------------------------
    # 1. Identifica o cliente
    # ---------------------------------------------------------

    client_ip = request.client.host


    # ---------------------------------------------------------
    # 2. Normaliza o e-mail e a senha
    # ---------------------------------------------------------

    clean_email = credentials.email.strip().lower()
    clean_password = credentials.password.strip()


    # ---------------------------------------------------------
    # 3. Verifica o rate limiting
    # ---------------------------------------------------------

    await check_login_attempts(
        client_ip,
        clean_email
    )


    # ---------------------------------------------------------
    # 4. Busca o usuário pelo e-mail
    # ---------------------------------------------------------

    with Session(engine) as session:

        statement = select(User).where(
            User.email == clean_email
        )

        user = session.exec(statement).first()


    # ---------------------------------------------------------
    # 5. Verifica usuário e senha
    # ---------------------------------------------------------

    if user is None or not bcrypt.checkpw(
    clean_password.encode("utf-8"),
    user.password_hash.encode("utf-8")
    ):

        await register_failed_attempt(
            client_ip,
            clean_email
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    # ---------------------------------------------------------
    # 6. Login realizado com sucesso
    # ---------------------------------------------------------

    await reset_login_attempts(
        client_ip,
        clean_email
    )


    # ---------------------------------------------------------
    # 7. Cria o JWT
    # ---------------------------------------------------------

    token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )


    # ---------------------------------------------------------
    # 8. Retorna o token
    # ---------------------------------------------------------

    return {
        "access_token": token,
        "token_type": "bearer"
    }