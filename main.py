import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import urllib.parse
import argparse
import time


def download_txt(filepath, response):
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(img_path, img_link):
    img_response = requests.get(img_link)
    img_response.raise_for_status()
    with open(img_path, 'wb') as file:
        file.write(img_response.content)

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    tag = soup.select_one('h1')
    text = tag.text.split("::", maxsplit=1)

    genre_tag = soup.select("d_book")[1]
    genre_links = genre_tag.find_all("a")
    genres = [genre.text for genre in genre_links]

    tag_comments = soup.select("texts")
    comments = [comment.select_one("black").text for comment in tag_comments]


    tag_img = soup.select_one("bookimage")
    img_link = tag_img.select_one("img")['src']

    book_name = text[0].strip()
    sort_book_name = sanitize_filename(book_name)
    auhtor = text[1].strip()

    book_elements = {
        "auhtor": auhtor,
        "book_name": sort_book_name,
        "genre": genres,
        "comments": comments,
        "img_link": img_link
    }
    return book_elements

if __name__ == '__main__':
    os.makedirs("parsing results\Books", exist_ok=True)
    os.makedirs("parsing results\images", exist_ok=True)

    parser = argparse.ArgumentParser(
        description='Программа скачивает книги с сайта tululu.org и достаёт данные о книге'
    )
    parser.add_argument('--start_id', help='Начало',default=1, type=int)
    parser.add_argument('--end_id', help='Конец',default=10, type=int)
    args = parser.parse_args()


    for number in range(args.start_id, args.end_id):
        url = f"https://tululu.org/txt.php"
        payload = {'id': number}



        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            book_page = requests.get(f"https://tululu.org/b{number}/")
            book_page.raise_for_status()
            check_for_redirect(book_page)


            book_elements = parse_book_page(book_page)

            img_link = urllib.parse.urljoin(f"https://tululu.org/b{number}/", f"{book_elements['img_link']}")

            img_name = book_elements["img_link"].split("/", maxsplit=-1)

            filepath = os.path.join('parsing results', 'Books', f'{book_elements["book_name"]}.txt')
            img_path = os.path.join('parsing results', 'images', f'{img_name[2]}')


            download_txt(filepath, response)
            download_image(img_path, img_link,)
        except requests.HTTPError:
            print("Книга не найдена")
        except requests.ConnectionError:
            print("Произошла ошибка подключения.")
            time.sleep(600)

