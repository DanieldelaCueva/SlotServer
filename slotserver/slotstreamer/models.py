from django.db import models

# Created models

class Session(models.Model):
    room_id = models.CharField(primary_key=True, max_length=264)
    session_name = models.CharField(max_length=264)

    def __str__(self):
        return str(self.room_id)


class Slot(models.Model):
    callsign = models.CharField(max_length=7, primary_key=True)
    room_id=models.ForeignKey(Session, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)
    type = models.CharField(max_length=4)
    eobt = models.TimeField(auto_now=False, auto_now_add=False)
    tsat = models.TimeField(auto_now=False, auto_now_add=False)
    destination = models.CharField(max_length=4)
    ttot = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.callsign)


