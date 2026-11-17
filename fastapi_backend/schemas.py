from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


# ── Predicciones ───────────────────────────────────────────────────
class PredictionInput(BaseModel):
    P1: int
    P2: int
    P3: int
    P4: int
    P5: int
    P6: int
    P7: int
    P8: int
    P9: int
    P10: int
    P11: int
    P12: int
    P13: int
    P14: int
    P15: int
    P16: int
    P17: int
    P18: int
    P19: int
    P20: int
    P21: int
    grado_carga: int


class PredictionOutput(BaseModel):
    id: int
    overload_score: float
    risk_level: str
    recommendation: str


class PredictionRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    P1: int
    P2: int
    P3: int
    P4: int
    P5: int
    P6: int
    P7: int
    P8: int
    P9: int
    P10: int
    P11: int
    P12: int
    P13: int
    P14: int
    P15: int
    P16: int
    P17: int
    P18: int
    P19: int
    P20: int
    P21: int
    grado_carga: int
    prediccion: int
    created_at: datetime | None = None


# ── Usuarios ───────────────────────────────────────────────────────
class UserResponse(BaseModel):
    """Schema de salida para un usuario. Nunca expone la contraseña."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    is_staff: bool
    is_superuser: bool
    is_active: bool
    date_joined: datetime | None = None

class UserCreate(BaseModel):
    """Schema de entrada para registrar un usuario nuevo."""
    username: str
    email: EmailStr
    password: str  # llegará en texto plano; el service la hashea
    first_name: str = ""
    last_name: str = ""

class UserUpdate(BaseModel):
    """
    Schema de entrada para actualizar un usuario.
    Todos los campos son opcionales: solo se actualizan los que se envíen.
    """
    username: str | None = None
    email: EmailStr | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
