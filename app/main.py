from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import Base, async_session, engine
from app.tasks import verify_signup_task, signup_task
app = FastAPI()


async def get_session():
    try:
        session = async_session()
        yield session
    finally:
        await session.close()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/signup")
async def signup(user: User, session: AsyncSession = Depends(get_session)):
    existent_username, existent_email = await verify_signup_task(user, session)
    if existent_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use."
        )
    if existent_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )
    await signup_task(user, session)


@app.post("/login")
async def login():
    return
