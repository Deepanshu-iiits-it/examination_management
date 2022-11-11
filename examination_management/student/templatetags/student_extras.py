from django import template

register = template.Library()


@register.filter
def hash(obj, key):
    return obj.get(key, None)