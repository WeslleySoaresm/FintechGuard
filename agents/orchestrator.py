from agents.intent_classifier import classify_intent
from agents.security_analyzer import analyze_security
from agents.response_generator import generate_response


def process_message(message: str) -> dict:
    # 1. Identifica a intenção do cliente
    intent = classify_intent(message)

    # 2. Analisa o risco da mensagem
    security = analyze_security(message)

    # 3. Gera uma resposta adequada
    response = generate_response(
        intent=intent,
        risk_level=security["risk_level"],
        requires_human=security["requires_human"],
    )

    # 4. Reúne os resultados
    return {
        "intent": intent,
        "risk_level": security["risk_level"],
        "requires_human": security["requires_human"],
        "response": response,
    }