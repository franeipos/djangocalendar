# Generated by Django 4.0.1 on 2022-02-08 17:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_calendar', '0013_remove_patientmonth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientmonth',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
