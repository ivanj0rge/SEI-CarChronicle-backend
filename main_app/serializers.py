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
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = CustomUser.objects.create_user(**validated_data)
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

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['owner_id', 'first_name', 'last_name', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    current_owner = UserSerializer()

    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_registrationNumber(self, value):
        return value
    
class VehicleCreateUpdateSerializer(VehicleSerializer):
    current_owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta(VehicleSerializer.Meta):
        exclude = ['current_owner']

    def create(self, validated_data):
        validated_data['current_owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('current_owner', None)
        return super().update(instance, validated_data)   

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
