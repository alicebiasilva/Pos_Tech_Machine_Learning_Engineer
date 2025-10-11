from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from pathlib import Path
import os

router = APIRouter()

# Carrega os dados do CSV ao iniciar a API
BASE_DIR = Path(__file__).resolve().parent
df_books = pd.read_csv(BASE_DIR / "data" / "books.csv")
df_books["id"] = df_books.index + 1


# Lista titulo de todos os livros
@router.get("/books", tags=["Livros"])
def get_books():
    """
    Retorna uma lista com os títulos de todos os livros disponíveis.

    Esta rota retorna apenas os nomes (títulos) dos livros,
    extraídos do DataFrame 'df_books'.

    Retorno:
        list[str]: Lista contendo os títulos dos livros.
    """
    return df_books["title"].tolist()


# Detalhes de um livro pelo ID
from fastapi import HTTPException

@router.get("/books/{book_id}", tags=["Livros"])
def get_book(book_id: int):
    """
    Retorna os detalhes completos de um livro pelo seu ID.

    Argumentos:
        book_id (int): Identificador único do livro.

    Retorno:
        dict: Um dicionário com todas as informações do livro correspondente ao ID fornecido.

    Exceções:
        HTTPException 404: Se nenhum livro com o ID informado for encontrado.
    """
    book = df_books[df_books["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book.to_dict(orient="records")[0]


# Busca livros por título e/ou categoria
@router.get("/books/search", tags=["Categorias"])
def search_books(title: str | None = Query(None), category: str | None = Query(None)):
    """
    Busca livros filtrando por título e/ou categoria.

    Parâmetros de consulta (query parameters):
        title (str, opcional): Texto para busca parcial no título do livro. A busca é case-insensitive.
        category (str, opcional): Texto para busca parcial na categoria do livro. A busca é case-insensitive.

    Retorna:
        list[dict]: Lista de livros que correspondem aos filtros aplicados. Cada livro é representado por um dicionário com todas as suas informações.

    Se nenhum filtro for fornecido, retorna todos os livros disponíveis.
    """
    result = df_books
    if title:
        result = result[result["title"].str.contains(title, case=False, na=False)]
    if category:
        result = result[result["category"].str.contains(category, case=False, na=False)]
    return result.to_dict(orient="records")

# Lista todas as categorias
@router.get("/categories", tags=["Categorias"])
def get_categories():
    """
    Retorna uma lista com todas as categorias únicas disponíveis nos livros.

    Retorno:
        dict: Um dicionário contendo a chave "categories" com uma lista de strings,
              onde cada string representa uma categoria distinta.
    """
    categories = df_books["category"].unique().tolist()
    return {"categories": categories}

@router.get("/health", tags=["Saúde"])
def health():
    """
    Verifica o status da API e a disponibilidade da base de dados (CSV).

    Retorna:
        dict: {"status": "ok"} se tudo estiver funcionando corretamente.
    
    Levanta HTTPException 503 se o arquivo CSV não estiver acessível ou inválido.
    """
    csv_path = "public/data/books.csv"
    
    # Verifica se o arquivo existe
    if not os.path.isfile(csv_path):
        raise HTTPException(status_code=503, detail="Base de dados não encontrada")
    
    # Tenta carregar o CSV para garantir que está legível
    try:
        pd.read_csv(csv_path)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao ler base de dados: {str(e)}")
    
    return {"status": "ok"}
