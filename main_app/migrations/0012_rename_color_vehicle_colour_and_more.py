# Generated by Django 4.2.7 on 2023-11-22 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_vehicle_cc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='color',
            new_name='colour',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cc',
            new_name='engineCapacity',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='registration',
            new_name='registrationNumber',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='year',
            new_name='yearOfManufacture',
        ),
    ]
