# accounts/templatetags/math_filters.py

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument
    Usage: {{ value|multiply:100 }}
    """
    try:
        return float(value or 0) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    Divide the value by the argument
    Usage: {{ value|divide:100 }}
    """
    try:
        arg = float(arg)
        if arg == 0:
            return 0
        return float(value or 0) / arg
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """
    Calculate percentage
    Usage: {{ value|percentage:total }}
    """
    try:
        total = float(total)
        if total == 0:
            return 0
        return (float(value or 0) / total) * 100
    except (ValueError, TypeError):
        return 0
