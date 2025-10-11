from tech_challenge.api.routes import router
from tech_challenge.api.config import Config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI(
    title=Config.SWAGGER_TITLE,
    version=Config.SWAGGER_VERSION,
    description="API pública para consulta de livros"
)

app.include_router(router, prefix="/api/v1")