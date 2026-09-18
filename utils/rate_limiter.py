import os

import redis.asyncio as redis
from redis.exceptions import RedisError
from fastapi import HTTPException, status


# ============================================================
# CONFIGURAÇÃO DO REDIS
# ============================================================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True,
    socket_timeout=1
)


# ============================================================
# CONFIGURAÇÃO DO RATE LIMITING
# ============================================================

# Número máximo de tentativas incorretas
MAX_ATTEMPTS = 5

# Tempo durante o qual o bloqueio permanece ativo
BLOCK_DURATION_SECONDS = 60


# ============================================================
# CHAVE DO REDIS
# ============================================================

def get_client_key(ip: str, username: str) -> str:
    """
    Cria uma chave única para controlar as tentativas
    de login por endereço IP e e-mail.
    """

    return f"login_attempts:{ip}:{username}"


# ============================================================
# VERIFICAR LIMITE
# ============================================================

async def check_login_attempts(ip: str, username: str):
    """
    Verifica se o cliente já atingiu o limite
    de tentativas de autenticação.
    """

    try:

        key = get_client_key(ip, username)

        attempts = await redis_client.get(key)

        if attempts and int(attempts) >= MAX_ATTEMPTS:

            ttl = await redis_client.ttl(key)

            if ttl > 0:
                seconds_left = ttl
            else:
                seconds_left = BLOCK_DURATION_SECONDS

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Muitas tentativas incorretas. "
                    f"Acesso bloqueado temporariamente. "
                    f"Tente novamente em {seconds_left} segundo(s)."
                )
            )

    except RedisError:

        # Não ignoramos uma falha do mecanismo de segurança.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação temporariamente indisponível."
        )


# ============================================================
# REGISTRAR TENTATIVA INCORRETA
# ============================================================

async def register_failed_attempt(ip: str, username: str):
    """
    Incrementa o contador de tentativas incorretas.
    """

    try:

        key = get_client_key(ip, username)

        attempts = await redis_client.incr(key)

        # Define a expiração somente na primeira tentativa.
        if attempts == 1:
            await redis_client.expire(
                key,
                BLOCK_DURATION_SECONDS
            )

    except RedisError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação temporariamente indisponível."
        )


# ============================================================
# RESETAR TENTATIVAS
# ============================================================

async def reset_login_attempts(ip: str, username: str):
    """
    Remove o contador quando o login é realizado com sucesso.
    """

    try:

        key = get_client_key(ip, username)

        await redis_client.delete(key)

    except RedisError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação temporariamente indisponível."
        )