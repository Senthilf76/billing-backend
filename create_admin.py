from app.database import SessionLocal
from app.models.user import User
from app.utiles.security import hash_password

db = SessionLocal()

admin = User(
    username="admin",
    password_hash=hash_password("admin@123"),
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("✅ Admin user created successfully")
