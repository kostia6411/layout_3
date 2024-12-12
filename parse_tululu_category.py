from bs4 import BeautifulSoup
import requests
import urllib.parse
from main import download_txt, download_image, parse_book_page, check_for_redirect
import os
import json
import argparse
import time

parser = argparse.ArgumentParser(
        description='Программа скачивает книги с сайта tululu.org и достаёт данные о книге'
    )
parser.add_argument('--start_page', help='Страница с которой начинается скачивание', default=1, type=int)
parser.add_argument('--end_page', help='Страница с которой заканчивается скачивание', default=4, type=int)

parser.add_argument('--dest_folder', help='название папки с результатами парсинга', default="parsing results")
parser.add_argument('--skip_imgs', help='Не скачивать изображения', action='store_true')
parser.add_argument('--skip_txt', help='Не скачивать текст', action='store_true')

args = parser.parse_args()

os.makedirs(f"{args.dest_folder}\Books", exist_ok=True)
os.makedirs(f"{args.dest_folder}\images", exist_ok=True)

for page in range(args.start_page, args.end_page):
    url = f"https://tululu.org/l55/{page}/"

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    card_book = soup.select('.d_book')

    books_info = []

    for book in card_book:

        tag = book.select_one('a')["href"]

        link = urllib.parse.urljoin("https://tululu.org/", tag)

        url_text = f"https://tululu.org/txt.php"
        payload = {'id': tag[2:-1]}

        try:

            response_text = requests.get(url_text, params=payload)
            response_text.raise_for_status()
            check_for_redirect(response_text)

            book_page = requests.get(f"https://tululu.org/{tag[1:-1]}/")
            book_page.raise_for_status()
            check_for_redirect(book_page)

            book_elements = parse_book_page(book_page)

            img_link = urllib.parse.urljoin(link, f"{book_elements['img_link']}")

            img_name = book_elements["img_link"].split("/", maxsplit=-1)

            filepath = os.path.join(f'{args.dest_folder}','Books', f'{book_elements["book_name"]}.txt')
            img_path = os.path.join(f'{args.dest_folder}','images', f'{img_name[2]}')

            if not args.skip_imgs:
                download_txt(filepath, response_text)
            if not args.skip_txt:
                download_image(img_path, img_link)

            book_elements['book_path'] = filepath

            book_elements.update({'img_link' : img_path})

            books_info.append(book_elements)

        except requests.HTTPError:
            print("Книга не найдена")
        except requests.ConnectionError:
            print("Произошла ошибка подключения.")
            time.sleep(600)

    books_info_json = json.dumps(books_info, ensure_ascii=False)

    with open(f"{args.dest_folder}/books_info.json", "w", encoding='utf8') as my_file:
        my_file.write(books_info_json)