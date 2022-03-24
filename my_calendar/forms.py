from django import forms
from django.forms import ModelForm

from .models import Event, PatientCalendar


# Create an Event Form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'date', 'patient_calendar', 'description', 'image', 'type', 'url_image')
        labels = {
            'title': '',
            'description': '',
            'date': '',
            'image': '',
            'patient_calendar': '',
            'type': ''
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'},
                format='%Y-%m-%d'),
            'patient_calendar': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Calendario', 'hidden': 'True'}),
            'type': forms.NumberInput(attrs={'class': 'form-control', 'hidden': 'True'}),
        }

    # def clean(self):
    #     data = self.cleaned_data
    #     if data['image'] and data['url_image']:
    #         self.add_error('image', 'No puede usar una imagen online y una de su ordenador. '
    #                                 'Por favor, utilice solo una de las opciones.')
    #     return data

    # def clean_date(self):
    #     new_date = self.cleaned_data.get('date')
    #     new_patient = self.cleaned_data.get('patient')
    #     event = Event.objects.filter(date=new_date, patient=new_patient)
    #     if event.exists():
    #         self.add_error('date', f'Ya existe un evento este día.')
    #
    #     return new_date


# Create an Patient Form
class PatientForm(ModelForm):
    class Meta:
        model = PatientCalendar
        fields = ('name', 'template_style', 'therapist')
        labels = {
            'name': '',
            'therapist': '',
            'template_style': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'template_style': forms.NumberInput(attrs={'class': 'form-control'}),
            'therapist': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Terapeuta', 'hidden': 'True'}),
        }

    def clean(self):
        data = self.cleaned_data
        calendars = PatientCalendar.objects.filter(name=data.get('name'), therapist=data.get('therapist')).exclude(
            pk=self.instance.pk)
        if calendars:
            self.add_error('name', 'Ya existe un calendario con este nombre')
        return data
