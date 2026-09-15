from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    access_token: str
    token_type: str = "bearer"