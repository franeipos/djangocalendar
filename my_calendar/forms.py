from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Event, PatientCalendar


# Create an Event Form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('header','title', 'date', 'patient_calendar', 'description', 'image', 'type', 'url_image')
        labels = {
            'header':'',
            'title': '',
            'description': '',
            'date': '',
            'image': '',
            'patient_calendar': '',
            'type': ''
        }

        widgets = {
            'header': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Encabezado de la caja'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Selecciona una fecha', 'type': 'date'},
                format='%Y-%m-%d'),
            'patient_calendar': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Calendario', 'hidden': 'True'}),
            'type': forms.NumberInput(attrs={'class': 'form-control', 'hidden': 'True'}),
        }

    # def clean_date(self):
    #     new_date = self.cleaned_data.get('date')
    #     calendar = self.cleaned_data.get('patient_calendar')
    #     print(self.cleaned_data)
    #     event = Event.objects.filter(date=new_date, patient_calendar=calendar)
    #     if event:
    #         self.add_error('date', 'Ya existe un evento este día.')
    #
    #     return new_date

    def clean(self):
        super().clean()
        data = self.cleaned_data

        # Only one event per date and calendar.
        existing_events = Event.objects.filter(date=data['date'], patient_calendar=data['patient_calendar'],
                                               type=data['type']).exclude(pk=self.instance.pk)
        print(existing_events)
        if existing_events:
            self.add_error('date', 'Ya existe un evento este día. '
                                   'Por favor, seleccione otra fecha.')


        if not data['title'] and not data['image'] and not data['url_image'] and not data['header']:
             # raise ValidationError("Debe proporcionar, al menos, una imagen o un nombre.")
            self.add_error('title', 'Debe proporcionar, al menos, una imagen, un nombre o un encabezado.')
            self.add_error('header', '')
            self.add_error('url_image', '')
            self.add_error('image', '')   


        # Verify if the fields are in the cleaned data and weren't removed from previous verifications.
        if not all(key in data for key in ('image', 'url_image')):
            pass
        # Only one image input source: local or online.
        elif data['image'] and data['url_image']:
            self.add_error('image', 'No puede usar una imagen online y una de su ordenador. '
                                    'Por favor, utilice solo una de las opciones.')
            self.add_error('url_image', '')

        return data


# Create an Patient Form
class PatientForm(ModelForm):
    class Meta:
        model = PatientCalendar
        fields = ('name', 'template_style', 'therapist', 'font_color', 'link_color', 'font_size', 'font_style',
                  'text_position_event', 'month_box', 'season_box', 'extra_box')
        labels = {
            'name': '',
            'therapist': '',
            'template_style': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'template_style': forms.NumberInput(attrs={'class': 'form-control'}),
            'month_box': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'season_box': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'extra_box': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'therapist': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Terapeuta', 'hidden': 'True'}),
        }


    def clean(self):
        data = self.cleaned_data
        calendars = PatientCalendar.objects.filter(name=data.get('name'), therapist=data.get('therapist')).exclude(
            pk=self.instance.pk)
        if calendars:
            self.add_error('name', 'Ya existe un calendario con este nombre')
        return data
