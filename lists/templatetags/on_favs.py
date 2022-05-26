from django import template

register = template.Library()


@register.simple_tag
def on_favs(value):
    pass
