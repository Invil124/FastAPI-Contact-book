import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

DATABASE_URL = config.get("DB", "url")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
