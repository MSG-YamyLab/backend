from django.db import models
from core.models import CoreModel
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class ChatModel(CoreModel):
    class Meta:
        db_table = "chat"
    users = models.ManyToManyField(UserModel, related_name='chat')
    typed = models.JSONField(default=list, blank=True) 



class GroupChatModel(CoreModel):
    class Meta:
        db_table = 'group_chat'

    name = models.CharField(max_length=50)
    users = models.ManyToManyField(UserModel, related_name='group_chat', null=True, blank=True)    
