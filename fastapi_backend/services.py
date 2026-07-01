import joblib
import pandas as pd
from .models import PredictionRecord
from .schemas import PredictionInput

modelo = joblib.load(
    "modelos/modelo_gb.pkl"
)

scaler = joblib.load(
    "modelos/scaler.pkl"
)

features = joblib.load(
    "modelos/features.pkl"
)

def predecir(data):

    datos = {
        "P1_encoded": data.P1,
        "P2_encoded": data.P2,
        "P3_encoded": data.P3,
        "P4_encoded": data.P4,
        "P5_encoded": data.P5,
        "P6_encoded": data.P6,
        "P7_encoded": data.P7,
        "P8_encoded": data.P8,
        "P9_encoded": data.P9,
        "P10_encoded": data.P10,
        "P11_encoded": data.P11,
        "P12_encoded": data.P12,
        "P13_encoded": data.P13,
        "P14_encoded": data.P14,
        "P15_encoded": data.P15,
        "P16_encoded": data.P16,
        "P17_encoded": data.P17,
        "P18_encoded": data.P18,
        "P19_encoded": data.P19,
        "P20_encoded": data.P20,
        "P21_encoded": data.P21,
        "grado_carga_encoded": data.grado_carga
    }

    df = pd.DataFrame([datos])

    X = df[features]

    X_scaled = scaler.transform(X)

    pred = int(modelo.predict(X_scaled)[0])

    return pred

def guardar_prediccion(db, data):

    pred = predecir(data)

    registro = PredictionRecord(
        P1=data.P1,
        P2=data.P2,
        P3=data.P3,
        P4=data.P4,
        P5=data.P5,
        P6=data.P6,
        P7=data.P7,
        P8=data.P8,
        P9=data.P9,
        P10=data.P10,
        P11=data.P11,
        P12=data.P12,
        P13=data.P13,
        P14=data.P14,
        P15=data.P15,
        P16=data.P16,
        P17=data.P17,
        P18=data.P18,
        P19=data.P19,
        P20=data.P20,
        P21=data.P21,
        grado_carga=data.grado_carga,
        prediccion=pred
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro

##def compute_prediction(data: PredictionInput):
##    relationship_weight = {
##        'spouse': 2.0,
##        'child': 1.5,
##        'parent': 1.8,
##        'other': 1.2,
##    }
##
##    sleep_deficit = max(0.0, 8.0 - data.sleep_hours)
##
##    score = (
##        data.caregiving_hours_per_day * 2.5
##        + data.caregiving_days_per_week * 1.5
##        + data.stress_level * 3.0
##        + data.patient_dependence * 2.2
##        + sleep_deficit * 2.0
##        + (6 - data.support_network) * 1.8
##        + relationship_weight.get(data.relationship_to_patient, 1.2)
##    )
##
##    score = round(score, 2)
##
##    if score < 22:
##        risk_level = 'low'
##        recommendation = 'Mantener seguimiento y reforzar hábitos de descanso.'
##    elif score < 35:
##        risk_level = 'medium'
##        recommendation = 'Revisar carga de cuidado, apoyo familiar y pausas regulares.'
##    else:
##        risk_level = 'high'
##        recommendation = 'Buscar apoyo profesional y redistribuir tareas de cuidado cuanto antes.'
##
##    return {
##        'overload_score': score,
##        'risk_level': risk_level,
##        'recommendation': recommendation,
##    }
##
##
##def create_prediction_record(db, data: PredictionInput):
##    result = compute_prediction(data)
##
##    record = PredictionRecord(
##        caregiver_age=data.caregiver_age,
##        caregiving_hours_per_day=data.caregiving_hours_per_day,
##        caregiving_days_per_week=data.caregiving_days_per_week,
##        sleep_hours=data.sleep_hours,
##        stress_level=data.stress_level,
##        support_network=data.support_network,
##        patient_dependence=data.patient_dependence,
##        relationship_to_patient=data.relationship_to_patient,
##        overload_score=result['overload_score'],
##        risk_level=result['risk_level'],
##        recommendation=result['recommendation'],
##    )
##    db.add(record)
##    db.commit()
##    db.refresh(record)
##
##    return record
