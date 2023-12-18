# FastAPI app
### Описание
Проект в рамках тестового задания.  
Доска объявлений.  
  
Стек:  
FastAPI - web framework  
PostgreSQL - database  
Asyncpg - async driver for Postgres db  
SQLAlchemy - ORM  
Alembic - migrations  
Pydantic - validation  
Uvicorn - ASGI web server  
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MikhailBogachev/fastapi_bulletin_board.git
```

```
cd fastapi_bulletin_board
```

### Запуск. Необходим Python 3.10.*:
Создать файл .env с переменными окружения для подключения к вашей БД (за основу можно взять файл env_example):
```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=
```

Создать и активировать виртуальное окружение:  

```
python -m venv venv
```

Windows Bash
```
source venv/Scripts/activate
```

Linux
```
source venv/bin/activate
```

Установить зависимости:

```
pip install -r requirements.txt
```

Перейти в папку app:

```
cd app/
```

Выполнить миграции:
```
alembic upgrade head
```

Запустить приложение:
```
python main.py
```


После этого приложение будет доступно по адресу: http://localhost:8000/  
Дока: http://localhost:8000/docs/  
  
Все методы требуют аутентификации, кроме:  
1) POST users/sign-up - регистрация
2) POST users/auth - получения токена  
Токен требуется передавать в загаловке к каждому запросу:
```
--header 'Authorization: Bearer <token>'
```
