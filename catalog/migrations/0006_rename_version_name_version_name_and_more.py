# Generated by Django 5.0.3 on 2024-05-07 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='version_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='version',
            old_name='version_number',
            new_name='number',
        ),
    ]
