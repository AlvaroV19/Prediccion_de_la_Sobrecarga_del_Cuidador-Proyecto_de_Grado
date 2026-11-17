from pathlib import Path

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from .models import PredictionRecord
from .schemas import PredictionInput

# ── Carga de artefactos ML ─────────────────────────────────────────
# Rutas ancladas a la ubicación de este archivo, no al directorio
# desde el que se ejecute el proceso (uvicorn, tests, etc.)
BASE_DIR = Path(__file__).resolve().parent
MODELOS_DIR = BASE_DIR / "modelos"

# ── Carga de artefactos ML ─────────────────────────────────────────
modelo = joblib.load(MODELOS_DIR / "modelo_gb.pkl")
scaler = joblib.load(MODELOS_DIR / "scaler.pkl")
features = joblib.load(MODELOS_DIR / "features.pkl")

# ── Lógica de predicción ───────────────────────────────────────────
def predecir(data: PredictionInput) -> int:

    datos = {
        "P1_encoded": data.P1,
        "P2_encoded": data.P2,
        "P3_encoded": data.P3,
        "P4_encoded": data.P4,
        "P5_encoded": data.P5,
        "P6_encoded": data.P6,
        "P7_encoded": data.P7,
        "P8_encoded": data.P8,
        "P9_encoded": data.P9,
        "P10_encoded": data.P10,
        "P11_encoded": data.P11,
        "P12_encoded": data.P12,
        "P13_encoded": data.P13,
        "P14_encoded": data.P14,
        "P15_encoded": data.P15,
        "P16_encoded": data.P16,
        "P17_encoded": data.P17,
        "P18_encoded": data.P18,
        "P19_encoded": data.P19,
        "P20_encoded": data.P20,
        "P21_encoded": data.P21,
        "grado_carga_encoded": data.grado_carga
    }

    df = pd.DataFrame([datos])
    X = df[features]
    X_scaled = scaler.transform(X)

    return int(modelo.predict(X_scaled)[0])

# ── Guardar predicción en BD ───────────────────────────────────────
def guardar_prediccion(db: Session, data: PredictionInput, user_id: int,) -> PredictionRecord:

    pred = predecir(data)

    registro = PredictionRecord(
        user_id=user_id,
        P1=data.P1,
        P2=data.P2,
        P3=data.P3,
        P4=data.P4,
        P5=data.P5,
        P6=data.P6,
        P7=data.P7,
        P8=data.P8,
        P9=data.P9,
        P10=data.P10,
        P11=data.P11,
        P12=data.P12,
        P13=data.P13,
        P14=data.P14,
        P15=data.P15,
        P16=data.P16,
        P17=data.P17,
        P18=data.P18,
        P19=data.P19,
        P20=data.P20,
        P21=data.P21,
        grado_carga=data.grado_carga,
        prediccion=pred
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro

# ── Consultas ──────────────────────────────────────────────────────
def obtener_predicciones(db: Session) -> list[PredictionRecord]:
    return db.query(PredictionRecord).order_by(PredictionRecord.id.asc()).all()

def obtener_predicciones_por_usuario(db: Session, user_id: int) -> list[PredictionRecord]:
    """Devuelve solo las predicciones del usuario autenticado."""
    return (
        db.query(PredictionRecord)
        .filter(PredictionRecord.user_id == user_id)
        .order_by(PredictionRecord.id.asc())
        .all()
    )