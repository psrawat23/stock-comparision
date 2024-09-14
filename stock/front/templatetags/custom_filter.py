from django import template

register = template.Library()

@register.filter(name='ValueIn')
def ValueIn(value, arg):
    """
    Multiplies the given value by the argument.
    Usage: {{ dict|ValueIn:arg }}
    """
    try:
        return value[arg]
    except (ValueError, TypeError):
        return ''
