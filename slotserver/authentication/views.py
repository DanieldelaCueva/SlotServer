from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import UserSerializer, PasswordSerializer

# Create your views here.

@api_view(['GET'])
def authOverview(request):
    auth_urls = {
        'Authorization': {
            'Login': '/authorization/login/',
            'Logout': '/authorization/logout/ [AUTHENTICATION REQUIRED]',
            'Change Password': '/authorization/change-password/<str:username>/ [AUTHENTICATION REQUIRED]'
        }
    }
    return Response(auth_urls)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def userLogout(request):
    key = request.META.get('HTTP_AUTHORIZATION').split()[1]
    token = Token.objects.get(key=key)
    token.delete()
    return Response("Logged out successfully")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userChangePassword(request, username):
    user = User.objects.get(username=username)
    idSerializer = UserSerializer(user, many=False)
    id = idSerializer.data['id']
    
    password = request.data['password']
    securePassword = make_password(password)
    serializer = PasswordSerializer(instance=user, data=request.data)

    token_key = Token.objects.get(user=id)

    if serializer.is_valid():
        serializer.validated_data['password'] = securePassword
        
        if str(token_key) == request.META.get('HTTP_AUTHORIZATION').split()[1]:
            serializer.save()
            return Response("Password reset successfully for user " + str(serializer.data['username']))
        else:
            return Response("Can't change others users password")

    else:
        return Response("Invalid data")