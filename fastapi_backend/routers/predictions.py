from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd

from ..database import get_db
from ..schemas import PredictionInput, PredictionRecordOut
from ..services import guardar_prediccion, obtener_predicciones, obtener_predicciones_por_usuario
from ..auth import require_user, require_admin
from ..django_auth_models import DjangoUser

router = APIRouter(prefix="/predictions", tags=["Predictions"])


# ── Etiquetas y recomendaciones ────────────────────────────────────
ETIQUETAS = {
    0: "Sobrecarga Baja",
    1: "Sobrecarga Media",
    2: "Sobrecarga Alta",
}

RECOMENDACIONES = {
    0: "Mantener seguimiento periódico.",
    1: "Se recomienda apoyo familiar y monitoreo.",
    2: "Se recomienda intervención profesional.",
}

COLUMNAS_P = [f"P{i}" for i in range(1, 22)]

RESPONSE_LABELS = ["Nunca", "Casi nunca", "A veces", "Bastantes veces", "Casi siempre"]


# ── Endpoints ──────────────────────────────────────────────────────
@router.post("/", summary="Realizar una predicción")
def predict(
    payload: PredictionInput,
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_user),
):
    """
    Recibe los datos del cuidador, corre el modelo ML
    y guarda el resultado en la base de datos.
    Requiere usuario autenticado (admin o user).
    """
    record = guardar_prediccion(db, payload, user_id=current_user.id)

    return {
        "id": record.id,
        "usuario": current_user.username,
        "prediccion": record.prediccion,
        "nivel": ETIQUETAS.get(record.prediccion, "Desconocido"),
        "recomendacion": RECOMENDACIONES.get(record.prediccion, "Sin recomendación"),
    }


@router.get(
    "/",
    response_model=list[PredictionRecordOut],
    summary="Listar todas las predicciones",
)
def list_predictions(
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
):
    """
    Devuelve todas las predicciones registradas.
    Requiere usuario autenticado (admin).
    """
    return obtener_predicciones(db)


@router.get(
    "/usuario/{user_id}",
    response_model=list[PredictionRecordOut],
    summary="Predicciones de un usuario específico",
)
def predictions_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
):
    """Solo accesible por administradores."""
    return obtener_predicciones_por_usuario(db, user_id)


@router.get(
    "/statistics",
    summary="Estadísticas generales de predicciones",
)
def get_statistics(
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
):
    registros = obtener_predicciones(db)

    # Sin datos aún
    if not registros:
        return {
            "total_records": 0,
            "chart_response_labels": RESPONSE_LABELS,
            "chart_response_values": [0, 0, 0, 0, 0],
            "prediction_labels": [],
            "prediction_values": [],
            "question_labels": COLUMNAS_P,
            "rows": [],
        }
    

# ── Construir DataFrame ────────────────────────────────────────
    data = [
        {col: getattr(r, col) for col in COLUMNAS_P} | {"prediccion": r.prediccion}
        for r in registros
    ]
    df = pd.DataFrame(data)

# ── Frecuencia de respuestas (valores 1-5 en todas las columnas P) ──
    p_cols   = df[COLUMNAS_P]
    counts   = [int((p_cols == v).sum().sum()) for v in range(1, 6)]

# ── Distribución de predicciones ───────────────────────────────
    pred_counts   = df["prediccion"].value_counts().sort_index()
    pred_labels   = [ETIQUETAS.get(int(k), str(k)) for k in pred_counts.index]
    pred_values   = [int(v) for v in pred_counts.values]

# ── Métricas por pregunta ──────────────────────────────────────
    desc = p_cols.describe().T   # filas = P1..P21, cols = count/mean/std/min/25%/50%/75%/max
    rows = []
    for col in COLUMNAS_P:
        s = desc.loc[col]
        rows.append({
            "question": col,
            "count": int(s["count"]),
            "mean": round(float(s["mean"]), 4),
            "std": round(float(s["std"]),  4) if s["count"] > 1 else None,
            "min": int(s["min"]),
            "q25": round(float(s["25%"]), 4),
            "q50": round(float(s["50%"]), 4),
            "q75": round(float(s["75%"]), 4),
            "max": int(s["max"]),
        })

    return {
        "total_records": len(registros),
        "chart_response_labels": RESPONSE_LABELS,
        "chart_response_values": counts,
        "prediction_labels": pred_labels,
        "prediction_values": pred_values,
        "question_labels": COLUMNAS_P,
        "rows": rows,
    }
