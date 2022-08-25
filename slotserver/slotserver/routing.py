from channels.auth import AuthMiddlewareStack
from channels.router import ProtocolTypeRouter, URLRouter
import slotstreamer.routing

from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            slotstreamer.routing.websocket_urlpatterns
        )
    ),
})