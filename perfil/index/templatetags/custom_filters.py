from django import template
import math

register = template.Library()

@register.filter(name='get_star_rating')
def get_star_rating(avaliacao_media):
    try:
        avaliacao_media = int(avaliacao_media)  # Tenta converter para inteiro
    except (ValueError, TypeError):
        return "<span>Não avaliado</span>"  # Retorna uma mensagem amigável

    estrelas = ''
    for i in range(avaliacao_media):
        estrelas += '<i class="fas fa-star"></i>'
    for i in range(5 - avaliacao_media):
        estrelas += '<i class="far fa-star"></i>'
    return estrelas
