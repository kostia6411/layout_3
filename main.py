import requests
import os


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.makedirs("Books", exist_ok=True)
    for id in range(10):
        url = f"https://tululu.org/txt.php?id={id}"

        try:

            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)

            filename = f'Books/id{id}.txt'
            with open(filename, 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            print("Книга не найдена")



