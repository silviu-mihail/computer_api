import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from authentication_model import User
from auth_logger import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "authenticator.db")

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class AuthenticationRepository:
    @staticmethod
    async def insert_user(email, password):
        logger.info('Trying to insert an user into the database')

        async with AsyncSessionLocal() as session:
            async with session.begin():
                user = User(email=email, password=password)
                session.add(user)

    @staticmethod
    async def get_user(email):
        logger.info('Trying to fetch an user from the database')

        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user
