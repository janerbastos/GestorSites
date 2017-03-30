# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import User
from manage_main.models import Papel, GrupoPapel
from portalufopa.models import ContentType

register = template.Library()

@register.assignment_tag(takes_context=True)
def has_list_users(context, **kwargs):
    list_users = User.objects.filter(is_superuser=False)
    if 'users' in kwargs:
        users = kwargs['users'].values_list('user__id', flat=True)
        list_users = list_users.exclude(id__in=users)
        
    
    return list_users

@register.assignment_tag(takes_context=True)
def has_list_papeis(context, **kwargs):
    list_papeis = Papel.objects.all()
    if 'grupo' in kwargs:
        try:
            grupo_papeis = GrupoPapel.objects.get(grupo__grupo_name=kwargs['grupo'])
            papeis = grupo_papeis.papeis.all()
            list = papeis.values_list('id', flat=True)
            list_papeis = list_papeis.exclude(id__in=list)
        except:
            pass
   
    return list_papeis

@register.assignment_tag
def has_list_permissoes(**kwargs):
    tipo = kwargs['tipo']
    list_papeis = kwargs['papeis']
    list_papeis = list_papeis.filter(content_type=tipo)
    return list_papeis

@register.assignment_tag(takes_context=True)
def has_list_permissoes_from_grupo_papel(context, **kwargs):
    _results = None
    if 'papeis' in kwargs:
        _list = kwargs['papeis']
        _list = _list.values_list('content_type__id', flat=True).distinct()
        _results = ContentType.objects.filter(id__in=_list)
    
    if 'permissoes' in kwargs:
        permissoes = kwargs['permissoes']
        if 'tipo' in kwargs:
            tipo = kwargs['tipo']
            _results = permissoes.filter(content_type=tipo)
    
    return _results

@register.assignment_tag(takes_context=True)
def has_list_contents(context, **kwargs):
    _result = ContentType.objects.all()
    return _result
    