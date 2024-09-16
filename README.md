# Книги

## Описание

Этот проект представляет собой Flask REST API для хранения, добавления, изменения и удаления книг и авторов в базе данных.

## Функциональность

- **Flask RESTful**: Использована библиотека `flask_restful` для создания REST API.
- **Marshmallow**: Использована библиотека `marshmallow` для создания схем: Книги, Добавления книги и Автора. Также используется для валидации и упрощения сериализации и десериализации объектов.
- **Flasgger**: Использована библиотека `flasgger` для создания Swagger документации в формате YAML и JSON.
- **SQLite**: Создана база данных с использованием SQLite.
- **Postman**: Создана коллекция Postman для запросов к серверу.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/MaryNGer/book_table.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd book_table
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите Flask приложение:
   ```bash
   python routes.py
   ```

## Использование

1. Запустите Flask приложение из файла `routes.py`.
2. Перейдите на сайт [http://localhost:5000](http://localhost:5000).
3. Просмотр документации: [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/).
4. Добавьте коллекцию Postman и откройте ее методы для взаимодействия с API.

## Примеры запросов

### Получение списка книг

```bash
GET http://localhost:5000/books
```

### Добавление новой книги

```bash
POST http://localhost:5000/books
Content-Type: application/json

{
  "title": "Новая книга",
  "author": id-автора
}
```

### Обновление информации о книге

```bash
PUT http://localhost:5000/books/1
Content-Type: application/json

{
  "title": "Обновленная книга",
  "author": id-автора
}
```

### Удаление книги

```bash
DELETE http://localhost:5000/books/1
```

## Тестирование

Для тестирования API используйте коллекцию Postman, которая предоставлена в репозитории.


## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной:

- Email: ваш-email@example.com
- Telegram: [Your_4_Mind](https://t.me/Your_4_Mind)

