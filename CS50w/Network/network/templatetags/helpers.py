from tarfile import REGULAR_TYPES
from django import template

register = template.Library()

# simle Tag


@register.filter
def order_by(queryset, args):
    return queryset.order_by(args)


@register.filter
def all(queryset):
    return queryset.all()


@register.filter
def subtract(value, arg):
    return value - int(arg)


@register.filter
def add(value, arg):
    return value + int(arg)
