from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.user import User
from app.models import User as InputUser
from app.models import UserInDB


class UserDAL():
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_user(self, user: UserInDB):
        user_to_add = User(
            username=user.username,
            fullname=user.fullname,
            email=user.email,
            hashed_password=user.hashed_password
        )
        self.db_session.add(user_to_add)
        await self.db_session.commit()

    async def verify_username(self, user: InputUser):
        username_entries = await self.db_session.execute(select(User.username))
        username_list = username_entries.scalars().all()
        return user.username in username_list

    async def verify_email(self, user: InputUser):
        email_entries = await self.db_session.execute(select(User.email))
        email_list = email_entries.scalars().all()
        return user.email in email_list

