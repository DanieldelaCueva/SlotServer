from django.contrib import admin
from .models import PublicToken, UserAdditionalData

# Registered models

admin.site.register(PublicToken)
admin.site.register(UserAdditionalData)