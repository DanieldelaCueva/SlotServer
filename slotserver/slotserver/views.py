from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def index(request):
    """
    Contains API URL patterns
    """

    return Response({
        "Applications": {
            "SlotStreamer": {
                "Connect to WS": "connect/<str:room_id>/",
                "Upload Slots": "/slot-upload/ [AUTHENTICATION REQUIRED]",
                "Delete Slots": "/slot-delete/ [AUTHENTICATION REQUIRED]"
            },
            "Authentication": {
                "Url overview": "/",
                "Login": "/authentication/login/",
                "Logout": "/authentication/logout/ [AUTHENTICATION REQUIRED]",
                "Check User Login": "/check-login/<str:username>",
                "Upload Users": "/user-upload/ [AUTHENTICATION REQUIRED]",
                "Delete Users": "/user-delete/ [AUTHENTICATION REQUIRED]"
            },
        },
        "Docs": {
            "Postman documentation": "/docs"
        }
    }, status=status.HTTP_200_OK)
