from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..schemas import PredictionInput, PredictionRecordOut
from ..services import guardar_prediccion, obtener_predicciones

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/predictions')
def predict(payload: PredictionInput, db: Session = Depends(get_db)):
    record = guardar_prediccion(db, payload)
    etiquetas = {
        0: "Sobrecarga Baja",
        1: "Sobrecarga Media",
        2: "Sobrecarga Alta"
    }
    recomendaciones = {
    0: "Mantener seguimiento periódico.",
    1: "Se recomienda apoyo familiar y monitoreo.",
    2: "Se recomienda intervención profesional."
    }
    return {
        "id": record.id,
        "prediccion": record.prediccion,
        "nivel": etiquetas.get(record.prediccion, "Desconocido"),
        "recomendacion": recomendaciones.get(record.prediccion, "Recomendación no disponible")
    }


@router.get('/predictions', response_model=list[PredictionRecordOut], summary='List all predictions')
def list_predictions(db: Session = Depends(get_db)):
    return obtener_predicciones(db)
