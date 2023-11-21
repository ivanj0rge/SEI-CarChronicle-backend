# Generated by Django 4.2.7 on 2023-11-21 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0007_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='current_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='previous_owners',
            field=models.ManyToManyField(blank=True, related_name='previous_owners', to=settings.AUTH_USER_MODEL),
        ),
    ]