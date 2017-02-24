# -*- coding: utf-8 -*-

from datetime import date

from django.shortcuts import get_object_or_404

from ..models import Site, PortalUrl, PortalCatalog, Pagina, Noticia, Imagem, Banner, Informe, Evento,\
    Agenda


TYPE_NAME = ['pagina', 'noticia', 'link', 'imagem', 'banner', 'arquivo', 'agenda', 'evento', 'agenda', 'pasta', 'informe']
CREATE_OBJECT = 'createObject'
FOLDER_CONTENTS = 'folder_contents'
CONTENT_STATUS_MODIFY = 'content_status_modify'
SELECT_DEFAULT_PAGE = 'select_default_page'
ORGANIZADOR_CONTENT = 'organizador_content'
IMAGE_BROWSE_URL = 'image_browse_url'
EDIT_OBJECT = 'edit'
ICONS = {
    'ATPasta' : '<i class=\"fa fa-folder-o\" aria-hidden=\"true\"></i>',
    'ATPagina' : '<i class=\"fa fa-file-text-o\" aria-hidden=\"true\"></i>',
    'ATNoticia' : '<i class=\"fa fa-newspaper-o\" aria-hidden=\"true\"></i>',
    'ATImagem' : '<i class=\"fa fa-file-image-o\" aria-hidden=\"true\"></i>',
    'ATLink' : '<i class=\"fa fa-link\" aria-hidden=\"true\"></i>',
    'ATBanner' : '<i class=\"fa fa-image\" aria-hidden=\"true\"></i>',
    'ATArquivo' : '<i class=\"fa fa-file-o\" aria-hidden=\"true\"></i>',
    'ATEvento' : '<i class=\"fa fa-calendar-o\" aria-hidden=\"true\"></i>',
    'ATAgenda' : '<i class=\"fa fa-calendar\" aria-hidden=\"true\"></i>',
    'ATInforme' : '<i class=\"fa fa-tv\" aria-hidden=\"true\"></i>',
    }

CONTENT_BY_TYPE = {
        'pasta' : 'ATPasta',
        'pagina': 'ATPagina',
        'noticia' : 'ATNoticia',
        'imagem' : 'ATImagem',
        'link' : 'ATLink',
        'banner' : 'ATBanner',
        'arquivo' : 'ATArquivo',
        'evento' : 'ATEvento',
        'agenda' : 'ATAgenda',
        'informe' : 'ATInforme',
    }

WORKFLOW_COLOR = {
    'Publicado' : 'text-default',
    'Privado' : 'text-danger',
    'Revisao pendente': 'text-warning',
    }

WORKFLOW_ACTION = ['publicar', 'retirar', 'rejeitar', 'enviar_publicar']

WORKFLOW = {
    'publicar' : 'Publicado',
    'retirar' : 'Privado',
    'rejeitar' : 'Privado',
    'enviar_publicar' : 'Revisao pendente',
    }

def get_url_request(request):
    return request.path.strip('/').split('/')

def get_site_url(url):
    return get_object_or_404(Site, url=url)

def get_indice_url(url, site):
    try:
        portal_url = PortalUrl.objects.filter(site=site).get(url=url)
        return portal_url.indice
    except PortalUrl.DoesNotExist:
        return 0

def get_content_by_portal_catalog(_portal_catalog):
    
    _obj_select = None
    
    if _portal_catalog.tipo == 'ATPagina':
        _obj_select = Pagina.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
        
    if _portal_catalog.tipo == 'ATNoticia':
        _obj_select = Noticia.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
    
    if _portal_catalog.tipo == 'ATImagen':
        _obj_select = Imagem.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
    
    if _portal_catalog.tipo == 'ATBanner':
        _obj_select = Banner.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
    
    if _portal_catalog.tipo == 'ATInforme':
        _obj_select = Informe.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
        
    if _portal_catalog.tipo == 'ATEvento':
        _obj_select = Evento.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
    
    if _portal_catalog.tipo == 'ATAgenda':
        _obj_select = Agenda.objects.filter(site=_portal_catalog.site).get(url=_portal_catalog.url)
    
    return _obj_select

def get_content_by_tipo(url_site, _id, tipo):
    _object = None
    if tipo=='ATPagina':
        _object = Pagina.objects.filter(site__url=url_site,).get(id=_id)
    if tipo=='ATImagem':
        _object = Imagem.objects.filter(site__url=url_site,).get(id=_id)
    if tipo== 'ATBanner':
        _object = Banner.objects.filter(site__url=url_site,).get(id=_id)
    if tipo== 'ATNoticia':
        _object = Noticia.objects.filter(site__url=url_site,).get(id=_id)
    if tipo== 'ATInforme':
        _object = Informe.objects.filter(site__url=url_site,).get(id=_id)
    if tipo== 'ATEvento':
        _object = Evento.objects.filter(site__url=url_site,).get(id=_id)
    if tipo== 'ATAgenda':
        _object = Agenda.objects.filter(site__url=url_site,).get(id=_id)
    return _object

def save_indice_url(url, indice, site):
    try:
        portal_url = PortalUrl.objects.filter(site=site).get(url=url)
        portal_url.indice = indice
        portal_url.save()
    except PortalUrl.DoesNotExist:
        portal_url = PortalUrl(url=url, indice=indice, site=site)
        portal_url.save()
        
def create_portal_catalog(content, path_url=None):
    
    try:
        portal = PortalCatalog.objects.filter(site=content.site).get(url=content.url)
    except PortalCatalog.DoesNotExist:
        portal = PortalCatalog()
    
    portal.url = content.url
    portal.titulo = content.titulo
    portal.descricao = content.descricao
    portal.create_at = content.create_at
    portal.update_at = content.update_at
    portal.public_at = content.public_at
    portal.workflow = content.workflow
    portal.tipo = content.tipo
    portal.site = content.site
    portal.excluir_nav = content.excluir_nav
    portal.path_url = path_url
    portal.dono = content.dono
    portal.save()

def delete_portal_catalog(instancia):
    try:
        pc = PortalCatalog.objects.filter(site=instancia.site).get(url=instancia.url)
        pc.delete()
        return True
    except PortalCatalog.DoesNotExist:
        return False
    
def update_portal_catalog(instancia):
    pc = PortalCatalog.objects.filter(site=instancia.site).get(url=instancia.url)
    pc.titulo      = instancia.titulo
    pc.descricao   = instancia.descricao
    pc.workflow    = instancia.workflow
    pc.update_at   = instancia.update_at
    pc.public_at   = instancia.public_at
    pc.excluir_nav = instancia.excluir_nav
    pc.content_id  = instancia.id
    pc.save()

def content_workflow_modify(instancia, workflow):
    instancia.workflow = workflow
    if not instancia.public_at:
        instancia.public_at = date.today()
    instancia.save()
    update_portal_catalog(instancia)