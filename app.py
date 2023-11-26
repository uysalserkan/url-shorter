"""URL Shorter API."""
from datetime import datetime, timedelta
from fastapi import FastAPI
from sqlmodel import create_engine, Session
from models.urls import URLS

app = FastAPI(
    title="URL Shorter Service",
    description="Short your long url links.",
)

sqlite_file_name = "models/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def get_all_shorts():
    """Docstrings."""


@app.get(
    path='/',
    description="Home page.",
)
def home_page():
    """Docstring."""
    return "Amazing Home page."


@app.post(
    path='/create/{url}',
    description="Create a new url shorter."
)
def create_url(url: str, day: int, min: int, sec: int):
    """Docstring"""
    print("URL is:", url)
    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=day, minutes=min, seconds=sec).total_seconds()

    expire_date = unix_time + delta

    url_obj = URLS(
        long_url=url,
        generated_url="aaaa",
        expire_date=expire_date
    )
    print("URL object is:", url_obj)

    with Session(engine) as session:
        session.add(url_obj)
        session.commit()
        session.refresh(url_obj)

    return url_obj
