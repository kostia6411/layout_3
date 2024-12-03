from bs4 import BeautifulSoup
import requests
import urllib.parse
from main import download_txt, download_image, parse_book_page, check_for_redirect
import os
import json


for page in range(1, 4):
    url = f"https://tululu.org/l55/{page}/"

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    card_book = soup.find_all('table', class_='d_book')

    books_info = []

    for book in card_book:

        tag = book.find('a')["href"]

        link = urllib.parse.urljoin("https://tululu.org/", tag)

        # print(tag[1:-1])

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
        # download_image(img_path, img_link,)

        book_elements['book_path'] = filepath

        book_elements.update({'img_link' : img_path})

        books_info.append(book_elements)

    # print(books_info)

    books_info_json = json.dumps(books_info, ensure_ascii=False)

    with open("books_info.json", "w", encoding='utf8') as my_file:
        my_file.write(books_info_json)