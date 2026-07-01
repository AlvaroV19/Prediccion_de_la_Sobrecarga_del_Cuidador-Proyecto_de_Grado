from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class PredictionRecord(Base):
    __tablename__ = 'prediction_records'

    id = Column(Integer, primary_key=True, index=True)

    P1 = Column(Integer)
    P2 = Column(Integer)
    P3 = Column(Integer)
    P4 = Column(Integer)
    P5 = Column(Integer)
    P6 = Column(Integer)
    P7 = Column(Integer)
    P8 = Column(Integer)
    P9 = Column(Integer)
    P10 = Column(Integer)
    P11 = Column(Integer)
    P12 = Column(Integer)
    P13 = Column(Integer)
    P14 = Column(Integer)
    P15 = Column(Integer)
    P16 = Column(Integer)
    P17 = Column(Integer)
    P18 = Column(Integer)
    P19 = Column(Integer)
    P20 = Column(Integer)
    P21 = Column(Integer)

    grado_carga = Column(Integer)

    prediccion = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    ##caregiver_age = Column(Integer, nullable=False)
    ##caregiving_hours_per_day = Column(Integer, nullable=False)
    ##caregiving_days_per_week = Column(Integer, nullable=False)
    ##sleep_hours = Column(Float, nullable=False)
    ##stress_level = Column(Integer, nullable=False)
    ##support_network = Column(Integer, nullable=False)
    ##patient_dependence = Column(Integer, nullable=False)
    ##relationship_to_patient = Column(String(30), nullable=False)
    ##overload_score = Column(Float, nullable=False)
    ##risk_level = Column(String(20), nullable=False)
    ##recommendation = Column(String(255), nullable=False)
    ##created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
