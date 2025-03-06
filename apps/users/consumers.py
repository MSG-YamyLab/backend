from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import UserContactsSerializers, UserModel
from asgiref.sync import async_to_sync, sync_to_async
from .serializers import UserSerializer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model



class UserStatusOnlineOfflineConsumer(AsyncWebsocketConsumer):
    async def connect(self):    
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            raise DenyConnection("Authentication required")
        
        await self.set_user_status(True)
        await self.accept()
    
    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.set_user_status(False)
    
    @database_sync_to_async
    def set_user_status(self, status):
        User = get_user_model()
        user = User.objects.get(id=self.user.id)
        user.is_online = status
        user.save()


  

class GetUserConntactsConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            raise DenyConnection("Authenticated required")
        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_user_data()

    async def send_user_data(self):
        
        user = await self.get_user_data()
    
        await self.send(text_data=json.dumps(user))
    

    @database_sync_to_async
    def get_user_contacts(self):
        return UserSerializer(self.user.contacts.all(), many=True).data

    @database_sync_to_async
    def get_user_data(self):
        serializer = UserContactsSerializers(self.user)
        return serializer.data


    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def user_update(self,event):
        await self.send(text_data = json.dumps(event["data"]))


