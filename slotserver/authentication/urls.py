from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('/', views.authOverview, name="auth-overview"),
    path('login/', auth_views.obtain_auth_token, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('change-password/<str:username>', views.userChangePassword, name='change-password'),
]