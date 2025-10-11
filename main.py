from tech_challenge.api.routes import router
from tech_challenge.api.config import Config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title=Config.SWAGGER_TITLE,
    version=Config.SWAGGER_VERSION,
    description="API pública para consulta de livros"
)

app.include_router(router, prefix="/api/v1")

# Monta a pasta 'frontend' como arquivos estáticos
current_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(current_dir, "public")

app.mount("/", StaticFiles(directory=public_dir, html=True), name="frontend")