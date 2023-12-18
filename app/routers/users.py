from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependecies import get_current_user
from db.base import get_session
from schemas import users
from utils import users as users_utils
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post("/sign-up", response_model=users.User)
async def create_user(
    user: users.UserCreate,
    session: AsyncSession = Depends(get_session)
):
    db_user = await users_utils.get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(session, user=user)


@router.post("/auth", response_model=users.TokenBase)
async def auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await users_utils.get_user_by_email(session=session,
                                               email=form_data.username)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect email or password")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user[0][3]
    ):
        raise HTTPException(status_code=400,
                            detail="Incorrect email or password")

    return await users_utils.create_user_token(session=session,
                                               user_id=user[0][0])


@router.get("/{user_id}/make-admin", response_model=users.UserBase)
async def make_user_an_admin(
    user_id: int,
    current_user: users.User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    cur_user = current_user._mapping
    if not cur_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No rights to perform the operation")

    user = await users_utils.get_user_by_id(session=session,
                                            user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown user")

    updated_user = await users_utils.make_user_an_admin(session=session,
                                                        user_id=user_id)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update user")

    return updated_user


@router.get("/{user_id}/ban", response_model=users.UserBase)
async def ban_user(
    user_id: int,
    current_user: users.User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    cur_user = current_user._mapping
    if not cur_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No rights to perform the operation")

    user = await users_utils.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown user")

    updated_user = await users_utils.ban_unban_user(
        session=session, user_id=user_id, ban=True
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to ban user")

    return updated_user


@router.get("/{user_id}/unban", response_model=users.UserBase)
async def unban_user(
    user_id: int,
    current_user: users.User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    cur_user = current_user._mapping
    if not cur_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No rights to perform the operation")

    user = await users_utils.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unknown user")

    updated_user = await users_utils.ban_unban_user(
        session=session, user_id=user_id, ban=False
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to unban user")

    return updated_user
