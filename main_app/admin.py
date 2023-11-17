from django.contrib import admin
from .models import Owner, Vehicle, History, Mechanic, Company

# Register your models here.

admin.site.register(Owner)
admin.site.register(Vehicle)
admin.site.register(History)
admin.site.register(Mechanic)
admin.site.register(Company)