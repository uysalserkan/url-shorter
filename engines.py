"""Database singlethon class"""
import os
from fastapi import UploadFile
from minio import Minio
from sqlmodel import create_engine, Session
from config import settings, secrets


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


class MinIOEngine(Singlethon):
    """MinIO Engine"""
    def __init__(self):
        self.client =  Minio(
            endpoint=settings.BUCKET.MINIO_SERVER,
            access_key=secrets.development.MINIO_USERNAME,
            secret_key=secrets.development.MINIO_PASSWORD,
            secure=False
        )
        self.bucket_name = settings.BUCKET.MINIO_BUCKET

    def add(self, file: UploadFile, short_name: str):
        try:
            _ = self.put_object(
                bucket_name=self.bucket_name,
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

        except Exception as exc:
            print("Error:", exc)

    def get(self, short_name: str):
        try:
            return self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=short_name
            )

        except Exception as exc:
            print("Error", exc)

    def create_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)

        except Exception as exc:
            print(exc)

    def delete(self, short_url):
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=short_url
            )

        except Exception as exc:
            print(exc)
