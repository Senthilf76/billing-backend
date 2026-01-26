from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.database import engine, Base
from app.routers import auth, invoice, gst

app = FastAPI()


@app.on_event("startup")
async def startup():
    # ✅ Create tables
    Base.metadata.create_all(bind=engine)

    # 🔐 Create admin user IF NOT EXISTS
    from app.database import SessionLocal
    from app.models.user import User
    from app.utils.security import get_password_hash

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created")
        else:
            print("ℹ️ Admin user already exists")
    finally:
        db.close()


# ✅ CORS (PRODUCTION SAFE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gst-billing-frontend.vercel.app",
    ],
    allow_credentials=False,  # IMPORTANT (no cookies)
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ GLOBAL OPTIONS HANDLER (CRITICAL FIX)
@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    return Response(status_code=200)


# ✅ Routers
app.include_router(auth.router)
app.include_router(invoice.router)
app.include_router(gst.router)


@app.get("/")
def root():
    return {"status": "Billing API running"}
