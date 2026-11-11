
import logging
from pathlib import Path

import joblib

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "intent_classifier_v3.joblib"

if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"Modelo de classificação não encontrado: {MODEL_PATH}"
    )

try:
    model = joblib.load(MODEL_PATH)
except Exception as error:
    logger.exception("Não foi possível carregar o modelo de classificação.")
    raise RuntimeError(
        "Falha ao carregar o modelo de classificação."
    ) from error


def predict_intent(text: str) -> dict:
    """
    Classifica uma mensagem usando o modelo ML V2.

    Retorna:
        {
            "intent": str,
            "confidence": float
        }
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("A mensagem não pode estar vazia.")

    if not hasattr(model, "predict_proba"):
        raise RuntimeError(
            "O modelo carregado não oferece suporte a predict_proba."
        )

    probabilities = model.predict_proba([text])[0]
    classes = model.classes_

    if len(probabilities) != len(classes):
        raise RuntimeError(
            "A saída do modelo não corresponde às classes disponíveis."
        )

    best_index = int(probabilities.argmax())

    confidence = float(probabilities[best_index])
    intent = str(classes[best_index])

    if not 0.0 <= confidence <= 1.0:
        raise RuntimeError(
            "O modelo retornou um nível de confiança inválido."
        )

    return {
        "intent": intent,
        "confidence": round(confidence, 4),
    }
