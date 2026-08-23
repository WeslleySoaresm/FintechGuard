
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
# Importe verify_token em vez de create_access_token
from utils.auth import verify_token

router = APIRouter(prefix="/predict", tags=["Predição de IA"])

# Schema de entrada para a requisição
class PredictRequest(BaseModel):
    ticket_description: str
    ticket_subject: str | None = None

# Schema de resposta
class PredictResponse(BaseModel):
    status: str
    predicted_category: str
    confidence: float

@router.post("", response_model=PredictResponse, status_code=status.HTTP_200_OK)
def predict_ticket_intent(
    payload: PredictRequest,
    current_user: dict = Depends(verify_token)  # Usa verify_token para validar o JWT
):
    """
    Endpoint placeholder para predição de intenção via IA.
    Requer autenticação JWT via Bearer Token.
    """
    # Lógica Mocked (Placeholder para a etapa de ML/Agentes de IA)
    return {
        "status": "success",
        "predicted_category": "Technical Issue",
        "confidence": 0.95
    }