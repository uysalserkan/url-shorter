"""Database singlethon class"""
import os
from sqlmodel import create_engine, Session, select
from config import settings


class Singlethon:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance


class DatabaseEngine(Singlethon):
    """Database Engine."""
    def __init__(self):
        sql_file_path = os.path.join(settings.DATABASE.FOLDER_PATH, settings.DATABASE.NAME)
        sqlite_url = f"sqlite:///{sql_file_path}"

        self.engine = create_engine(sqlite_url, echo=False)

    def get(self, statement, first: bool):
        """Get elements of the sql statement."""
        with Session(self.engine) as sess:
            results = sess.exec(
                statement=statement
            ).all()

            return results[0] if first else results

    def add(self, obj, batch: bool = False):
        """Add object."""
        if not batch:
            with Session(self.engine) as sess:
                sess.add(obj)
                sess.commit()
                sess.refresh(obj)

    def delete(self, obj, batch: bool = False) -> bool:
        """Delete object."""
        if not batch:
            with Session(self.engine) as sess:
                if not obj:
                    return False

                sess.delete(obj)
                sess.commit()

                return True
