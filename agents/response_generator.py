from typing import Any


def generate_response(
    intent: str,
    risk_level: str,
    requires_human: bool,
) -> str:
    """
    Gera uma resposta de atendimento com base
    na intenção e no nível de risco.
    """

    if requires_human:
        if risk_level == "critical":
            return (
                "Sua mensagem apresenta uma situação que exige "
                "atenção imediata. Não compartilhe senhas, códigos "
                "de autenticação ou dados completos do cartão. "
                "Seu atendimento precisa ser encaminhado para "
                "uma equipe especializada."
            )

        if risk_level == "high":
            return (
                "Identificamos uma situação que precisa de análise "
                "especializada. Não realize novas operações relacionadas "
                "ao problema até receber orientação oficial. "
                "Seu atendimento será encaminhado para uma equipe humana."
            )

    responses = {
        "Account Access": (
            "Entendi que você está com dificuldades para acessar "
            "sua conta. Podemos orientar você pelos procedimentos "
            "oficiais de recuperação de acesso."
        ),
        "Card": (
            "Entendi que sua solicitação está relacionada ao cartão. "
            "Podemos orientar você sobre os procedimentos disponíveis."
        ),
        "Transaction": (
            "Entendi que sua solicitação está relacionada a uma "
            "transação. Podemos ajudar a identificar os próximos passos."
        ),
        "Billing": (
            "Entendi que você tem uma dúvida relacionada a uma "
            "cobrança ou fatura. Podemos orientar você."
        ),
        "Refund": (
            "Entendi que sua solicitação está relacionada a um "
            "reembolso. Podemos ajudar a verificar os procedimentos."
        ),
        "Technical Issue": (
            "Entendi que você está enfrentando um problema técnico. "
            "Vamos orientar você sobre os próximos passos."
        ),
        "Loan": (
            "Entendi que sua solicitação está relacionada a um "
            "empréstimo. Podemos apresentar as orientações disponíveis."
        ),
        "Fraud": (
            "Sua mensagem relata uma possível situação de fraude. "
            "Precisamos encaminhar o caso para análise especializada."
        ),
        "Other": (
            "Recebemos sua mensagem. Poderia fornecer mais detalhes "
            "para que possamos identificar como ajudar?"
        ),
    }

    return responses.get(
        intent,
        responses["Other"],
    )