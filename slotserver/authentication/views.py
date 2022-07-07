from urllib.error import HTTPError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import UserSerializer

from .models import PublicToken, UserAdditionalData

from slotstreamer.models import Session

from uuid import uuid4
import wget
import os


@api_view(["GET"])
def authenticationIndex(request):
    """
        URL overview endpoint
    """
    auth_urls = {
        "Authentication": {
            "Url overview": "/",
            "Login": "/authentication/login/",
            "Logout": "/authentication/logout/ [AUTHENTICATION REQUIRED]",
            "Check User Login": "/check-login/<str:username>",
            "Upload Users": "/user-upload/ [AUTHENTICATION REQUIRED]",
            "Delete Users": "/user-delete/ [AUTHENTICATION REQUIRED]"
        }
    }
    return Response(auth_urls, status=status.HTTP_200_OK)


@api_view(["POST"])
def authenticateUser(request):
    """
        Takes username and password and returns tokens and room if credentials are correct, returns error message otherwise
    """

    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        private_token, priv_token_created = Token.objects.get_or_create(
            user=user)
        if priv_token_created:
            public_token = uuid4()
            public_token = str(public_token).replace("-", "")
            PublicToken.objects.create(
                username=user, public_token=public_token, private_token=private_token)
        else:
            public_token = PublicToken.objects.get(private_token=private_token).public_token

        user_additional_data = UserAdditionalData.objects.get(username=user)
        return Response({
            "username": username,
            "private_token": str(private_token),
            "public_token": str(public_token),
            "room": str(user_additional_data.room),
            "is_admin": str(user_additional_data.is_admin)
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def userLogout(request):
    """
    Logs out an authenticated user. Private token has to be provided in order to perform authentication   
    """
    key = request.META.get("HTTP_AUTHORIZATION").split()[1]
    priv_token = Token.objects.get(key=key)
    public_token = PublicToken.objects.get(private_token=priv_token)
    public_token.delete()
    priv_token.delete()
    return Response({
        "operation_result": "Logout successful"
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
def checkIfLoggedIn(request, username):
    """
    Retrus true if the user is logged in, false otherwise
    """
    user = User.objects.get(username=username)
    userSerializer = UserSerializer(user, many=False)
    id = userSerializer.data["id"]
    try:
        key = Token.objects.get(user=id)
        return Response({
            "operation_result": "true"
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            "operation_result": "false"
        }, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def userUpload(request):
    """
    Reads users from a csv file and uploads them to the database
    """

    try:
        user_file_url = request.data["user_file_url"]

        temp_csv_file = wget.download(user_file_url, os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))

        local_file_name = os.listdir(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))[0]

        if local_file_name[-4::] == ".csv":
            with open(temp_csv_file, "r") as file:
                f = file.readlines()
                for slot in range(1, len(f)):
                    slot_line = f[slot].split(";")
                    try:
                        room = Session.objects.get(room_id=slot_line[2])
                        User.objects.create(
                            username=slot_line[0], password=make_password(slot_line[1]))
                        new_user = User.objects.get(username=slot_line[0])
                        UserAdditionalData.objects.create(
                            username=new_user, room=room)
                    except Session.DoesNotExist:
                        os.remove(temp_csv_file)
                        return Response({
                            "error": "The session id doesn't exist"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    except IntegrityError:
                        existing_user = User.objects.get(username=slot_line[0])
                        existing_user.delete()

                        User.objects.create(
                            username=slot_line[0], password=make_password(slot_line[1]))
                        new_user = User.objects.get(username=slot_line[0])
                        UserAdditionalData.objects.create(
                            username=new_user, room=room)

            os.remove(temp_csv_file)

            return Response({
                "operation_result": "Users uploaded successfully"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "operation_result": "Error. Wrong file extension, .csv required"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
    except HTTPError:
        return Response({
            "operation_result": "Error. The file was not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def userDelete(request):
    """
    Reads users from a csv file and deletes them from the database
    """

    try:
        user_file_url = request.data["user_file_url"]

        temp_csv_file = wget.download(user_file_url, os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))

        local_file_name = os.listdir(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))[0]

        if local_file_name[-4::] == ".csv":
            with open(temp_csv_file, "r") as file:
                f = file.readlines()
                for slot in range(1, len(f)):
                    slot_line = f[slot].split(";")
                    try:
                        user = User.objects.get(username=slot_line[0])
                        user.delete()
                    except User.DoesNotExist:
                        pass

            os.remove(temp_csv_file)

            return Response({
                "operation_result": "Users deleted successfully"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "operation_result": "Error. Wrong file extension, .csv required"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
    except HTTPError:
        return Response({
            "operation_result": "Error. The file was not found"
        }, status=status.HTTP_404_NOT_FOUND)
