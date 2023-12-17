from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependecies import get_current_user
from db.base import get_session
from schemas import users
from utils import users as users_utils
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=['Bulletins']
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
    user = await users_utils.get_user_by_email(session=session, email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user[3]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_utils.create_user_token(session=session, user_id=user[0])

@router.get("/users/me", response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user
