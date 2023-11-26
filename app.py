"""URL Shorter API."""
from datetime import datetime, timedelta
from fastapi import FastAPI
from sqlmodel import create_engine, Session, select
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
    with Session(engine) as sess:
        all_inputs = sess.exec(select(URLS.generated_url)).all()

        return all_inputs


def generate_short():
    """Docstrings."""
    all_shorts_list = get_all_shorts()
    while True:
        generated_short = URLS.generate_randoms()
        if generated_short not in all_shorts_list:
            return generated_short


@app.get(
    path='/all',
    description="All short urls"
)
def shorts():
    """Docstring."""
    return get_all_shorts()


@app.get(
    path='/',
    description="Home page.",
)
def home_page():
    """Docstring."""
    return "Amazing Home page."


@app.post(
    path='/create',
    description="Create a new url shorter."
)
def create_url(url: str, day: int, mins: int):
    """Docstring"""
    print("URL is:", url)
    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=day, minutes=mins).total_seconds()

    expire_date = unix_time + delta

    url_obj = URLS(
        long_url=url,
        generated_url=generate_short(),
        expire_date=expire_date
    )
    print("URL object is:", url_obj)

    with Session(engine) as session:
        session.add(url_obj)
        session.commit()
        session.refresh(url_obj)

    return url_obj
