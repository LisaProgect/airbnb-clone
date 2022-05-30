from django import template
from lists.models import List

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list = List.objects.get_or_none(user=user)
    return the_list.rooms.contains(room)
