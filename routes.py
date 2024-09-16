from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

from models import (
    DATA,
    DATA_AUTHOR,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_all_books_author,
    add_author,
    get_author_by_id,
    delete_author_by_id
)

from schemas import BookSchema, AuthorSchema, BookEdit

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BooksEdit(Resource):
    def get(self, book_id):
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200

    def put(self, book_id):
        data = request.json
        schema = BookEdit()
        if get_book_by_id(book_id) is None:
            return 'Книги в БД нет, нельзя изменить того чего нет', 404
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        update_book_by_id(book)
        return schema.dump(book), 200

    def patch(self, book_id):
        data = request.get_json()
        schema = BookSchema()
        book = get_book_by_id(book_id)
        if book is None:
            return f'Книги id={book_id} в БД нет', 400
        for key, value in data.items():
            book[key] = value

        return schema.dump(update_book_by_id(book)), 200

    def delete(self, book_id):
        schema = BookSchema()
        if get_book_by_id(book_id) is None:
            return f'Книги id={book_id} в БД нет', 400
        return schema.dump(delete_book_by_id(book_id)), 200


class AuthorsList(Resource):
    def get(self, author_id):
        schema = BookSchema()
        return schema.dump(get_all_books_author(author_id), many=True), 200

    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    def delete(self, author_id):
        schema = AuthorSchema()
        if get_author_by_id(author_id) is None:
            return f'Книги id={author_id} в БД нет', 400
        return schema.dump(delete_author_by_id(author_id)), 200


api.add_resource(BookList, '/api/books')
api.add_resource(BooksEdit, '/api/books/<int:book_id>')
api.add_resource(AuthorsList, '/api/authors/<int:author_id>', '/api/authors/')


# swagger = Swagger(app, template_file='docs/swagger_author.json')
swagger = Swagger(app, template_file='docs/swagger_books.yml')

if __name__ == '__main__':
    init_db(initial_records=DATA, authors_records=DATA_AUTHOR)
    app.run(debug=True)
