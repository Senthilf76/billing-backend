import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read environment
ENV = os.getenv("ENV", "production")

# Choose database URL
if ENV == "local":
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

# Safety check (VERY IMPORTANT)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

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
