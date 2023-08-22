from django import template

register = template.Library()

@register.filter
def substract(value1,value2):
    try:
        return value1-value2
    except:
        pass