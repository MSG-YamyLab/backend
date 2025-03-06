from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .serializers import UserContactsSerializers, UserModel, UserSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 


@receiver(m2m_changed, sender=UserModel.contacts.through)
def notify_user_contacts_update(sender, instance, **kwargs):
    action = kwargs.pop('action', None)
    if action=="post_add" or action == "post_remove":
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.id}",
            {
                "type":"user_update",
                "data":UserContactsSerializers(instance).data 
            }
        )

@receiver(post_save,sender=UserModel)
def notify_user_update_from_contacts(sender, instance, **kwargs):
    users_contacts = UserModel.objects.filter(contacts=instance)
    for user in users_contacts:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type":"user_update",
                "data":UserContactsSerializers(user).data
            }
                
        )

    


