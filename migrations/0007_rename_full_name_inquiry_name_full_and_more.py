# Generated by Django 5.0.6 on 2024-11-26 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spl_discoveries', '0006_inquiry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inquiry',
            old_name='full_name',
            new_name='name_full',
        ),
        migrations.RenameField(
            model_name='inquiry',
            old_name='prefered_name',
            new_name='name_prefered',
        ),
    ]