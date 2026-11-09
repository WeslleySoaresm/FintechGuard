
import os
import logging

import httpx
from dotenv import load_dotenv
from agents import function_tool

logger = logging.getLogger(__name__)

load_dotenv()

API_URL = os.getenv(
    "FINTECHGUARD_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

API_EMAIL = os.getenv("FINTECHGUARD_API_EMAIL")
API_PASSWORD = os.getenv("FINTECHGUARD_API_PASSWORD")


async def get_access_token(client: httpx.AsyncClient) -> str:
    """Autentica na API e retorna um JWT."""

    if not API_EMAIL or not API_PASSWORD:
        raise RuntimeError(
            "Configure FINTECHGUARD_API_EMAIL e "
            "FINTECHGUARD_API_PASSWORD no arquivo .env."
        )

    response = await client.post(
        f"{API_URL}/auth/token",
        json={
            "email": API_EMAIL,
            "password": API_PASSWORD
        }
    )

    response.raise_for_status()

    data = response.json()
    token = data.get("access_token")

    if not token:
        raise RuntimeError(
            "A API não retornou um access_token válido."
        )

    return token


@function_tool
async def classify_customer_message(text: str) -> dict:
    """
    Classifica uma mensagem de atendimento usando
    o endpoint protegido do FintechGuard.
    """

    if not text or not text.strip():
        raise ValueError("A mensagem não pode estar vazia.")

    url = f"{API_URL}/classify/"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:

            # 1. Autentica na API
            token = await get_access_token(client)

            # 2. Prepara a requisição protegida
            headers = {
                "Authorization": f"Bearer {token}"
            }

            payload = {
                "text": text.strip()
            }

            # 3. Solicita a classificação
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )

            response.raise_for_status()

            data = response.json()

            return {
                "intent": data["intent"],
                "confidence": data["confidence"]
            }

    except httpx.HTTPStatusError as error:
        logger.exception(
            "Erro HTTP ao consultar o classificador."
        )

        raise RuntimeError(
            f"Erro HTTP na API FintechGuard: "
            f"{error.response.status_code}."
        ) from error

    except httpx.RequestError as error:
        logger.exception(
            "Falha de conexão com a API FintechGuard."
        )

        raise RuntimeError(
            "Não foi possível conectar à API FintechGuard."
        ) from error

    except (KeyError, ValueError) as error:
        logger.exception(
            "Resposta inesperada do classificador."
        )

        raise RuntimeError(
            "A API retornou uma resposta em formato inesperado."
        ) from error
