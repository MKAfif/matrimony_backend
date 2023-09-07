# # from channels.generic.websocket import WebSocketConsumer
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json 
# from asgiref.sync import async_to_sync
    

# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_code']
#         self.room_group_name = f'room_{self.room_name}'

    
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()


#         await self.send(text_data=json.dumps({
#             'message': 'Connected'
#         }))
    
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )



# testing


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# from chatapp.models import Room,Message,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.roomGroupName = 'chat_%s' % self.room_name
        
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
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        # username = text_data_json.get("name", "")
        
        # room_name = text_data_json.get("room_name", "")
        
        
        # await self.save_message(message, username)  
        # await self.save_message(message)   

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                # "username": username,
                # "room_name": room_name,
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        # username = event["username"]
        # await self.send(text_data=json.dumps({"message": message, "username": username}))
        await self.send(text_data=json.dumps({"message": message }))
    
    # @sync_to_async
    # def save_message(self, message, username, room_name):
    #     print(username,room_name,"----------------------")
    #     user=User.objects.get(username=username)
    #     room=Room.objects.get(name=room_name)
        
    #     Message.objects.create(user=user,room=room,content=message)
