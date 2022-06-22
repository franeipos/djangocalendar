from datetime import datetime
from email import header
import locale
import os
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML

import requests
from requests.auth import HTTPBasicAuth

from decouple import config

from .models import Event, PatientCalendar
from .utils import Calendar
from .forms import EventForm, PatientForm

# Create your views here.


def home_view(request):
    return render(request, "my_calendar/index.html", {"message": "hello fran"})


@login_required
def calendar_view(request, id_patient, month=datetime.now().month, year=datetime.now().year):
    """
    Shows the HTML calendar for a selected month and a selected year. The full month is shown.
    :param id_patient: id of the patient we want to show the calendar
    :param request:
    :param month: month we want to show on the calendar
    :param year: year of the month we want to show
    :return: html calendar of the month and year with the events of each day.
    """
    if request.method == 'POST':
        query = request.POST['month'].split("-")
        if len(query) == 2:
            year = int(query[0])
            month = int(query[1])

    cal = Calendar(year, month)
    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(id_patient, withyear=True)

    # Retrieve the month, season and weather images
    month_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year=year, type=2)
    season_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year=year, type=3)
    weather_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year=year, type=4)
    extra_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year=year, type=5)

    context = {
        "calendar": mark_safe(html_cal),
        'id_patient': id_patient,
        'month': str(month).zfill(2),  # fill with leading 0 to use it in the input value form control.
        'year': year,
        'month_event': month_event,
        'season_event': season_event,
        'weather_event': weather_event,
        'extra_event': extra_event,
        'patient_calendar': PatientCalendar.objects.get(id=id_patient)
    }
    print(context['season_event'])
    return render(request, "my_calendar/calendar.html", context)


@login_required
def all_events_view(request, id_patient):
    events_list = Event.objects.filter(patient_calendar=id_patient)
    context = {
        'events_list': events_list,
        'id_patient': id_patient
    }
    return render(request, 'my_calendar/events_list.html', context)


@login_required
def event_detail(request, event_id=None):
    context = {}
    if event_id is not None:
        event = Event.objects.get(id=event_id)
        context['event'] = event

    return render(request, "my_calendar/event_detail.html", context)


@login_required
def add_event(request, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year):
    context = {
        'day': str(day).zfill(2),
        'month': str(month).zfill(2),
        'year': year,
    }

    event_date = f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'

    picto = request.GET.get('picto', 'None')
    if picto is not None:
        context['picto_id'] = picto

    initial_values = {
        'date': event_date
    }

    # Init the form with the given patient.
    id_patient = request.GET.get('id_patient', None)
    if id_patient is not None:
        initial_values['patient_calendar'] = id_patient

    # Init the form with the given type of event.
    event_type = request.GET.get('type', None)
    if event_type is not None:
        initial_values['type'] = event_type
    else:
        initial_values['type'] = '1'

    context['id_patient'] = id_patient
    context['type'] = event_type

    if request.method == "POST":
        # Si no es tipo evento, debemos añadir el dia 01 al mes para que lo admita la BD.
        if request.POST.get('type') != '1':
            post = request.POST.copy()
            post['date'] = f'{post["date"]}-01'
            request.POST = post

        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            new_event = form.save()
            messages.success(request, 'EXITO! El evento se ha creado correctamente.')
            return redirect('event-detail', event_id=new_event.id)

        context['previous_page'] = request.POST.get('back')  # obtain previous web page.
    else:
        form = EventForm(initial=initial_values)
        context['previous_page'] = request.META.get('HTTP_REFERER')  # obtain previous web page.

    context['form'] = form

    return render(request, 'my_calendar/add_eventV2.html', context)


@login_required
def update_event(request, event_id):
    context = {}
    event = Event.objects.get(id=event_id)
    context['event'] = event

    if request.method == "POST":
        # Si no es tipo evento, debemos añadir el dia 01 al mes para que lo admita la BD.
        if request.POST.get('type') != '1':
            post = request.POST.copy()
            post['date'] = f'{post["date"]}-01'
            request.POST = post

        if event.image:
            image_path = event.image.path

        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            print(request.POST.get('image-clear'))
            if request.POST.get('image-clear') == 'on':
                if os.path.exists(image_path):
                    os.remove(image_path)
            form.save()
            print('Guardado')
            return redirect('event-detail', event_id=event_id)
        else:
            print('Not valid')
    else:
        form = EventForm(instance=event)

    context['form'] = form
    print(form.non_field_errors)

    return render(request, 'my_calendar/update_eventV2.html', context)


