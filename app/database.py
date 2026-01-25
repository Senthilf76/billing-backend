from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL credentials
username = "root"
password = "Senthil@07"  # your actual password
host = "localhost"
database = "gst_billings"

# URL-encode the password
encoded_password = quote_plus(password)

# Create the database URL
DATABASE_URL = f"mysql+pymysql://{username}:{encoded_password}@{host}/{database}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Optional: create tables
Base.metadata.create_all(bind=engine)
