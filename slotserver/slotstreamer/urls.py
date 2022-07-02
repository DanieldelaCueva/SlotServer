from django.urls import path

from . import views

urlpatterns = [
    path("", views.slotStreamerIndex, name="alotstreamer-index"),
    path('connect/<str:room_id>/', views.room, name='room'),
    path("slot-upload/", views.slotUpload, name='slot-upload'),
    path("slot-delete/", views.slotDelete, name='slot-delete'),
    path("create-session", views.createSession, name='create-session'),
    path("delete-session", views.deleteSession, name='delete-session'),
    path("get-sessions", views.getSessions, name='get-sessions'),
    path("get-users-by-session/<str:session_id>", views.getUsersBySession, name='get-users-by-session')
]