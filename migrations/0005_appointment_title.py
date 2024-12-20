# Generated by Django 5.0.6 on 2024-11-14 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_discoveries', '0004_remove_appointment_customers_request_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='title',
            field=models.CharField(blank=True, help_text='A title for the appointment (ex, help Brenda with her tablet)', max_length=255, verbose_name='title'),
        ),
    ]
