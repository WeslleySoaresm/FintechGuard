
from typing import Any


def make_decision(
    intent: str,
    risk_level: str,
    requires_human: bool,
) -> dict[str, Any]:
    """
    Determina a ação que o agente deve executar
    com base na intenção e no nível de risco.
    """

    # 1. Riscos críticos exigem encaminhamento imediato.
    if risk_level == "critical":
        return {
            "action": "emergency_escalation",
            "priority": "urgent",
            "requires_human": True,
        }

    # 2. Riscos altos exigem análise humana.
    if risk_level == "high" or requires_human:
        return {
            "action": "human_escalation",
            "priority": "high",
            "requires_human": True,
        }

    # 3. Risco médio exige atenção, mas pode continuar
    # no atendimento automatizado.
    if risk_level == "medium":
        return {
            "action": "automated_assistance",
            "priority": "medium",
            "requires_human": False,
        }

    # 4. Solicitações comuns seguem para atendimento automático.
    return {
        "action": "automated_assistance",
        "priority": "normal",
        "requires_human": False,
    }
