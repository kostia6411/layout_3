# Парсер книг с сайта tululu.org

Программа скачивает книги, обложки книг с сайта tululu.org и достаёт данные (автора, название книги, жанр, коментариии, ссылки на изображение) о книге.

### Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Как запустить 

Для запуска напишите в командной строке:

```
python main.py
```

Втаком случае программа скачает книги с 1 по 10.
Если же вам нужны книги в определённом диапазоне, то в таком случае напишите в командную строку:

```
python main.py --start_id (число) --end_id (число)
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
