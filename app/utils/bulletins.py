from sqlalchemy import desc, literal_column, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.bulletins import BulletinSchema
from models.bulletins import bulletins_table, bulletin_types_table
from models.users import users_table


async def get_bulletins(session: AsyncSession) -> list[bulletins_table]:
    query = select(bulletins_table
                   ).join(bulletin_types_table
                          ).join(users_table
                                 ).order_by(desc(bulletins_table.c.created_at))
    result = await session.execute(query)
    return result.all()


async def add_bulletin(
    session: AsyncSession,
    bulletin: BulletinSchema,
    bull_type_id: int,
    user_id: int
) -> bulletins_table:
    query = bulletins_table.insert().values(
        name=bulletin.name,
        description=bulletin.description,
        type=bull_type_id,
        author_id=user_id
    )
    result = await session.execute(query)
    await session.commit()
    return result.inserted_primary_key


async def get_bulletin_by_id(session: AsyncSession, bull_id: int):
    query = select(bulletins_table
                   ).join(bulletin_types_table
                          ).join(users_table
                                 ).where(bulletins_table.c.id == bull_id)
    result = await session.execute(query)
    return result.first()


async def get_bulletin_type_id_by_name(session: AsyncSession, bull_type: str):
    query = select(bulletin_types_table.c.id).where(
        bulletin_types_table.c.name == bull_type
    )
    result = await session.execute(query)
    return result.first()


async def delete_bulletin_by_id(session: AsyncSession, bull_id: int):
    query = delete(bulletins_table).where(bulletins_table.c.id == bull_id)
    await session.execute(query)
    await session.commit()
    return


async def change_bulletin_type(
        session: AsyncSession,
        bull_id: int,
        bull_type_id: int
):
    query = bulletins_table.update().where(
        bulletins_table.c.id == bull_id
    ).values(type=bull_type_id).returning(literal_column('*'))

    result = await session.execute(query)
    await session.commit()
    return result.first()
