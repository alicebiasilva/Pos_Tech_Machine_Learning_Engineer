from extract_data import scrape_all_books
from load_data import save_books_csv

def main():
    books = scrape_all_books()
    save_books_csv(books)

if __name__ == "__main__":
    main()
