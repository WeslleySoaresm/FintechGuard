import os
import redis
from fastapi import HTTPException, status

# Lê o host das variáveis de ambiente. Se não existir, usa 'localhost'
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

MAX_ATTEMPTS = 3
BLOCK_DURATION_SECONDS = 180  # 3 minutos


def get_client_key(ip: str, username: str) -> str:
    return f"login_attempts:{ip}:{username}"


def check_login_attempts(ip: str, username: str):
    key = get_client_key(ip, username)
    attempts = redis_client.get(key)

    if attempts and int(attempts) >= MAX_ATTEMPTS:
        ttl = redis_client.ttl(key)
        minutes_left = (ttl // 60) + 1 if ttl > 0 else 1
        
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Muitas tentativas incorretas. Acesso bloqueado por mais {minutes_left} minuto(s)."
        )


def register_failed_attempt(ip: str, username: str):
    key = get_client_key(ip, username)
    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(key, BLOCK_DURATION_SECONDS)


def reset_login_attempts(ip: str, username: str):
    key = get_client_key(ip, username)
    redis_client.delete(key)