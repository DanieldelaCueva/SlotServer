from django.urls import path

from . import views

urlpatterns = [
    path('connect/<str:room_id>/', views.room, name='room'),
    path("slot-upload/", views.slotUpload, name='slot-upload'),
    path("slot-delete/", views.slotDelete, name='slot-delete'),
]