
import json
import os
import uuid
from pathlib import Path
from typing import Optional

import bcrypt
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Session, select

from data.db import engine
from models.model_events import User


router = APIRouter(prefix="/admin", tags=["Administração"])

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
SETTINGS_FILE = DATA_DIR / "site_settings.json"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SETTINGS = {
    "site_name": "FintechGuard",
    "tagline": "Segurança e confiança para suas finanças",
    "description": "Plataforma de atendimento financeiro.",
    "contact_email": "",
    "support_url": "",
    "brand_name": "FintechGuard",
    "logo_url": "",
    "primary_color": "#14557f",
    "accent_color": "#36a3d9",
}


class AdminLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_name: Optional[str] = Field(default=None, max_length=100)
    tagline: Optional[str] = Field(default=None, max_length=160)
    description: Optional[str] = Field(default=None, max_length=1000)
    contact_email: Optional[str] = Field(default=None, max_length=254)
    support_url: Optional[str] = Field(default=None, max_length=500)
    brand_name: Optional[str] = Field(default=None, max_length=100)
    logo_url: Optional[str] = Field(default=None, max_length=500)
    primary_color: Optional[str] = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    accent_color: Optional[str] = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


def read_settings() -> dict:
    if not SETTINGS_FILE.exists():
        write_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Mantém valores padrão para chaves novas ou ausentes.
        return {**DEFAULT_SETTINGS, **data}
    except (OSError, json.JSONDecodeError):
        raise HTTPException(
            status_code=500,
            detail="Não foi possível carregar as configurações."
        )


def write_settings(data: dict) -> None:
    temporary_file = SETTINGS_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    temporary_file.replace(SETTINGS_FILE)


def get_admin(request: Request) -> User:
    user_id = request.session.get("admin_user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Faça login como administrador.")

    with Session(engine) as session:
        user = session.get(User, int(user_id))

        if user is None or str(user.role).upper() != "ADMIN":
            request.session.clear()
            raise HTTPException(status_code=403, detail="Acesso restrito a administradores.")

        # Devolve o objeto carregado enquanto a sessão permanece aberta.
        # Os campos necessários são copiados antes do fechamento.
        session.expunge(user)
        return user


@router.get("/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html"
    )


@router.post("/login")
def admin_login(payload: AdminLogin, request: Request):
    normalized_email = payload.email.strip().lower()

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == normalized_email)
        ).first()

        valid_password = False

        if user and user.password_hash:
            stored_hash = user.password_hash
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            try:
                valid_password = bcrypt.checkpw(
                    payload.password.encode("utf-8"),
                    stored_hash
                )
            except (ValueError, TypeError):
                valid_password = False

        if (
            not user
            or not valid_password
            or str(user.role).upper() != "ADMIN"
        ):
            raise HTTPException(
                status_code=401,
                detail="E-mail, senha ou permissão inválidos."
            )

        user_id = user.id

    # Limpa qualquer sessão anterior para evitar reaproveitamento.
    request.session.clear()
    request.session["admin_user_id"] = int(user_id)

    return {"message": "Login administrativo realizado com sucesso."}


@router.get("", response_class=HTMLResponse)
def admin_panel(request: Request):
    get_admin(request)

    return templates.TemplateResponse(
        request=request,
        name="admin/panel.html"
    )


@router.get("/api/settings")
def get_site_settings(request: Request):
    get_admin(request)
    return read_settings()


@router.put("/api/settings")
def update_site_settings(
    payload: SettingsUpdate,
    request: Request
):
    get_admin(request)

    current = read_settings()
    changes = payload.model_dump(exclude_unset=True)

    # Não aceita valores nulos nem textos compostos só por espaços
    # para campos textuais; mantém o valor anterior nesses casos.
    for key, value in changes.items():
        if value is None:
            continue

        if isinstance(value, str):
            value = value.strip()

        current[key] = value

    write_settings(current)

    return {
        "message": "Configurações atualizadas.",
        **current
    }


@router.post("/api/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...)
):
    get_admin(request)

    # O limite também é validado no servidor, não só no JavaScript.
    max_size = 5 * 1024 * 1024
    content = await file.read(max_size + 1)
    await file.close()

    if not content:
        raise HTTPException(status_code=400, detail="O arquivo está vazio.")

    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="O arquivo excede 5 MB.")

    # Valida a assinatura do arquivo, não confia apenas no nome ou MIME.
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        extension = ".png"
    elif content.startswith(b"\xff\xd8\xff"):
        extension = ".jpg"
    elif (
        len(content) >= 12
        and content[:4] == b"RIFF"
        and content[8:12] == b"WEBP"
    ):
        extension = ".webp"
    else:
        raise HTTPException(
            status_code=415,
            detail="Formato inválido. Envie PNG, JPG ou WEBP."
        )

    # O nome original do usuário nunca é usado como nome no servidor.
    filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename

    try:
        destination.write_bytes(content)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar o arquivo."
        )

    return {"url": f"/static/uploads/{filename}"}


@router.post("/logout")
def admin_logout(request: Request):
    request.session.clear()
    return {"message": "Sessão administrativa encerrada."}
