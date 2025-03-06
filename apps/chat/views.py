from http.client import NOT_FOUND
from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, DestroyAPIView
from .serializers import ChatRepresentationSerializer, ChatSerializers, GroupChatSerializers, JoinToGroupSerializers
from .models import ChatModel, GroupChatModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import UserModel


class CreateChatApiView(CreateAPIView):
    serializer_class = ChatSerializers
    permission_classes = (IsAuthenticated, )
    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = ChatSerializers(data=data, context = {'id': user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateGroupChatApiView(CreateAPIView):
    serializer_class = GroupChatSerializers
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = GroupChatSerializers(data=data, context = {'user':user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllGroupChatApiView(ListAPIView):
    serializer_class = GroupChatSerializers
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return GroupChatModel.objects.filter(users = user)


class JoinToGroupChatApiView(GenericAPIView):
    serializer_class   = JoinToGroupSerializers
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = JoinToGroupSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data   
        pk  = self.kwargs.get('pk')
        group_chat = GroupChatModel.objects.filter(id = pk, users=user).first()
        if not group_chat:
            raise Http404('Group not found')
        
        group_chat.users.add(*data)
        serializer = GroupChatSerializers(group_chat)
        return Response(serializer.data, status=status.HTTP_200_OK)




class GetAllUserChatApiView(ListAPIView):
    serializer_class = ChatRepresentationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.filter(users = user)

    def get(self, request, *args, **kwargs):
        my_chat = self.get_queryset()
        serializer = ChatRepresentationSerializer(my_chat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class GetChatByUserIdApiView(ListAPIView):
    serializer_class = ChatSerializers
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.id
        pk = self.kwargs.get('pk')
        return ChatModel.objects.filter(users=user_id).filter(users=pk)

class DeleteChatApiView(DestroyAPIView):
    serializer_class = ChatSerializers
    permission_classes = (IsAuthenticated, )
    queryset = ChatModel.objects.all()

class LeaveGroupChatApiView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = ChatModel.objects.all()

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.request.user 
        group_chat = GroupChatModel.objects.filter(id = pk, users = user).first()
        if  not group_chat:
            raise Http404('Group chat not fou4nd') 
        if group_chat.users.count() == 1:
            group_chat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        group_chat.users.remove(user)
        serializer = GroupChatSerializers(group_chat)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetChatById(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatRepresentationSerializer

    def get_queryset(self):
        return ChatModel.objects.filter(users = self.request.user)

    def get(self, *args, **kwargs):
        chat = self.get_object()
        return Response(ChatRepresentationSerializer(chat).data, status = status.HTTP_200_OK)
