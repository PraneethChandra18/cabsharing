import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Booking,Current_Booking,Request,Chat,Notification
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.user = self.scope['user']
        if self.user.pk > int(self.pk):
            self.room_group_name = 'chat_' + str(self.pk) + '_' + str(self.user.pk)
        else:
            self.room_group_name = 'chat_' + str(self.user.pk) + '_' + str(self.pk)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    def chat_message(self, event):
        data = event['data']
        self.user = self.scope['user']
        if data:
            from_user_pk = int(data['from_user'])
            to_user_pk = int(data['to_user'])
            from_user = User.objects.get(pk=from_user_pk)
            to_user = User.objects.get(pk=to_user_pk)
            message = data['message']
            if from_user_pk == self.user.pk:
                c = Chat(from_user=from_user,to_user=to_user,message=message)
                c.save()

        self.send(text_data=json.dumps(data))

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_group_name = 'notify'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notifications',
                'data': data
            }
        )

    def notifications(self, event):
        data = event['data']
        self.user = self.scope['user']
        if data:
            from_user_pk = int(data['from_user'])
            to_user_pk = int(data['to_user'])
            to_user = User.objects.get(pk=to_user_pk)
            type = data['type']
            message = data['message']
            if from_user_pk == self.user.pk:
                c = Notification(to_user=to_user,type=type,notification=message)
                c.save()

        self.send(text_data=json.dumps(data))
