from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from router.ticket_router import router as ticket_router
from router.auth_router import router as auth_router

app = FastAPI(title="FintechGuard API", version="1.0.0")

# Define o caminho absoluto da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

# Aponta dinamicamente para a pasta templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Inclui as rotas dos módulos
app.include_router(auth_router)
app.include_router(ticket_router)


@app.get("/login", response_class=HTMLResponse)
def render_login(request: Request):
    """Renderiza a página visual de Login."""
    # Sintaxe atualizada mantendo o request no contexto
    return templates.TemplateResponse(
        request=request, 
        name="login.html"
    )

@app.get("/dashboard", response_class=HTMLResponse)
def render_dashboard(request: Request):
    """Renderiza o painel do sistema."""
    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )

@app.get("/")
def root():
    return {"message": "API FintechGuard em execução"}

