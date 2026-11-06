from agents.intent_classifier import normalize_text


CRITICAL_KEYWORDS = [
    "senha",
    "palavra passe",
    "codigo de autenticacao",
    "codigo de verificacao",
    "codigo sms",
    "token",
    "cvv",
    "cvc",
    "numero completo do cartao",
    "numero do cartao",
    "dados bancarios",
]

HIGH_RISK_KEYWORDS = [
    "fraude",
    "cartao clonado",
    "cartao foi clonado",
    "compra nao reconhecida",
    "nao reconheco essa compra",
    "transacao suspeita",
    "movimentacao desconhecida",
    "nao fui eu",
    "conta invadida",
    "conta hackeada",
    "roubaram meu cartao",
    "perdi meu cartao",
    "desbloquear meu cartao",
    "alterar meus dados bancarios",
    "transferir dinheiro",
    
]

MEDIUM_RISK_KEYWORDS = [
    "cobranca indevida",
    "valor incorreto",
    "saldo incorreto",
    "nao recebi meu reembolso",
    "problema com pagamento",
]


def analyze_security(message: str) -> dict:
    normalized_message = normalize_text(message)

    if any(keyword in normalized_message for keyword in CRITICAL_KEYWORDS):
        return {
            "risk_level": "critical",
            "requires_human": True,
        }

    if any(keyword in normalized_message for keyword in HIGH_RISK_KEYWORDS):
        return {
            "risk_level": "high",
            "requires_human": True,
        }

    if any(keyword in normalized_message for keyword in MEDIUM_RISK_KEYWORDS):
        return {
            "risk_level": "medium",
            "requires_human": False,
        }

    return {
        "risk_level": "low",
        "requires_human": False,
    }