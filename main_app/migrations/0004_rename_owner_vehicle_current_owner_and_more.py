# Generated by Django 4.2.7 on 2023-11-17 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_company_vehicle_mechanic_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='owner',
            new_name='current_owner',
        ),
        migrations.RemoveField(
            model_name='history',
            name='previous_owners_count',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='current_v5c_number',
            field=models.CharField(default=0, max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='V5C number must be 11 digits.', regex='^\\d{11}$')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='previous_owners',
            field=models.ManyToManyField(blank=True, related_name='previous_owners', to='main_app.owner'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='previous_owners_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_number',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message='Company number must be 8 digits.', regex='^\\d{8}$')]),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registration',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]
