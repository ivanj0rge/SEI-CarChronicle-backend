from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'groups', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = ['id', 'username', 'email']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['owner_id', 'first_name', 'last_name', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    current_owner = UserSerializer()
    class Meta:
        model = Vehicle
        fields = ['registration', 'current_owner', 'color', 'make', 'model', 'year', 'fuel', 'current_v5c_number', 'previous_owners_count', 'previous_owners']

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
