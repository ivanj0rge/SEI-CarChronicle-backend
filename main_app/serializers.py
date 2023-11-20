from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Owner, Vehicle, History, Mechanic, Company

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'groups']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove confirm_password from validated_data
        user = User.objects.create_user(**validated_data)
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['owner_id', 'first_name', 'last_name', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    current_owner = OwnerSerializer()
    class Meta:
        model = Vehicle
        fields = ['registration', 'current_owner', 'color', 'make', 'model', 'year', 'current_v5c_number', 'previous_owners_count', 'previous_owners']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_number', 'name', 'address']

class MechanicSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Mechanic
        fields = ['mechanic_id', 'first_name', 'last_name', 'company']

class HistorySerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    mechanic = MechanicSerializer()
    company = CompanySerializer()
    class Meta:
        model = History
        fields = ['history_id', 'vehicle', 'date', 'mileage', 'service_type', 'description', 'mechanic', 'company']
