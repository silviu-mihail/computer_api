import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from .calculator_models import PowerOperation, FactorialOperation, FibonacciOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "calculator.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class PowerRepository:
    @staticmethod
    async def insert(base: int, exponent: int, result: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                record = PowerOperation(base=base, exponent=exponent, result=result)
                session.add(record)

    @staticmethod
    async def get_result(base: int, exponent: int):
        async with AsyncSessionLocal() as session:
            stmt = select(PowerOperation).where(
                PowerOperation.base == base,
                PowerOperation.exponent == exponent
            )
            result = await session.execute(stmt)
            return result.scalars().first()


class FactorialRepository:
    @staticmethod
    async def insert(number: int, result: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                record = FactorialOperation(number=number, result=result)
                session.add(record)

    @staticmethod
    async def get_result(number: int):
        async with AsyncSessionLocal() as session:
            stmt = select(FactorialOperation).where(FactorialOperation.number == number)
            result = await session.execute(stmt)
            return result.scalars().first()


class FibonacciRepository:
    @staticmethod
    async def insert(n: int, result: int):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                record = FibonacciOperation(n=n, result=result)
                session.add(record)

    @staticmethod
    async def get_result(n: int):
        async with AsyncSessionLocal() as session:
            stmt = select(FibonacciOperation).where(FibonacciOperation.n == n)
            result = await session.execute(stmt)
            return result.scalars().first()
