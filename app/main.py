from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import Base, async_session, engine
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
async def signup():
    return


@app.post("/login")
async def login():
    return
