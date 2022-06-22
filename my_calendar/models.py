from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.
class PatientCalendar(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False, default="Nombre Calendario")
    template_style = models.PositiveSmallIntegerField(blank=False, null=False, default=1)  # 1: white, 2: gray,
    # 3: yellow, 4: blue, 5: green

    # Text style
    font_style = models.CharField(max_length=20, blank=False, null=False, default='Arial,sans-serif')
    font_color = models.CharField(max_length=7, blank=False, null=False, default='#000000')
    link_color = models.CharField(max_length=7, blank=False, null=False, default='#000000')
    font_size = models.PositiveSmallIntegerField(blank=False, null=False, default=12)
    text_position_event = models.PositiveSmallIntegerField(blank=False, null=False, default=1)  # 1: above, 2: below

    month_box = models.BooleanField(default = True)
    season_box = models.BooleanField(default = True)
    extra_box = models.BooleanField(default = False)
    header_extra_box = models.CharField(max_length=50, blank=True, default='')

    therapist = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('name', 'therapist',)  # a therapist cannot repeat the calendar name

    def __str__(self):
        return self.name  # just to see the title in admin area


class Event(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    url_image = models.URLField(blank=True, null=True)
    type = models.PositiveSmallIntegerField(blank=False, null=False, default=1)  # 1:day event, 2:month, 3:season,
    # 4:weather, 5:extra
    patient_calendar = models.ForeignKey(PatientCalendar, blank=False, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  # just to see the title in admin area
