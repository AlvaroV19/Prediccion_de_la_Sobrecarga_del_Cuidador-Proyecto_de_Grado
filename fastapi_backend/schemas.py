from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class PredictionInput(BaseModel):
    ## caregiver_age: int = Field(ge=18, le=100)
    ## caregiving_hours_per_day: int = Field(ge=1, le=24)
    ## caregiving_days_per_week: int = Field(ge=1, le=7)
    ## sleep_hours: float = Field(ge=0, le=24)
    ## stress_level: int = Field(ge=1, le=10)
    ## support_network: int = Field(ge=1, le=5)
    ## patient_dependence: int = Field(ge=1, le=5)
    ## relationship_to_patient: str = Field(pattern='^(spouse|child|parent|other)$')

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
