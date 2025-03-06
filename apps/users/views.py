from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AvatarModel
from .serializers import AvatarSerializer, UserContactsSerializers, UserIdSerializers, UserModel, UserRegistrationSerializer, UserSerializer, ProfileModel, ProfileSerializer, UserNicknameSerializers
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

class CreateUserApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class GetAllUserApiView(ListAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()



class GetMeApiView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    def get_object(self):
        return self.request.user

class GetUserByNickname(GenericAPIView):
    serializer_class = UserNicknameSerializers
    permission_classes = (IsAuthenticated,)
    
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = UserNicknameSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        user_list = UserModel.objects.filter(nickname__startswith=serializer.data.get('nickname'))
        return Response(UserSerializer(user_list, many=True).data, status=status.HTTP_200_OK)


class AddToContactById(GenericAPIView):
    serializer_class = UserIdSerializers
    permission_classes = (IsAuthenticated, )
    
    def post(self, *args, **kwargs):
        data = self.request.data 
        user = self.request.user 
        serializer = UserIdSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        user_to_add = UserModel.objects.filter(id = serializer.data.get('id')).first()
        if not user_to_add:
            raise serializers.ValidationError({"detail":"User don't exist"})
        if user_to_add == user:
            raise serializers.ValidationError({"detail":"Can't add yorself"})
        user.contacts.add(user_to_add)
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class DeleteToContactById(GenericAPIView):
    serializer_class = UserIdSerializers
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user

        serializer = UserIdSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        user_to_delete = UserModel.objects.filter(id = serializer.data.get('id')).first()
        if not user_to_delete:
            raise serializers.ValidationError({"detail":"User don't exist"})
        user.contacts.remove(user_to_delete)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class GetMyContactsApiView(GenericAPIView):
    serializer_class = UserContactsSerializers
    

    def get(self, *args, **kwargs):
        user = self.request.user 
        serializer = UserContactsSerializers(user)
        return Response(serializer.data)

class SetImageUserApiVIew(GenericAPIView):
    serializer_class = AvatarSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = AvatarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        profile = user.profile
        avatar = AvatarModel.objects.create(profile=profile, **serializer.validated_data)
        avatar.save()
        serializer = UserSerializer(user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class UpdateProfileApiView(UpdateAPIView):
    serializer_class = ProfileSerializer
    http_method_names = ('patch',)

    def get_object(self):
        return self.request.user.profile

    def patch(self,*args,**kwargs):
        profile = self.get_object()
        data =self.request.data
        serializer = ProfileSerializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(self.request.user).data, status=status.HTTP_200_OK)

class UpdateUserApiView(UpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ('patch',)

    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


