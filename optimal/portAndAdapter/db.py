from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine,Connection
from collections.abc import Generator

engine: Engine | None = None

def get_db() -> Generator[Connection,None,None]:
    if engine is None:
        raise RuntimeError("not init engine first")
    with engine.begin() as conn:
        yield conn

def init_db(db_url: str) -> None:
    global engine
    engine = create_engine(db_url, future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    sku TEXT PRIMARY KEY,
                    stock INTEGER NOT NULL
                )
                """
            )
        )
        count = conn.execute(text("SELECT COUNT(*) FROM inventory")).scalar_one()
        if count == 0:
            conn.execute(
                text("INSERT INTO inventory(sku, stock) VALUES (:sku, :stock)"),
                [{"sku": "ABC", "stock": 10}, {"sku": "XYZ", "stock": 2}],
            )
