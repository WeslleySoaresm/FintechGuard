
import joblib
from pathlib import Path

# Diretório onde está este arquivo.
BASE_DIR = Path(__file__).resolve().parent

# O agente passa a utilizar o modelo V2.
MODEL_PATH = BASE_DIR / "intent_classifier_v2.joblib"

# Carrega o modelo uma única vez.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Modelo de classificação não encontrado: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


def predict_intent(text: str) -> dict:
    """
    Classifica uma mensagem e retorna a intenção
    prevista e o nível de confiança do modelo.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("A mensagem não pode estar vazia.")

    probabilities = model.predict_proba([text])[0]
    classes = model.classes_
    best_index = probabilities.argmax()

    return {
        "intent": str(classes[best_index]),
        "confidence": round(
            float(probabilities[best_index]),
            4
        )
    }
