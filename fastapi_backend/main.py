from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers.predictions import router as predictions_router
from .routers.auth import router as auth_router
from .routers.users import router as users_router

# Crea las tablas en BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Caregiver Overload Prediction System",
    version="1.0.0",
    description="API para predicción de sobrecarga en cuidadores",
)

# ── CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # En producción reemplazar con el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────
app.include_router(auth_router)                          # /auth/token
app.include_router(predictions_router, prefix="/api/v1") # /api/v1/predictions
app.include_router(users_router, prefix="/api/v1")       # /api/v1/users

# ── Health check ───────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
