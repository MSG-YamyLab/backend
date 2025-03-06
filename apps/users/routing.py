from django.urls import path 
from .consumers import  GetUserConntactsConsumers, UserStatusOnlineOfflineConsumer
from apps.chat.routing import ws_urlpatterns as ws_chat
ws_urlpatterns = [
    path("ws/users/status", UserStatusOnlineOfflineConsumer.as_asgi(), name="online_offline"
         ),
    path("ws/users/test", GetUserConntactsConsumers.as_asgi(), name="get_user_data" )
]
ws_urlpatterns += ws_chat
