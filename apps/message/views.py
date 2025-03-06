from typing_extensions import List
from django.template import context
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.views import Response
from django.core.exceptions import PermissionDenied

from .serializers import MessageSerializers, MessageSerializersDelete, MessageGroupSerializersDelete
from .models import MessageModel
from apps.chat.serializers import ChatSerializers
from apps.chat.models import ChatModel, GroupChatModel

class CreateMessageApiView(CreateAPIView):
    serializer_class = MessageSerializers
    permission_classes = (IsAuthenticated, )
    
    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = MessageSerializers(data=data, context = {"owner":user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class DeleteMessageApiView(GenericAPIView):
    serializer_class = MessageSerializersDelete
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        
        serializer = MessageSerializersDelete(data=data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        MessageModel.objects.delete_messenge_for_me(user=user, **serializer.validated_data)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteMessageAllUsersApiView(GenericAPIView):
    serializer_class = MessageSerializersDelete
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = MessageSerializersDelete(data=data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        MessageModel.objects.delete_messenge_for_all_user(user=user, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteMessageGroupChatApiView(GenericAPIView):
    serializer_class = MessageGroupSerializersDelete
    permission_classes = (IsAuthenticated, )


    def post(self, *args, **kwargs):
        user = self.request.user 
        data = self.request.data 

        serializer = MessageGroupSerializersDelete(data=data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        MessageModel.objects.delete_messenge_group_for_me(user=user, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)        
        
class GetAllMessageByChatIdApiView(ListAPIView):
    serializer_class = MessageSerializers
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        chat = ChatModel.objects.filter(id = pk).filter(users = self.request.user).first()
        if not chat:
            raise PermissionDenied("Access denied")
        return MessageModel.objects.filter(chat=pk).exclude(delete_me = self.request.user)

class GetAllMessageByGroupChatIdApiView(ListAPIView):
    serializer_class = MessageSerializers
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        chat = GroupChatModel.objects.filter(id = pk).filter(users = self.request.user).first()
        if not chat:
            raise PermissionDenied("Access denied")
        return MessageModel.objects.filter(chat_group=pk)

