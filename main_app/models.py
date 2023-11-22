from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Permission, Group
from PIL import Image

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

# Model for the owner
class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=150, unique=True, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Vehicle(models.Model):
    registrationNumber = models.CharField(primary_key=True, max_length=8, unique=True)
    current_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service_type} on {self.date}"

# Model for the mechanic
class Mechanic(models.Model):
    mechanic_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name}, {self.company.name}"
    
# Model for the company
class Company(models.Model):
    company_number = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[validate_eight_digits],
        unique=True
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.company_number}"
    

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize the profile picture if it exists
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            # Resize the image if it's larger than 300x300
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

    def __str__(self):
        return self.username