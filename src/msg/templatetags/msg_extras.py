from django import template

register = template.Library()


@register.filter
def get_other_user(obj, user):
    return obj.other_user(user)
