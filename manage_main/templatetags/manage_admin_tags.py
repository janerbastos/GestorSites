# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.assignment_tag(takes_context=True)
def has_list_users(context, **kwargs):
    list_users = User.objects.filter(is_superuser=False)
    if 'users' in kwargs:
        users = kwargs['users'].values_list('user__id', flat=True)
        list_users = list_users.exclude(id__in=users)
        
    
    return list_users
    