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
            "Admin": {
                "Admin page": "/admin"
            },
            "Authentication": {
                "Url overview": "/",
                "Login": "/authentication/login/",
                "Logout": "/authentication/logout/ [AUTHENTICATION REQUIRED]",
                "Check User Login": "/check-login/<str:username>",
                "Upload Users": "/user-upload/ [AUTHENTICATION REQUIRED]",
                "Delete Users": "/user-delete/ [AUTHENTICATION REQUIRED]"
            },
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
            },
        },
        "Docs": {
            "Postman documentation": "/docs"
        }
    }, status=status.HTTP_200_OK)
