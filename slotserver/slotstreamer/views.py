from .models import Slot, Session

from django.db import IntegrityError
from django.contrib.auth.models import User

from authentication.models import UserAdditionalData

import os

from uuid import uuid4

import wget

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import SessionSerializer


@api_view(['GET'])
def slotStreamerIndex(request):
    """
        URL overview endpoint
    """
    return Response({
        "SlotStreamer": {
            "Url overview": "/",
            "Connect to WS": "connect/<str:room_id>/",
            "Upload Slots": "/slot-upload/ [AUTHENTICATION REQUIRED]",
            "Delete Slots": "/slot-delete/ [AUTHENTICATION REQUIRED]",
            "Create Session": "/create-session/ [AUTHENTICATION REQUIRED]",
            "Delete Session": "/delete-session/ [AUTHENTICATION REQUIRED]",
            "Get Sessions": "/get-sessions/ [AUTHENTICATION REQUIRED]",
            "Get Users by Session": "/get-users-by-session/<str:session_id>/ [AUTHENTICATION REQUIRED]",
            "Get Slots by Session": "/get-slots-by-session/<str:session_id>/ [AUTHENTICATION REQUIRED]"
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def room(request, room_id):
    """
        HTTP endpoint before WS upgrade
    """
    return Response({
        'message': "connected successfully",
        "room_id": room_id
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def slotUpload(request):
    """
    Reads slots from a csv file and uploads them to the database
    """
    room = request.data['room']

    try:
        session = Session.objects.get(room_id=room)

        slot_file_url = request.data['slot_file_url']

        temp_csv_file = wget.download(slot_file_url, os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))

        local_file_name = os.listdir(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"))[0]

        if local_file_name[-4::] == ".csv":
            with open(temp_csv_file, "r") as file:
                f = file.readlines()
                for slot in range(1, len(f)):
                    slot_line = f[slot].split(",")
                    Slot.objects.create(callsign=slot_line[0], type=slot_line[1], eobt=slot_line[2],
                                        tsat=slot_line[3], destination=slot_line[4], ttot=slot_line[5], room_id=session)

            os.remove(temp_csv_file)

            return Response({
                "operation_result": "Slots uploaded successfully"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "operation_result": "Error. Wrong file extension, .csv required"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Session.DoesNotExist:
        return Response({
            "operation_result": "Error. The session id doesn't exist"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def slotDelete(request):
    """
    Reads slots from a csv file and deletes them from the database
    """
    slot_file_url = request.data['slot_file_url']

    temp_csv_file = wget.download(slot_file_url, os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "temp"))

    local_file_name = os.listdir(os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "temp"))[0]

    if local_file_name[-4::] == ".csv":

        with open(temp_csv_file, "r") as file:
            f = file.readlines()
            for slot in range(1, len(f)):
                slot_line = f[slot].split(",")
                try:
                    selected_slot = Slot.objects.get(callsign=slot_line[0])
                    selected_slot.delete()
                except Slot.DoesNotExist:
                    os.remove(temp_csv_file)
                    return Response({
                        "error": "Trying to delete unexisting slot"
                    }, status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError:
                    os.remove(temp_csv_file)
                    return Response({
                        "error": "User already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)

        os.remove(temp_csv_file)

        return Response({
            "operation_result": "Slots deleted successfully"
        }, status=status.HTTP_200_OK)

    else:
        return Response({
            "operation_result": "Error. Wrong file extension, .csv required"
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSession(request):
    """
        Cretes a new session in the database
    """
    room_id = uuid4()
    session_name = request.data['session_name']

    try:
        Session.objects.create(room_id=room_id, session_name=session_name)

        return Response({
            "operation_result": "Session created successfully"
        }, status=status.HTTP_200_OK)
    except IntegrityError:
        return Response({
            "error": "Session already exists"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSession(request):
    """
        Deletes a session from the database
    """
    room_id = request.data['room_id']
    try:
        session = Session.objects.get(room_id=room_id)
        session.delete()

        return Response({
            "operation_result": "Session deleted successfully"
        }, status=status.HTTP_200_OK)

    except Session.DoesNotExist:
        return Response({
            "error": "Session does not exist"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSessions(request):
    """
    Retrieves the sessions from the database
    """
    session_list = Session.objects.all()
    serializer = SessionSerializer(session_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsersBySession(request, session_id):
    """
    Retrieves the users for a given session from the database
    """
    user_add_data_for_session = UserAdditionalData.objects.filter(room=session_id).values()

    user_list = []

    for entry in user_add_data_for_session:
        user = User.objects.get(id=entry["username_id"])
        new_user = {
            'username': user.username
        }
        user_list.append(new_user)

    return Response(user_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSlotsBySession(request, session_id):
    """
    Retrieves the users for a given session from the database
    """
    slot_list = Slot.objects.filter(room_id=session_id).values()

    return Response(slot_list, status=status.HTTP_200_OK)