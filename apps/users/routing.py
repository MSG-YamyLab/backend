from django.urls import path 
from .consumers import   UserStatusOnlineOfflineConsumer, GetMyContactsConsumers

ws_urlpatterns = [
    path("ws/users/status", UserStatusOnlineOfflineConsumer.as_asgi(), name="online_offline"
         ),
    path("ws/users/my/contacts", GetMyContactsConsumers.as_asgi(), name="get_my_contacts" ),
]
# ws_urlpatterns += ws_chat
