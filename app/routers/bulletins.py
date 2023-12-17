from fastapi import APIRouter, Depends, HTTPException
from schemas.bulletins import BulletinSchema

from db.base import get_session
from utils import bulletins
from sqlalchemy.ext.asyncio import AsyncSession
from utils.dependecies import get_current_user
from schemas import users




router = APIRouter(
    prefix='/bulletins',
    tags=['Bulletins']
)

@router.post("/")
async def add_bulletin(
    bulletin: BulletinSchema,
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bul_type = await bulletins.get_bulletin_type_from_name(session=session, bul_type=bulletin.type)
    print(bul_type)
    if not bul_type.id:
        # 
        raise HTTPException(status_code=400, detail=" Unknown bblletin type ")

    new_bul = await bulletins.add_bulletin(
        session=session, 
        bulletin=bulletin,
        bul_type_id=bul_type.id,
        user_id=current_user._mapping.user_id
        )
    
    return 1


@router.get("", response_model=list[BulletinSchema])
async def get_bulletins(session: AsyncSession = Depends(get_session)):
    bulletins = await bulletins.get_bulletins_from_db(session)
    return bulletins