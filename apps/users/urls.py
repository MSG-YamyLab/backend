from django.urls import path
from .views import AddToContactById, CreateUserApiView, GetAllUserApiView, GetMeApiView, GetMyContactsApiView, GetUserByNickname, DeleteToContactById, SetImageUserApiVIew, UpdateProfileApiView, UpdateUserApiView

urlpatterns = [
    path('register', CreateUserApiView.as_view(), name = "register"),
    path('users', GetAllUserApiView.as_view(), name="get_all_users"),
    path('me', GetMeApiView.as_view(), name="get_me"),
    path('avatar/add', SetImageUserApiVIew.as_view(), name="set_avatar_user"),
    path('find/nickname', GetUserByNickname.as_view(), name="get_user_by_nickname"),
    path('contact/add', AddToContactById.as_view(), name="add_user_to_contact"),
    path('contact/del', DeleteToContactById.as_view(), name="delete_user_to_contact"),
    path('profile/update', UpdateProfileApiView.as_view(), name="update_profile_user"),
    path('user/update', UpdateUserApiView.as_view(), name="update_user")

]
