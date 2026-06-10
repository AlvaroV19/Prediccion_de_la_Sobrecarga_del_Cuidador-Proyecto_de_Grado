from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    caregiver_age: int = Field(ge=18, le=100)
    caregiving_hours_per_day: int = Field(ge=1, le=24)
    caregiving_days_per_week: int = Field(ge=1, le=7)
    sleep_hours: float = Field(ge=0, le=24)
    stress_level: int = Field(ge=1, le=10)
    support_network: int = Field(ge=1, le=5)
    patient_dependence: int = Field(ge=1, le=5)
    relationship_to_patient: str = Field(pattern='^(spouse|child|parent|other)$')

class PredictionOutput(BaseModel):
    id: int
    overload_score: float
    risk_level: str
    recommendation: str
