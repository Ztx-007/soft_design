from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from decimal import Decimal
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_currency: Mapped[str] = mapped_column(String)
    to_currency: Mapped[str] = mapped_column(String)
    amount: Mapped[Decimal] = mapped_column()
    result: Mapped[Decimal] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default = datetime.now())

class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_currency: Mapped[str] = mapped_column(String)
    to_currency: Mapped[str] = mapped_column(String)
    rate: Mapped[Decimal] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default = datetime.now())
