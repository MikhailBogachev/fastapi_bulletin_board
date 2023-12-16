from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from main import BulletinSchema
from models.bulletins import bulletins_table, bulletin_types_table


async def get_bulletins(session: AsyncSession) -> list[bulletins_table]:
    query = select(bulletins_table).join(bulletin_types_table)
    result = await session.execute(query)
    return result.all()

async def add_bulletin(session: AsyncSession, bulletin: BulletinSchema) -> bulletins_table:
    query = bulletins_table.insert().values(
        **bulletin.model_dump(),

    )

async def get_bulletin_type_from_name(session: AsyncSession, type: str):
    pass
