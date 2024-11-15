# Generated by Django 5.0.3 on 2024-05-24 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_discoveries', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='customers_available',
        ),
        migrations.AddField(
            model_name='appointment',
            name='customers_availability',
            field=models.TextField(blank=True, help_text="The customer's preference regarding scheduling", verbose_name="customer's availability"),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customers_request',
            field=models.TextField(blank=True, help_text='The description of the issue, copied from the form', verbose_name="customer's request"),
        ),
    ]
