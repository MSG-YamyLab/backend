from django.db.models.manager import BaseManager, Manager

class MessageMeneger(Manager):
    def delete_messenge_for_me(self, list_id, chat_id, user):
        msg = self.filter(id__in=list_id, delete_me__isnull=False, chat = chat_id)
        
        if msg.exists():
            msg.delete()
        return self.filter(id__in = list_id, chat = chat_id).update(delete_me=user)
   

    def delete_messenge_for_all_user(self, list_id, chat_id, user):
        return self.filter(id__in = list_id, chat = chat_id).delete()

    def delete_messenge_group_for_me(self, list_id, group_chat_id, user):
        return self.filter(id__in=list_id, chat_group=group_chat_id, owner=user).delete()
