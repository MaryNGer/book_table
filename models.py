import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 2},
    {'id': 3, 'title': 'War and Peace', 'author': 3},
]

DATA_AUTHOR = [
    {'author_id': 1, 'first_name': 'Чендр', 'last_name': 'Сваруп', 'middle_name': 'Нараян'},
    {'author_id': 2, 'first_name': 'Герман', 'last_name': 'Мелвилл', 'middle_name': None},
    {'author_id': 3, 'first_name': 'Лев', 'last_name': 'Толстой', 'middle_name': 'Николаевич'}
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHOR_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: Optional[int]
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)

    def __setitem__(self, key: str, value):
        setattr(self, key, value)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: str
    id: Optional[int] = None

    def __getitem__(self, item) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict], authors_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHOR_TABLE_NAME}'
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHOR_TABLE_NAME}` (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50)
                );
                """
            )

            cursor.executemany(
                f"""
                INSERT INTO `{AUTHOR_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES(?, ?, ?)
                """, [
                    (item['first_name'], item['last_name'], item['middle_name'])
                    for item in authors_records
                ]
            )

        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author INTEGER NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )
            conn.commit()


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_all_books_author(author_id: int) -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
        SELECT *
        FROM {BOOKS_TABLE_NAME} b
        JOIN {AUTHOR_TABLE_NAME} a ON b.author = a.author_id
        WHERE a.author_id = ?
        """, (author_id,)
                       )
        all_books = cursor.fetchall()
        print(all_books)
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHOR_TABLE_NAME}`
            (first_name, last_name, middle_name) VALUES(?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHOR_TABLE_NAME}` 
            WHERE author_id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {AUTHOR_TABLE_NAME}
            WHERE author_id = ?
            """,
            (author_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_author_by_id(author: Author) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {AUTHOR_TABLE_NAME}
            SET first_name = ?, last_name = ?, middle_name = ?
            WHERE author_id = ?
            """,
            (author.first_name, author.last_name, author.middle_name, author.id)
        )
        conn.commit()


def get_author_by_name(author_name) -> Optional[Author]:
    f_name, l_name, m_name = author_name
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT * FROM {AUTHOR_TABLE_NAME}
            WHERE first_name = ? AND last_name = ? AND middle_name = ?
            """,
            (f_name, l_name, m_name)
        )

        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


if __name__ == '__main__':
    delete_author_by_id(5)
