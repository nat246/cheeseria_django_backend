from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(operation_description="Register a new user",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['email', 'username', 'password'],
                             properties={
                                 'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                                 'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                                 'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
                             }
                         ))
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    @swagger_auto_schema(operation_description="Login a user",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['email', 'password'],
                             properties={
                                 'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                                 'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
                             }
                         ))
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)

        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    @swagger_auto_schema(operation_description="Logout a user")
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    @swagger_auto_schema(operation_description="Get user details")
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
