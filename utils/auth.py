import os
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from sqlmodel import Session, select

from data.db import engine
from models.model_events import User


# Carrega as variáveis do arquivo .env
load_dotenv(override=True)


SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)


security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """
    Cria um token JWT com tempo de expiração.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Valida o JWT e recupera o usuário correspondente no banco.
    """

    token = credentials.credentials

    try:
        # 1. Decodifica e valida o JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # 2. Recupera o identificador do usuário
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token não contém identificação do usuário.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Converte o ID do JWT para inteiro
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identificação do usuário inválida.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 4. Consulta o usuário no banco
        with Session(engine) as session:

            statement = select(User).where(
                User.id == user_id
            )

            user = session.exec(statement).first()

        # 5. Usuário precisa existir
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 6. Retorna somente informações necessárias
        return {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
        }

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )