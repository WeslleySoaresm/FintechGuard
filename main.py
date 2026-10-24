from pathlib import Path
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from router.predict_router import router as predict_router
from router.ticket_router import router as ticket_router
from router.auth_router import router as auth_router
from router.dashboard_router import router as dashboard_router
from starlette.middleware.sessions import SessionMiddleware
from router.admin_router import router as admin_router
from router.public_router import router as public_router

# ============================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(
    title="FintechGuard API",
    version="1.0.0"
)

SESSION_SECRET = os.getenv("SESSION_SECRET")

if not SESSION_SECRET:
    if ENVIRONMENT == "production":
        raise RuntimeError(
            "Defina SESSION_SECRET nas variáveis de ambiente."
        )

    SESSION_SECRET = "dev-only-change-this-secret"

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="fg_admin_session",
    max_age=1800,
    same_site="lax",
    https_only=(ENVIRONMENT == "production"),
)

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# ARQUIVOS ESTÁTICOS
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static"
)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ============================================================
# CONFIGURAÇÃO DE CORS
# ============================================================

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEADERS DE SEGURANÇA HTTP
# ============================================================

@app.middleware("http")
async def security_headers(
    request: Request,
    call_next
):
    response = await call_next(request)

    # --------------------------------------------------------
    # HSTS
    # --------------------------------------------------------
    # Ativado somente em produção porque exige HTTPS.
    # --------------------------------------------------------

    if ENVIRONMENT == "production":

        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; "
            "includeSubDomains"
        )

    # --------------------------------------------------------
    # PROTEÇÃO CONTRA CLICKJACKING
    # --------------------------------------------------------

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    # --------------------------------------------------------
    # MIME SNIFFING
    # --------------------------------------------------------

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    # --------------------------------------------------------
    # CONTENT SECURITY POLICY
    # --------------------------------------------------------

    if ENVIRONMENT == "production":

        response.headers[
            "Content-Security-Policy"
        ] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self';"
        )

    else:

        # Desenvolvimento:
        # permite os recursos necessários ao Swagger e CDNs.
        response.headers[
            "Content-Security-Policy"
        ] = (
            "default-src 'self' https://cdn.jsdelivr.net; "
            "script-src 'self' https://cdn.jsdelivr.net ; "
            "style-src 'self' https://cdn.jsdelivr.net ; "
            "img-src 'self' data:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self';"
        )

    return response


# ============================================================
# ROTAS
# ============================================================

app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(predict_router)
app.include_router(dashboard_router)
app.include_router(admin_router)
app.include_router(public_router)
# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["Health Check"]
)
def health_check():

    return {
        "status": "ok",
        "service": "FintechGuard API"
    }


# ============================================================
# LOGIN
# ============================================================

@app.get(
    "/login",
    tags=["Initial Login"],
    response_class=HTMLResponse
)
def render_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )