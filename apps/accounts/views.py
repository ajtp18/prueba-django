from apps.accounts.serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status


class CreateUser(CreateAPIView):
    user = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(APIView):

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['username'])

        if not user.check_password(request.data['password']):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({'token': str(token.key), 'user': serializer.data}, status=status.HTTP_200_OK)

class UserLogout(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({f'User {request.user.username} has been logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)