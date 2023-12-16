from fastapi import APIRouter, Depends, HTTPException
from db.base import get_session
from utils.bulletins import get_bulletins as get_bulletins_from_db
from main import BulletinSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix='/bulletins',
    tags=['Posts'],
)

@router.post("/")
async def add_bulletin(
    bullet: BulletinSchema,
    session: AsyncSession = Depends(get_session)
):
    pass


@router.get("", response_model=list[BulletinSchema])
async def get_bulletins(session: AsyncSession = Depends(get_session)):
    bulletins = await get_bulletins_from_db(session)
    return bulletins