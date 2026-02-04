from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os


def get_engine() -> Engine:
    load_dotenv()
    db_url = os.getenv("DB_URL")
    if db_url:
        return create_engine(db_url)

    db_path = os.getenv("DB_PATH", "./data/vgsales.sqlite")
    db_path = Path(db_path).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return create_engine(f"sqlite:///{db_path}")
