"""URL Shorter API."""
import multiprocessing
import time
from datetime import datetime, timedelta

from fastapi import FastAPI, Response, UploadFile, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlmodel import select
from prometheus_fastapi_instrumentator import Instrumentator

from models.urls import URLS
from controller.url_c import URLController
from config import settings, secrets
from engines import DatabaseEngine, MinIOEngine

app = FastAPI(
    title="URL Shorter Service",
    description="Short your long url links.",
)

Instrumentator().instrument(app).expose(app)


DB_engine = DatabaseEngine()
MINIO_engine = MinIOEngine()


def delete_cron():
    """Delete expired urls."""
    while True:
        all_entries = DB_engine.get(statement=select(URLS), first=False)
        cur_time = time.time()
        for each_entry in all_entries:
            if each_entry.expire_date - cur_time <= 0:
                url_obj = URLController.get(each_entry.id)
                if url_obj.long_url == settings.BUCKET.MINIO_OBJECT:
                    print("MinIO Object", url_obj.long_url, "will be deleted.")
                    MinIOEngine.delete(short_url=url_obj.generated_url)
                    URLController.delete(url_id=url_obj.id)
                else:
                    print("Short URL", url_obj.long_url, "will be deleted.")
                    URLController.delete(url_id=url_obj.id)
            else:
                print("remain", each_entry.id)
        time.sleep(settings.REMOVE.CHECK_DELAY)


def upload_minio(file: UploadFile, days, hours, mins) -> str:
    """Upload a file to minio server."""
    try:
        short_name = generate_short()
        MINIO_engine.add(file=file, short_name=short_name)
        minio_save_db(short_name=short_name, days=days, hours=hours, mins=mins)

        return short_name

    except Exception as exc:
        print("Failed from upload a file", exc)


def get_minio_object(short_name: str):
    """Get minio object."""
    try:
        obj = MINIO_engine.get(short_name=short_name)

        return obj

    except Exception as exc:
        print("Encountered error when trying to get object:", exc)


def get_all_shorts():
    """Docstrings."""
    all_inputs = DB_engine.get(statement=select(URLS.generated_url), first=False)

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
    full_url = DB_engine.get(
        statement=select(URLS.long_url).filter(URLS.generated_url == short_url),
        first=True
    )

    return full_url


def is_minio_object(short_url: str) -> bool:
    """Check this short url is minio object or not."""
    full_url = DB_engine.get(
        statement=select(URLS.long_url).filter(URLS.generated_url == short_url),
        first=True
    )

    if full_url == settings.BUCKET.MINIO_OBJECT:
        return True

    return False


@app.on_event("startup")
async def before_startup():
    MINIO_engine.create_bucket()

    delete_process = multiprocessing.Process(target=delete_cron)
    delete_process.start()


@app.get(
    path='/all',
    description="All short urls"
)
def shorts():
    """Docstring."""
    return get_all_shorts()


def minio_save_db(short_name: str, days: int, hours: int, mins: int):
    """Create minio object url to db."""

    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=days, hours=hours, minutes=mins).total_seconds()

    expire_date = unix_time + delta

    url_obj = URLS(
        long_url=settings.BUCKET.MINIO_OBJECT,
        generated_url=short_name,
        expire_date=expire_date
    )

    DB_engine.add(obj=url_obj, batch=False)


@app.get(
    path='/',
    description="Home page.",
)
async def home_page(request: Request):
    """Docstring."""
    agent = request.headers.get("User-Agent").lower()
    if ("curl" in agent) or ("wget" in agent) or ("postman" in agent):
        print("Agent->", agent)
    print("User Agent:", agent)
    return request.headers


@app.post(
    path='/create',
    description="Create a new url shorter."
)
def create_url(url: str, days: int = 0, hours: int = 0, mins: int = 0):
    """Docstring"""
    print("URL is:", url)
    if not days and not hours and not mins:
        return "Please enter any mins or days value."

    unix_time = datetime.utcnow().timestamp()
    delta = timedelta(days=days, hours=hours, minutes=mins).total_seconds()

    expire_date = unix_time + delta

    url_obj = URLS(
        long_url=url,
        generated_url=generate_short(),
        expire_date=expire_date
    )
    print("URL object is:", url_obj)

    DB_engine.add(obj=url_obj, batch=False)

    return url_obj


@app.post("/file")
def upload_file(file: UploadFile, days: int = 0, hours: int = 0, mins: int = 0):
    """Upload a file to minio."""
    if not days and not hours and not mins:
        return "Please enter any mins or days value."

    try:
        short_name = upload_minio(file=file, days=days, hours=hours, mins=mins)

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
def redirect(short_url: str, request: Request):
    """Docstring."""
    is_browser = True
    agent = request.headers.get("User-Agent").lower()
    if ("curl" in agent) or ("wget" in agent) or ("postman" in agent):
        is_browser = False

    if is_minio_object(short_url):
        obj = get_minio_object(short_name=short_url)
        response = Response(content=obj.read(), media_type=obj.info()['Content-Type'])
        response.headers["Content-Disposition"] = f"attachment; filename={obj.info()['x-amz-meta-filename']}"

        # if is_browser:
        #     response = Response(content="# Header", media_type="text/html")
        #     response.status_code = 302

    else:
        full_url = get_full_url(short_url=short_url)
        if is_browser:
            response = RedirectResponse(url=full_url)
        else:
            response = full_url

    return response
