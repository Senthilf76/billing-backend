import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load local env file ONLY if DB_URL is not already set
if "DB_URL" not in os.environ:
    try:
        from dotenv import load_dotenv
        load_dotenv(".env.local")
    except Exception:
        pass  # dotenv not required in production

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DB_URL is not set. "
        "Set it locally in .env.local or as an environment variable."
    )

# ✅ IMPORTANT: MySQL + Railway safe engine config
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # prevents stale connections
    pool_recycle=1800,      # reconnect every 30 min
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
