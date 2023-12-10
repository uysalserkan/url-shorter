"""URL Shorter API."""
import io
from datetime import datetime, timedelta
from fastapi import FastAPI, Response, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
from sqlmodel import create_engine, Session, select
from models.urls import URLS
from minio import Minio
from config import settings
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="URL Shorter Service",
    description="Short your long url links.",
)

Instrumentator().instrument(app).expose(app)

sqlite_file_name = "models/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

minio_client = Minio(
    endpoint=settings.default.MINIO_SERVER,
    access_key=settings.development.MINIO_USERNAME,
    secret_key=settings.development.MINIO_PASSWORD,
    secure=False
)


def create_bucket():
    """Create minio bucket."""
    try:
        minio_client.make_bucket(settings.default.MINIO_BUCKET)

    except Exception as exc:
        raise f"Some error countered: {exc}"


def upload_minio(file: UploadFile, days, mins) -> str:
    """Upload a file to minio server."""
    try:
        short_name = generate_short()

        result = minio_client.put_object(
            bucket_name=settings.default.MINIO_BUCKET,
            object_name=short_name,
            data=file.file,
            length=file.size,
            metadata={
                'filename': file.filename,
                'content_type': file.content_type,
                'headers': file.headers,
                'size': file.size
            }
        )

        minio_save_db(short_name=short_name, days=days,mins=mins)

        return short_name

    except Exception as exc:
        print("Failed from upload a file", exc)


def get_minio_object(short_name: str):
    """Get minio object."""
    try:
        obj = minio_client.get_object(
            bucket_name=settings.default.MINIO_BUCKET,
            object_name=short_name
        )

        return obj

    except Exception as exc:
        print(f"Encountered error when trying to get object:", exc)


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


def get_full_url(short_url: str) -> str:
    """Docstring."""
    with (Session(engine) as sess):
        full_url = sess.exec(select(URLS.long_url).filter(URLS.generated_url == short_url)).first()

        return full_url


def is_minio_object(short_url: str) -> bool:
    """Check this short url is minio object or not."""
    with (Session(engine) as sess):
        full_url = sess.exec(select(URLS.long_url).filter(URLS.generated_url == short_url)).first()

        if full_url == settings.default.MINIO_OBJECT:
            return True

        return False


@app.get(
    path='/all',
    description="All short urls"
)
def shorts():
    """Docstring."""
    return get_all_shorts()


def minio_save_db(short_name: str, days: int, mins: int) -> bool:
    """Create minio object url to db."""

    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=days, minutes=mins).total_seconds()

    expire_date = unix_time + delta

    url_obj = URLS(
        long_url=settings.default.MINIO_OBJECT,
        generated_url=short_name,
        expire_date=expire_date
    )
    print("URL object is:", url_obj)

    with Session(engine) as session:
        session.add(url_obj)
        session.commit()
        session.refresh(url_obj)



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
def create_url(url: str, days: int = 0, mins: int = 0):
    """Docstring"""
    print("URL is:", url)
    if not days and not mins:
        return "Please enter any mins or days value."

    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=days, minutes=mins).total_seconds()

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


@app.post("/file")
def upload_file(file: UploadFile, days: int = 0, mins: int = 0):
    """Upload a file to minio."""
    if not days and not mins:
        return "Please enter any mins or days value."

    try:
        is_bucket_exist = minio_client.bucket_exists(settings.default.MINIO_BUCKET)

        if not is_bucket_exist:
            create_bucket()

        short_name = upload_minio(file=file, days=days, mins=mins)

        return JSONResponse(
            status_code=200,
            content={
                "info": f"Upload done, url is: {short_name}"
            }
        )

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=f"Fake uploaded Failed. {exc}."
        )


@app.get("/{short_url}")
def redirect(short_url: str):
    """Docstring."""
    if is_minio_object(short_url):
        obj = get_minio_object(short_name=short_url)
        response = Response(content=obj.read(), media_type=obj.info()['Content-Type'])
        response.headers["Content-Disposition"] = f"attachment; filename={obj.info()['x-amz-meta-filename']}"

    else:
        full_url = get_full_url(short_url=short_url)
        response = RedirectResponse(url=full_url)

    return response
