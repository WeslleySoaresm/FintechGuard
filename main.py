from fastapi import FastAPI
from router.ticket_router import router as ticket_router
from router.auth_router import router as auth_router

app = FastAPI(title="FintechGuard API", version="1.0.0")

# Inclui as rotas dos módulos
app.include_router(auth_router)
app.include_router(ticket_router)


@app.get("/")
def root():
    return {"message": "API FintechGuard em execução"}