import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# 1️⃣ Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# 2️⃣ Database connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# 3️⃣ Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    db = SessionLocal()

    username = "admin"
    password = "admin123"
    role = "admin"

    hashed_password = hash_password(password)

    # 4️⃣ INSERT using correct column name
    db.execute(
        text("""
            INSERT INTO users (username, password_hash, role)
            VALUES (:username, :password_hash, :role)
        """),
        {
            "username": username,
            "password_hash": hashed_password,
            "role": role,
        }
    )

    db.commit()
    db.close()

    print("✅ Admin user created successfully")
    print("Username:", username)
    print("Password:", password)

if __name__ == "__main__":
    create_admin()
