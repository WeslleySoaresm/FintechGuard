
import os
import sys
from importlib.metadata import version, PackageNotFoundError

def diagnostico():
    pacotes = [
        "openai-agents",
        "openai",
        "pydantic",
        "pydantic-core",
    ]

    resultado = {
        "python": sys.version,
        "pacotes": {},
        "openai_api_key_configurada": bool(
            os.getenv("OPENAI_API_KEY")
        ),
        "openai_api_key_tamanho": len(
            os.getenv("OPENAI_API_KEY", "")
        ),
    }

    for pacote in pacotes:
        try:
            resultado["pacotes"][pacote] = version(pacote)
        except PackageNotFoundError:
            resultado["pacotes"][pacote] = "Não instalado"

    return resultado
