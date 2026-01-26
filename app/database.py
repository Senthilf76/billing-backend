import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read environment (default to production on Railway)
ENV = os.getenv("ENV", "production")

# Choose database URL
if ENV == "local":
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
else:
    # IMPORTANT: use DB_URL instead of DATABASE_URL on Railway
    DATABASE_URL = os.getenv("DB_URL")

# Safety check
if not DATABASE_URL:
    raise RuntimeError("DB_URL is not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
