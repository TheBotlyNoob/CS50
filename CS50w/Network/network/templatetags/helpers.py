from django import template

register = template.Library()

# simle Tag


@register.filter
def order_by(queryset, args):
    return queryset.order_by(args)
