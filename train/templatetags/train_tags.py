import math

from django import template

register = template.Library()

@register.filter()
def format_seconds(s):
    s = int(s)
    if s < 60:
        return str(s) + "s"
    mins = math.floor(s / 60);
    return str(mins) + "m";
