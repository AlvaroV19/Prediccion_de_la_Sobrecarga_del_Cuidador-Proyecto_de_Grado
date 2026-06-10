from .models import PredictionRecord
from .schemas import PredictionInput

def compute_prediction(data: PredictionInput):
    relationship_weight = {
        'spouse': 2.0,
        'child': 1.5,
        'parent': 1.8,
        'other': 1.2,
    }

    sleep_deficit = max(0.0, 8.0 - data.sleep_hours)

    score = (
        data.caregiving_hours_per_day * 2.5
        + data.caregiving_days_per_week * 1.5
        + data.stress_level * 3.0
        + data.patient_dependence * 2.2
        + sleep_deficit * 2.0
        + (6 - data.support_network) * 1.8
        + relationship_weight.get(data.relationship_to_patient, 1.2)
    )

    score = round(score, 2)

    if score < 22:
        risk_level = 'low'
        recommendation = 'Mantener seguimiento y reforzar hábitos de descanso.'
    elif score < 35:
        risk_level = 'medium'
        recommendation = 'Revisar carga de cuidado, apoyo familiar y pausas regulares.'
    else:
        risk_level = 'high'
        recommendation = 'Buscar apoyo profesional y redistribuir tareas de cuidado cuanto antes.'

    return {
        'overload_score': score,
        'risk_level': risk_level,
        'recommendation': recommendation,
    }


def create_prediction_record(db, data: PredictionInput):
    result = compute_prediction(data)

    record = PredictionRecord(
        caregiver_age=data.caregiver_age,
        caregiving_hours_per_day=data.caregiving_hours_per_day,
        caregiving_days_per_week=data.caregiving_days_per_week,
        sleep_hours=data.sleep_hours,
        stress_level=data.stress_level,
        support_network=data.support_network,
        patient_dependence=data.patient_dependence,
        relationship_to_patient=data.relationship_to_patient,
        overload_score=result['overload_score'],
        risk_level=result['risk_level'],
        recommendation=result['recommendation'],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record
