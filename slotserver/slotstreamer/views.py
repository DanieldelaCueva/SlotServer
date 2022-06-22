from .models import Slot

import os

import wget

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.


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
                                    tsat=slot_line[3], destination=slot_line[4], ttot=slot_line[5], room_id=room)

        os.remove(temp_csv_file)

        return Response({
            "operation_result": "Slots uploaded successfully"
        }, status=status.HTTP_200_OK)

    else:
        return Response({
            "operation_result": "Error. Wrong file extension, .csv required"
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


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
                selected_slot = Slot.objects.get(callsign=slot_line[0])
                selected_slot.delete()

        os.remove(temp_csv_file)

        return Response({
            "operation_result": "Slots deleted successfully"
        }, status=status.HTTP_200_OK)

    else:
        return Response({
            "operation_result": "Error. Wrong file extension, .csv required"
        }, status=status.HTTP_406_NOT_ACCEPTABLE)
