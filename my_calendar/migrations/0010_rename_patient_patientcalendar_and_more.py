# Generated by Django 4.0.1 on 2022-02-08 16:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_calendar', '0009_alter_patient_unique_together_alter_patient_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patient',
            new_name='PatientCalendar',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='patient',
            new_name='patient_calendar',
        ),
    ]
