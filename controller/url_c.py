"""URL Controllers."""
import os
import sys
from pathlib import Path
from sqlmodel import select


FOLDER_PATH = Path(__file__).resolve().parent
ROOT_PATH = FOLDER_PATH.parent
sys.path.append(str(ROOT_PATH))

from models.urls import URLS
from engines import DatabaseEngine

DB_engine = DatabaseEngine()


class URLController:
    """Universal URL Controller."""
    @classmethod
    def get(cls, url_id):
        """Get URL object with id field."""
        try:
            url_obj = DB_engine.get(statement=select(URLS).where(URLS.id == url_id), first=True)

            return url_obj

        except Exception as exc:
            print("ERROR:", exc)

    @classmethod
    def delete(cls, url_id):
        """Delete a url with id field."""
        try:
            url_obj = cls.get(url_id=url_id)
            status = DB_engine.delete(obj=url_obj, batch=False)
            if not status:
                raise Exception("Did not delete.")

        except Exception as exc:
            print("ERROR:", exc)


if __name__ == '__main__':
    URLController.delete(7)
