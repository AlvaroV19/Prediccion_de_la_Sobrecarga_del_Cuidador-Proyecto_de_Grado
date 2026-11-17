import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carga explícita del .env de este mismo paquete, sin depender de
# desde qué directorio se lance el proceso (uvicorn, pytest, etc.)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg2://postgres:1907@localhost:5432/caregiver_db'
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Dependencia de base de datos ───────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
