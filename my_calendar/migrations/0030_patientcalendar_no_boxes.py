# Generated by Django 4.0.1 on 2022-05-18 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_calendar', '0029_remove_patientcalendar_number_box_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientcalendar',
            name='no_boxes',
            field=models.BooleanField(default=False),
        ),
    ]