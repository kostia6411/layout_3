import requests
import os


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for id in range(10):
        url = f"https://tululu.org/txt.php?id={id}"

        response = requests.get(url)
        response.raise_for_status()

        os.makedirs("Books", exist_ok=True)

        filename = f'Books/id{id}.txt'
        with open(filename, 'wb') as file:
            file.write(response.content)

