from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class PredictionRecord(Base):
    __tablename__ = 'prediction_records'

    id = Column(Integer, primary_key=True, index=True)
    caregiver_age = Column(Integer, nullable=False)
    caregiving_hours_per_day = Column(Integer, nullable=False)
    caregiving_days_per_week = Column(Integer, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    stress_level = Column(Integer, nullable=False)
    support_network = Column(Integer, nullable=False)
    patient_dependence = Column(Integer, nullable=False)
    relationship_to_patient = Column(String(30), nullable=False)
    overload_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    recommendation = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
