from django.db import models
from apps.chat.models import ChatModel, GroupChatModel
from core.models import CoreModel
from apps.users.serializers import UserModel
from .manager import MessageMeneger

class MessageModel(CoreModel):
    class Meta:
        db_table = "message"
    
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE, related_name='message', null=True, blank=True)
    chat_group = models.ForeignKey(GroupChatModel, on_delete=models.CASCADE, related_name='message', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='message')
    is_read = models.BooleanField(default=False)
    delete_me = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='delete_message', null=True, blank=True)
    
    objects = MessageMeneger()
