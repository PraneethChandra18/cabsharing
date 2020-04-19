from channels.routing import ProtocolTypeRouter
from django.urls import re_path, include
from . import consumers

websocket_urlpatterns = [
 re_path(r'ws/chat/(?P<pk>[0-9]+)/$', consumers.ChatConsumer),
 re_path(r'ws/notification/',consumers.NotificationConsumer),
 ]
