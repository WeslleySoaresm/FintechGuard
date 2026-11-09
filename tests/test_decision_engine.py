
import pytest

from fintechguard_agents.decision_engine import make_decision


@pytest.mark.parametrize(
    "intent, risk, human, expected_action, expected_priority",
    [
        ("Billing", "low", False, "automated_assistance", "normal"),
        ("Refund", "medium", False, "automated_assistance", "medium"),
        ("Fraud", "high", True, "human_escalation", "high"),
        ("Account Access", "critical", True, "emergency_escalation", "urgent"),
    ],
)
def test_make_decision(
    intent,
    risk,
    human,
    expected_action,
    expected_priority,
):
    result = make_decision(intent, risk, human)

    assert result["action"] == expected_action
    assert result["priority"] == expected_priority
    assert result["requires_human"] == human
