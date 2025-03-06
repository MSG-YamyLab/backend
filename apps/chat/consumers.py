from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import ChatRepresentationSerializer, ChatModel
import json 
from channels.db import database_sync_to_async
from apps.message.models import MessageModel
from apps.message.serializers import MessageSerializers

class GetMyChatByIdConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.id = self.scope["url_route"]["kwargs"]["pk"]
        if not self.user.is_authenticated:
            raise DenyConnection("Authenticated required")
        self.group_name = f"me_chat_{self.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        data = await self.get_chat_by_id()
        await self.send_to_chat_me(data)
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def get_chat_by_id(self):
        chat = ChatModel.objects.filter(id = self.id).first()
        if not chat:
            raise DenyConnection("Chat not found")
        return ChatRepresentationSerializer(chat).data 
    
    @database_sync_to_async
    def get_update_chat_by_id(self, users):
        chat = ChatModel.objects.filter(id = self.id).first()
        if not chat:
            raise DenyConnection("Chat not found")
        chat.typed = users
        chat.save()
        return ChatRepresentationSerializer(chat).data 


    async def send_to_chat_me(self,data):
        await self.send(text_data=json.dumps(data))


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        users = data.get('users')
        data = await self.get_update_chat_by_id(users)
        await self.send_to_chat_me(data)

    async def update_chat_me(self, event):
        await  self.send(text_data=json.dumps(event["data"]))
 

        


class GetMeChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            raise DenyConnection("Authenticated required")
        self.group_name = f"me_chat_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_users_chats()
    

    async def send_users_chats(self):
        data = await self.get_my_chats_db()
        await self.send(text_data=json.dumps(data))


    @database_sync_to_async 
    def get_my_chats_db(self):
        my_chat = ChatModel.objects.filter(users=self.user)
        serializer = ChatRepresentationSerializer(my_chat, many=True)
        return serializer.data        



    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    

 

    async def update_chat(self, event):
        await self.send(text_data=json.dumps(event["data"]))



class GetMyChatFromMessage(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.chat = self.scope["url_route"]["kwargs"]["pk"]
        if not self.chat:
            raise DenyConnection("Not found chat")
        if not self.user.is_authenticated:
            raise DenyConnection("Authentiacated required")
        
        if hasattr(self, "group_name") and self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

        self.group_name = f"message_chat_{self.chat}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_message_by_chat()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def send_message_by_chat(self):
        data =await self.get_message_by_chat()
        await self.send(text_data=json.dumps(data))
    
    @database_sync_to_async
    def get_message_by_chat(self):
        message = MessageModel.objects.filter(chat_id = self.chat)
        serializer = MessageSerializers(message, many=True)
        return serializer.data 

    @database_sync_to_async
    def save_message(self, data):
        serializer = MessageSerializers(data=data, context = {'owner':self.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
        
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.save_message(data)
        await self.send_message_by_chat()
   
    async def new_message(self, event):
        await  self.send(text_data=json.dumps(event["data"]))


