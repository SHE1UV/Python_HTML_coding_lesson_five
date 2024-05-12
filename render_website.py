import json
from pathlib import Path
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():

    parser = argparse.ArgumentParser(
        description="Программа предоставляет доступ к сайту с книгами"
    )
    parser.add_argument(
        "--json_path",
        type=str,
        help="путь к JSON файлу",
        default="books.json"
    )
    args = parser.parse_args()

    with open(args.json_path, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")

    page_books_number = 10
    row_books_number = 2
    per_page_books = list(chunked(books, page_books_number))
    pages_count = len(per_page_books)

    for number, page in enumerate(per_page_books, 1):
        row_of_books = list(chunked(page, row_books_number))
        rendered_page = template.render(
            row_of_books=row_of_books,
            page_number=number,
            pages_count=pages_count
        )
        with open(f"pages/index{number}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    folder = "pages/"
    Path(folder).mkdir(parents=True, exist_ok=True)
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".",  default_filename="pages/index1.html")


if __name__ == "__main__":
    main()
