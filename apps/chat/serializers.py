from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import ChatModel, GroupChatModel
from apps.users.serializers import UserModel, UserSerializer
from apps.message.serializers import MessageSerializers

class ChatSerializers(ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = ChatModel
        fields = ('id', 'users', 'update_at', 'user_id')
        read_only_fields = ('update_at','users')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        if not UserModel.objects.filter(id=user_id).first():
            raise serializers.ValidationError(f'User user_id:{user_id} not exist')
        id = self.context.get('id')
        chat = ChatModel.objects.filter(users=id).filter(users=user_id).first()
        if chat:
            return chat
        chat = ChatModel.objects.create(**validated_data)
        chat.users.set([user_id, id])
        return chat

class ChatRepresentationSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    message = SerializerMethodField()
    class Meta:
        model = ChatModel
        fields = ('id', 'users', 'update_at', 'message', 'typed')
    
    def get_message(self, obj):
        last_message = obj.message.order_by('-create_at').first()
        return MessageSerializers(last_message).data if last_message else None 

class GroupChatSerializers(ModelSerializer):
    class Meta:
        model = GroupChatModel
        fields = ('id', 'users', 'update_at', 'name')
        read_only_fileds = ('update_at', 'users')

    def create(self, validated_data):
        user = self.context.get('user')
        users = validated_data.pop('users')
        group_chat = GroupChatModel.objects.create(**validated_data)
        group_chat.users.set([user])
        if users:
            group_chat.users.add(*users)
        return group_chat


class JoinToGroupSerializers(serializers.Serializer):
    user_id = serializers.ListField(child = serializers.IntegerField(write_only = True))
    
    def validate(self, attrs):
        users = attrs.get('user_id')
        users = UserModel.objects.filter(id__in = users)
        if not users:
            raise serializers.ValidationError({'error':'Users not exsist'})
        return users 
