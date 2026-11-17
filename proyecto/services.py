print(">>> CARGÓ proyecto/services.py <<<")

import os
import requests
from django.conf import settings


def _auth_headers(token=None):

    print("TOKEN ENVIADO:")
    print(token)

    if not token:
        return {}

    return {'Authorization': f'Bearer {token}'}


def get_fastapi_token(username, password):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    path = getattr(settings, 'FASTAPI_AUTH_PATH', os.getenv('FASTAPI_AUTH_PATH', '/auth/token'))
    url = f"{base_url.rstrip('/')}{path}"

    try:
        response = requests.post(
            url,
            data={'username': username, 'password': password},
            timeout=15,
        )

        # Si FastAPI respondió que las credenciales son incorrectas
        if response.status_code == 401:
            return {
            "error": "Usuario o contraseña incorrectos."
        }

        # Si ocurrió cualquier otro error HTTP
        response.raise_for_status()

        data = response.json()

    except requests.RequestException as exc:
        return {
        "error": f"No fue posible autenticar con FastAPI: {exc}"
    }

    except ValueError:
        return {
        "error": "FastAPI respondió con un formato inválido al autenticar."
    }

    # Obtener el token
    token = data.get("access_token") or data.get("token")
    token_type = data.get("token_type", "bearer")

    if not token:
        return {
            "error": "FastAPI no devolvió un token de acceso."
        }

    return {
        "access_token": token,
        "token_type": token_type,
    }


def submit_prediction(payload, token=None):

    print(">>> Entró a submit_prediction <<<")
    print(token)
    
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    path = getattr(settings, 'FASTAPI_PREDICTION_PATH', os.getenv('FASTAPI_PREDICTION_PATH', '/api/v1/predictions'))
    url = f"{base_url.rstrip('/')}{path}"

    try:
        response = requests.post(url, json=payload, headers=_auth_headers(token), timeout=15)
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


def get_statistics_context(token=None):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    path = getattr(settings, 'FASTAPI_STATS_PATH', os.getenv('FASTAPI_STATS_PATH', '/api/v1/predictions/statistics'))
    url = f"{base_url.rstrip('/')}{path}"

    try:
        response = requests.get(url, headers=_auth_headers(token), timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return {
            'total_records': 0,
            'chart_response_labels': ['Nunca', 'Casi nunca', 'A veces', 'Bastantes veces', 'Casi siempre'],
            'chart_response_values': [0, 0, 0, 0, 0],
            'prediction_labels': [],
            'prediction_values': [],
            'question_labels': [f'P{number}' for number in range(1, 22)],
            'metrics': ['count', 'mean', 'std', 'min', 'q25', 'q50', 'q75', 'max'],
            'rows': [],
        }


def register_user(username, email, password, first_name="", last_name=""):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    url = f"{base_url.rstrip('/')}/api/v1/users/register"

    try:
        response = requests.post(
            url,
            json={
                'username': username,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
            },
            timeout=15,
        )

        if response.status_code == 409:
            try:
                detail = response.json().get('detail', 'El usuario o correo ya están registrados.')
            except ValueError:
                detail = 'El usuario o correo ya están registrados.'
            return {'error': detail}

        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        return {'error': f'No fue posible registrar el usuario: {exc}'}

    except ValueError:
        return {'error': 'FastAPI respondió con un formato inválido.'}


def forgot_password(email):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    url = f"{base_url.rstrip('/')}/auth/forgot-password"
    try:
        response = requests.post(url, json={'email': email}, timeout=15)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        return {'error': str(exc)}


def reset_password(token, new_password):
    base_url = getattr(settings, 'FASTAPI_BASE_URL', os.getenv('FASTAPI_BASE_URL', 'http://127.0.0.1:8000'))
    url = f"{base_url.rstrip('/')}/auth/reset-password"
    try:
        response = requests.post(
            url,
            json={'token': token, 'new_password': new_password},
            timeout=15,
        )
        if response.status_code == 400:
            return {'error': response.json().get('detail', 'Token inválido o expirado.')}
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        return {'error': str(exc)}
