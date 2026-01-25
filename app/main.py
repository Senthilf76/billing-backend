from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import invoice, auth, gst

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ RUN DB INIT ON STARTUP (SAFE)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ INCLUDE ROUTERS
app.include_router(auth.router)
app.include_router(invoice.router)
app.include_router(gst.router)

# ✅ HEALTH CHECK
@app.get("/")
def home():
    return {"status": "Billing API running"}
