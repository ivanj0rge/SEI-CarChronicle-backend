# Generated by Django 4.2.7 on 2023-11-23 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mechanic',
            name='company',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.RemoveField(
            model_name='history',
            name='company',
        ),
        migrations.RemoveField(
            model_name='history',
            name='mechanic',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Mechanic',
        ),
    ]
