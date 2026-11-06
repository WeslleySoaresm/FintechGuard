from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1, max_length=5000)
    ticket_id: int | None = Field(default=None, gt=0)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("A mensagem não pode estar vazia.")

        return value


class AgentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: str
    risk_level: Literal["low", "medium", "high", "critical"]
    requires_human: bool
    response: str