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
