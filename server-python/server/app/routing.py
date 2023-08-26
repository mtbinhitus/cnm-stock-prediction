from django.urls import re_path
from app.socket_kline import KlineConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', KlineConsumer.as_asgi()),
]