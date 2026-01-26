import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env.local ONLY for local development
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv(".env.local")

# Detect environment
ENV = os.getenv("ENV", "local")

if ENV == "local":
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
else:
    DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise RuntimeError("Database URL is not set for current environment")

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
