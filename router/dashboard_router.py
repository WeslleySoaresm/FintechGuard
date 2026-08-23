import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Dashboard"])

# Mapeia o caminho absoluto até a raiz do projeto e encontra a pasta 'templates'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/dashboard", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html"
    )