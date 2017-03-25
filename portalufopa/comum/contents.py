# -*- coding: utf-8 -*-
from portalufopa.models import Site, PortalCatalog
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils.text import slugify

OBJ_SERVICE = ('sessions_manage', 'createObject', 'folder_contents', 'content_status_modify',
               'select_default_page', 'organizer_content', 'image_browse_url', 'edit', '@@manage-portlets', 'delete')

TYPE_NAME = ['pagina', 'noticia', 'link', 'imagem', 'banner', 'arquivo', 'agenda', 'evento', 'agenda', 'pasta', 'informe']

WORKFLOW_ACTION = ['publicar', 'retirar', 'rejeitar', 'enviar_publicar']

WORKFLOW = {
    'publicar' : 'Publicado',
    'retirar' : 'Privado',
    'rejeitar' : 'Privado',
    'enviar_publicar' : 'Revisao pendente',
    }

def __gerar():
    import random
    resposta = ('%s%s') % (random.randrange(0, 101, 2), random.choice('abcdefghij'))
    return resposta

def __get_url_fraguiment(request):
    return request.path.strip('/').split('/')

def fraguiment_url(request):
    return __get_url_fraguiment(request) 

def get_site_url(request):
    _url_id = __get_url_fraguiment(request)[0]
    site = get_object_or_404(Site, url=_url_id)
    return site

def get_site_url_id(request):
    _url_site = __get_url_fraguiment(request)[0]
    return _url_site

def reescrever_url(request):
    _fragment_url = __get_url_fraguiment(request)
    _new_url = request.path
    for i in OBJ_SERVICE:
        if i in _fragment_url:
            _substituir = '/%s' % i
            _new_url = _new_url.replace(_substituir, '')
    return _new_url

def get_url_id_content(request):
    _url = reescrever_url(request)
    return _url.strip('/').split('/')[-1]

def save_in_portal_catalog(instance, url=None):
    try:
        portal = instance.get_portal_catalog()
    except PortalCatalog.DoesNotExist:
        portal = PortalCatalog()
        portal.path_url = url
        portal.site = instance.site
        portal.tipo = instance.tipo
        portal.dono = instance.dono
    
    if portal.content_id == 0 or portal.content_id == None:
        portal.content_id = instance.id
        
    if instance.workflow == 'Publicado' and portal.public_at==None:
        portal.public_at = datetime.now()
    
    portal.url = instance.url
    portal.titulo = instance.titulo
    portal.descricao = instance.descricao
    portal.update_at = instance.update_at
    portal.workflow = instance.workflow
    portal.excluir_nav = instance.excluir_nav
    portal.save()
    
def save_indice_url(request, titulo, tipo=None):
    _url_code = slugify(titulo)
    _url = reescrever_url(request)
    _site = get_site_url(request)
    try:
        pc = PortalCatalog.objects.filter(site=_site, path_url__icontains=_url).get(url=_url_code)
        _url_code = ('%s-%s') % (_url_code, __gerar())
    except:
        pass
    
    return _url_code