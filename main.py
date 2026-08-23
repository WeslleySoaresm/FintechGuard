from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from router.predict_router import router as predict_router
from router.ticket_router import read_tickets, router as ticket_router
from router.auth_router import router as auth_router
from router.predict_router import router as predict_router
from router.dashboard_router import router as dashboard_router
app = FastAPI(title="FintechGuard API", version="1.0.0")

# Define o caminho absoluto da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

# Aponta dinamicamente para a pasta templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Inclui as rotas dos módulos
app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(predict_router)
app.include_router(dashboard_router)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "service": "FintechGuard API"}

@app.get("/login", tags=["Initial Login"], response_class=HTMLResponse)
def render_login(request: Request):
    """Renderiza a página visual de Login."""
    # Sintaxe atualizada mantendo o request no contexto
    return templates.TemplateResponse(
        request=request, 
        name="login.html"
    )



