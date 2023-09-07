import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from app1.models import Message,Member
from django.utils import timezone
from channels.db import database_sync_to_async
import random
import string




class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("reachhhhhhhhhh")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name,"room name")
        self.roomGroupName = f'chat_{self.room_name}'
        print("This is the room name: ", self.roomGroupName)
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        await super().disconnect(close_code)
        
    async def receive(self, text_data=None):
        data           = json.loads(text_data)
        message        = data["message"]
        sender_id      = data["sender_id"]
        receiver_id    = data["recipient"]

       
        await self.save_message(message , sender_id , receiver_id)   

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type"        : "sendMessage",
                "message"     : message,
                "sender_id"   : sender_id,
                "receiver_id" : receiver_id
                
            }
        )
    
    async def sendMessage(self, event):
        message      = event["message"]
        sender_id    = event["sender_id"]
        recipient_id = event["receiver_id"]

        await self.send(text_data=json.dumps({
            "type": "message",  
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "content": message,
        }))

    
    @database_sync_to_async
    def save_message(self, message, sender_id, receiver_id):
      
        sender = Member.objects.get(id=int(sender_id))
        receiver = Member.objects.get(id=int(receiver_id))
       
        message = Message.objects.create(sender_id=sender.id, receiver_id=receiver.id, content=message, timestamp=timezone.now())
        message.save()
        return message
    






   

