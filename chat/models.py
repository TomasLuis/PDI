from django.db import models
from django.conf import settings  # Para referenciar o utilizador ativo
from perfil.models import Servico  # O teu modelo de serviço

class Conversation(models.Model):
    participant1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_participant1'
    )
    participant2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_participant2'
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.SET_NULL,
        related_name='conversation',
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant1', 'participant2', 'servico')

    def __str__(self):
        return f"Conversa entre {self.participant1.username} e {self.participant2.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Mensagem de {self.sender.username} em {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class ConversationRead(models.Model):
    """
    Guarda, para cada usuário e conversa, a última vez que esse usuário leu as mensagens.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='reads'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    last_read = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"{self.user.username} leu conversa {self.conversation.id} em {self.last_read}"
