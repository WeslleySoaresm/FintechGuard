import os
import redis
from redis.exceptions import ConnectionError
from fastapi import HTTPException, status
import redis.asyncio as redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Adicionado socket_timeout para não travar a API se o Redis não responder
redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=0, 
    decode_responses=True,
    socket_timeout=1
)

MAX_ATTEMPTS = 3
BLOCK_DURATION_SECONDS = 180  # 3 minutos

def get_client_key(ip: str, username: str) -> str:
    return f"login_attempts:{ip}:{username}"

async def check_login_attempts(ip: str, username: str):
    try:
        key = get_client_key(ip, username)
        attempts = await redis_client.get(key)

        if attempts and int(attempts) >= MAX_ATTEMPTS:
            ttl = redis_client.ttl(key)
            minutes_left = (ttl // 60) + 1 if ttl > 0 else 1
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Muitas tentativas incorretas. Acesso bloqueado por mais {minutes_left} minuto(s)."
            )
    except ConnectionError:
        # Se o Redis falhar, permite a requisição passar sem derrubar o sistema
        pass

async def register_failed_attempt(ip: str, username: str):
    try:
        key = get_client_key(ip, username)
        attempts = await redis_client.incr(key)

        if attempts == 1:
           await redis_client.expire(key, BLOCK_DURATION_SECONDS)
    except ConnectionError:
        pass

async def reset_login_attempts(ip: str, username: str):
    try:
        key = get_client_key(ip, username)
        await redis_client.delete(key)
    except ConnectionError:
        pass