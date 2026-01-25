from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import invoice, auth, gst   # ✅ import routers

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ INCLUDE ROUTERS (AFTER app exists)
app.include_router(auth.router)
app.include_router(invoice.router)
app.include_router(gst.router)

# ✅ HEALTH CHECK
@app.get("/")
def home():
    return {"status": "Billing API running"}
