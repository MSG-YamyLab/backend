from django.urls import path
from .views import LoginApiView, TokenUpdateApiView, GetMeApiView

urlpatterns = [
    path('login', LoginApiView.as_view(), name="login"),
    path('token/refresh', TokenUpdateApiView.as_view(), name="refresh"),
    
    #me 
    path('me', GetMeApiView.as_view(), name="me")
]
