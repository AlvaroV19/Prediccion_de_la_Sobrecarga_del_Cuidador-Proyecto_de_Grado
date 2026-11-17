import jwt as pyjwt

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .services import (
    submit_prediction,
    format_result_for_template,
    get_statistics_context,
    get_fastapi_token,
    register_user,
    forgot_password,
    reset_password,
)


QUESTION_ITEMS = [
    {
        'field_name': 'P1',
        'number': 1,
        'question': '¿Siente que su familiar solicita más ayuda de la que realmente necesita?',
    },
    {
        'field_name': 'P2',
        'number': 2,
        'question': '¿Siente que debido al tiempo que dedica a su familiar ya no dispone de tiempo suficiente para usted?',
    },
    {
        'field_name': 'P3',
        'number': 3,
        'question': '¿Se siente tenso cuando tiene que cuidar a su familiar y atender además otras responsabilidades?',
    },
    {
        'field_name': 'P4',
        'number': 4,
        'question': '¿Se siente avergonzado por la conducta de su familiar?',
    },
    {
        'field_name': 'P5',
        'number': 5,
        'question': '¿Se siente enfadado cuando está cerca de su familiar?',
    },
    {
        'field_name': 'P6',
        'number': 6,
        'question': '¿Cree que la situación actual afecta de manera negativa a su relación con amigos y otros miembros de su familia?',
    },
    {
        'field_name': 'P7',
        'number': 7,
        'question': '¿Siente temor por el futuro que le espera a su familiar?',
    },
    {
        'field_name': 'P8',
        'number': 8,
        'question': '¿Siente que su familiar depende de usted?',
    },
    {
        'field_name': 'P9',
        'number': 9,
        'question': '¿Se siente agobiado cuando tiene que estar junto a su familiar?',
    },
    {
        'field_name': 'P10',
        'number': 10,
        'question': '¿Siente que su salud se ha resentido por cuidar a su familiar?',
    },
    {
        'field_name': 'P11',
        'number': 11,
        'question': '¿Siente que no tiene la vida privada que desearía debido a su familiar?',
    },
    {
        'field_name': 'P12',
        'number': 12,
        'question': '¿Cree que su vida social se ha visto afectada por tener que cuidar de su familiar?',
    },
    {
        'field_name': 'P13',
        'number': 13,
        'question': '¿Se siente incómodo para invitar amigos a casa, a causa de su familiar?',
    },
    {
        'field_name': 'P14',
        'number': 14,
        'question': '¿Cree que su familiar espera que usted le cuide, como si fuera la única persona con la que puede contar?',
    },
    {
        'field_name': 'P15',
        'number': 15,
        'question': '¿Cree que no dispone de dinero suficiente para cuidar a su familiar además de sus otros gastos?',
    },
    {
        'field_name': 'P16',
        'number': 16,
        'question': '¿Siente que será incapaz de cuidar a su familiar por mucho más tiempo?',
    },
    {
        'field_name': 'P17',
        'number': 17,
        'question': '¿Siente que ha perdido el control sobre su vida desde que la enfermedad de su familiar se manifestó?',
    },
    {
        'field_name': 'P18',
        'number': 18,
        'question': '¿Desearía poder encargar el cuidado de su familiar a otras personas?',
    },
    {
        'field_name': 'P19',
        'number': 19,
        'question': '¿Se siente inseguro acerca de lo que debe hacer con su familiar?',
    },
    {
        'field_name': 'P20',
        'number': 20,
        'question': '¿Siente que debería hacer más de lo que hace por su familiar?',
    },
    {
        'field_name': 'P21',
        'number': 21,
        'question': '¿Cree que podría cuidar de su familiar mejor de lo que lo hace?',
    },
    {
        'field_name': 'grado_carga',
        'number': 22,
        'question': 'En general: ¿Se siente muy sobrecargado por tener que cuidar de su familiar?',
    },
]

ZARIT_OPTIONS = [
    {'value': '1', 'label': 'Nunca'},
    {'value': '2', 'label': 'Casi nunca'},
    {'value': '3', 'label': 'A veces'},
    {'value': '4', 'label': 'Bastantes veces'},
    {'value': '5', 'label': 'Casi siempre'},
]


def _zarit_context(form_data=None):
    form_data = form_data or {}
    return {
        'zarit_items': [
            {
                'number': item['number'],
                'field_name': item['field_name'],
                'question': item['question'],
                'value': form_data.get(item['field_name'], ''),
            }
            for item in QUESTION_ITEMS
        ],
        'zarit_options': ZARIT_OPTIONS,
    }


def _result_context(result):
    # Delegate normalization to services.format_result_for_template
    return format_result_for_template(result)


def _is_authenticated(request):
    return bool(request.session.get('login_ok'))


