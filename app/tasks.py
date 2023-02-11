import asyncio
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.dals.user_dal import UserDAL
from app.models import Token, User, UserInDB
from app.utils import create_access_token, get_password_hash, verify_password


async def signup_task(user: User, session: AsyncSession):
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(username=user.username,
                       fullname=user.fullname,
                       email=user.email,
                       hashed_password=hashed_password)
    # Add user to DB
    await add_to_user_db(db_user, session)


async def login_task(form_data: OAuth2PasswordRequestForm):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


async def verify_signup_task(user: User, session: AsyncSession):
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            existent_username = await user_dal.verify_username(user)
            existent_email = await user_dal.verify_email(user)

            return existent_username, existent_email


async def add_to_user_db(user: UserInDB, session: AsyncSession):
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            await user_dal.add_user(user)
