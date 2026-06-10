from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..schemas import PredictionInput
from ..services import create_prediction_record

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/predictions')
def predict(payload: PredictionInput, db: Session = Depends(get_db)):
    record = create_prediction_record(db, payload)
    return {
        'record_id': record.id,
        'overload_score': record.overload_score,
        'risk_level': record.risk_level,
        'recommendation': record.recommendation,
    }
