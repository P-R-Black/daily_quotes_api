from django import template
import re

register = template.Library()

@register.filter
def string_to_number(value):
    try:
        # Try converting to an integer
        int_value = int(value)
        return True  # It's a number
    except ValueError:
        return False  # Not a number