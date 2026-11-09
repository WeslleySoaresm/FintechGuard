
import unicodedata

from fintechguard_agents.intent_classifier import classify_intent
from fintechguard_agents.predict_intent import predict_intent
from fintechguard_agents.security_analyzer import analyze_security
from fintechguard_agents.response_generator import generate_response
from fintechguard_agents.decision_engine import make_decision

# Confiança mínima exigida para aceitar a classificação do modelo ML.
ML_CONFIDENCE_THRESHOLD = 0.60


# Converte as categorias do modelo ML para as categorias
# utilizadas pelo restante da aplicação.
INTENT_MAPPING = {
    "billing inquiry": "Billing",
    "cancellation request": "Cancellation",
    "product inquiry": "Product Inquiry",
    "refund request": "Refund",
    "technical issue": "Technical Issue",
}


# Termos que identificam mensagens relacionadas ao domínio bancário.
# Os termos são armazenados sem acentos.
DOMAIN_TERMS = [
    "payment",
    "billing",
    "refund",
    "charge",
    "invoice",
    "cancel",
    "subscription",
    "product",
    "feature",
    "application",
    "app",
    "crash",
    "error",
    "transaction",
    "card",
    "account",
    "transfer",
    "loan",
    "credit",
    "cobranca",
    "fatura",
    "reembolso",
    "estorno",
    "pagamento",
    "cartao",
    "conta",
    "transferencia",
    "emprestimo",
    "credito",
    "aplicativo",
    "cancelar",
    "tarifa",
    "tarifas",
    "cobrado",
    "cobrada",
    "cobraram",
    "cobrança",
    "duplicada",
    "duplicado",
    "duas vezes",
    "dinheiro de volta",
    "estorno",
]


# Categorias preservadas pelo classificador antigo.
# Funcionam como fallback caso o modelo ML não tenha
# confiança suficiente para classificar a mensagem.
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
    """
    Normaliza o texto para facilitar a identificação
    de termos bancários, removendo acentos e espaços externos.
    """

    text = text.lower().strip()

    text = unicodedata.normalize("NFD", text)

    return "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )


def classify_message(message: str) -> str:
    """
    Classifica uma mensagem utilizando uma arquitetura híbrida:

    1. Regras antigas para fraude e acesso à conta.
    2. Verificação de termos relacionados ao domínio bancário.
    3. Modelo de Machine Learning para as cinco categorias treinadas.
    4. Regras antigas como fallback quando necessário.
    5. Categoria Other quando não houver classificação adequada.
    """

    # 1. Executa o classificador baseado em regras.
    rule_intent = classify_intent(message)

    # 2. Preserva as regras críticas de fraude e acesso à conta.
    if rule_intent in {"Fraud", "Account Access"}:
        return rule_intent

    # 3. Normaliza o texto para remover diferenças de acentuação.
    normalized_message = normalize_domain_text(message)

    # 4. Verifica se a mensagem pertence ao domínio bancário.
    has_domain_term = any(
        term in normalized_message
        for term in DOMAIN_TERMS
    )

    # Se não for uma mensagem bancária, não força uma classificação.
    if not has_domain_term:
        if rule_intent in LEGACY_INTENTS:
            return rule_intent

        return "Other"

    # 5. Tenta classificar utilizando o modelo de Machine Learning.
    try:
        prediction = predict_intent(message)

        predicted_intent = prediction["intent"]
        confidence = prediction["confidence"]

        # Converte a categoria do modelo para a categoria da aplicação.
        mapped_intent = INTENT_MAPPING.get(predicted_intent)

        # Aceita a previsão somente quando a confiança é suficiente.
        if mapped_intent and confidence >= ML_CONFIDENCE_THRESHOLD:
            return mapped_intent

    except Exception:
        # Se o modelo falhar, a aplicação continua utilizando
        # as regras antigas como mecanismo alternativo.
        pass

    # 6. Fallback para as regras antigas.
    if rule_intent in LEGACY_INTENTS:
        return rule_intent

    # 7. Não foi possível classificar com segurança.
    return "Other"


def process_message(message: str) -> dict:
    """
    Coordena a análise da mensagem e a decisão do agente.
    """

    # 1. Identifica a intenção do cliente.
    intent = classify_message(message)

    # 2. Avalia o risco de segurança.
    security = analyze_security(message)

    # 3. Decide qual ação deve ser executada.
    decision = make_decision(
        intent=intent,
        risk_level=security["risk_level"],
        requires_human=security["requires_human"],
    )

    # 4. Gera a resposta adequada.
    response = generate_response(
        intent=intent,
        risk_level=security["risk_level"],
        requires_human=decision["requires_human"],
    )

    # 5. Retorna o resultado completo.
    return {
        "intent": intent,
        "risk_level": security["risk_level"],
        "requires_human": decision["requires_human"],
        "action": decision["action"],
        "priority": decision["priority"],
        "response": response,
    }