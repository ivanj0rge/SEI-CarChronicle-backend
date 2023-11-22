import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from .models import *
from .serializers import *
import environ
import os


environ.Env()
environ.Env.read_env()

# Create your views here.

def get_csrf_token(request):
    # Get the CSRF token using Django's get_token method
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

CustomUser = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class UpdateUserView(UpdateAPIView):
    parser_classes = [MultiPartParser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        if 'partial' in kwargs:
            kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleCreateUpdateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(current_owner=self.request.user)

class UpdateVehicleView(RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(current_owner=self.request.user)

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class HomeView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def proxy_view(request):
    if request.method == 'POST':
        url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'

        body = request.body
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'Wld1wxKxVJ8De9lDFnjTK9dap9vz1Kr78Y1yDBtY',
        }

        response = requests.post(url, data=body, headers=headers)
        data = response.json()

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request method'})

