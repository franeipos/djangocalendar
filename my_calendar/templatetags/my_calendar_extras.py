from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='get_id')
def get_id(value):
    return value.get('_id', None)
