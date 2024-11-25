from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserCreateSerializer, UserAuthSerializer, ConfirmationCodeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import secrets

class RegisterUserView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
            confirmation_code = secrets.token_urlsafe(16)
            ConfirmationCode.objects.create(user=user, code=confirmation_code)

        return Response(data={"username": username, "confirmation_code": confirmation_code}, status=status.HTTP_201_CREATED)

class AuthorizationView(CreateAPIView):
    serializer_class = UserAuthSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"key": token.key}, status=status.HTTP_200_OK)
        return Response(data={"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)

class ConfirmationCodeView(RetrieveAPIView):
    serializer_class = ConfirmationCodeSerializer

    def get_object(self):
        code = self.request.data.get('code')
        try:
            return ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user.is_active = True
        user.save()
        return Response({'message': 'User activated'}, status=status.HTTP_200_OK)