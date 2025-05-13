import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        user = self.scope['user']

        # Se quiseres validar se o user pertence à conversa, descomenta isto:
        # is_participant = await self.is_user_in_conversation(user)
        # if not is_participant:
        #     await self.close()
        #     return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
        timestamp = timezone.now().strftime('%H:%M')

        # Guarda a mensagem na BD
        await self.create_and_save_message(int(self.room_name), sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @sync_to_async
    def is_user_in_conversation(self, user):
        from .models import Conversation  # ✅ importar aqui
        try:
            conversation = Conversation.objects.get(pk=int(self.room_name))
            return conversation.participant1 == user or conversation.participant2 == user
        except Conversation.DoesNotExist:
            return False

    @sync_to_async
    def create_and_save_message(self, conversation_id, sender, content):
        from .models import Conversation, Message  # ✅ importar aqui
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
            Message.objects.create(
                conversation=conversation,
                sender=sender,
                content=content
            )
        except Exception as e:
            print(f"Erro ao guardar mensagem: {e}")
