import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import urllib.parse
import argparse


def download_txt(filepath, response):
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(imgpath, img_link, number):
    response_img = requests.get(urllib.parse.urljoin(f"https://tululu.org/b{number}/", f"{img_link}"))
    response_img.raise_for_status()
    with open(imgpath, 'wb') as file:
        file.write(response_img.content)

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    tag = soup.find('h1')
    text = tag.text.split("::", maxsplit=1)

    genres = []
    genre_tag = soup.find_all(class_="d_book")[1]
    genre_links = genre_tag.find_all("a")
    for genre in genre_links:
        genres.append(genre.text)

    comments = []
    tag_comments = soup.find_all(class_="texts")
    for comment in tag_comments:
        comment_content = comment.find(class_="black")
        comments.append(comment_content.text)

    tag_img = soup.find(class_="bookimage")
    img_link = tag_img.find("img")['src']

    book_name = text[0].strip()
    sort_book_name = sanitize_filename(book_name)
    auhtor = text[1].strip()

    book_info = {
        "auhtor": auhtor,
        "book_name": sort_book_name,
        "genre": genres,
        "comments": comments,
        "img_link": img_link
    }
    return book_info

if __name__ == '__main__':
    os.makedirs("Books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

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

            response_author = requests.get(f"https://tululu.org/b{number}/")

            book_info = parse_book_page(response_author)

            img_name = book_info["img_link"].split("/", maxsplit=-1)

            filepath = os.path.join('Books', f'{book_info["book_name"]}.txt')
            imgpath = os.path.join('images', f'{img_name[2]}')


            download_txt(filepath, response)
            download_image(imgpath, book_info["img_link"], number)
        except requests.HTTPError:
            print("Книга не найдена")

