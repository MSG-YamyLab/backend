from django.contrib.auth import PermissionDenied
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MessageModel
from apps.chat.models import ChatModel, GroupChatModel
from apps.users.serializers import UserSerializer

class MessageSerializers(ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = MessageModel
        fields = ('id', 'create_at',  'chat', 'chat_group', 'content', 'owner', 'is_read', 'delete_me')
        read_only_fields = ('id', 'owner', 'is_read', 'delete_me')

    def validate(self, attrs):
        if attrs.get('chat') and attrs.get('chat_group'):
            raise serializers.ValidationError({'Errors':'Message can  atachment only one instance'})
        if not attrs.get('chat') and not attrs.get('chat_group'):
            raise serializers.ValidationError({'Errors':'Message must be atachment to instance chat or group_chat'})

        return super().validate(attrs)


    def create(self, validated_data):
        owner = self.context.get('owner')
        msg = MessageModel.objects.create(owner = owner, **validated_data)
        return msg


class MessageSerializersDelete(serializers.Serializer):
    list_id = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    chat_id = serializers.IntegerField(write_only=True)


    def validate(self, attrs):
        user = self.context.get('user')
        chat_id = attrs.get('chat_id')
        chat = ChatModel.objects.filter(users = user, id = chat_id).first()
        if not chat:
            raise PermissionDenied('Access Deneid')

        return super().validate(attrs)

class MessageGroupSerializersDelete(serializers.Serializer):
    list_id = serializers.ListField(child = serializers.IntegerField(), write_only = True)
    group_chat_id = serializers.IntegerField(write_only = True)
    

    def validate(self, attrs):
        user = self.context.get('user')
        group_chat_id = attrs.get('group_chat_id')
        group_chat = GroupChatModel.objects.filter(users = user, id = group_chat_id).first()
        if not group_chat:
            raise PermissionDenied('Access Deinied')

        return super().validate(attrs)
    
    
