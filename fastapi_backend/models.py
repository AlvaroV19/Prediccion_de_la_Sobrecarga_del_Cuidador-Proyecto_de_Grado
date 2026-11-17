from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from .database import Base

class PredictionRecord(Base):
    __tablename__ = 'prediction_records'

    id = Column(Integer, primary_key=True, index=True)

    # Relación con auth_user de Django
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

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

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime (timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)

class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
