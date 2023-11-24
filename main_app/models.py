from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group, Permission, AbstractUser


# Define a validator for an 8-digit number
validate_eight_digits = RegexValidator(
    regex=r'^\d{8}$',
    message='Company number must be 8 digits.'
)

validate_v5c_number = RegexValidator(
    regex=r'^\d{11}$',
    message='V5C number must be 11 digits.'
)

# Create your models here.

class Vehicle(models.Model):
    registrationNumber = models.CharField(primary_key=True, max_length=8, unique=True)
    current_owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    colour = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    yearOfManufacture = models.IntegerField()
    fuel_type = models.CharField(max_length=20, default='Petrol')
    engineCapacity = models.IntegerField(default=0)
    current_v5c_number = models.CharField(max_length=11, validators=[validate_v5c_number], unique=True)
    previous_owners_count = models.IntegerField(default=0)
    previous_owners = models.ManyToManyField(get_user_model(), related_name='previous_owners', blank=True)

    def __str__(self):
        return f"{self.registrationNumber} - {self.yearOfManufacture} {self.make} ({self.model})"
    
# Model for the history
SERVICE_TYPES = [
    ('minor', 'Minor Repair'),
    ('major', 'Major Repair'),
    ('service', 'Service'),
    ('full', 'Full Service'),
    ('mot', 'MOT'),
    ('body', 'Body Work'),
]
class History(models.Model):
    history_id = models.AutoField(primary_key=True) # update
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    date = models.DateField()
    mileage = models.IntegerField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()

    def __str__(self):
        return f"{self.service_type} on {self.date}"
    