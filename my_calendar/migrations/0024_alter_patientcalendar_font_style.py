# Generated by Django 4.0.1 on 2022-05-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_calendar', '0023_alter_patientcalendar_font_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientcalendar',
            name='font_style',
            field=models.CharField(default='Arial,sans-serif', max_length=20),
        ),
    ]