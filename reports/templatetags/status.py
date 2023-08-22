from django import template

register = template.Library()

@register.filter
def status(value1,value2):
    try:
        if value1-value2 >= 0:
            return 'OK'
        else:
            return 'NOT OK'
    except:
        pass

    