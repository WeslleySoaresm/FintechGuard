
from pathlib import Path
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from router.predict_router import router as predict_router
from router.ticket_router import router as ticket_router
from router.auth_router import router as auth_router
from router.dashboard_router import router as dashboard_router
from router.admin_router import router as admin_router
from router.public_router import router as public_router
from router.agent_router import router as agent_router
from router.classifier_router import router as classifier_router

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
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    is_docs = request.url.path in {
        "/docs",
        "/redoc",
        "/openapi.json",
    }

    if ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"

    if is_docs:
        # Permissões específicas para Swagger UI e ReDoc.
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self' data: https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "object-src 'none';"
        )
    else:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "object-src 'none';"
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
app.include_router(agent_router)
app.include_router(classifier_router)

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


from diagnostico import diagnostico
from fastapi import Depends

@app.get("/diagnostico-interno")
async def diagnostico_interno(
    current_user=Depends(get_current_user)
):
    return diagnostico()