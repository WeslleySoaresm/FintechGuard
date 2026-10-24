import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates


# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretório dos templates HTML
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Arquivo de configurações públicas
SETTINGS_FILE = BASE_DIR / "data" / "site_settings.json"

router = APIRouter(tags=["Plataforma Pública"])


# Configurações padrão utilizadas quando o arquivo ainda não existe
DEFAULT_SETTINGS = {
    "site_name": "FintechGuard",
    "brand_name": "FintechGuard",
    "tagline": "Seu dinheiro merece uma experiência melhor.",
    "description": (
        "Uma plataforma financeira digital com foco em segurança, "
        "transparência e atendimento."
    ),
    "hero_title": "Seu dinheiro merece uma experiência melhor.",
    "hero_description": (
        "Conheça uma nova forma de organizar sua vida financeira, "
        "com informações claras, tecnologia e foco na segurança."
    ),
    "primary_color": "#155eef",
    "primary_dark_color": "#1249c7",
    "accent_color": "#26c6a3",
    "logo_url": "",
    "hero_image_url": "",
    "contact_email": "",
    "support_url": "",
}


def load_public_settings() -> dict:
    """
    Lê as configurações do site.

    Se o arquivo ainda não existir ou estiver inválido,
    utiliza as configurações padrão.
    """
    settings = DEFAULT_SETTINGS.copy()

    try:
        if SETTINGS_FILE.exists():
            with SETTINGS_FILE.open("r", encoding="utf-8") as file:
                saved_settings = json.load(file)

            if isinstance(saved_settings, dict):
                settings.update(saved_settings)

    except (OSError, json.JSONDecodeError):
        # Mantém os valores padrão se houver problema na leitura.
        pass

    return settings


@router.get("/", response_class=HTMLResponse, name="home")
async def public_home(request: Request):
    """
    Exibe a página inicial pública do FintechGuard.
    """
    settings = load_public_settings()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "request": request,
            "settings": settings,
        },
    )

@router.get("/sobre", response_class=HTMLResponse, name="about")
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request,
            "settings": load_public_settings(),
        },
    )
@router.get("/seguranca", response_class=HTMLResponse, name="security")
async def security_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="security.html",
        context={
            "request": request,
            "settings": load_public_settings(),
        },
    )
    
@router.get("/servicos", response_class=HTMLResponse, name="services")
async def services_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="services.html",
        context={
            "request": request,
            "settings": load_public_settings(),
        },
    )

@router.get("/contato", response_class=HTMLResponse, name="contact")
async def contact_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "request": request,
            "settings": load_public_settings(),
        },
    )

@router.get("/privacidade", response_class=HTMLResponse, name="privacy")
async def privacy_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="privacy.html",
        context={
            "request": request,
            "settings": load_public_settings(),
        },
    )

@router.get(
    "/api/public/settings",
    response_class=JSONResponse,
    name="public_settings",
)
async def get_public_settings():
    """
    Disponibiliza somente as configurações necessárias
    para personalizar a página pública.
    """
    settings = load_public_settings()

    # Lista permitida: não expõe outras propriedades que
    # eventualmente sejam adicionadas ao arquivo de configuração.
    public_fields = {
        "site_name",
        "brand_name",
        "tagline",
        "description",
        "hero_title",
        "hero_description",
        "primary_color",
        "primary_dark_color",
        "accent_color",
        "logo_url",
        "hero_image_url",
        "contact_email",
        "support_url",
    }

    public_settings = {
        key: settings[key]
        for key in public_fields
        if key in settings
    }

    return JSONResponse(content=public_settings)
