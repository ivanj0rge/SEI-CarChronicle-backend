from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'groups', 'first_name', 'last_name']
        read_only_fields = ['id']

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            **validated_data)
        return user
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        print(request.data)
        
        validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        return super().update(instance, validated_data)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    current_owner = serializers.PrimaryKeyRelatedField(
        read_only=False, 
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_registrationNumber(self, value):
        return value

    def create(self, validated_data):
        validated_data['current_owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'current_owner' in validated_data and validated_data['current_owner'] is None:
            # Remove the current owner
            validated_data.pop('current_owner', None)
        return super().update(instance, validated_data) 

class HistorySerializer(serializers.ModelSerializer):
    vehicle_registration_number = serializers.CharField(write_only=True)
    
    class Meta:
        model = History
        fields = ['history_id', 'vehicle_registration_number', 'date', 'mileage', 'service_type', 'description']

    def create(self, validated_data):
        # Extract the registration number from validated data
        vehicle_registration_number = validated_data.pop('vehicle_registration_number')

        # Get the associated Vehicle object
        vehicle = Vehicle.objects.get(registrationNumber=vehicle_registration_number)

        # Create the history log with the associated vehicle
        history = History.objects.create(vehicle=vehicle, **validated_data)
        return history