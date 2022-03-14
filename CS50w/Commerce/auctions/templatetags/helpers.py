from django import template

register = template.Library()


def format_date(value, format='%d/%m/%Y'):
    return value.strftime(format)


register.filter("format_date", format_date)
