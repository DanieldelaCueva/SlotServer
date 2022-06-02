from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def room(request, room_id):

    return Response({
        'message': "connected successfully",
        "room_id": room_id
    }, status = status.HTTP_201_CREATED)