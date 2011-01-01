from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
from vexim.controlpanel.models import Domain

import types

register = template.Library()

@register.filter
@stringfilter
def domain_admins(value):
    users = User.objects.filter(userprofile__domain__domain=value).get()
    if not users:
        admin = 'None'
    elif type(users) == types.ListType:
        admins = 'Multiple admins'
    else:
        admins = users.email
    return admins
domain_admins.is_safe = True


@register.filter
@stringfilter
def domain_admins_count(value):
    users = User.objects.filter(userprofile__domain__domain=value)
    return users.count()
domain_admins_count.is_safe = True
