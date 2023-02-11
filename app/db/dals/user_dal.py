from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
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

