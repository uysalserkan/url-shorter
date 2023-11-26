"""Class defination for using and creating SQL Lite schemas."""
import random
import string
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


class URLS(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    long_url: str = Field(nullable=False)
    generated_url: str = Field(nullable=True)
    created_date: int = datetime.utcnow().timestamp()
    expire_date: int = Field(nullable=False)

    @classmethod
    def generate_randoms(cls):
        """Docstring."""
        characters = string.ascii_letters + string.digits

        return ''.join(random.choice(characters) for _ in range(10))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_db_and_tables()