def _is_admin(request):
    """Lee el JWT de la sesión y verifica si el rol es admin."""
    token = request.session.get('fastapi_token')
    if not token:
        return False
    try:
        payload = pyjwt.decode(token, options={"verify_signature": False})
        return payload.get('role') == 'admin'
    except Exception:
        return False
    

def main(request):
    if not _is_authenticated(request):
        return redirect('login')

    return render(request, 'menu.html', context={
        'is_admin': _is_admin(request),
    })


def statistics(request):
    if not _is_authenticated(request):
        return redirect('login')
    if not _is_admin(request):       
        return redirect('main')
    
    return render(request, 'estadisticas.html', context=get_statistics_context(request.session.get('fastapi_token')))


def login_screen(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        token_response = get_fastapi_token(username, password)

        if 'error' not in token_response:
            request.session['login_ok'] = True
            request.session['fastapi_token'] = token_response['access_token']
            print("TOKEN RECIBIDO:")
            print(request.session['fastapi_token'])
            return redirect('main')

        messages.error(request, token_response['error'])

    return render(request, 'login.html', context={
        'auth_mode': 'Token de FastAPI',
    })


def register_screen(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username or not email or not password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'register.html')

        error = _validate_password(password, confirm)
        if error:
            messages.error(request, error)
            return render(request, 'register.html')

        result = register_user(username, email, password, first_name, last_name)

        if 'error' in result:
            messages.error(request, result['error'])
            return render(request, 'register.html')

        # ── Login automático tras registro exitoso ─────────────────
        token_response = get_fastapi_token(username, password)

        if 'error' not in token_response:
            request.session['login_ok']      = True
            request.session['fastapi_token'] = token_response['access_token']
            return redirect('main')

        # Si el token falla por alguna razón, redirigir al login
        messages.success(request, '¡Cuenta creada! Inicia sesión para continuar.')
        return redirect('login')

    return render(request, 'register.html')


def forgot_password_screen(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'El correo es obligatorio.')
            return render(request, 'forgot_password.html')

        result = forgot_password(email)

        if 'error' in result:
            messages.error(request, result['error'])
            return render(request, 'forgot_password.html')

        # El token de desarrollo solo se guarda en sesión si DEBUG=True.
        # En producción, FastAPI debe enviar el email y este bloque no debe ejecutarse.
        if settings.DEBUG and 'dev_token' in result:
            request.session['reset_token'] = result['dev_token']

        return redirect('pendiente_reset')

    return render(request, 'forgot_password.html')


def pending_reset_screen(request):
    """Pantalla de espera tras solicitar recuperación."""
    dev_token = request.session.get('reset_token', '') if settings.DEBUG else ''
    request.session.pop('reset_token', None)  # se consume una sola vez
    return render(request, 'pending_reset.html', {'dev_token': dev_token})


def reset_password_screen(request, token):      # ← recibe token por URL
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm      = request.POST.get('confirm_password', '')

        error = _validate_password(new_password, confirm)
        if error:
            messages.error(request, error)
            return render(request, 'reset_password.html', {'token': token})

        result = reset_password(token, new_password)

        if 'error' in result:
            # Token inválido o expirado: no tiene sentido reintentar en el mismo
            # formulario, el token ya no sirve. Enviamos a pedir uno nuevo.
            messages.error(
                request,
                f"{result['error']} Por favor solicita un nuevo enlace de recuperación."
            )
            return redirect('recuperar_password')

        request.session.pop('reset_token', None)
        messages.success(request, '¡Contraseña actualizada! Ya puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'reset_password.html', {'token': token})


def _validate_password(password: str, confirm: str) -> str | None:
    """
    Retorna un mensaje de error si la contraseña no cumple la política.
    Retorna None si todo está bien.
    """
    import re
    if password != confirm:
        return 'Las contraseñas no coinciden.'
    if len(password) < 8:
        return 'La contraseña debe tener al menos 8 caracteres.'
    if not re.search(r'[A-Z]', password):
        return 'La contraseña debe tener al menos una letra mayúscula.'
    if not re.search(r'[a-z]', password):
        return 'La contraseña debe tener al menos una letra minúscula.'
    if not re.search(r'\d', password):
        return 'La contraseña debe tener al menos un número.'
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', password):
        return 'La contraseña debe tener al menos un carácter especial.'
    return None


def predict(request):
    print(">>> Entró a predict <<<")
    print(request.method)
    if not _is_authenticated(request):
        return redirect('login')

    if request.method != 'POST':
        return render(request, 'index.html', context=_zarit_context())

    payload = {item['field_name']: request.POST.get(item['field_name']) for item in QUESTION_ITEMS}

    result = submit_prediction(payload, token=request.session.get('fastapi_token'))

    if 'error' in result:
        messages.error(request, result['error'])
        return render(request, 'index.html', context=_zarit_context(payload))

    return render(request, 'resultado.html', context=_result_context(result))
