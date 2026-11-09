
from fintechguard_agents.intent_classifier import normalize_text


CRITICAL_KEYWORDS = [
    # Credenciais e informações altamente sensíveis
    "palavra passe",
    "codigo de autenticacao",
    "codigo de verificacao",
    "codigo sms",
    "token",
    "cvv",
    "cvc",
    "numero completo do cartao",
    "numero do cartao",

    # English
    "authentication code",
    "verification code",
    "security code",
]
SUSPICIOUS_CREDENTIAL_PATTERNS = [
    "pedindo minha senha",
    "pediu minha senha",
    "solicitou minha senha",
    "quer minha senha",
    "pedindo meu codigo",
    "pediu meu codigo",
    "solicitou meu codigo",
    "quer meu codigo",
    "compartilhei minha senha",
    "enviei minha senha",
    "informei minha senha",
    "passei minha senha",
    "minha senha foi roubada",
    "roubaram minha senha",
    "minha senha foi comprometida",
    "minha senha foi exposta",
    "senha de outro cliente",
    "senha de outro usuario",
    "senha de outra pessoa",
    "me informe a senha",
    "informe a senha de outro cliente",
    "revelar a senha de outro cliente",
]

HIGH_RISK_KEYWORDS = [
    # Transações não reconhecidas
    "nao reconheco essa compra",
    "nao reconheco o lancamento",
    "nao reconheco essa transferencia",
    "nao reconheco a transacao",
    "nao autorizei",
    "nao fiz essa transferencia",
    "compra nao reconhecida",
    "transacao nao autorizada",
    "movimentacao desconhecida",
    "transferencia desconhecida",
    "nao reconheco uma transferencia",
    "nao reconheco um pagamento",
    "nao reconheco um debito",
    "nao reconheco uma compra",

    # Fraude e comprometimento de conta
    "fraude",
    "cartao clonado",
    "cartao foi clonado",
    "cartao esta clonado",
    "meu cartao foi clonado",
    "meu cartao esta clonado",
    "conta invadida",
    "conta hackeada",
    "minha conta foi invadida",
    "roubaram meu cartao",
    "perdi meu cartao",

    # English
    "fraud",
    "unauthorized charge",
    "unauthorized transaction",
    "unrecognized transaction",
    "unknown transaction",
    "account hacked",
    "account compromised",
    "card stolen",
    "card cloned",
]


MEDIUM_RISK_KEYWORDS = [
    "cobranca indevida",
    "valor incorreto",
    "saldo incorreto",
    "nao recebi meu reembolso",
    "problema com pagamento",
    "fui cobrado duas vezes",
    "cobraram duas vezes",
    "cobranca duplicada",
    "pagamento duplicado",
    "valor debitado incorretamente",

    # English
    "incorrect charge",
    "charged twice",
    "duplicate charge",
    "incorrect balance",
    "incorrect amount",
    "payment problem",
]


def analyze_security(message: str) -> dict:
    normalized_message = normalize_text(message)
    

    if any(
        pattern in normalized_message
        for pattern in SUSPICIOUS_CREDENTIAL_PATTERNS
    ):
        return {
            "risk_level": "critical",
            "requires_human": True,
        }

    if any(
        keyword in normalized_message
        for keyword in HIGH_RISK_KEYWORDS
    ):
        return {
            "risk_level": "high",
            "requires_human": True,
        }

    if any(
        keyword in normalized_message
        for keyword in MEDIUM_RISK_KEYWORDS
    ):
        return {
            "risk_level": "medium",
            "requires_human": False,
        }

    return {
        "risk_level": "low",
        "requires_human": False,
    }
