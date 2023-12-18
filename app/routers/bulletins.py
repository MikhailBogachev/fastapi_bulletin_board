from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.bulletins import BulletinSchema, BulletinSchemaOut
from schemas import users
from db.base import get_session
from utils import bulletins
from utils.dependecies import get_current_user


router = APIRouter(
    prefix='/bulletins',
    tags=['Bulletins']
)


@router.post("/", response_model=BulletinSchemaOut)
async def add_bulletin(
    bulletin: BulletinSchema,
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bull_type_id = await bulletins.get_bulletin_type_id_by_name(
        session=session, bull_type=bulletin.type
    )

    if not bull_type_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown bulletin type")

    new_bull_id = await bulletins.add_bulletin(
        session=session,
        bulletin=bulletin,
        bull_type_id=bull_type_id._mapping.id,
        user_id=current_user._mapping.user_id
        )
    if not new_bull_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed to add bulletin")

    new_bull_id = new_bull_id._mapping.id
    new_bull = await bulletins.get_bulletin_by_id(session=session,
                                                  bull_id=new_bull_id)
    if not new_bull:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to receive bulletin")

    return BulletinSchemaOut(**new_bull._mapping)


@router.get("/", response_model=list[BulletinSchemaOut])
async def get_bulletins(
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bulls = await bulletins.get_bulletins(session)
    return [BulletinSchemaOut(**bul._mapping) for bul in bulls]


@router.get("/{bulletin_id}", response_model=BulletinSchemaOut)
async def get_bulletins_by_id(
    bulletin_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bull = await bulletins.get_bulletin_by_id(session=session,
                                              bull_id=bulletin_id)
    if not bull:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown bulletin")
    return BulletinSchemaOut(**bull._mapping)


@router.delete("/{bulletin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bulletins_by_id(
    bulletin_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bull = await bulletins.get_bulletin_by_id(session=session,
                                              bull_id=bulletin_id)
    if not bull:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown bulletin")
    bull = bull._mapping

    cur_user = current_user._mapping
    if bull.author_id != cur_user.user_id and not cur_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No rights to perform the operation")

    await bulletins.delete_bulletin_by_id(session=session,
                                          bull_id=bulletin_id)
    return


@router.patch("/{bulletin_id}", response_model=BulletinSchemaOut)
async def change_bulletin_type(
    bulletin_id: int,
    bulletin_type: str,
    session: AsyncSession = Depends(get_session),
    current_user: users.User = Depends(get_current_user)
):
    bull = await bulletins.get_bulletin_by_id(session=session,
                                              bull_id=bulletin_id)
    if not bull:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown bulletin")
    bull = bull._mapping

    cur_user = current_user._mapping
    if bull.author_id != cur_user.user_id and not cur_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No rights to perform the operation")

    bull_type_id = await bulletins.get_bulletin_type_id_by_name(
        session=session, bull_type=bulletin_type)
    if not bull_type_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown bulletin type")
    bull_type_id = bull_type_id._mapping.id

    updated_bull = await bulletins.change_bulletin_type(
        session=session, bull_id=bulletin_id, bull_type_id=bull_type_id
    )
    if not updated_bull:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to change bulletin type")
    return updated_bull
