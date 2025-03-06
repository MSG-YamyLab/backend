from django.urls import path
from .views import CreateMessageApiView, DeleteMessageApiView, GetAllMessageByChatIdApiView, DeleteMessageAllUsersApiView, DeleteMessageGroupChatApiView, GetAllMessageByGroupChatIdApiView


urlpatterns = [
    path('create', CreateMessageApiView.as_view(), name = "create_message"),
    path('delete/me', DeleteMessageApiView.as_view(), name="delete_message"),
    path('delete/all', DeleteMessageAllUsersApiView.as_view(), name="delete_all_message"),
    path('delete/group', DeleteMessageGroupChatApiView.as_view(), name="delete_my_message"),
    path('chat/<int:pk>', GetAllMessageByChatIdApiView.as_view(), name="all_message_chat"),
    path('group/<int:pk>', GetAllMessageByGroupChatIdApiView.as_view(), name="all_message_group")
] 
