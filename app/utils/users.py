import hashlib
import random
import string
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

# from app.models.database import database
from models.users import tokens_table, users_table
from schemas import users as user_schema

def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(session: AsyncSession, email: str):
    """ Возвращает информацию о пользователе """
    query = users_table.select().where(users_table.c.email == email)
    result = await session.execute(query)
    return result.all()[0]


async def get_user_by_token(session: AsyncSession, token: str):
    """ Возвращает информацию о владельце указанного токена """
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    result = await session.execute(query)
    return result.all()[0]


async def create_user_token(session: AsyncSession, user_id: int):
    """ Создает токен для пользователя с указанным user_id """
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    result = await session.execute(query)
    await session.commit()
    return result.all()[0]


async def create_user(session: AsyncSession, user: user_schema.UserCreate):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}"
    ).returning(users_table.c.id, users_table.c.name, users_table.c.email)

    user = await session.execute(query)
    user_all = user.all()[0]
    user_id = user_all[0]

    token = await create_user_token(session=session, user_id=user_id)
    token_dict = {"token": UUID(token[0]), "expires": token[1]}

    await session.commit()

    return {"name": user_all[1], "email": user_all[2], "id": user_id, "is_active": True, "token": token_dict}
