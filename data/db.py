from pathlib import Path

from sqlmodel import Session, create_engine


DATABASE_URL = "sqlite:///./fintechguard.db"

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "customer_support_tickets.csv"

engine = create_engine(
    DATABASE_URL,
    echo=False
)


def get_session():
    with Session(engine) as session:
        yield session