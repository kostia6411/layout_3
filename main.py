import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(filepath, response):
    with open(filepath, 'wb') as file:
        file.write(response.content)

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

if __name__ == '__main__':
    os.makedirs("Books", exist_ok=True)

    for id in range(1, 10):
        url = f"https://tululu.org/txt.php?id={id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)

            response_author = requests.get(f"https://tululu.org/b{id}/")
            soup = BeautifulSoup(response_author.text, 'lxml')
            tag = soup.find('h1')
            text = tag.text.split("::", maxsplit=1)

            book_name = text[0].strip()
            sort_book_name = sanitize_filename(book_name)
            auhtor = text[1].strip()
            print(book_name)
            print(auhtor)

            filepath = os.path.join('Books', f'{sort_book_name}.txt')
            print(sort_book_name)
            download_txt(filepath, response)
        except requests.HTTPError:
            print("Книга не найдена")

