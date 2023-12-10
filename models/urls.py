"""Class defination for using and creating SQL Lite schemas."""
from pathlib import Path
import sys
import random
import string
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine

FOLDER_PATH = Path(__file__).resolve().parent
ROOT_PATH = FOLDER_PATH.parent
sys.path.append(str(ROOT_PATH))

from config import settings

sql_file_path = settings.DATABASE.NAME
sqlite_url = f"sqlite:///{sql_file_path}"

engine = create_engine(sqlite_url, echo=False)


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
