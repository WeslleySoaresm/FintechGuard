
import pytest

# Importa a função que utiliza o modelo treinado.
from fintechguard_agents.predict_intent import predict_intent


# Agrupa exemplos de mensagens e suas intenções esperadas.
@pytest.mark.parametrize(
    "message, expected_intent",
    [
        (
            "I want to know the details of my last payment.",
            "billing inquiry"
        ),
        (
            "I want to cancel my subscription.",
            "cancellation request"
        ),
        (
            "What features does this product offer?",
            "product inquiry"
        ),
        (
            "I want to request a refund for my payment.",
            "refund request"
        ),
        (
            "My application keeps crashing when I try to log in.",
            "technical issue"
        ),
    ]
)
def test_predict_intent(message, expected_intent):
    # Executa a previsão utilizando o modelo treinado.
    result = predict_intent(message)

    # Confirma que a intenção retornada é a esperada.
    assert result["intent"] == expected_intent

    # Confirma que a confiança está dentro do intervalo permitido.
    assert 0 <= result["confidence"] <= 1


def test_predict_intent_returns_valid_structure():
    # Verifica se a função retorna os campos necessários.
    result = predict_intent(
        "I need help with my account payment."
    )

    assert "intent" in result
    assert "confidence" in result


@pytest.mark.parametrize(
    "invalid_message",
    [
        "",
        "   ",
    ]
)
def test_predict_intent_rejects_empty_message(invalid_message):
    # Mensagens vazias não devem chegar ao modelo.
    with pytest.raises(ValueError):
        predict_intent(invalid_message)
