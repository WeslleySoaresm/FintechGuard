
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from fintechguard_agents.predict_intent import predict_intent
from utils.auth import verify_token


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/classify",
    tags=["Intent Classification"],
)


class ClassificationRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Mensagem enviada pelo cliente",
    )


class ClassificationResponse(BaseModel):
    intent: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


@router.post(
    "/",
    response_model=ClassificationResponse,
    status_code=status.HTTP_200_OK,
)
def classify_message(
    request: ClassificationRequest,
    current_user: dict = Depends(verify_token),
):
    try:
        result = predict_intent(request.text)

        return ClassificationResponse(**result)

    except ValueError as error:
        logger.warning(
            "Mensagem inválida enviada ao classificador: %s",
            error,
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível classificar a mensagem enviada.",
        ) from error

    except Exception as error:
        logger.exception(
            "Erro interno durante a classificação de intenção."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao classificar a mensagem.",
        ) from error
