import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.exceptions import APIException,status
from rest_framework.response import Response

class KlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # self.room_group_name = 'btcusdt_realtime'
        await self.channel_layer.group_add(
            'btcusdt_realtime',
            self.channel_name
        )
        print(self.channel_layer)
        
        self.accept()
        # await self.send(text_data=json.dumps({'message': 'hello'}))
        print("#######CONNECTED############")
    async def recive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Message: ', message)

        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": 'send_message_to_frontend',
                "message": message
            }
        )
    
    async def send_message_to_frontend(self, event):
        print("EVENT TRIGERED")
        # Receive message from room group
        message = event['message']
        # print(message)
        # Send message to WebSocket
        await self.send(text_data=message.to_json())

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(
            'btcusdt_realtime',
            self.channel_name
        )
        print("DISCONNECTED")
        print(close_code)
