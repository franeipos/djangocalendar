# Generated by Django 4.0.1 on 2022-05-20 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_calendar', '0037_alter_patientcalendar_header_extra_box'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientcalendar',
            name='header_extra_box',
        ),
    ]