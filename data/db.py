
import os
from pathlib import Path

from sqlmodel import Session, create_engine


# Usa PostgreSQL quando DATABASE_URL estiver configurada.
# Caso contrário, utiliza SQLite localmente.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fintechguard.db"
)

# Compatibilidade com URLs antigas do PostgreSQL.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

# Configuração específica do SQLite.
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "customer_support_tickets.csv"


def get_session():
    with Session(engine) as session:
        yield session
