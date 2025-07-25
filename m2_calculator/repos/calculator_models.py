from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

Base = declarative_base()


class PowerOperation(Base):
    __tablename__ = 'power_operations'

    id = Column(Integer, primary_key=True, index=True)
    base = Column(Integer, nullable=False)
    exponent = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FactorialOperation(Base):
    __tablename__ = 'factorial_operations'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FibonacciOperation(Base):
    __tablename__ = 'fibonacci_operations'

    id = Column(Integer, primary_key=True, index=True)
    n = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
