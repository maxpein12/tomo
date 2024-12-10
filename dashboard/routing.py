from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .consumers import UserStatusConsumer

websocket_urlpatterns = [
    re_path(r'^user-status/$', UserStatusConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})