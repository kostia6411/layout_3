from bs4 import BeautifulSoup
import requests
import urllib.parse
from main import download_txt, download_image, parse_book_page, check_for_redirect
import os
import json
import argparse

parser = argparse.ArgumentParser(
        description='Программа скачивает книги с сайта tululu.org и достаёт данные о книге'
    )
parser.add_argument('--start_page', help='Страница с которой начинается скачивание', default=1, type=int)
parser.add_argument('--end_page', help='Страница с которой заканчивается скачивание', default=4, type=int)
args = parser.parse_args()

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

        print(link)

        url_text = f"https://tululu.org/txt.php"
        payload = {'id': tag[1:-1]}

        response_text = requests.get(url_text, params=payload)
        response_text.raise_for_status()

        book_page = requests.get(f"https://tululu.org/{tag[1:-1]}/")
        book_page.raise_for_status()
        check_for_redirect(book_page)

        book_elements = parse_book_page(book_page)

        img_link = urllib.parse.urljoin(link, f"{book_elements['img_link']}")

        img_name = book_elements["img_link"].split("/", maxsplit=-1)

        filepath = os.path.join('Books', f'{book_elements["book_name"]}.txt')
        img_path = os.path.join('images', f'{img_name[2]}')

        # download_txt(filepath, response)
        # download_image(img_path, img_link)

        book_elements['book_path'] = filepath

        book_elements.update({'img_link' : img_path})

        books_info.append(book_elements)

    # print(books_info)

    books_info_json = json.dumps(books_info, ensure_ascii=False)

    with open("books_info.json", "w", encoding='utf8') as my_file:
        my_file.write(books_info_json)