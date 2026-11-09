
from fintechguard_agents.intent_classifier import normalize_text


CRITICAL_KEYWORDS = [
    "palavra passe",
    "codigo de autenticacao",
    "codigo de verificacao",
    "codigo sms",
    "token",
    "cvv",
    "cvc",
    "numero completo do cartao",
    "numero do cartao",
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
    "incorrect charge",
    "charged twice",
    "duplicate charge",
    "incorrect balance",
    "incorrect amount",
    "payment problem",
]


def contains_keyword(message: str, keywords: list[str]) -> bool:
    """Verifica palavras e expressões após normalização."""

    return any(
        normalize_text(keyword) in message
        for keyword in keywords
    )


def analyze_security(message: str) -> dict:
    """
    Analisa sinais de risco na mensagem.

    Prioridade:
    1. Solicitação ou exposição suspeita de credenciais.
    2. Indícios de fraude ou transação não autorizada.
    3. Problemas financeiros que exigem atenção.
    4. Risco baixo.
    """

    if not isinstance(message, str) or not message.strip():
        return {
            "risk_level": "low",
            "requires_human": False,
        }

    normalized_message = normalize_text(message)

    # Risco crítico: possível comprometimento de credenciais.
    if contains_keyword(
        normalized_message,
        SUSPICIOUS_CREDENTIAL_PATTERNS,
    ):
        return {
            "risk_level": "critical",
            "requires_human": True,
        }

    # Risco alto: suspeita de fraude ou transação não autorizada.
    if contains_keyword(
        normalized_message,
        HIGH_RISK_KEYWORDS,
    ):
        return {
            "risk_level": "high",
            "requires_human": True,
        }

    # Risco médio: problemas financeiros.
    if contains_keyword(
        normalized_message,
        MEDIUM_RISK_KEYWORDS,
    ):
        return {
            "risk_level": "medium",
            "requires_human": False,
        }

    return {
        "risk_level": "low",
        "requires_human": False,
    }
