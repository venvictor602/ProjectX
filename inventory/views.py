
from django.views import View
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from rest_framework.exceptions import NotFound

from .permissions import DepartmentPermission  # Import custom permission class
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class SalesLoginView(APIView):
    """
    Custom view for Sales department login.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user belongs to the 'Sales' department
        if not user.groups.filter(name='Sales').exists():
            raise PermissionDenied("You do not belong to the Sales department.")

        # Issue tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "department": "Sales"
        }, status=status.HTTP_200_OK)


class InventoryLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user belongs to the 'Inventory Management' department
        if not user.groups.filter(name='Inventory Management').exists():
            raise PermissionDenied("You do not belong to the Inventory Management department.")

        # Issue tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "department": "Inventory Management"
        }, status=status.HTTP_200_OK)


class FinanceLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user belongs to the 'Finance' department
        if not user.groups.filter(name='Finance').exists():
            raise PermissionDenied("You do not belong to the Finance department.")

        # Issue tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "department": "Finance"
        }, status=status.HTTP_200_OK)


class CustomerSupportLoginView(APIView):
    """
    Custom view for Customer Support department login.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user belongs to the 'Customer Support' department
        if not user.groups.filter(name='Customer Support').exists():
            raise PermissionDenied("You do not belong to the Customer Support department.")

        # Issue tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "department": "Customer Support"
        }, status=status.HTTP_200_OK)






class RegisterSuperAdminView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SuperAdminRegistrationSerializer(data=request.data)
        
        # Validate and create the user
        if serializer.is_valid():
            serializer.save()  # This will call the `create` method in the serializer
            return Response({"message": "Super admin created successfully!"}, status=status.HTTP_201_CREATED)
        
        # If invalid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this endpoint

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            return Response({"detail": "Invalid test email or password."}, status=status.HTTP_401_UNAUTHORIZED)


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')  # Redirect to the login page after logout
    return HttpResponseForbidden("Invalid request method.")