from django.contrib import admin

from .models import Slot, Session

# Registered models

admin.site.register(Slot)
admin.site.register(Session)