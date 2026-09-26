from django.urls import re_path
from .consumers import VideoStatusConsumer


websocket_urlpatterns = [
    re_path(r'^ws/videos/$', VideoStatusConsumer.as_asgi()),
]