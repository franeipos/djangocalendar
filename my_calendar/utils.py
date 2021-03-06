from datetime import datetime, timedelta
import locale
from pathlib import Path
from django.urls import reverse

from django.conf import settings

from calendar import HTMLCalendar
from .models import Event, PatientCalendar


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        if settings.DEBUG:
            locale.setlocale(locale.LC_ALL, 'es_ES')  # set ES as language for the calendar in local server.
        else:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # set ES as language for the calendar.
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, id_patient):
        events_per_day = events.filter(date__day=day)
        patient_calendar = PatientCalendar.objects.get(id=id_patient)
        text_position_event = patient_calendar.text_position_event
        d = ''
        for event in events_per_day:
            d += f'<a class="fs-6" href="{reverse("event-detail", args=(event.id,))}">'
            if event.title and text_position_event == 1:
                d += f'{event.title} </br>'

            if event.url_image:
                d += f'<img class="my-1" src="{event.url_image}">'
            elif event.image:
                d += f'<img class="my-1" src="{event.image.url}">'

            if event.title and text_position_event == 2:
                d += f'</br> {event.title}'
            d += '</a>'
        if day != 0:
            return f'<td onclick=redirect_add_event("{reverse("add-event", args=(day, self.month, self.year,))}?id_patient={id_patient}&type=1") ' \
                   f'class="clickable">' \
                   f'<span class="date">{day}</span><div class="calendar-event text-center"> {d} </div></td>'
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, id_patient):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, id_patient)
        return f'<tr> {week} </tr>'

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        day_names = ["LUNES", "MARTES", "MI??RCOLES", "JUEVES", "VIERNES", "S??BADO", "DOMINGO"]
        day_event_types = [10, 11, 12, 13, 14, 15, 16, 17]
        # event = Event.objects.filter(patient_calendar=id_patient, type=day_event_types[day])
        day_image = f'day_{day}'
        print(settings.MEDIA_ROOT)
        return f'<th class="week-header {self.cssclasses_weekday_head[day]}">' \
               f'<img class = "image-week-header my-1" src="{settings.MEDIA_URL}/week_days/{day_image}.png"></br> {day_names[day]}</th>'

        # formats a month as a table
        # filter events by year, month and patient
    def formatmonth(self, id_patient, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month, patient_calendar=id_patient, type=1)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar table">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, id_patient)}\n'
        return cal
