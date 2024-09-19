import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import urllib.parse


def download_txt(filepath, response):
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(imgpath):
    response_img = requests.get(urllib.parse.urljoin(f"https://tululu.org/b{id}/", f"{img_link}"))
    response_img.raise_for_status()
    with open(imgpath, 'wb') as file:
        file.write(response_img.content)

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

if __name__ == '__main__':
    os.makedirs("Books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

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

            tag_comments = soup.find_all(class_="texts")

            for comment in tag_comments:
                comments = comment.find("span")
                comments_text = comments.text
                # print(comments_text)

            tag_img = soup.find(class_="bookimage")
            img_link = tag_img.find("img")['src']

            book_name = text[0].strip()
            sort_book_name = sanitize_filename(book_name)
            auhtor = text[1].strip()
            # print(book_name)
            # print(auhtor)
            img_name = img_link.split("/", maxsplit=-1)
            # print(img_name)

            filepath = os.path.join('Books', f'{sort_book_name}.txt')
            imgpath = os.path.join('images', f'{img_name[2]}')
            # print(imgpath)

            download_txt(filepath, response)
            download_image(imgpath)
        except requests.HTTPError:
            print("Книга не найдена")

