
import logging
import re
import unicodedata

from fintechguard_agents.intent_classifier import classify_intent
from fintechguard_agents.predict_intent import predict_intent
from fintechguard_agents.security_analyzer import analyze_security
from fintechguard_agents.response_generator import generate_response
from fintechguard_agents.decision_engine import make_decision

logger = logging.getLogger(__name__)

ML_CONFIDENCE_THRESHOLD = 0.60

INTENT_MAPPING = {
    "billing inquiry": "Billing",
    "cancellation request": "Cancellation",
    "product inquiry": "Product Inquiry",
    "refund request": "Refund",
    "technical issue": "Technical Issue",
}

DOMAIN_TERMS = [
    "payment", "billing", "refund", "charge", "invoice",
    "cancel", "subscription", "product", "feature",
    "application", "app", "crash", "error", "transaction",
    "card", "account", "transfer", "loan", "credit",
    "cobranca", "fatura", "reembolso", "estorno",
    "pagamento", "cartao", "conta", "transferencia",
    "emprestimo", "credito", "aplicativo", "cancelar",
    "tarifa", "tarifas", "cobrado", "cobrada",
    "cobraram", "duplicada", "duplicado",
    "duas vezes", "dinheiro de volta",
]

LEGACY_INTENTS = {
    "Fraud",
    "Account Access",
    "Card",
    "Transaction",
    "Billing",
    "Refund",
    "Loan",
}


def normalize_domain_text(text: str) -> str:
    """Normaliza o texto, removendo acentos e padronizando espaços."""
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return re.sub(r"\s+", " ", text)


def contains_domain_term(message: str) -> bool:
    """Identifica termos bancários sem aceitar correspondências parciais."""
    normalized_message = normalize_domain_text(message)

    for term in DOMAIN_TERMS:
        normalized_term = normalize_domain_text(term)

        pattern = (
            r"(?<!\w)"
            + re.escape(normalized_term)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_message):
            return True

    return False


def classify_message(message: str) -> str:
    """
    Arquitetura híbrida:
    1. Preserva fraude e acesso à conta.
    2. Verifica se a mensagem pertence ao domínio bancário.
    3. Utiliza o modelo ML V2.
    4. Utiliza o classificador antigo como fallback.
    5. Retorna Other quando não há classificação adequada.
    """

    if not isinstance(message, str) or not message.strip():
        return "Other"

    # Classificação baseada em regras.
    rule_intent = classify_intent(message)

    # Preserva categorias críticas do classificador antigo.
    if rule_intent in {"Fraud", "Account Access"}:
        return rule_intent

    # Não força classificação bancária em mensagens fora do domínio.
    if not contains_domain_term(message):
        if rule_intent in LEGACY_INTENTS:
            return rule_intent

        return "Other"

    # Classificação pelo modelo de Machine Learning.
    try:
        prediction = predict_intent(message)

        predicted_intent = prediction.get("intent")
        confidence = float(prediction.get("confidence", 0.0))

        mapped_intent = INTENT_MAPPING.get(predicted_intent)

        if (
            mapped_intent
            and 0.0 <= confidence <= 1.0
            and confidence >= ML_CONFIDENCE_THRESHOLD
        ):
            return mapped_intent

        logger.warning(
            "Classificação ML não aceita. Intenção=%s, confiança=%.4f",
            predicted_intent,
            confidence,
        )

    except Exception:
        logger.exception(
            "Falha ao executar a classificação pelo modelo ML."
        )

    # Fallback para as regras antigas.
    if rule_intent in LEGACY_INTENTS:
        return rule_intent

    return "Other"


def process_message(message: str) -> dict:
    """Coordena classificação, segurança, decisão e resposta."""

    if not isinstance(message, str) or not message.strip():
        raise ValueError("A mensagem não pode estar vazia.")

    intent = classify_message(message)

    security = analyze_security(message)

    decision = make_decision(
        intent=intent,
        risk_level=security["risk_level"],
        requires_human=security["requires_human"],
    )

    response = generate_response(
        intent=intent,
        risk_level=security["risk_level"],
        requires_human=decision["requires_human"],
    )

    return {
        "intent": intent,
        "risk_level": security["risk_level"],
        "requires_human": decision["requires_human"],
        "action": decision["action"],
        "priority": decision["priority"],
        "response": response,
    }
