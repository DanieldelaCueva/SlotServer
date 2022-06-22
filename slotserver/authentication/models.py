from django.db import models
from django.contrib.auth.models import User

# Created models

class PublicToken(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    public_token = models.CharField(max_length=255, default="", primary_key=True)
    private_token = models.CharField(max_length=255, default="")

class UserAdditionalData(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=255, default="test_room")
