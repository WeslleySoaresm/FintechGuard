
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

# Importa a função responsável por executar a previsão.
from fintechguard_agents.predict_intent import predict_intent

# Reutiliza a autenticação JWT existente no projeto.
from utils.auth import verify_token


# Cria um grupo de rotas para o classificador.
router = APIRouter(
    prefix="/classify",
    tags=["Intent Classification"]
)


# Define o formato de entrada da requisição.
class ClassificationRequest(BaseModel):
    # Rejeita campos extras e remove espaços desnecessários.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Mensagem enviada pelo cliente"
    )


# Define o formato da resposta.
class ClassificationResponse(BaseModel):
    intent: str
    confidence: float


# Endpoint protegido por autenticação JWT.
@router.post("/", response_model=ClassificationResponse)
def classify_message(
    request: ClassificationRequest,
    current_user: dict = Depends(verify_token)
):
    try:
        # Executa a classificação da mensagem.
        result = predict_intent(request.text)

        return ClassificationResponse(**result)

    except Exception:
        # Evita expor detalhes internos do modelo ao cliente.
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao classificar a mensagem."
        )
