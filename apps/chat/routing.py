from django.urls import path
from .consumers import GetMeChatConsumer, GetMyChatFromMessage, GetMyChatByIdConsumers 

ws_urlpatterns = [
    path("ws/chat/me", GetMeChatConsumer.as_asgi(), name="get_me_chat"),
    path("ws/chat/<int:pk>/messages", GetMyChatFromMessage.as_asgi(), name="get_message_by_chat_id"),
    path("ws/chat/me/<int:pk>", GetMyChatByIdConsumers.as_asgi(), name="get_chat_by_id"),
]
