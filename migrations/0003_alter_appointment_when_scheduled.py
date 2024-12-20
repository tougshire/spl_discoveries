# Generated by Django 5.0.6 on 2024-07-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_discoveries', '0002_remove_appointment_customers_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='when_scheduled',
            field=models.DateTimeField(blank=True, help_text='The date and time the appointment is scheduled or, if done, occured', null=True, verbose_name='scheduled/occured'),
        ),
    ]
