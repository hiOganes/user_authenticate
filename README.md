# User Authenticate

## Warning

Перед изучением проета, хочу заметить, что в проекте 
не были спрятаны конфеденциальные данные.
Это было сделанно намеренно, для простоты установки проекта.
В любом другом случае данные нужно скрывать с помощью определенных инструментов
которые были для этого созданы, например файла: .env

## Description

Это приложение позоляет проходить аутентификацию по номеру телефона и коду из СМС.
Также здесь можно активировать код приглашения других пользователей и посмотреть на тех, кто активировал твой код

## Functional

1. Отпарвка кода по СМС, это отдельный эндпоинт, который:
   - Имитирует отправку кода по СМС в виде задержки на 2 секунды
   - Проверяет есть ли номер телефона в бд, если нет записывает
   - Генерирует и записывает код приглашения для этого юзера
   - Записывает код смс в бд и время до которого код будет действовать
   - Возвращает код который должен был быть отправлен по СМС
2. Профиль пользователя:
   - Можно увидеть номера всех пользователей которые испльзовали код приглашения нашего пользователя
   - Можно проверить существует ли определенный код приглашения
   - 1 раз можно активировать любой код приглашения
3. Аутентификация:
   - Второй шаг после получения смс кода, это аутентификация с помощью этого кода
   - Также можно поменять токены с помощью refresh токена

## Table of Contents

- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)

## Technologies

- Python 3.12.3
- Django 5.2.4
- PostgreSQL 17.5

## Installation

1. Clone the repository
    ```
    https://github.com/hiOganes/user_authenticate.git
    ```

2. Create and activate a virtual environment
    ```
    python3 -m venv .venv
    source .venv/bin/activate # for linux
   
    python -m venv .venv
    .venv\Scripts\activate # for Windows
    ```

3. Install dependencies
    ```
    pip install -r requirements.txt
    ```

4. Change database data in the `setting.py` file
    ```
   DATABASES = {
       "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "your_db_name",
            "USER": "your_user_db_name",
            "PASSWORD": "your_password",
            "HOST": "your_host_name",
            "PORT": "port_psql",
        }
    }
   
    ```

## Configuration

1. Apply database migrations
    ```
    python manage.py migrate
    ```

## Running the Project

1. Start the development server
    ```
    python manage.py runserver
    ```
3. Open your browser and go to [ReDoc](http://127.0.0.1:8000/api/schema/redoc/)
3. Open your browser and go to [OpenAPI](http://127.0.0.1:8000/api/schema/swagger-ui/)
