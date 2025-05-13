# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message, ConversationRead
from django.contrib import messages
# Importe o modelo Servico da app index (assumindo que está lá)
from perfil.models import Servico
from django.contrib.auth import get_user_model # Para obter o modelo de utilizador
from django.db.models import Count, Max
from django.utils import timezone



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conversation
from perfil.models import Servico, Perfil




User = get_user_model() # Obtém o modelo de utilizador ativo



@login_required
def chat_room(request, conversation_id):
    # Busca a conversa, garantindo que o utilizador é participante
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    # Marca todas as mensagens até este momento como lidas
    ConversationRead.objects.update_or_create(
        conversation=conversation,
        user=request.user,
        defaults={'last_read': timezone.now()}
    )

    # Carrega as mensagens em ordem cronológica
    messages = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')

    # Determina quem é “o outro” participante
    if conversation.participant1 == request.user:
        other_participant = conversation.participant2
    else:
        other_participant = conversation.participant1

    # Pega o nome ou username para exibir no header
    try:
        other_name = other_participant.perfil.nome or other_participant.username
    except Perfil.DoesNotExist:
        other_name = other_participant.username

    # Texto completo do serviço (categoria + nome)
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
    # Obtém todas as conversas onde o utilizador logado é participant1 ou participant2
    # Usamos Q() para criar uma condição OR na query
    conversations = Conversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).order_by('-timestamp') # Opcional: ordenar pela data da última mensagem ou criação

    context = {
        'conversations': conversations,
        'user': request.user
    }

    # Renderiza o template da lista de conversas
    return render(request, 'chat/chat_list.html', context)


@login_required
def iniciar_conversa(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)
    # Verificações de integridade
    if not servico.prestador or not hasattr(servico.prestador, 'user'):
        messages.error(request, "Prestador inválido ou apagado.")
        return redirect('index:index')

    if not servico.prestador.user:
        messages.error(request, "Utilizador do prestador não existe.")
        return redirect('index:index')

    if request.user == servico.prestador.user:
        messages.warning(request, "Não pode iniciar uma conversa consigo mesmo.")
        return redirect('index:index')

    # Participantes (ordenar por ID para garantir unicidade da conversa)
    participante1 = request.user
    participante2 = servico.prestador.user

    if participante1.id > participante2.id:
        participante1, participante2 = participante2, participante1

    # Criar ou obter conversa existente
    conversa, created = Conversation.objects.get_or_create(
        participant1=participante1,
        participant2=participante2,
        servico=servico
    )

    return redirect('chat:chat_room', conversation_id=conversa.id)




@login_required
def minhas_conversas(request):
    user = request.user

    # Pega todas as conversas onde o user participa e que já tenham >=1 mensagem
    conversas = Conversation.objects.annotate(
        num_mensagens=Count('messages'),
        ultima_mensagem=Max('messages__timestamp')
    ).filter(
        Q(participant1=user) | Q(participant2=user),
        num_mensagens__gt=0
    ).order_by('-ultima_mensagem')

    # Para cada conversa, calcula quantas mensagens têm timestamp > last_read
    for conv in conversas:
        try:
            last_read = ConversationRead.objects.get(
            conversation=conv,
            user=user
        ).last_read
        except ConversationRead.DoesNotExist:
            last_read = None

    if last_read:
        # só as dos outros após last_read
        unread = conv.messages.filter(
            timestamp__gt=last_read
        ).exclude(sender=user).count()
    else:
        # nunca entrou: conta apenas as mensagens dos outros
        unread = conv.messages.exclude(sender=user).count()

    conv.unread = unread


    # Mantém teu código de definição de papel...
    papel = "cliente"
    if conversas.exists():
        primeira = conversas.first()
        papel = "cliente" if primeira.participant1 == user else "prestador"

    return render(request, 'chat/minhas_conversas.html', {
        'conversas': conversas,
        'papel': papel,
        'user': user,
    })