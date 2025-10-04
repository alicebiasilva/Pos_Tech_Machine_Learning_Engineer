# tech_challenge/api/config.py

class Config:
    SECRET_KEY = "sua_chave_secreta"             # Para segurança geral
    CACHE_TYPE = "simple"                         # Se quiser usar cache
    SWAGGER_TITLE = "Book API - Tech Challenge"  # Título Swagger
    SWAGGER_VERSION = "1.0.0"                    # Versão API
    SQLALCHEMY_DATABASE_URI = "sqlite:///books.db"  # Se usar SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "sua_chave_jwt_secreta"     # Se usar JWT
