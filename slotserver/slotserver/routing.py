from channels.auth import AuthMiddlewareStack
from channels.router import ProtocolTypeRouter, URLRouter
import slotstreamer.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            slotstreamer.routing.websocket_urlpatterns
        )
    ),
})