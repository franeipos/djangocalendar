from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.
class PatientCalendar(models.Model):
    name = models.CharField(max_length=50, unique=True)
    template_style = models.PositiveSmallIntegerField(blank=False, null=False, default=1)  # 1:base, 2:dark, 3:
    # summer, 4:winter, 5:autumn, 6:spring
    therapist = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name  # just to see the title in admin area


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    type = models.PositiveSmallIntegerField(blank=False, null=False, default=1)  # 1:day event, 2:month, 3:season,
    # 4:weather
    patient_calendar = models.ForeignKey(PatientCalendar, blank=False, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  # just to see the title in admin area
