import os
import requests
from django.conf import settings


def submit_prediction(payload):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    path = getattr(settings, 'FASTAPI_PREDICTION_PATH', os.getenv('FASTAPI_PREDICTION_PATH', '/api/v1/predictions'))
    url = f"{base_url.rstrip('/')}{path}"

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {'error': f'No fue posible comunicarse con FastAPI: {exc}'}
    except ValueError:
        return {'error': 'FastAPI respondió con un formato inválido.'}


def format_result_for_template(result: dict) -> dict:
        """Normalize FastAPI response into the template context keys.

        Expected FastAPI response example:
            { 'id': 1, 'prediccion': 1, 'nivel': 'Sobrecarga Media', 'recomendacion': '...' }

        Returned dict contains: overload_score, risk_level, recommendation, record_id
        """
        
        return {
                'record_id': result.get('id'),
                'risk_level': result.get('nivel'),
                'recommendation': result.get('recomendacion'),
                
        }
