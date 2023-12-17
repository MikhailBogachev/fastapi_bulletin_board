from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.bulletins import BulletinSchema, BulletinTypeSchema
from schemas.users import UserBase

from models.bulletins import bulletins_table, bulletin_types_table
from models.users import users_table


async def get_bulletins(session: AsyncSession) -> list[bulletins_table]:
    query = select(bulletins_table).join(bulletin_types_table)
    result = await session.execute(query)
    return result.all()

async def add_bulletin(
        session: AsyncSession,
        bulletin: BulletinSchema,
        bul_type_id: int,
        user_id: int
) -> bulletins_table:
    query = bulletins_table.insert().values(
        name=bulletin.name,
        description=bulletin.description,
        type=bul_type_id,
        author_id=user_id
    )
    result = await session.execute(query)
    return result.inserted_primary_key

async def get_bulletin_by_id(session: AsyncSession, bul_id: int):
    query = select(bulletins_table).join(bulletin_types_table).join(users_table)
    result = await session.execute(query)
    print(result)
    return result.all()

async def get_bulletin_type_from_name(session: AsyncSession, bul_type: str) -> BulletinTypeSchema:
    query = select(bulletin_types_table).where(bulletin_types_table.c.name == bul_type)
    result = await session.execute(query)
    return BulletinTypeSchema(**result.all()[0]._mapping)
