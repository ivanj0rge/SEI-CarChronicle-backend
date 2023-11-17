from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Owner, Vehicle, History, Mechanic, Company

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['owner_id', 'first_name', 'last_name', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['registration', 'current_owner', 'color', 'make', 'model', 'year', 'current_v5c_number', 'previous_owners_count', 'previous_owners']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['history_id', 'vehicle', 'date', 'mileage', 'service_type', 'description', 'mechanic', 'company']

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = ['mechanic_id', 'first_name', 'last_name', 'company']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_number', 'name', 'address']

