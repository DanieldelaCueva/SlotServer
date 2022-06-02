from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'slotstreamer/(?P<room_id>\w+)/$', consumers.SlotStreamerConsumer())
]