@login_required
def delete_event(request, event_id):
    context = {}
    event = Event.objects.get(id=event_id)
    id_patient = event.patient_calendar.id
    month = event.date.month
    year = event.date.year
    if event.image and os.path.exists(event.image.path):
        os.remove(event.image.path)
    event.delete()
    messages.success(request, 'EXITO! EL evento se ha eliminao correctamente.')
    return redirect('calendar', id_patient, month, year)


def search_pictograms(request):
    context = {}

    if request.method == 'POST':
        searched = request.POST['searched']
        context['searched'] = searched

        # Query data to the API
        language = 'es'
        url = f'https://api.arasaac.org/api/pictograms/{language}/search/{searched}'
        api_user = config('API_USER')
        api_pass = config('API_PASS')
        response = requests.get(url, auth=HTTPBasicAuth(api_user, api_pass))

        if response.status_code == 200:
            result = response.json()
            context['result'] = result
            context['success'] = True
        else:
            context['success'] = False
            context['msg'] = 'ERROR, try again.'

    return render(request, 'my_calendar/search_pictograms.html', context)


def pictogram_detail(request, picto_id):
    context = {}

    # Query data to the API
    language = 'es'
    url = f'https://api.arasaac.org/api/pictograms/es/{picto_id}'
    user = config("API_USER")
    password = config("API_PASS")
    response = requests.get(url, auth=HTTPBasicAuth(user, password))

    if response.status_code == 200:
        context['result'] = response.json()
        context['success'] = True
    else:
        context['success'] = False
        context['msg'] = 'ERROR, try again.'
    return render(request, 'my_calendar/pictogram_detail.html', context)


@login_required
def patients_list(request):
    patients = PatientCalendar.objects.filter(therapist_id=request.user.id)
    context = {
        'patients_list': patients
    }
    return render(request, 'my_calendar/patients_list.html', context)


@login_required
def add_patient(request):

    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "EXITO! El calendario se ha creado correctamente.")
            return redirect('patients-list')
        else:
            print(form.errors.as_data())
    else:
        form = PatientForm(initial={'therapist': request.user.id})

    context = {
        'form': form,
    }
    return render(request, 'my_calendar/add_patient.html', context)


@login_required
def update_patient(request, id_patient):
    """
    Actualizar datos del calendario enviado por id_patient
    :param request:
    :param id_patient: id del calendario a actualizar
    :return: si los datos son validos se redirecciona al calendario. Si la peticion es GET se renderiza el
    formulario para actualizar los datos.
    """

    context = {}
    patient = PatientCalendar.objects.get(id=id_patient)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "EXITO! El calendario ha sido actualizado!")
            return redirect('calendar', id_patient)
        else:
            print(form.errors)
    else:
        form = PatientForm(instance=patient)

    context['form'] = form
    context['patient'] = patient

    return render(request, 'my_calendar/update_patient.html', context)


@login_required
def delete_patient(request, id_patient):
    """
    Eliminar un calendario.
    :param request:
    :param id_patient: id del calendario del paciente a eliminar
    :return: redirección a la lista de calendarios
    """

    patient = PatientCalendar.objects.get(id=id_patient)
    if patient is not None:
        patient.delete()
        messages.success(request, 'EXITO! El calendario se ha eliminado correctamente.')
        return redirect('patients-list')


@login_required
def calendar_to_pdf(request, id_patient, month=datetime.now().month, year=datetime.now().year):
    cal = Calendar(year, month)
    html_cal = cal.formatmonth(id_patient, withyear=True)

    patient = PatientCalendar.objects.get(id=id_patient)

    # Retrieve the month, season and weather images
    month_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year= year, type=2)
    season_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year= year, type=3)
    weather_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year= year, type=4)
    extra_event = Event.objects.filter(patient_calendar=id_patient, date__month=month, date__year=year, type=5)

    context = {
        "calendar": mark_safe(html_cal),
        "nombre": patient.name,
        'month_event': month_event,
        'season_event': season_event,
        'weather_event': weather_event,
        'extra_event': extra_event,
        'patient_calendar': patient
    }
    html = render_to_string('my_calendar/pdf_calendar.html', context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    # return render(request, 'my_calendar/pdf_calendar.html', context)

    return response


def show_information(request):
    return render(request, 'my_calendar/information.html', {})
