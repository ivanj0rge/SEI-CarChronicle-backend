from django.db import models
from django.core.validators import RegexValidator

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
    registration = models.CharField(primary_key=True, max_length=8, unique=True)
    current_owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    current_v5c_number = models.CharField(max_length=11, validators=[validate_v5c_number], unique=True)
    previous_owners_count = models.IntegerField(default=0)
    previous_owners = models.ManyToManyField('Owner', related_name='previous_owners', blank=True)

    def __str__(self):
        return f"{self.registration} - {self.year} {self.make} ({self.model})"
    
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
    first_name = models.CharField(max_length=50)
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