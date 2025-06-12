# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Max
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Conversation, Message, ConversationRead
from perfil.models import Servico
from django.views.decorators.http import require_POST

User = get_user_model()  # modelo user


@login_required
def chat_room(request, conversation_id):
    # busca conversa
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    # marcar como lida
    ConversationRead.objects.update_or_create(
        conversation=conversation,
        user=request.user,
        defaults={'last_read': timezone.now()}
    )

    # mensagens
    messages = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')

    # outro participante
    if conversation.participant1 == request.user:
        other_participant = conversation.participant2
    else:
        other_participant = conversation.participant1

    # nome exibido
    try:
        other_name = other_participant.perfil.nome or other_participant.username
    except Perfil.DoesNotExist:
        other_name = other_participant.username

    # nome do serviço
    servico_nome_completo = (
        f"{conversation.servico.categoria} - {conversation.servico.nome}"
    )

    return render(request, 'chat/chat_room.html', {
        'conversation': conversation,
        'messages': messages,
        'other_participant': other_participant,
        'other_name': other_name,
        'servico_nome_completo': servico_nome_completo,
    })


@login_required
def chat_list(request):
    # conversas do user
    conversations = Conversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).order_by('-timestamp')

    context = {
        'conversations': conversations,
        'user': request.user
    }

    return render(request, 'chat/chat_list.html', context)


@login_required
def iniciar_conversa(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)

    # valida prestador
    if not servico.prestador or not hasattr(servico.prestador, 'user'):
        messages.error(request, "Prestador inválido ou apagado.")
        return redirect('index:index')

    if not servico.prestador.user:
        messages.error(request, "Utilizador do prestador não existe.")
        return redirect('index:index')

    if request.user == servico.prestador.user:
        messages.warning(request, "Não pode iniciar uma conversa consigo mesmo.")
        return redirect('index:index')

    # ordem dos participantes
    participante1 = request.user
    participante2 = servico.prestador.user

    if participante1.id > participante2.id:
        participante1, participante2 = participante2, participante1

    # obter ou criar
    conversa, created = Conversation.objects.get_or_create(
        participant1=participante1,
        participant2=participante2,
        servico=servico
    )

    return redirect('chat:chat_room', conversation_id=conversa.id)


@login_required
def minhas_conversas(request):
    user = request.user

    # com mensagens
    conversas = Conversation.objects.annotate(
        num_mensagens=Count('messages'),
        ultima_mensagem=Max('messages__timestamp')
    ).filter(
        Q(participant1=user) | Q(participant2=user),
        num_mensagens__gt=0
    ).order_by('-ultima_mensagem')

    for conv in conversas:
        try:
            last_read = ConversationRead.objects.get(conversation=conv, user=user).last_read
        except ConversationRead.DoesNotExist:
            last_read = None

        # mensagens não lidas
        if last_read:
            unread = conv.messages.filter(timestamp__gt=last_read).exclude(sender=user).count()
        else:
            unread = conv.messages.exclude(sender=user).count()

        conv.unread = unread  # atributo extra

    # papel do user
    if conversas.exists():
        primeira = conversas.first()
        papel = "prestador" if primeira.participant1 == user else "cliente"
    else:
        papel = "cliente"

    return render(request, 'chat/minhas_conversas.html', {
        'conversas': conversas,
        'papel': papel,
        'user': user,
    })


@login_required
@require_POST
def apagar_conversa(request, conversation_id):
    conversa = get_object_or_404(Conversation, id=conversation_id)

    # Garantir que o utilizador faz parte da conversa
    if request.user == conversa.participant1 or request.user == conversa.participant2:
        conversa.delete()
        messages.success(request, "Conversa apagada com sucesso.")
    else:
        messages.error(request, "Não tem permissão para apagar esta conversa.")

    return redirect('chat:minhas_conversas')  # ou 'chat:chat_list' dependendo da rota