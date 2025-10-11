import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://books.toscrape.com/"

def fetch_page(url: str) -> str:
    """Faz uma requisição e retorna o HTML corretamente decodificado."""
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'ISO-8859-1'

    return response.text

def download_image(img_url: str, save_folder: str = "public/images") -> str:
    """Baixa a imagem e retorna o caminho salvo localmente."""
    os.makedirs(save_folder, exist_ok=True)
    filename = os.path.join(save_folder, img_url.split("/")[-1])
    
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Erro ao baixar imagem: {img_url}")
    
    return filename  # caminho local do arquivo salvo

def parse_books_from_page(html: str, category_name: str) -> list[dict]:
    """Extrai livros de uma página e retorna lista de dicionários."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        availability = book.select_one(".availability").text.strip()
        rating_class = book.p["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "None"

        # URL da imagem (relativa no site)
        img_relative = book.select_one("div.image_container img")["src"]
        img_url = BASE_URL + img_relative.replace("../", "")
        img_path = download_image(img_url)  # baixa a imagem

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "category": category_name,
            "image_path": img_path
        })

    return books

def scrape_all_books() -> list[dict]:
    """Percorre todas as categorias e páginas e retorna todos os livros."""
    categories_html = fetch_page(BASE_URL)
    soup = BeautifulSoup(categories_html, "html.parser")
    categories = {
        cat.text.strip(): BASE_URL + cat["href"]
        for cat in soup.select(".side_categories ul li ul li a")
    }

    all_books = []
    for name, url in categories.items():
        print(f"Coletando livros da categoria: {name}")
        page_url = url
        while True:
            html = fetch_page(page_url)
            books = parse_books_from_page(html, name)
            all_books.extend(books)

            next_page = BeautifulSoup(html, "html.parser").select_one("li.next a")
            if next_page:
                page_url = url.rsplit("/", 1)[0] + "/" + next_page["href"]
            else:
                break

    return all_books
