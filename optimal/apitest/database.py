from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decimal import Decimal
from datetime import datetime
from model import Base, ConversionRate
from setting import get_settings

setting_for_this = get_settings()


engine = create_engine(setting_for_this.db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind= engine)


RATES = {
    ("USD", "EUR"): Decimal("0.91"),
    ("EUR", "USD"): Decimal("1.10"),
    ("USD", "JPY"): Decimal("150.0"),
}


def seed_rates() -> None:
    with SessionLocal() as session:
        existing = session.query(ConversionRate).first()
        if existing is not None:
            return
        now = datetime.now()
        for (from_currency, to_currency), rate in RATES.items():
            session.add(
                ConversionRate(
                    from_currency=from_currency,
                    to_currency=to_currency,
                    rate=rate,
                    timestamp=now,
                )
            )
        session.commit()

Base.metadata.create_all(bind= engine)

seed_rates()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()