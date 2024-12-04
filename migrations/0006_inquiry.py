# Generated by Django 5.0.6 on 2024-11-24 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_discoveries', '0005_appointment_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Your full name', max_length=120, verbose_name='full name')),
                ('prefered_name', models.CharField(blank=True, help_text='How you would like us to address you (ex: John, Jill, JT, Ms. Tiller )', max_length=30, verbose_name='prefered name')),
                ('availability', models.CharField(blank=True, help_text='Please describe what days or times would work best for you.  You can be specific (June 1ST or 2nd at 11:00) or more general (Monday afternoons or Wednesday evenings)', max_length=255, verbose_name='availability')),
                ('summary', models.CharField(help_text="A summary of the assistance you're requesting", max_length=80, verbose_name='request summary')),
                ('details', models.TextField(help_text='Optionally, more details about your request request', verbose_name='details')),
                ('when_submitted', models.DateField(blank=True, help_text='The date and time that the customer submitted the request', null=True, verbose_name='date submitted')),
                ('honeypot', models.CharField(blank=True, help_text='The size of your shoe', max_length=50, verbose_name='shoe size')),
                ('where_desired', models.ForeignKey(blank=True, help_text='The scheduled location for the appointment', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_discoveries.location')),
            ],
            options={
                'ordering': ('when_submitted',),
            },
        ),
    ]
