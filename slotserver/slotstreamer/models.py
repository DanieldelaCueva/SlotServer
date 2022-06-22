from django.db import models

# Created models

class Slot(models.Model):
    callsign = models.CharField(max_length=7, primary_key=True)
    room_id=models.CharField(max_length=254, default="test_room")
    cleared = models.BooleanField(default=False)
    type = models.CharField(max_length=4)
    eobt = models.TimeField(auto_now=False, auto_now_add=False)
    tsat = models.TimeField(auto_now=False, auto_now_add=False)
    destination = models.CharField(max_length=4)
    ttot = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.callsign)
