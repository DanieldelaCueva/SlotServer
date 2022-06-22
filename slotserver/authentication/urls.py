from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('', views.authenticationIndex, name="auth-overview"),
    path('login/', views.authenticateUser, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('check-login/<str:username>', views.checkIfLoggedIn, name='check-login'),
    path("user-upload/", views.userUpload, name='user-upload'),
    path("user-delete/", views.userDelete, name='user-delete')
]