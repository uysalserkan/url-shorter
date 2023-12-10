"""URL Controllers."""
import os
import sys
from pathlib import Path
from sqlmodel import create_engine, Session, select


FOLDER_PATH = Path(__file__).resolve().parent
ROOT_PATH = FOLDER_PATH.parent
sys.path.append(str(ROOT_PATH))

from models.urls import URLS
from config import settings

sql_file_path = os.path.join(ROOT_PATH, settings.DATABASE.FOLDER_PATH, settings.DATABASE.NAME)
sqlite_url = f"sqlite:///{sql_file_path}"

engine = create_engine(sqlite_url, echo=False)


class URLController:
    """Universal URL Controller."""
    @classmethod
    def get(cls, url_id):
        """Get URL object with id field."""
        try:
            with Session(engine) as sess:
                url_obj = sess.exec(
                    statement=select(URLS).where(URLS.id == url_id)
                ).first()

                return url_obj

        except Exception as exc:
            print("ERROR:", exc)

    @classmethod
    def delete(cls, url_id):
        """Delete a url with id field."""
        try:
            with Session(engine) as sess:
                url_obj = cls.get(url_id=url_id)
                if not url_obj:
                    return False

                sess.delete(url_obj)

                sess.commit()

                return True

        except Exception as exc:
            print("ERROR:", exc)


if __name__ == '__main__':
    URLController.delete(7)
