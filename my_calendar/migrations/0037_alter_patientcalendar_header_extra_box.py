# Generated by Django 4.0.1 on 2022-05-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_calendar', '0036_alter_patientcalendar_header_extra_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientcalendar',
            name='header_extra_box',
            field=models.CharField(default='Test', max_length=50),
        ),
    ]
