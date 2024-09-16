from typing import Optional
from flasgger import Schema, fields, ValidationError
from marshmallow import validates, post_load

from models import get_book_by_title, get_author_by_id, get_author_by_name, Book, Author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author')
    def validate_author(self, author: int) -> None:
        author = get_author_by_id(author)
        if author is None:
            raise ValidationError(
                f'There is no such author id={author}.'
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    author_name = fields.List(fields.Str(), required=True)

    @validates('author_name')
    def validate_name(self, author_name) -> None:
        if get_author_by_name(author_name) is not None:
            raise ValidationError(
                f'An author with this name {author_name} '
                f'already exists.'
            )

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        data_list = data['author_name']
        data_dct = dict()
        data_dct['first_name'], data_dct['last_name'], data_dct['middle_name'] = data_list
        return Author(**data_dct)


class BookEdit(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Int(required=True)

    @validates('author')
    def validate_author(self, author: int) -> None:
        author = get_author_by_id(author)
        if author is None:
            raise ValidationError(
                f'There is no such author id={author}.'
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)
