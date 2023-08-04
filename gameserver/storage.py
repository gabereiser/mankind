from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from items.base.item import item

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/mankind.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def save_item(item: item) -> bool:
    return True
