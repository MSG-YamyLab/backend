from django.urls import path
from .views import CreateChatApiView, DeleteChatApiView, GetAllUserChatApiView, GetAllGroupChatApiView, GetChatByUserIdApiView, CreateGroupChatApiView, JoinToGroupChatApiView, LeaveGroupChatApiView,GetChatById


urlpatterns = [
    path('create', CreateChatApiView.as_view(), name="create_chat"),
    path('group/create',CreateGroupChatApiView.as_view(), name="create_group_chat"),
    path('my', GetAllUserChatApiView.as_view(), name="my_chat"),
    path('my/group', GetAllGroupChatApiView.as_view(), name="my_group_chat"),
    path('join/group/<int:pk>', JoinToGroupChatApiView.as_view(), name="join_to_group"),
    path('leave/group/<int:pk>', LeaveGroupChatApiView.as_view(), name="leave_to_group"),
    path('user/<int:pk>', GetChatByUserIdApiView.as_view(), name = "chat_by_user_id"),
    path('delete/<int:pk>', DeleteChatApiView.as_view(), name="delete_chat_by_id"),
    path('my/<int:pk>', GetChatById.as_view(), name="get_chat_by_id")
]
