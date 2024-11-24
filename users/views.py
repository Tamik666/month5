from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializer import UserCreateSerializer, UserAuthSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from secrets import token_urlsafe

# Create your views here.

@api_view(['POST'])
def confirmation_code_api_view(request):
    code = request.data.get('code')
    try:
        confirmation_code = ConfirmationCode.objects.get(code=code)
        user = confirmation_code.user
        user.is_active = True
        user.save()
        return Response({'message': 'User activated'}, status=status.HTTP_200_OK)
    except ConfirmationCode.DoesNotExist:
        return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
        confirmation_code = token_urlsafe(6)
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

    return Response(data={"username": username, "confirmation_code": confirmation_code}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"key": token.key}, status=status.HTTP_200_OK)
    return Response(data={"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)