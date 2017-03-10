# -*- coding: utf-8 -*-

from ..models import Pagina, Noticia, Imagem, Banner, Informe, Evento,\
    Agenda


TYPE_NAME = ['pagina', 'noticia', 'link', 'imagem', 'banner', 'arquivo', 'agenda', 'evento', 'agenda', 'pasta', 'informe']

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

MAIS_CONTENTS = {
    'pasta' : 'mais pastas',
    'pagina': 'mais paginas',
    'noticia' : 'mais notícias',
    'imagem' : 'mais imagens',
    'link' : 'mais links',
    'banner' : 'mais banners',
    'arquivo' : 'mais aquivos',
    'evento' : 'mais eventos',
    'agenda' : 'mais agenda',
    'informe' : 'mais informes',
    }


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
