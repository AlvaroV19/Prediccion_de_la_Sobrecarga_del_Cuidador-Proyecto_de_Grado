from django.shortcuts import render, redirect
from django.contrib import messages
from .services import submit_prediction


def main(request):
    return render(request, 'index.html', context={})


def predict(request):
    if request.method != 'POST':
        return redirect('main')

    payload = {
        'caregiver_age': request.POST.get('caregiver_age'),
        'caregiving_hours_per_day': request.POST.get('caregiving_hours_per_day'),
        'caregiving_days_per_week': request.POST.get('caregiving_days_per_week'),
        'sleep_hours': request.POST.get('sleep_hours'),
        'stress_level': request.POST.get('stress_level'),
        'support_network': request.POST.get('support_network'),
        'patient_dependence': request.POST.get('patient_dependence'),
        'relationship_to_patient': request.POST.get('relationship_to_patient'),
    }

    result = submit_prediction(payload)

    if 'error' in result:
        messages.error(request, result['error'])
        return render(request, 'index.html', context={'form_data': payload})

    return render(request, 'resultado.html', context=result)
