# Generated by Django 4.2.7 on 2023-11-20 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_mechanic_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='fuel',
            field=models.CharField(choices=[('p', 'Petrol'), ('d', 'Diesel'), ('h', 'Hybrid'), ('e', 'Electric')], default='Petrol', max_length=20),
        ),
    ]
