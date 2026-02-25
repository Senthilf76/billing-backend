from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

db = SessionLocal()

admin = db.query(User).filter(User.username == "admin").first()

if not admin:
    print("❌ Admin user not found")
else:
    admin.password_hash = get_password_hash("admin123")
    db.commit()
    print("✅ Admin password reset successfully (pbkdf2)")

db.close()
