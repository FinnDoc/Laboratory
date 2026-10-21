from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./news.db"

# FastAPI обрабатывает запросы в пуле потоков, а соединение SQLite
# по умолчанию разрешено использовать только в создавшем его потоке.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# LOWER и LIKE в SQLite не меняют регистр кириллицы.
@event.listens_for(engine, "connect")
def _register_unicode_lower(dbapi_connection, _):
    dbapi_connection.create_function(
        "py_lower", 1, lambda value: value.lower() if isinstance(value, str) else value
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
