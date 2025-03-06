from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import UserSerializer, UserModel
from rest_framework import status

class LoginApiView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)



class TokenUpdateApiView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

class GetMeApiView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, *args, **kwargs):
        return  Response(UserSerializer(self.request.user).data, status=status.HTTP_200_OK)

