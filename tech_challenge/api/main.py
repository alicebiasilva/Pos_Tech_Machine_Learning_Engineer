from fastapi import FastAPI
from .routes import router
from .config import Config

app = FastAPI(
    title=Config.SWAGGER_TITLE,
    version=Config.SWAGGER_VERSION,
    description="API pública para consulta de livros"
)

app.include_router(router, prefix="/api/v1")