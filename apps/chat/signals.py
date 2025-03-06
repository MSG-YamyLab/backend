from django.db.models.signals import post_save, m2m_changed, pre_delete, post_delete
from django.dispatch import receiver
from .serializers import ChatRepresentationSerializer, ChatModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 
from apps.message.models import MessageModel
from apps.message.serializers import MessageSerializers



@receiver(m2m_changed, sender=ChatModel.users.through)
def notify_user_update_chat(sender, instance, **kwargs):
    action = kwargs.pop('action', None)
    if action == "post_add" or action == "post_remove" or action == "post_clear":  
        chat_user = instance.users.all()
        channel_layer = get_channel_layer()
        for user in chat_user:
            async_to_sync(channel_layer.group_send)(
                f"me_chat_{user.id}",
                {
                    "type":"update_chat",
                    "data":ChatRepresentationSerializer(ChatModel.objects.filter(users=user), many=True).data 
                }
            )

@receiver(pre_delete, sender=ChatModel)
def notify_user_del(sender, instance, **kwargs):
    chat_user = instance.users.all()
    channel_layer = get_channel_layer()
    for user in chat_user:
        async_to_sync(channel_layer.group_send)(
            f"me_chat_{user.id}",
                {
                    "type":"update_chat",
                    "data":ChatRepresentationSerializer(ChatModel.objects.filter(users=user).exclude(id = instance.id), many=True).data 
                }
            )


def update_chat_by_message(chat): 
    channel_layer = get_channel_layer()
    chat_user = chat.users.all()
    for user in chat_user:
        async_to_sync(channel_layer.group_send)(
            f"me_chat_{user.id}",
                {
                    "type":"update_chat",
                    "data":ChatRepresentationSerializer(ChatModel.objects.filter(users = user), many=True).data
                }
            )

def delete_chat_message(chat):
    channel_layer = get_channel_layer()
    chat_user = chat.users.all()
    for user in chat_user:
        async_to_sync(channel_layer.group_send)(
            f"me_chat_{user.id}",
            {
                "type":"update_chat",
                "data":ChatRepresentationSerializer(ChatModel.objects.filter(users=user).filter(id != chat.id),many=True).data
            }
        )

@receiver(post_save, sender=MessageModel)
def notify_user_message_by_chat(sender, instance, created, **kwargs):
    if created:
        update_chat_by_message(instance.chat)


@receiver(post_save, sender=MessageModel)
def notify_user_message_by_chat_messenger(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        chat = instance.chat
        async_to_sync(channel_layer.group_send)(
            f"message_chat_{chat.id}",
            {
                "type":"new_message",
                "data":MessageSerializers(MessageModel.objects.filter(chat_id=chat.id), many=True).data
            }

        )

@receiver(post_save, sender=ChatModel)
def notify_chat_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
            f"me_chat_{instance.id}",
            {
                "type":"update_chat_me",
                "data":ChatRepresentationSerializer(instance).data 
            }

        )
