from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import UserContactsSerializers, UserModel
from asgiref.sync import async_to_sync, sync_to_async
from .serializers import UserSerializer,MyContactsSerializer
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
        await self.get_me()

    @database_sync_to_async
    def update_user(self, data):
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user = await self.update_user(data)
        await self.send(text_data=json.dumps(user))

    async def get_me(self):
        await self.send(text_data=json.dumps(UserSerializer(self.user).data))

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.set_user_status(False)
    
    @database_sync_to_async
    def set_user_status(self, status):
        User = get_user_model()
        user = User.objects.get(id=self.user.id)
        user.is_online = status
        user.save()
  



class GetMyContactsConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user =self.scope["user"]
        if not self.user.is_authenticated:
            raise DenyConnection("Auth required")
        self.group_name = f"me_{self.user.id}_contacts"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_contacts()
    
    async def disconnect(self, code):
        if  self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
    async def send_contacts(self):
        my_contacts = await self.get_my_contacts()
        await self.send(text_data=json.dumps(my_contacts))
    
    async def update_user_from_contacts(self, event):
        await self.send(text_data = json.dumps(event["data"]))

    @database_sync_to_async
    def get_my_contacts(self):
        serializer = MyContactsSerializer(self.user)
        return serializer.data
    

