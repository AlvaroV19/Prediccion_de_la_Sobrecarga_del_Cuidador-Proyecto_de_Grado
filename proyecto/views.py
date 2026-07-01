from django.shortcuts import render, redirect
from django.contrib import messages
from .services import submit_prediction, format_result_for_template


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


def main(request):
    if not _is_authenticated(request):
        return redirect('login')

    return render(request, 'index.html', context=_zarit_context())


def login_screen(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if username == 'admin' and password == 'zarit2026':
            request.session['login_ok'] = True
            return redirect('main')

        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html', context={
        'default_username': 'admin',
        'default_password': 'zarit2026',
    })


def predict(request):
    if not _is_authenticated(request):
        return redirect('login')

    if request.method != 'POST':
        return redirect('main')

    payload = {item['field_name']: request.POST.get(item['field_name']) for item in QUESTION_ITEMS}

    result = submit_prediction(payload)

    if 'error' in result:
        messages.error(request, result['error'])
        return render(request, 'index.html', context=_zarit_context(payload))

    return render(request, 'resultado.html', context=_result_context(result))
