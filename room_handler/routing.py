from django.urls import path
from . import ws_api

websocket_urlpatterns=[
    path('ws/<str:room_name>/',ws_api.ChatConsumer.as_asgi())
]