import re
import unicodedata


INTENT_KEYWORDS = {
    "Fraud": [
    "fraude",
    "fraud",
    "cartao clonado",
    "cartão clonado",
    "cartao foi clonado",
    "cartão foi clonado",
    "nao reconheco essa compra",
    "não reconheço essa compra",
    "compra nao reconhecida",
    "compra não reconhecida",
    "transacao suspeita",
    "transação suspeita",
    "movimentacao desconhecida",
    "movimentação desconhecida",
    "nao fui eu",
    "não fui eu",
],
    "Account Access": [
        "senha",
        "login",
        "acessar minha conta",
        "acesso a conta",
        "acesso à conta",
        "conta bloqueada",
        "bloqueio da conta",
    ],
    "Card": [
        "cartao",
        "cartão",
        "credito",
        "crédito",
        "debito",
        "débito",
    ],
    "Transaction": [
        "transferencia",
        "transferência",
        "pix",
        "pagamento",
        "transacao",
        "transação",
    ],
    "Billing": [
        "cobranca",
        "cobrança",
        "fatura",
        "tarifa",
        "taxa",
    ],
    "Refund": [
        "reembolso",
        "estorno",
        "devolucao",
        "devolução",
    ],
    "Technical Issue": [
        "erro no aplicativo",
        "aplicativo nao funciona",
        "aplicativo não funciona",
        "sistema fora do ar",
        "erro no sistema",
        "problema tecnico",
        "problema técnico",
    ],
    "Loan": [
        "emprestimo",
        "empréstimo",
        "financiamento",
        "credito pessoal",
        "crédito pessoal",
    ],
}


def normalize_text(text: str) -> str:
    """
    Normaliza o texto para facilitar a comparação
    entre palavras com e sem acentos.
    """

    text = text.lower().strip()

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return text


def classify_intent(message: str) -> str:
    """
    Classifica a intenção com base em palavras-chave.
    Retorna a primeira categoria correspondente.
    """

    normalized_message = normalize_text(message)

    priority_order = [
        "Fraud",
        "Account Access",
        "Card",
        "Transaction",
        "Billing",
        "Refund",
        "Technical Issue",
        "Loan",
    ]

    for intent in priority_order:
        keywords = INTENT_KEYWORDS[intent]

        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            pattern = (
                r"(?<!\w)"
                + re.escape(normalized_keyword)
                + r"(?!\w)"
            )

            if re.search(pattern, normalized_message):
                return intent

    return "Other"